# %% [markdown]
# # 04. Risk index and spatial patterns
#
# This notebook answers Q5: where is risk concentrated, and how stable is that ranking?
#
# The index is built from exposure and sensitivity. Adaptive capacity is not included,
# because no published district series was assembled, and values are never estimated or
# filled. The index shows where to look more closely. It is not an allocation rule, and it is
# not evidence that the data are correct.
#
# A ranking from one set of choices is not robust on its own. So the index is rebuilt under
# every combination of normalisation, aggregation and weights, and each district's position
# is reported as a range.

# %%
import json
import sys
import warnings
from pathlib import Path

import esda
import geopandas as gpd
import libpysal
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd().parent
FRAMEWORK = ROOT.parent / "bd-boro-data-framework"
sys.path.insert(0, str(FRAMEWORK / "v2" / "src"))
from common import canon_district                        # noqa: E402

OUT = ROOT / "outputs"
RNG = np.random.default_rng(20261101)
HAOR = ["Sunamganj", "Habiganj", "Netrokona", "Kishoreganj", "Sylhet", "Moulvibazar", "Brahmanbaria"]
SMALL_HA = 15000
R = {}
p = pd.read_parquet(ROOT / "data" / "analysis_panel.parquet")

# %% [markdown]
# ## Components
#
# **Exposure** uses flood on Boro land from both records, plus heat at flowering and cold at
# the reproductive stage. **Sensitivity** uses how much production and area move, and how low
# yields are. Trends are removed first, so steady growth is not counted as instability.

# %%
def detrended_sd(s):
    t = s.harvest_year - s.harvest_year.mean()
    y = np.log(s.iloc[:, 0])
    return float(np.std(y - np.polyval(np.polyfit(t, y, 1), t), ddof=2))


def worst_drop(s):
    t = s.harvest_year - s.harvest_year.mean()
    y = np.log(s.iloc[:, 0])
    return float(-(y - np.polyval(np.polyfit(t, y, 1), t)).min())


g = p.groupby("district")
c = pd.DataFrame({
    "flash_flood": (g.jrc_flash_boro.mean() + g.s1_flash_boro.mean()) / 2,
    "monsoon_flood": (g.jrc_monsoon_boro.mean() + g.s1_monsoon_boro.mean()) / 2,
    "heat": g.hot_days_flower.mean(),
    "cold": g.cold_days_repro.mean(),
    "production_instability": p.groupby("district")[["production_t", "harvest_year"]].apply(detrended_sd),
    "worst_area_drop": p.groupby("district")[["area_ha", "harvest_year"]].apply(worst_drop),
    "low_yield": -g.yield_t_ha.mean(),
})
DIMENSIONS = {"Exposure": ["flash_flood", "monsoon_flood", "heat", "cold"],
              "Sensitivity": ["production_instability", "worst_area_drop", "low_yield"]}
COMP = [v for d in DIMENSIONS.values() for v in d]
c = c[COMP]
c.round(4).to_csv(OUT / "table_index_components.csv")
print(c.describe().T[["mean", "std", "min", "max"]].round(3).to_string())
print(c.corr(method="spearman").round(2).to_string())

# %% [markdown]
# ## Every combination of choices
#
# Three normalisations, two aggregations and four weighting schemes are combined. Random
# weights use 1,000 draws. For each district this gives the range of its rank, how often it is
# in the top ten, and how often it stays in the same fifth of the ranking.

# %%
def normalise(d, how):
    if how == "min-max":
        return (d - d.min()) / (d.max() - d.min())
    if how == "z-score":
        return (d - d.mean()) / d.std()
    return d.rank() / len(d)


def aggregate(n, w, how):
    if how == "arithmetic":
        return n.mul(w).sum(axis=1)
    s = n - n.min() + 0.01              # the geometric mean needs positive values
    return np.exp(np.log(s).mul(w).sum(axis=1))


def weights():
    eq = pd.Series(1 / len(COMP), index=COMP)
    dim = pd.Series({v: 0.5 / len(vs) for vs in DIMENSIONS.values() for v in vs})[COMP]
    z = (c - c.mean()) / c.std()
    vec = np.linalg.svd(z.values, full_matrices=False)[2][0]
    vec = np.abs(vec) / np.abs(vec).sum()
    out = {"equal": eq, "by dimension": dim, "first principal component": pd.Series(vec, index=COMP)}
    return out


base_w = weights()
R["pca_weights"] = base_w["first principal component"].round(3).to_dict()
ranks, labels = [], []
for nh in ("min-max", "z-score", "rank"):
    n = normalise(c, nh)
    for ah in ("arithmetic", "geometric"):
        for wn, w in base_w.items():
            ranks.append(aggregate(n, w, ah).rank(ascending=False))
            labels.append(f"{nh} | {ah} | {wn}")
        for _ in range(1000):
            w = pd.Series(RNG.dirichlet(np.ones(len(COMP))), index=COMP)
            ranks.append(aggregate(n, w, ah).rank(ascending=False))
            labels.append(f"{nh} | {ah} | random")
rk = pd.concat(ranks, axis=1)
rk.columns = range(rk.shape[1])
base = aggregate(normalise(c, "min-max"), base_w["by dimension"], "arithmetic")
res = pd.DataFrame({"index": base, "rank": base.rank(ascending=False).astype(int), "rank_median": rk.median(axis=1),
                    "rank_p05": rk.quantile(0.05, axis=1), "rank_p95": rk.quantile(0.95, axis=1), "top10_share": (rk <= 10).mean(axis=1)})
tier = np.ceil(rk / 64 * 5).astype(int)
base_tier = np.ceil(res["rank"] / 64 * 5).astype(int)
res["tier"] = base_tier
res["tier_stability"] = tier.eq(base_tier, axis=0).mean(axis=1)
res["haor"] = res.index.isin(HAOR)
# Added after the first results: with little Boro, shares and instability are unreliable
res["small_base"] = p.groupby("district").area_ha.mean().reindex(res.index) < SMALL_HA
res = res.sort_values("rank")
res.round(4).to_csv(OUT / "table_index.csv")
print(res.head(12).round(3).to_string())
R["index"] = dict(combinations=int(rk.shape[1]), top10=res.head(10).index.tolist(),
                  always_top10=res[res.top10_share >= 0.9].index.tolist(),
                  spearman_median=float(rk.corrwith(base.rank(ascending=False), method="spearman").median()),
                  spearman_p05=float(rk.corrwith(base.rank(ascending=False), method="spearman").quantile(0.05)),
                  tier_stability_median=float(res.tier_stability.median()),
                  haor_in_top10=int(res.head(10).haor.sum()), small_base=res[res.small_base].index.tolist(),
                  top10_large=res[~res.small_base].head(10).index.tolist(),
                  haor_in_top10_large=int(res[~res.small_base].head(10).haor.sum()))

# %% [markdown]
# ## Would a yield-only view see the same risk?
#
# The main argument of the paper is that yield can hide flood loss. A ranking from yield alone
# is compared here with one from production. If yield hides loss, the most flooded districts
# should look much safer on yield.

# %%
def detr_sd_for(col):
    return p.groupby("district")[[col, "harvest_year"]].apply(detrended_sd)


view = pd.DataFrame({"yield_sd": detr_sd_for("yield_t_ha"), "production_sd": detr_sd_for("production_t"), "area_sd": detr_sd_for("area_ha")})
view["rank_yield"] = view.yield_sd.rank(ascending=False)
view["rank_production"] = view.production_sd.rank(ascending=False)
view["rank_area"] = view.area_sd.rank(ascending=False)
view["haor"] = view.index.isin(HAOR)
view.sort_values("rank_production").round(4).to_csv(OUT / "table_yield_vs_production_risk.csv")
print(view.sort_values("rank_production").head(10).round(3).to_string())
rho = stats.spearmanr(view.rank_yield, view.rank_production)[0]
R["yield_view"] = dict(spearman=float(rho), haor_mean_rank_yield=float(view[view.haor].rank_yield.mean()),
                       haor_mean_rank_production=float(view[view.haor].rank_production.mean()),
                       sunamganj_rank_yield=int(view.loc["Sunamganj", "rank_yield"]),
                       sunamganj_rank_production=int(view.loc["Sunamganj", "rank_production"]))
print(R["yield_view"])

# %% [markdown]
# ## Spatial patterns under several neighbour definitions
#
# Moran's I and LISA depend on what counts as a neighbour, so each is run under contiguity,
# four and six nearest neighbours, and a 100 km distance band. Local clusters are corrected
# with false discovery rate control.

# %%
sh = gpd.read_file(FRAMEWORK / "data" / "bronze" / "gadm_shapefiles" / "gadm41_BGD_2.shp")
sh["district"] = sh.NAME_2.map(canon_district)
sh = sh.sort_values("district").reset_index(drop=True).to_crs(32646)
pts = np.column_stack([sh.geometry.centroid.x, sh.geometry.centroid.y])
Ws = {"Contiguity": libpysal.weights.fuzzy_contiguity(sh, tolerance=0, buffering=True, buffer=100),
      "4 nearest": libpysal.weights.KNN.from_array(pts, k=4), "6 nearest": libpysal.weights.KNN.from_array(pts, k=6),
      "100 km band": libpysal.weights.DistanceBand.from_array(pts, threshold=100000, binary=True, silence_warnings=True)}
y = res["index"].reindex(sh.district).values
rows, hh = [], pd.DataFrame(index=sh.district)
for name, w in Ws.items():
    w.transform = "r"
    np.random.seed(1)
    m = esda.Moran(y, w, permutations=9999)
    l = esda.Moran_Local(y, w, permutations=9999, seed=1)
    q = multipletests(l.p_sim, method="fdr_bh")[1]
    hot = (l.q == 1) & (l.p_sim < 0.05)
    hot_fdr = (l.q == 1) & (q < 0.05)
    hh[name] = hot
    rows.append(dict(neighbours=name, moran_i=m.I, z=m.z_sim, p=m.p_sim, hh_005=sh.district[hot].tolist(), hh_fdr=sh.district[hot_fdr].tolist()))
sp = pd.DataFrame(rows)
sp.to_csv(OUT / "table_spatial.csv", index=False)
print(sp[["neighbours", "moran_i", "z", "p"]].round(3).to_string())
print(sp[["neighbours", "hh_005", "hh_fdr"]].to_string())
hh["share"] = hh.mean(axis=1)
R["spatial"] = dict(rows=sp.to_dict("records"), hh_all_definitions=hh[hh.share == 1].index.tolist())
hh.reset_index().to_csv(OUT / "table_hotspots.csv", index=False)
json.dump(R, open(OUT / "results_index.json", "w"), indent=1, default=float)
print("written")

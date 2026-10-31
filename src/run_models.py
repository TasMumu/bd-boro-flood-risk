# %% [markdown]
# # 03. Flood models and checks
#
# This notebook runs the models fixed in `docs/analysis_plan.md`, in the order given there.
# Every number reported in the paper is written to `outputs/`.
#
# Outcomes are the logs of harvested area, yield and production. Since production is area
# times yield, the area and yield effects must add up to the production effect, which is
# checked below. Flood fractions are scaled so that coefficients are per 10 points of a
# district's area.

# %%
import json
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import libpysal
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from scipy import stats
from scipy.optimize import minimize
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd().parent
FRAMEWORK = ROOT.parent / "bd-boro-data-framework"
sys.path.insert(0, str(FRAMEWORK / "v2" / "src"))
from common import canon_district                        # noqa: E402

OUT = ROOT / "outputs"
RNG = np.random.default_rng(20261031)
HAOR = ["Sunamganj", "Habiganj", "Netrokona", "Kishoreganj", "Sylhet", "Moulvibazar", "Brahmanbaria"]
EVENT_YEARS = [2016, 2017, 2022]
CONTROLS = ["tmean_c", "precip_100", "hot_days"]
OUTCOMES = {"log_area": "Harvested area", "log_yield": "Yield", "log_prod": "Production"}
SPECS = {"s1": dict(label="Sentinel-1", years=(2016, 2025), flash="s1_flash_10", monsoon="s1_monsoon_10"),
         "jrc": dict(label="JRC", years=(2011, 2021), flash="jrc_flash_10", monsoon="jrc_monsoon_10")}
RI_MAIN, RI_CHECK, CUTOFF_KM, SERIAL_LAGS, YIELD_BOUND = 9999, 1999, 100, 2, 0.02
SMALL_HA = 15000                  # mean Boro area below which a district has a small base
R = {}

# %% [markdown]
# ## Prepare the data
#
# The panel comes from `02_Build_Panel`. Weather controls are the same as Paper 1. District
# centroids are used for Conley errors, and neighbours for the spillover check.

# %%
p = pd.read_parquet(ROOT / "data" / "analysis_panel.parquet").sort_values(["district", "harvest_year"]).reset_index(drop=True)
p["log_area"], p["log_yield"], p["log_prod"] = np.log(p.area_ha), np.log(p.yield_t_ha), np.log(p.production_t)
p["precip_100"] = p.precip_mm / 100
p["haor"] = p.district.isin(HAOR).astype(int)
for base, new in (("s1_flash_flood", "s1_flash_10"), ("s1_monsoon_flood", "s1_monsoon_10"),
                  ("jrc_flash_flood", "jrc_flash_10"), ("jrc_monsoon_flood", "jrc_monsoon_10")):
    p[new] = p[base] * 10
for c in ("s1_flash_boro", "s1_monsoon_boro", "jrc_flash_boro", "jrc_monsoon_boro", "s1_early_wd", "s1_late_wd",
          "jrc_early_wd", "jrc_late_wd", "s1_early_boro", "s1_late_boro", "jrc_early_boro", "jrc_late_boro",
          "s1_flash_m16_wd", "s1_flash_m20_wd"):
    p[c + "_10"] = p[c] * 10
p["s1_scenes_flash_10"], p["s1_scenes_dry_10"] = p.s1_scenes_flash / 10, p.s1_scenes_dry / 10
# Lead variables for the placebo tests: next year's flash flood, and flood after this harvest,
# which is next harvest year's monsoon variable (June-October of t)
for c in ("s1_flash_10", "jrc_flash_10", "s1_monsoon_10", "jrc_monsoon_10"):
    p[c + "_lead"] = p.groupby("district")[c].shift(-1)

g = gpd.read_file(FRAMEWORK / "data" / "bronze" / "gadm_shapefiles" / "gadm41_BGD_2.shp")
g["district"] = g.NAME_2.map(canon_district)
g = g.sort_values("district").reset_index(drop=True).to_crs(32646)
XY = pd.DataFrame({"x": g.geometry.centroid.x.values / 1000, "y": g.geometry.centroid.y.values / 1000}, index=g.district.values)
W = libpysal.weights.fuzzy_contiguity(g, tolerance=0, buffering=True, buffer=100)
W.transform = "r"
for c in ("s1_flash_10", "jrc_flash_10"):
    wide = p.pivot(index="district", columns="harvest_year", values=c).loc[g.district]
    lag = pd.DataFrame(libpysal.weights.lag_spatial(W, wide.fillna(0).values), index=wide.index, columns=wide.columns)
    lag = lag.where(wide.notna()).stack().rename(c + "_nbr").reset_index()
    p = p.merge(lag, on=["district", "harvest_year"], how="left")
print(p.shape)

# %% [markdown]
# ## Four ways to measure uncertainty
#
# With few treated districts, no single method can be trusted alone, so every main estimate
# is reported under all four:
#
# - **Clustered by district**, the usual choice, which can overstate certainty here.
# - **Driscoll–Kraay**, which allows shocks shared across districts in a year.
# - **Conley spatial errors**, which allow nearby districts to be correlated, with a 100 km
#   cut-off and 2 years of serial correlation.
# - **Randomisation inference**, which reassigns whole flood years across the panel. This
#   keeps each flood's real spatial pattern and asks how often a flood-year map placed in the
#   wrong year gives an effect this large.

# %%
def within(df, cols):
    a = df[cols].astype(float)
    return a - a.groupby(df.district).transform("mean") - a.groupby(df.harvest_year).transform("mean") + a.mean()


def panel_fit(df, y, x, cov):
    d = df.set_index(["district", "harvest_year"])
    m = PanelOLS(d[y], d[x], entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
    if cov == "cluster":
        return m.fit(cov_type="clustered", cluster_entity=True)
    return m.fit(cov_type="kernel", kernel="bartlett", bandwidth=2)


def conley_se(df, y, x):
    w = within(df, [y] + x)
    X, Y = w[x].values, w[y].values
    XtXi = np.linalg.pinv(X.T @ X)
    e = Y - X @ (XtXi @ X.T @ Y)
    u = pd.DataFrame(X * e[:, None], columns=x, index=df.index)
    u["district"], u["harvest_year"] = df.district.values, df.harvest_year.values
    k = len(x)
    meat = np.zeros((k, k))
    for _, s in u.groupby("harvest_year"):
        c = XY.loc[s.district.values].values
        dist = np.sqrt(((c[:, None, :] - c[None, :, :]) ** 2).sum(2))
        K = np.clip(1 - dist / CUTOFF_KM, 0, None)
        S = s[x].values
        meat += S.T @ K @ S
    for _, s in u.groupby("district"):
        S = s.sort_values("harvest_year")[x].values
        for lag in range(1, SERIAL_LAGS + 1):
            a = S[lag:].T @ S[:-lag] * (1 - lag / (SERIAL_LAGS + 1))
            meat += a + a.T
    V = XtXi @ meat @ XtXi
    return pd.Series(np.sqrt(np.clip(np.diag(V), 0, None)), index=x)


def ri_p(df, y, x, focal, n):
    """Permutes whole years of the focal variable, holding the other regressors fixed."""
    d = df.sort_values(["district", "harvest_year"])
    N, T = d.district.nunique(), d.harvest_year.nunique()
    if len(d) != N * T:
        return np.nan
    w = within(d, [y] + x)
    others = [c for c in x if c != focal]
    Z = w[others].values
    P = np.eye(len(d)) if not others else None
    res = (lambda v: v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0]) if others else (lambda v: v)
    yr = res(w[y].values)
    xw = w[focal].values.reshape(N, T)
    xr = res(xw.ravel())
    b0 = xr @ yr / (xr @ xr)
    count = 0
    for _ in range(n):
        v = res(xw[:, RNG.permutation(T)].ravel())
        count += abs(v @ yr / (v @ v)) >= abs(b0)
    return (count + 1) / (n + 1)


def estimate(df, y, x, focal, ri=RI_CHECK, conley=True):
    """One coefficient under all four methods."""
    c, k = panel_fit(df, y, x, "cluster"), panel_fit(df, y, x, "dk")
    b, se_c, se_k = float(c.params[focal]), float(c.std_errors[focal]), float(k.std_errors[focal])
    out = dict(b=b, se_cluster=se_c, p_cluster=float(c.pvalues[focal]), se_dk=se_k, p_dk=float(k.pvalues[focal]),
               n=int(c.nobs), r2_within=float(c.rsquared))
    if conley:
        se = float(conley_se(df, y, x)[focal])
        out.update(se_conley=se, p_conley=float(2 * stats.norm.sf(abs(b) / se)) if se > 0 else np.nan)
    if ri:
        out["p_ri"] = float(ri_p(df, y, x, focal, ri))
    return out


def sample(years, cols):
    return p[p.harvest_year.between(*years)].dropna(subset=cols).copy()


def pct(b):
    return 100 * (np.exp(b) - 1)


# %% [markdown]
# ## Limits of randomisation inference
#
# With T flood years, a single event can land in its true year only once in T tries, so a
# result driven by one event cannot reach a p-value below 1/T. For two events the limit is
# 1/(T(T−1)). This is calculated from the sample sizes alone, before looking at any model.

# %%
floors = {}
for k, s in SPECS.items():
    T = s["years"][1] - s["years"][0] + 1
    floors[k] = dict(years=T, one_event=1 / T, two_events=1 / (T * (T - 1)))
R["ri_floor"] = floors
print(floors)

# %% [markdown]
# ## Main flood models
#
# Each model has the flash flood, the monsoon flood and the weather controls together, with
# district and year fixed effects. Sentinel-1 covers 2016–2025 and JRC 2011–2021. The sum of
# the area and yield effects is compared with the production effect.

# %%
main, rows = {}, []
for key, s in SPECS.items():
    x = [s["flash"], s["monsoon"]] + CONTROLS
    df = sample(s["years"], x + list(OUTCOMES))
    main[key] = {}
    for y, label in OUTCOMES.items():
        main[key][y] = {}
        for var, name in ((s["flash"], "flash"), (s["monsoon"], "monsoon")):
            e = estimate(df, y, x, var, ri=RI_MAIN)
            main[key][y][name] = e
            rows.append(dict(source=s["label"], flood=name, outcome=label, **e, pct=pct(e["b"])))
    print(key, "identity gap", abs(main[key]["log_prod"]["flash"]["b"] - main[key]["log_area"]["flash"]["b"] - main[key]["log_yield"]["flash"]["b"]))
R["main"] = main
table_main = pd.DataFrame(rows)
table_main.to_csv(OUT / "table_main.csv", index=False)
print(table_main[["source", "flood", "outcome", "b", "pct", "p_cluster", "p_dk", "p_conley", "p_ri", "n"]].round(3).to_string())

# %% [markdown]
# ## Is the yield effect negligible?
#
# The yield claim needs positive evidence. It holds only if the 95 % interval lies within
# ±2 % per 10 points under every method that gives an interval.

# %%
neg = {}
for key in SPECS:
    e = main[key]["log_yield"]["flash"]
    ci = {m: (e["b"] - 1.96 * e[f"se_{m}"], e["b"] + 1.96 * e[f"se_{m}"]) for m in ("cluster", "dk", "conley")}
    neg[key] = dict(ci={m: [pct(a), pct(b)] for m, (a, b) in ci.items()},
                    negligible=all(a >= -YIELD_BOUND and b <= YIELD_BOUND for a, b in ci.values()))
R["yield_negligible"] = neg
print(json.dumps(neg, indent=1))

# %% [markdown]
# ## Year-by-year comparison of haor and other districts
#
# This shows any trend before a flood, the size of each drop, and whether area recovers.
# Each haor-by-year coefficient is measured against 2015, the last year before the two
# largest floods.

# %%
rows = []
d = p.copy()
years = [t for t in sorted(d.harvest_year.unique()) if t != 2015]
for t in years:
    d[f"h{t}"] = ((d.harvest_year == t) & (d.haor == 1)).astype(float)
xs = [f"h{t}" for t in years] + CONTROLS
for y, label in OUTCOMES.items():
    r = panel_fit(d, y, xs, "cluster")
    for t in years:
        rows.append(dict(outcome=label, year=t, b=float(r.params[f"h{t}"]), se=float(r.std_errors[f"h{t}"]), p=float(r.pvalues[f"h{t}"]),
                         event=t in EVENT_YEARS))
    rows.append(dict(outcome=label, year=2015, b=0.0, se=0.0, p=np.nan, event=False))
ev = pd.DataFrame(rows).sort_values(["outcome", "year"])
ev["pct"] = pct(ev.b)
ev.to_csv(OUT / "table_haor_by_year.csv", index=False)
print(ev.pivot(index="year", columns="outcome", values="pct").round(1).to_string())
pre = ev[(ev.outcome == "Harvested area") & (ev.year < 2015)]
R["haor_by_year"] = {o: {str(int(r.year)): dict(pct=r.pct, p=r.p) for r in ev[ev.outcome == o].itertuples()} for o in OUTCOMES.values()}
R["haor_pre_trend"] = dict(max_abs_pct=float(pre.pct.abs().max()), any_sig=bool((pre.p < 0.05).any()))

# %% [markdown]
# ## Synthetic control for the 2017 flood
#
# For each of the five most flooded districts in 2017, a weighted mix of non-haor districts
# is chosen to match its path in 2011–2015. The 2016 flood is left out of the fit. The gap in
# 2017 is the estimated effect. Inference comes from running the same method on every donor
# district, and ranking the treated district's gap relative to its pre-flood fit.

# %%
def synth_path(wide, unit, donors, pre):
    Y1 = wide.loc[unit] - wide.loc[unit, pre].mean()
    Y0 = wide.loc[donors].sub(wide.loc[donors, pre].mean(axis=1), axis=0)
    A, b = Y0[pre].T.values, Y1[pre].values
    n = len(donors)
    f = lambda w: ((A @ w - b) ** 2).sum() + 1e-4 * (w ** 2).sum()
    res = minimize(f, np.ones(n) / n, bounds=[(0, 1)] * n, constraints={"type": "eq", "fun": lambda w: w.sum() - 1},
                   method="SLSQP", options=dict(maxiter=300, ftol=1e-9))
    gap = Y1 - pd.Series(res.x @ Y0.values, index=wide.columns)
    return gap, float(np.sqrt((gap[pre] ** 2).mean()))


PRE = [2011, 2012, 2013, 2014, 2015]
top5 = p[p.harvest_year == 2017].nlargest(5, "s1_flash_flood").district.tolist()
donors = sorted(set(p.district) - set(HAOR))
rows = []
for y, label in OUTCOMES.items():
    wide = p.pivot(index="district", columns="harvest_year", values=y)
    placebo, placebo_gap = [], []
    for dn in donors:
        gap, rm = synth_path(wide, dn, [x for x in donors if x != dn], PRE)
        placebo.append(abs(gap[2017]) / rm if rm > 0 else 0)
        placebo_gap.append(abs(gap[2017]))
    placebo, placebo_gap = np.array(placebo), np.array(placebo_gap)
    for u in top5:
        gap, rm = synth_path(wide, u, donors, PRE)
        ratio = abs(gap[2017]) / rm if rm > 0 else np.inf
        rows.append(dict(outcome=label, district=u, gap_2016=pct(gap[2016]), gap_2017=pct(gap[2017]), gap_2018=pct(gap[2018]),
                         pre_rmse=rm, ratio=ratio, rank_p=(1 + (placebo >= ratio).sum()) / (len(placebo) + 1),
                         gap_rank_p=(1 + (placebo_gap >= abs(gap[2017])).sum()) / (len(placebo_gap) + 1)))
syn = pd.DataFrame(rows)
syn.to_csv(OUT / "table_synthetic_control.csv", index=False)
print(syn.round(3).to_string())
R["synth"] = {o: g.drop(columns="outcome").to_dict("records") for o, g in syn.groupby("outcome")}

# %% [markdown]
# ## Are flood effects concentrated in the haor? (Q3)
#
# The flash-flood effect is allowed to differ between haor and other districts. Few floods
# of any size occur outside the haor, so this estimate is limited.

# %%
rows = []
for key, s in SPECS.items():
    df = sample(s["years"], [s["flash"], s["monsoon"]] + CONTROLS + list(OUTCOMES))
    df["fx"] = df[s["flash"]] * df.haor
    x = [s["flash"], "fx", s["monsoon"]] + CONTROLS
    for y, label in OUTCOMES.items():
        e = estimate(df, y, x, "fx", ri=RI_CHECK, conley=False)
        c = panel_fit(df, y, x, "cluster")
        rows.append(dict(source=s["label"], outcome=label, other_b=float(c.params[s["flash"]]), other_p=float(c.pvalues[s["flash"]]),
                         extra_haor_b=e["b"], p_cluster=e["p_cluster"], p_dk=e["p_dk"], p_ri=e["p_ri"]))
q3 = pd.DataFrame(rows)
q3.to_csv(OUT / "table_haor_interaction.csv", index=False)
print(q3.round(3).to_string())
R["q3"] = q3.to_dict("records")

# %% [markdown]
# ## Normal and extreme floods (Q2 and bins)
#
# Banerjee (2010) and Asada et al. (2005) suggest that normal monsoon floods help and extreme
# ones harm. Flood fractions are put in bins, against the group below 1 %, so that the
# relationship need not be a straight line.

# %%
BINS = [(1, 5, "1-5"), (5, 20, "5-20"), (20, 101, "20+")]
rows = []
for key, s in SPECS.items():
    for var, name in ((s["flash"], "flash"), (s["monsoon"], "monsoon")):
        df = sample(s["years"], [s["flash"], s["monsoon"]] + CONTROLS + list(OUTCOMES))
        pc = df[var] * 10
        b = []
        for lo, hi, lab in BINS:
            c = "b_" + lab.replace("-", "_").replace("+", "p")
            df[c] = pc.between(lo, hi, inclusive="left").astype(float)
            b.append((c, lab))
        other = s["monsoon"] if name == "flash" else s["flash"]
        x = [c for c, _ in b] + [other] + CONTROLS
        for y, label in OUTCOMES.items():
            cl, dk = panel_fit(df, y, x, "cluster"), panel_fit(df, y, x, "dk")
            for c, lab in b:
                rows.append(dict(source=s["label"], flood=name, outcome=label, bin=lab, n_in_bin=int(df[c].sum()), b=float(cl.params[c]), se=float(cl.std_errors[c]),
                                 pct=pct(float(cl.params[c])), p_cluster=float(cl.pvalues[c]), p_dk=float(dk.pvalues[c])))
bins = pd.DataFrame(rows)
bins.to_csv(OUT / "table_flood_bins.csv", index=False)
print(bins.round(3).to_string())
R["bins"] = bins.to_dict("records")

# %% [markdown]
# ## Required and reported checks
#
# Each check reruns the main area and yield models with one change. The pass rules were fixed
# in the analysis plan before this code was run. `required` marks checks that a supported
# result must pass.

# %%
checks = []


def add(name, kind, required, key, y, e, base, rule):
    if rule == "leave":
        ok = np.sign(e["b"]) == np.sign(base["b"]) and abs(e["b"]) >= 0.5 * abs(base["b"])
    elif rule == "placebo":
        ok = e["p_cluster"] >= 0.05 and e["p_dk"] >= 0.05
    elif rule == "sign":
        ok = np.sign(e["b"]) == np.sign(base["b"]) and e["p_dk"] < 0.05
    else:
        ok = None
    checks.append(dict(check=name, kind=kind, required=required, source=SPECS[key]["label"], outcome=OUTCOMES[y], b=e["b"], se_cluster=e.get("se_cluster", np.nan), pct=pct(e["b"]),
                       p_cluster=e["p_cluster"], p_dk=e["p_dk"], p_conley=e.get("p_conley", np.nan), p_ri=e.get("p_ri", np.nan), n=e["n"], passed=ok))


for key, s in SPECS.items():
    fl, mo = s["flash"], s["monsoon"]
    x = [fl, mo] + CONTROLS
    base_df = sample(s["years"], x + list(OUTCOMES))
    for y in ("log_area", "log_yield"):
        base = main[key][y]["flash"]
        for t in EVENT_YEARS:
            if base_df.harvest_year.eq(t).any():
                add(f"Leave out {t}", "event", True, key, y, estimate(base_df[base_df.harvest_year != t], y, x, fl, ri=999), base, "leave")
        two = base_df[~base_df.harvest_year.isin([2016, 2017])]
        add("Leave out 2016 and 2017", "event", False, key, y, estimate(two, y, x, fl, ri=999), base, "leave")
        for dist in ("Sunamganj", "Kishoreganj", "Sylhet", "Netrokona"):
            add(f"Leave out {dist}", "district", True, key, y, estimate(base_df[base_df.district != dist], y, x, fl, ri=999), base, "leave")
        lead = sample(s["years"], x + [fl + "_lead"] + list(OUTCOMES))
        add("Next year's flash flood (placebo)", "placebo", True, key, y, estimate(lead, y, x + [fl + "_lead"], fl + "_lead"), base, "placebo")
        post = sample(s["years"], x + [mo + "_lead"] + list(OUTCOMES))
        add("Flood after harvest (placebo)", "placebo", True, key, y, estimate(post, y, x + [mo + "_lead"], mo + "_lead"), base, "placebo")
        rice = key + "_flash_boro_10"
        rmon = key + "_monsoon_boro_10"
        add("Rice land only", "measure", True, key, y, estimate(sample(s["years"], [rice, rmon] + CONTROLS + list(OUTCOMES)), y, [rice, rmon] + CONTROLS, rice), base, "sign")
        early, late = key + "_early_wd_10", key + "_late_wd_10"
        df = sample(s["years"], [early, late, mo] + CONTROLS + list(OUTCOMES))
        add("January-February baseline, early window", "measure", True, key, y, estimate(df, y, [early, late, mo] + CONTROLS, early), base, "sign")
        add("January-February baseline, late window", "measure", False, key, y, estimate(df, y, [early, late, mo] + CONTROLS, late), base, None)
        early_r, late_r = key + "_early_boro_10", key + "_late_boro_10"
        df = sample(s["years"], [early_r, late_r, mo] + CONTROLS + list(OUTCOMES))
        add("Early window on rice land", "measure", False, key, y, estimate(df, y, [early_r, late_r, mo] + CONTROLS, early_r), base, None)
        if key == "s1":
            df = sample(s["years"], x + ["s1_scenes_flash_10", "s1_scenes_dry_10"] + list(OUTCOMES))
            add("Scene counts as controls", "coverage", True, key, y, estimate(df, y, x + ["s1_scenes_flash_10", "s1_scenes_dry_10"], fl), base, "sign")
            alt = sample((2015, 2025), [fl] + CONTROLS + list(OUTCOMES))
            add("Flash flood only, 2015-2025", "reported", False, key, y, estimate(alt, y, [fl] + CONTROLS, fl), base, None)
            for c, lab in (("s1_flash_m16_wd_10", "-16 dB"), ("s1_flash_m20_wd_10", "-20 dB")):
                df = sample(s["years"], [c, mo] + CONTROLS + list(OUTCOMES))
                add(f"Water threshold {lab}", "reported", False, key, y, estimate(df, y, [c, mo] + CONTROLS, c), base, None)
        # Added after the planned results: small districts and one unexplained value
        big = base_df.groupby("district").area_ha.transform("mean") >= SMALL_HA
        add("Districts under 15,000 ha left out", "reported", False, key, y, estimate(base_df[big], y, x, fl, ri=999), base, None)
        add("Leave out Chandpur", "reported", False, key, y, estimate(base_df[base_df.district != "Chandpur"], y, x, fl, ri=999), base, None)
        # Regional shocks: division-by-year effects
        df = base_df.copy()
        dum = pd.get_dummies(df.division.astype(str) + "_" + df.harvest_year.astype(str), dtype=float, drop_first=True)
        dum = dum.loc[:, dum.sum() > 1]
        dv = pd.concat([df, dum.add_prefix("dy_")], axis=1)
        xd = x + list(dum.add_prefix("dy_").columns)
        cl, dk = panel_fit(dv, y, xd, "cluster"), panel_fit(dv, y, xd, "dk")
        add("Division-by-year effects", "reported", False, key, y, dict(b=float(cl.params[fl]), se_cluster=float(cl.std_errors[fl]), p_cluster=float(cl.pvalues[fl]), p_dk=float(dk.pvalues[fl]), n=int(cl.nobs)), base, None)
        # Different long-run paths: district-specific linear trends
        df = base_df.copy()
        tr = pd.get_dummies(df.district, dtype=float, drop_first=True).mul(df.harvest_year - df.harvest_year.mean(), axis=0).add_prefix("tr_")
        dv = pd.concat([df, tr], axis=1)
        xd = x + list(tr.columns)
        cl, dk = panel_fit(dv, y, xd, "cluster"), panel_fit(dv, y, xd, "dk")
        add("District linear trends", "reported", False, key, y, dict(b=float(cl.params[fl]), se_cluster=float(cl.std_errors[fl]), p_cluster=float(cl.pvalues[fl]), p_dk=float(dk.pvalues[fl]), n=int(cl.nobs)), base, None)
        # Spillovers from neighbouring districts
        nb = fl + "_nbr"
        add("Neighbours' flood, own effect", "reported", False, key, y, estimate(sample(s["years"], x + [nb] + list(OUTCOMES)), y, x + [nb], fl, ri=999), base, None)
        add("Neighbours' flood, spillover", "reported", False, key, y, estimate(sample(s["years"], x + [nb] + list(OUTCOMES)), y, x + [nb], nb, ri=999), base, None)
    # Dependence on the log form: Poisson with district and year effects
    for y, level, yl in (("log_area", "area_ha", "log_area"), ("log_prod", "production_t", "log_prod")):
        D = pd.concat([base_df[x], pd.get_dummies(base_df.district, dtype=float, drop_first=True),
                       pd.get_dummies(base_df.harvest_year, dtype=float, drop_first=True).add_prefix("y")], axis=1)
        D = sm.add_constant(D.astype(float))
        r = sm.GLM(base_df[level].astype(float), D, family=sm.families.Poisson()).fit(cov_type="cluster", cov_kwds=dict(groups=base_df.district.astype("category").cat.codes))
        add("Poisson model", "reported", False, key, yl, dict(b=float(r.params[fl]), p_cluster=float(r.pvalues[fl]), p_dk=np.nan, n=int(r.nobs)), main[key][yl]["flash"], None)
ck = pd.DataFrame(checks)
ck.to_csv(OUT / "table_checks.csv", index=False)
print(ck[["check", "source", "outcome", "pct", "p_cluster", "p_dk", "p_conley", "p_ri", "passed"]].round(3).to_string())

# %% [markdown]
# ## Satellite crop loss: an independent check on BBS
#
# If floods really destroyed crops, satellite greenness on Boro land should fall in the same
# places and years, using no BBS data. Two links are tested: flood raises satellite loss, and
# satellite loss lowers BBS harvested area.

# %%
sat = {}
for key, s in SPECS.items():
    x = [s["flash"], s["monsoon"]] + CONTROLS
    a = estimate(sample(s["years"], x + ["loss_share"]), "loss_share", x, s["flash"], ri=RI_CHECK)
    sat[key] = dict(flood_to_loss=a)
df = p.dropna(subset=["loss_share"] + CONTROLS)
for y in ("log_area", "log_yield", "log_prod"):
    sat[y] = estimate(df, y, ["loss_share"] + CONTROLS, "loss_share", ri=RI_CHECK)
sat["passed"] = bool(all(sat[k]["flood_to_loss"]["b"] > 0 and sat[k]["flood_to_loss"]["p_dk"] < 0.05 for k in SPECS)
                     and sat["log_area"]["b"] < 0 and sat["log_area"]["p_dk"] < 0.05)
R["satellite_check"] = sat
print(json.dumps({k: (round(v["b"], 3), round(v["p_dk"], 4)) for k, v in sat.items() if k.startswith("log")}, indent=1))
print({k: (round(sat[k]["flood_to_loss"]["b"], 3), round(sat[k]["flood_to_loss"]["p_dk"], 4)) for k in SPECS}, "passed:", sat["passed"])
event17 = p[p.harvest_year == 2017].set_index("district")[["s1_flash_flood", "jrc_flash_flood", "loss_share", "ndvi_change_anom"]]
ref = p[p.harvest_year.isin([2015, 2018])].groupby("district")[["area_ha", "production_t", "yield_t_ha"]].mean()
now = p[p.harvest_year == 2017].set_index("district")[["area_ha", "production_t", "yield_t_ha"]]
chg = (now / ref - 1) * 100
event17 = event17.join(chg.add_suffix("_chg_pct")).sort_values("s1_flash_flood", ascending=False)
event17.round(3).to_csv(OUT / "table_event_2017.csv")
print(event17.head(9).round(2).to_string())
r_loss = np.corrcoef(event17.loss_share, event17.area_ha_chg_pct)[0, 1]
R["event_2017_corr_loss_area"] = float(r_loss)
haor = p[p.district.isin(HAOR)]
base = haor[haor.harvest_year.isin([2015, 2018])].groupby("district").production_t.mean().sum()
lost = base - haor[haor.harvest_year == 2017].production_t.sum()
# Published losses: Hossain et al. (2023) for the haor, Mondal et al. (2021) for Sunamganj
sun = p[p.district == "Sunamganj"]
sref = sun[sun.harvest_year.isin([2015, 2018])][["area_ha", "production_t"]].mean()
snow = sun[sun.harvest_year == 2017].iloc[0]
R["reported_2017"] = dict(bbs_haor_loss_mt=float(lost / 1e6), published_haor_loss_mt=0.88,
                          bbs_sunamganj_area_loss_ha=float(sref.area_ha - snow.area_ha), published_sunamganj_area_ha=149224,
                          bbs_sunamganj_prod_loss_t=float(sref.production_t - snow.production_t), published_sunamganj_prod_t=393855)
print(R["reported_2017"], "corr(loss, area change) 2017:", round(r_loss, 3))

# %% [markdown]
# ## NDVI and yield (Q4)
#
# The tests fixed in the plan: between and within districts, with and without year effects,
# in three windows, and by how much of the district is Boro land.

# %%
rows = []
for win, label in (("ndvi_peak", "January-April"), ("ndvi_feb_mar", "February to mid-March"), ("ndvi_heading", "Late March to early April")):
    d = p.dropna(subset=[win, "log_yield"])
    m = d.groupby("district")[[win, "log_yield"]].mean()
    between = np.corrcoef(m[win], m.log_yield)[0, 1]
    dm = d[[win, "log_yield"]] - d.groupby("district")[[win, "log_yield"]].transform("mean")
    within_d = np.corrcoef(dm[win], dm.log_yield)[0, 1]
    tw = within(d, [win, "log_yield"])
    within_two = np.corrcoef(tw[win], tw.log_yield)[0, 1]
    d = d.assign(ndvi_01=d[win] * 10)
    e = estimate(d, "log_yield", ["ndvi_01"] + CONTROLS, "ndvi_01", ri=RI_CHECK)
    rows.append(dict(window=label, between=between, within_district=within_d, within_two_way=within_two, b=e["b"], p_cluster=e["p_cluster"], p_dk=e["p_dk"], p_ri=e["p_ri"]))
ndvi = pd.DataFrame(rows)
ndvi.to_csv(OUT / "table_ndvi.csv", index=False)
print(ndvi.round(3).to_string())
p["purity"] = p.boro_stable_km2 / p.area_km2
pure = p.purity > p.groupby("district").purity.transform("first").median()
rows = []
for name, mask in (("More rice land", pure), ("Less rice land", ~pure)):
    tw = within(p[mask], ["ndvi_heading", "log_yield"])
    rows.append(dict(group=name, within_two_way=float(np.corrcoef(tw.ndvi_heading, tw.log_yield)[0, 1])))
R["ndvi_purity"] = rows
print(rows)

# %% [markdown]
# ## Exploratory analyses, added after the planned results were seen
#
# These were not in the analysis plan and are labelled as exploratory in the paper. The planned
# results showed that the 2016 and 2022 floods left no fall in BBS area, while 2017 did, and
# that the early-window check brought the two flood records close together. So this section
# asks how much of the early-window result rests on 2017, and when water arrived in each
# flood year. The planned verdict below is not changed by anything here.

# %%
rows = []
for key, s in SPECS.items():
    early, late, mo = key + "_early_wd_10", key + "_late_wd_10", s["monsoon"]
    x = [early, late, mo] + CONTROLS
    df = sample(s["years"], x + list(OUTCOMES))
    for y, label in OUTCOMES.items():
        for name, d in (("All years", df), ("Without 2017", df[df.harvest_year != 2017]), ("Without 2016", df[df.harvest_year != 2016])):
            e = estimate(d, y, x, early, ri=RI_CHECK)
            rows.append(dict(source=s["label"], outcome=label, sample=name, b=e["b"], pct=pct(e["b"]), p_cluster=e["p_cluster"],
                             p_dk=e["p_dk"], p_conley=e["p_conley"], p_ri=e["p_ri"], n=e["n"]))
early_tab = pd.DataFrame(rows)
early_tab.to_csv(OUT / "table_early_window.csv", index=False)
print(early_tab.round(3).to_string())

hy = p[p.district.isin(HAOR)].groupby("harvest_year")[["s1_early_wd", "s1_late_wd", "jrc_early_wd", "jrc_late_wd", "s1_flash_flood", "jrc_flash_flood", "loss_share"]].mean() * 100
hy.round(2).to_csv(OUT / "table_flood_timing.csv")
print(hy.round(1).to_string())
R["timing"] = {str(int(t)): r.to_dict() for t, r in hy.loc[[2016, 2017, 2022]].iterrows()}
out_h = p[~p.district.isin(HAOR)]
R["outside_haor"] = dict(s1_above_5=float((out_h.s1_flash_flood.dropna() >= 0.05).mean() * 100), s1_p99=float(out_h.s1_flash_flood.quantile(0.99) * 100))
print(R["outside_haor"])

# %% [markdown]
# ## Verdict on the main question
#
# The verdict applies the rule fixed in the plan, with no judgement added here.

# %%
def all_sig(e):
    return all(e[k] < 0.05 for k in ("p_cluster", "p_dk", "p_conley", "p_ri"))


area = {k: main[k]["log_area"]["flash"] for k in SPECS}
sig_by_source = {k: bool(all_sig(v)) for k, v in area.items()}
same_dir = bool(np.sign(area["s1"]["b"]) == np.sign(area["jrc"]["b"]))
req = ck[ck.required & (ck.outcome == "Harvested area")]
syn_a = syn[syn.outcome == "Harvested area"]
syn_ok = bool((syn_a.gap_2017 < 0).all() and (syn_a.rank_p <= 0.05).all())
hy = ev[(ev.outcome == "Harvested area") & (ev.year == 2017)].iloc[0]
designs = bool(area["s1"]["b"] < 0 and hy.b < 0 and (syn_a.gap_2017 < 0).all())
fail = req[req.passed == False][["check", "source"]].to_dict("records")       # noqa: E712
verdict = "supported" if all(sig_by_source.values()) and same_dir and designs and not fail and sat["passed"] and syn_ok else \
          "suggestive" if any(sig_by_source.values()) and same_dir and designs else "not supported"
R["verdict_q1"] = dict(verdict=verdict, significant_by_source=sig_by_source, same_direction=same_dir, designs_agree=designs,
                       required_failed=fail, n_required=int(len(req)), n_required_passed=int((req.passed == True).sum()),      # noqa: E712
                       satellite_passed=sat["passed"], synthetic_passed=syn_ok)
print(json.dumps(R["verdict_q1"], indent=1))

# %% [markdown]
# ## False discovery rate for secondary tests
#
# Monsoon-flood and haor-interaction tests are secondary, so their p-values are corrected
# together with the Benjamini–Hochberg method.

# %%
sec = table_main[table_main.flood == "monsoon"][["source", "outcome", "p_dk"]].assign(test="Monsoon flood")
sec = pd.concat([sec, q3[["source", "outcome", "p_dk"]].assign(test="Extra haor effect")], ignore_index=True)
sec["p_fdr"] = multipletests(sec.p_dk, method="fdr_bh")[1]
sec.to_csv(OUT / "table_secondary_fdr.csv", index=False)
print(sec.round(3).to_string())
R["fdr_any_sig"] = bool((sec.p_fdr < 0.05).any())
json.dump(R, open(OUT / "results.json", "w"), indent=1, default=float)
print("results written")

# %% [markdown]
# # 02. Build and validate the analysis panel
#
# This notebook joins the new Earth Engine variables to the Gold panel of Paper 1 and
# checks them before any model is run. Paper 1 is read and never changed.
#
# The most important check comes first. The new code recomputes Paper 1's flood rule, and
# the result must match the published values. If it does, the new variants are computed by
# code known to be correct.
#
# This notebook reads BBS area only to judge the rice mask: between districts, and as
# national totals. It fits no flood model.

# %%
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd().parent
FRAMEWORK = ROOT.parent / "bd-boro-data-framework"
sys.path.insert(0, str(FRAMEWORK / "v2" / "src"))
import duckdb                                            # noqa: E402
from common import V2_GOLD, panel_sha256                 # noqa: E402

BRONZE, OUT = ROOT / "data" / "bronze", ROOT / "outputs"
(ROOT / "data").mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
EXPECTED_PANEL = "5cbaeb1edaef99f3411a56d5797d32b4de475d10f6041df2df1fd7b7d5336d24"
checks = []


def check(name, ok, observed):
    checks.append(dict(check=name, observed=str(observed), status="PASS" if ok else "FAIL"))
    print(("PASS  " if ok else "FAIL  ") + name + ": " + str(observed))


# %% [markdown]
# ## Load the Gold panel and the extracts
#
# The panel checksum is confirmed first, so that every result in this paper is tied to the
# archived Paper 1 data (Zenodo 10.5281/zenodo.23795046).

# %%
check("Gold panel matches the archived Paper 1 panel", panel_sha256() == EXPECTED_PANEL, panel_sha256()[:12])
con = duckdb.connect(str(V2_GOLD), read_only=True)
panel = con.execute("SELECT * FROM fact_boro_panel").df()
con.close()


def load(name):
    return pd.concat([pd.read_csv(f) for f in sorted(BRONZE.glob(f"{name}_20*.csv"))], ignore_index=True)


extracts = {n: load(n) for n in ("modis", "weather", "ndviwin", "scenes", "s1", "jrc", "s1thr")}
EXPECTED_YEARS = {"modis": 15, "weather": 15, "ndviwin": 15, "scenes": 11, "s1": 11, "jrc": 11, "s1thr": 11}
for n, d in extracts.items():
    # Sentinel-1 has no monsoon value for 2015, because it begins in October 2014
    vals = d[d.harvest_year > 2015] if n == "s1" else d
    ok = len(d) == 64 * EXPECTED_YEARS[n] and not vals.isna().any().any()
    check(f"{n}: 64 districts in every year, no missing value", ok, f"{len(d)} rows")

# %% [markdown]
# ## Does the new code reproduce Paper 1?
#
# Each `_wd` column below recomputes a published Gold column. The largest absolute difference
# must be a rounding error.

# %%
p = panel.copy()
for d in extracts.values():
    p = p.merge(d, on=["district", "harvest_year"], how="left")
for new, old, in (("s1_flash_wd", "s1_flash_flood"), ("s1_monsoon_wd", "s1_monsoon_flood"),
                  ("jrc_flash_wd", "jrc_flash_flood")):
    x = p.dropna(subset=[new, old])
    diff = (x[new] - x[old]).abs().max()
    check(f"{new} reproduces Paper 1's {old}", diff < 1e-6, f"max difference {diff:.2e}, n={len(x)}")
x = p[p.harvest_year <= 2021].dropna(subset=["jrc_monsoon_wd", "jrc_monsoon_flood"])
diff = (x.jrc_monsoon_wd - x.jrc_monsoon_flood).abs().max()
check("jrc_monsoon_wd reproduces Paper 1's jrc_monsoon_flood", diff < 1e-6, f"max difference {diff:.2e}, n={len(x)}")

# %% [markdown]
# ## Are the new variables in range?

# %%
frac = [c for c in p.columns if c.endswith(("_wd", "_boro")) or c in ("loss_share", "loss_valid")]
lo, hi = np.nanmin(p[frac].values), np.nanmax(p[frac].values)
check("all fractions lie between 0 and 1", lo >= 0 and hi <= 1 + 1e-9, f"{lo:.4f} to {hi:.4f}")
check("Boro land never exceeds district area", (p.boro_km2 <= p.area_km2).all() and (p.boro_stable_km2 <= p.area_km2).all(),
      f"largest share {(p.boro_stable_km2 / p.area_km2).max():.2f}")
check("Sentinel-1 scenes exist in every district-year", (p.s1_scenes_flash.dropna() > 0).all(),
      f"minimum {p.s1_scenes_flash.min():.0f} in Apr-May")
check("satellite crop loss is observed on most Boro land", p.loss_valid.min() > 0.5, f"minimum valid share {p.loss_valid.min():.2f}")

# %% [markdown]
# ## Is the Boro mask credible?
#
# The mask is judged in two ways that do not involve flood effects: against BBS harvested
# area between districts, and against the national totals published by Shew and Ghosh (2019).
#
# Its 2017 area should not dip, because every image used predates the flood. BBS harvested
# area does dip in 2017, which is why the mask can estimate planted area.

# %%
mean = p.groupby("district")[["boro_km2", "boro_stable_km2", "area_ha"]].mean()
r_year = np.corrcoef(mean.boro_km2, mean.area_ha)[0, 1]
r_stable = np.corrcoef(mean.boro_stable_km2, mean.area_ha)[0, 1]
check("yearly mask agrees with BBS area between districts", r_year > 0.8, f"r = {r_year:.3f}")
check("stable mask agrees with BBS area between districts", r_stable > 0.8, f"r = {r_stable:.3f}")
nat = p.groupby("harvest_year").agg(mask_mha=("boro_km2", lambda s: s.sum() / 1e4), bbs_mha=("area_ha", lambda s: s.sum() / 1e6))
shew = pd.Series({2014: 4.285, 2015: 4.425, 2016: 4.645, 2017: 4.117, 2018: 4.407}, name="shew_ghosh_mha")
nat = nat.join(shew)
nat.round(3).to_csv(OUT / "table_mask_national.csv")
print(nat.round(2).to_string())
stable_mha = p.groupby("district").boro_stable_km2.first().sum() / 1e4
print(f"stable mask: {stable_mha:.2f} million ha")

# %% [markdown]
# ## Save the analysis panel

# %%
pd.DataFrame(checks).to_csv(OUT / "validation_variables.csv", index=False)
failed = [c["check"] for c in checks if c["status"] == "FAIL"]
p.to_parquet(ROOT / "data" / "analysis_panel.parquet", index=False)
json.dump(dict(checks=len(checks), failed=failed, stable_mask_mha=float(stable_mha), r_mask_year=float(r_year),
               r_mask_stable=float(r_stable), n_panel=len(p)), open(OUT / "dataset_summary.json", "w"), indent=1)
print(f"{len(checks)} checks, {len(failed)} failed")
if failed:
    raise SystemExit("validation failed: " + "; ".join(failed))

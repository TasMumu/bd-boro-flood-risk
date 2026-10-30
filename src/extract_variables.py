# %% [markdown]
# # 01. New variables from Earth Engine
#
# This notebook computes the district-by-year variables added for Paper 2. Flood rules,
# windows and thresholds are imported from Paper 1, and the Gold panel is read and never
# changed. The same flood rule is recomputed here as `*_wd` (whole district), which must
# reproduce the published Paper 1 values (checked in notebook 02).
#
# Harvest year t is the Boro crop sown in November of t-1 and harvested in April-May of t.

# %% [markdown]
# ## What is computed
#
# - **Boro mask.** MODIS MOD13Q1, 250 m, SummaryQA of 1 or less, on the cropland used in Paper 1.
#   A pixel is Boro land in year t if its peak NDVI from the composites starting in February
#   to early March reaches 0.50 and has risen by 0.20 since December to mid-January. All these
#   images end before the earliest flood, so the mask measures the crop before any loss.
# - **Stable mask.** Land meeting that rule in at least 5 of 15 years, used for flood fractions,
#   because the yearly mask varies with cloud and planting dates.
# - **Crop loss.** The change in NDVI from the pre-flood peak to the two composites starting in
#   April, minus that pixel's median change over all years, after the Disaster Vegetation Damage
#   Index of Rahman et al. (2020). `ndvi_change_anom` is the mean anomaly on Boro land, and
#   `loss_share` is the share of Boro land with an anomaly below -0.20.
# - **Flood.** Paper 1's rule (April-May against January-March), on Boro land and whole
#   district. `early` and `late` split the flash window against a January-February baseline,
#   so that water from a March flood is not counted as dry-season water. Sentinel-1 uses early
#   15 March-15 April and late 16 April-15 May, each as two half-month medians, because one
#   median over a month dilutes a flood that arrives midway. JRC is monthly, so it uses early
#   March-April and late May.
# - **Scenes.** Sentinel-1 scenes per district in January-March and April-May.
# - **Weather.** ERA5-Land: `hot_days_flower`, days above 35 C from 15 March to 30 April, and
#   `cold_days_repro`, days with mean temperature below 20 C from 15 February to 31 March. The
#   cold threshold is provisional.
#
# Results are cached per extract and year. An extract with any district or value missing is
# not saved, and nothing is gap filled.

# %%
"""Paper 2, step 3 - new district x harvest-year variables from Google Earth Engine.
Harvest year t = the Boro crop sown Nov(t-1), harvested Apr-May(t), as in Paper 1.

Paper 1 is read and never changed. Its flood rules, windows and thresholds are
imported from its schema, and the same rule is recomputed here as *_wd (whole
district), which must reproduce Paper 1's published values.

Boro mask   MODIS MOD13Q1, 250 m, SummaryQA <= 1, cropland as in Paper 1. A pixel is
            Boro land in year t if its peak NDVI over the composites starting
            Feb to mid-March reaches PEAK_NDVI and has risen by RISE_NDVI since
            Dec-mid Jan. All composites end before the earliest flood onset.
Crop loss   Change in NDVI from the pre-flood peak to the mean of the two composites
            starting in April, minus the pixel's median change over all years
            (after the Disaster Vegetation Damage Index of Rahman et al., 2020).
            ndvi_change_anom = mean anomaly on Boro land; loss_share = share of Boro
            land with an anomaly below LOSS_DROP.
Flood       Paper 1 rule (Apr-May against Jan-Mar), on Boro land and whole district.
            early and late split the flash window, against a Jan-Feb baseline, so
            that water from a March flood is not counted as dry-season water.
            Sentinel-1: early 15 Mar-15 Apr, late 16 Apr-15 May, each as two half-month
            medians, because one median over a month dilutes a flood that arrives midway.
            JRC is monthly: early Mar-Apr, late May.
Scenes      Sentinel-1 scenes per district in Jan-Mar and in Apr-May.
Weather     ERA5-Land: hot_days_flower, days with Tmax > 35 C, 15 Mar-30 Apr;
            cold_days_repro, days with Tmean < 20 C, 15 Feb-31 Mar.

Results are cached per extract and year in data/bronze/. An extract with any district
or value missing is not saved. Nothing is gap filled.

usage: python extract_variables.py [calibrate | test]
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd().parent
FRAMEWORK = ROOT.parent / "bd-boro-data-framework"
sys.path.insert(0, str(FRAMEWORK / "v2" / "src"))
from common import GEE_PROJECT, canon_district          # noqa: E402
from schema import EXTRACTS, window                      # noqa: E402

OUT = ROOT / "data" / "bronze"
OUT.mkdir(parents=True, exist_ok=True)
DATES = OUT / "extraction_dates.json"
PARAMS = OUT / "parameters.json"
YEARS = range(2011, 2026)
PEAK_NDVI, RISE_NDVI, LOSS_DROP = 0.50, 0.20, 0.20      # area barely changes for PEAK_NDVI 0.40-0.50 (`calibrate`)
STABLE_YEARS = 5
HOT_C, COLD_C = 35, 20
ee = None


# %% [markdown]
# ## Set-up

# %%
def setup_ee():
    global ee, FC, BD, MODIS, CROPLAND, ERA, JRC, S1, SLOPE_OK
    if ee is not None:
        return
    import ee as _ee
    ee = _ee
    ee.Initialize(project=GEE_PROJECT)
    g = gpd.read_file(FRAMEWORK / "data" / "bronze" / "gadm_shapefiles" / "gadm41_BGD_2.shp")
    g["district"] = g.NAME_2.map(canon_district)
    g["geometry"] = g.geometry.simplify(0.001, preserve_topology=True)
    gj = json.loads(g[["district", "geometry"]].to_json())
    FC = ee.FeatureCollection([ee.Feature(ee.Geometry(f["geometry"]), {"district": f["properties"]["district"]})
                               for f in gj["features"]])
    BD = FC.geometry().bounds()
    MODIS = ee.ImageCollection(EXTRACTS["ndvi"]["collection"])
    CROPLAND = (ee.Image("ESA/WorldCover/v200/2021").eq(40).unmask(0)
                .reduceResolution(ee.Reducer.mean(), maxPixels=1024)
                .reproject(MODIS.first().projection()).gt(0.5))
    ERA = ee.ImageCollection(EXTRACTS["climate"]["collection"])
    JRC = ee.ImageCollection(EXTRACTS["jrc"]["collection"])
    S1 = (ee.ImageCollection(EXTRACTS["s1"]["collection"])
          .filter(ee.Filter.eq("instrumentMode", "IW"))
          .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
          .filterBounds(BD).select("VV"))
    SLOPE_OK = ee.Terrain.slope(ee.Image("USGS/SRTMGL1_003")).lt(EXTRACTS["s1"]["slope_max_deg"])


def reduce(img, scale, reducer=None, tile=8, chunks=1):
    """District means or sums. A heavy request can be split into chunks of districts."""
    reducer = reducer or ee.Reducer.mean()
    bands = img.bandNames().getInfo()
    if len(bands) == 1:
        reducer = reducer.setOutputs(bands)
    names = FC.aggregate_array("district").getInfo()
    frames = []
    for i in range(chunks):
        fc = FC if chunks == 1 else FC.filter(ee.Filter.inList("district", names[i::chunks]))
        res = img.reduceRegions(collection=fc, reducer=reducer, scale=scale, tileScale=tile)
        rows = res.select(["district"] + bands, retainGeometry=False).getInfo()
        frames.append(pd.DataFrame([f["properties"] for f in rows["features"]]))
    return pd.concat(frames, ignore_index=True)


# %% [markdown]
# ## Boro mask and crop loss

# %%
def _ndvi(i):
    return i.select("NDVI").multiply(0.0001).updateMask(i.select("SummaryQA").lte(1))


def _peak(t):
    # Composites starting 2 Feb, 18 Feb and 6 Mar; the next one starts 22 Mar and could see a flood
    return MODIS.filterDate(f"{t}-02-01", f"{t}-03-20").map(_ndvi).max()


def _base(t):
    return MODIS.filterDate(f"{t - 1}-12-01", f"{t}-01-17").map(_ndvi).min()


def boro_mask(t, peak_ndvi=None):
    p = _peak(t)
    return p.gte(peak_ndvi or PEAK_NDVI).And(p.subtract(_base(t)).gte(RISE_NDVI)).And(CROPLAND).unmask(0)


def stable_mask():
    """Land that meets the yearly rule in at least STABLE_YEARS years, used for the flood
    fractions, because the yearly mask varies with cloud and planting dates."""
    return ee.ImageCollection([boro_mask(y).toInt() for y in YEARS]).sum().gte(STABLE_YEARS)


def _change(t):
    return MODIS.filterDate(f"{t}-04-06", f"{t}-05-08").map(_ndvi).mean().subtract(_peak(t))


def modis_vars(t):
    ref = ee.ImageCollection([_change(y) for y in YEARS]).median()
    anom = _change(t).subtract(ref)
    m = boro_mask(t)
    px = ee.Image.pixelArea().divide(1e6)
    area = reduce(px.updateMask(m).rename("boro_km2"), 250, ee.Reducer.sum())
    img = ee.Image.cat(anom.rename("ndvi_change_anom"), anom.lt(-LOSS_DROP).rename("loss_share")).updateMask(m)
    frac = reduce(img, 250)
    seen = reduce(anom.mask().gt(0).unmask(0).updateMask(m).rename("loss_valid"), 250)
    return area.merge(frac, on="district").merge(seen, on="district")


# %% [markdown]
# ## Flood fractions, scenes and weather

# %%
def _s1_water(start, end, db=None):
    e = EXTRACTS["s1"]
    vv = S1.filterDate(start, end).median().focal_median(e["focal_median_m"], "circle", "meters")
    return vv.lt(db or e["threshold_db"]).And(SLOPE_OK).unmask(0)


def _s1_any(year, w, db=None):
    offset, m0, m1 = w
    y = year + offset
    return ee.ImageCollection([_s1_water(*window(y, 0, m, m), db) for m in range(m0, m1 + 1)]).max()


def _s1_periods(periods):
    return ee.ImageCollection([_s1_water(a, b) for a, b in periods]).max()


def _jrc_water(year, w):
    offset, m0, m1 = w
    y = year + offset
    c = JRC.filter(ee.Filter.calendarRange(y, y, "year")).filter(ee.Filter.calendarRange(m0, m1, "month"))
    return c.map(lambda i: i.eq(2)).max().unmask(0)


def _flood_table(bands, mask, scale, prefix, chunks=1):
    """Whole-district fractions, and fractions on Boro land as share of that land."""
    img = []
    for name, b in bands.items():
        img += [b.rename(f"{name}_wd"), b.And(mask).rename(f"{name}_on")]
    # The first band sets the grid of the request, so flood bands come first, as in Paper 1
    df = reduce(ee.Image.cat(img + [mask.rename(f"{prefix}_mask")]).clip(BD), scale, chunks=chunks)
    for name in bands:
        df[f"{name}_boro"] = df[f"{name}_on"] / df[f"{prefix}_mask"]
    return df.drop(columns=[f"{n}_on" for n in bands] + [f"{prefix}_mask"])


def s1_vars(t):
    w = EXTRACTS["s1"]["windows"]
    dry, dry2 = _s1_water(*window(t, *w["flash_dry"])), _s1_water(f"{t}-01-01", f"{t}-03-01")
    bands = {"s1_flash": _s1_any(t, w["flash"]).And(dry.Not()),
             "s1_early": _s1_periods([(f"{t}-03-15", f"{t}-04-01"), (f"{t}-04-01", f"{t}-04-16")]).And(dry2.Not()),
             "s1_late": _s1_periods([(f"{t}-04-16", f"{t}-05-01"), (f"{t}-05-01", f"{t}-05-16")]).And(dry2.Not())}
    if t >= 2016:
        bands["s1_monsoon"] = _s1_any(t, w["monsoon"]).And(_s1_water(*window(t, *w["monsoon_dry"])).Not())
    return _flood_table(bands, stable_mask(), EXTRACTS["s1"]["scale_m"], "s1")


def jrc_vars(t):
    w = EXTRACTS["jrc"]["windows"]
    dry2 = _jrc_water(t, (0, 1, 2))
    bands = {"jrc_flash": _jrc_water(t, w["flash"]).And(_jrc_water(t, w["flash_dry"]).Not()),
             "jrc_early": _jrc_water(t, (0, 3, 4)).And(dry2.Not()),
             "jrc_late": _jrc_water(t, (0, 5, 5)).And(dry2.Not()),
             "jrc_monsoon": _jrc_water(t, w["monsoon"]).And(_jrc_water(t, w["monsoon_dry"]).Not())}
    return _flood_table(bands, stable_mask(), EXTRACTS["jrc"]["scale_m"], "jrc", chunks=6)   # 30 m is heavy


def s1_thresholds(t):
    """The Paper 1 flash-flood rule at other water thresholds, whole district."""
    w = EXTRACTS["s1"]["windows"]
    bands = [_s1_any(t, w["flash"], db).And(_s1_water(*window(t, *w["flash_dry"]), db).Not()).rename(name)
             for name, db in (("s1_flash_m16_wd", -16), ("s1_flash_m20_wd", -20))]
    return reduce(ee.Image.cat(bands).clip(BD), EXTRACTS["s1"]["scale_m"])


def ndvi_windows(t):
    """NDVI on stable Boro land before the flood window and around heading, plus that land's area."""
    m = stable_mask()
    img = ee.Image.cat(_peak(t).rename("ndvi_feb_mar"),
                       MODIS.filterDate(f"{t}-03-20", f"{t}-04-05").map(_ndvi).mean().rename("ndvi_heading"))
    area = reduce(ee.Image.pixelArea().divide(1e6).updateMask(m).rename("boro_stable_km2"), 250, ee.Reducer.sum())
    return reduce(img.updateMask(m), 250).merge(area, on="district")


def scenes(t):
    def count(f):
        c = S1.filterBounds(f.geometry())
        return f.set({"s1_scenes_dry": c.filterDate(f"{t}-01-01", f"{t}-04-01").size(),
                      "s1_scenes_flash": c.filterDate(f"{t}-04-01", f"{t}-06-01").size()})
    rows = FC.map(count).select(["district", "s1_scenes_dry", "s1_scenes_flash"], retainGeometry=False).getInfo()
    return pd.DataFrame([f["properties"] for f in rows["features"]])


def weather(t):
    def days(start, end, band, test):
        return ERA.filterDate(start, end).select(band).map(lambda i: test(i.subtract(273.15))).sum()
    hot = days(f"{t}-03-15", f"{t}-05-01", "temperature_2m_max", lambda x: x.gt(HOT_C)).rename("hot_days_flower")
    cold = days(f"{t}-02-15", f"{t}-04-01", "temperature_2m", lambda x: x.lt(COLD_C)).rename("cold_days_repro")
    return reduce(ee.Image.cat(hot, cold), EXTRACTS["climate"]["scale_m"])


# %% [markdown]
# ## Caching and completeness

# %%
JOBS = {"modis": (modis_vars, YEARS), "weather": (weather, YEARS), "ndviwin": (ndvi_windows, YEARS),
        "scenes": (scenes, range(2015, 2026)), "jrc": (jrc_vars, range(2011, 2022)), "s1": (s1_vars, range(2015, 2026)),
        "s1thr": (s1_thresholds, range(2015, 2026))}


def run(name, year):
    f = OUT / f"{name}_{year}.csv"
    if f.exists():
        return f"{name} {year}: cached"
    fn = JOBS[name][0]
    for attempt in range(3):
        try:
            t0 = time.time()
            df = fn(year)
            df["harvest_year"] = year
            if len(df) != 64 or df.district.nunique() != 64 or df.isna().any().any():
                bad = df.columns[df.isna().any()].tolist()
                raise ValueError(f"incomplete: {len(df)} rows, missing values in {bad}")
            df.to_csv(f, index=False)
            return f"{name} {year}: done in {time.time() - t0:.0f}s"
        except Exception as e:
            print(f"  {name} {year}: attempt {attempt + 1} failed: {str(e)[:160]}", flush=True)
            time.sleep(15)
    return f"{name} {year}: FAILED"


def record():
    PARAMS.write_text(json.dumps({
        "peak_ndvi": PEAK_NDVI, "rise_ndvi": RISE_NDVI, "stable_years": STABLE_YEARS, "loss_drop": LOSS_DROP,
        "hot_c": HOT_C, "cold_c": COLD_C,
        "reference_years": [YEARS[0], YEARS[-1]], "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d")}, indent=1))


def calibrate():
    """National Boro mask area for candidate thresholds, against the published 2014-2018 maps."""
    rows = []
    for t in (2014, 2015, 2016, 2017, 2018):
        img = ee.Image.cat([ee.Image.pixelArea().divide(1e6).updateMask(boro_mask(t, p)).rename(f"p{int(p * 100)}")
                            for p in (0.40, 0.45, 0.50, 0.55, 0.60)])
        d = reduce(img, 250, ee.Reducer.sum())
        d["harvest_year"] = t
        rows.append(d)
        print(t, "done", flush=True)
    pd.concat(rows).to_csv(OUT / "calibration_mask.csv", index=False)


# %% [markdown]
# ## Run the extraction
#
# Finished extracts are read from `data/bronze/`, so Earth Engine is contacted only for
# anything missing. The full extraction takes about an hour with five parallel requests.

# %%
what = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("calibrate", "test") else "all"
if what == "calibrate":
    setup_ee()
    calibrate()
elif what == "test":
    setup_ee()
    for name in ("modis", "weather", "scenes", "s1", "jrc"):
        print(run(name, 2017), flush=True)
else:
    tasks = [(n, y) for n in ("modis", "weather", "ndviwin", "scenes", "s1", "jrc", "s1thr") for y in JOBS[n][1]
             if not (OUT / f"{n}_{y}.csv").exists()]
    print(len(tasks), "extracts to compute")
    if tasks:
        setup_ee()
        record()
    with ThreadPoolExecutor(max_workers=5) as pool:
        for fut in as_completed([pool.submit(run, n, y) for n, y in tasks]):
            print(fut.result(), flush=True)

"""Paper 2 design check: where does the flood variation come from?
Reads exposure columns only; no outcome (area, yield, production) is loaded.
usage: python p2_exposure.py <Gold database>"""
import sys

import duckdb
import numpy as np
import pandas as pd

HAOR = ["Sunamganj", "Kishoreganj", "Netrokona", "Sylhet", "Habiganj", "Moulvibazar", "Brahmanbaria"]
VARS = ["s1_flash_flood", "jrc_flash_flood", "s1_monsoon_flood", "jrc_monsoon_flood"]

con = duckdb.connect(sys.argv[1], read_only=True)
p = con.sql(f"select district, division, harvest_year, {', '.join(VARS)}, jrc_flash_obs, jrc_monsoon_obs "
            "from fact_boro_panel").df()

for v in VARS:
    d = p.dropna(subset=[v]).copy()
    d["x"] = d[v] * 100
    d["r"] = d.x - d.groupby("district").x.transform("mean") - d.groupby("harvest_year").x.transform("mean") + d.x.mean()
    d["sh"] = d.r ** 2 / (d.r ** 2).sum()
    s = d.sort_values("sh", ascending=False)
    print(f"\n=== {v}: {d.harvest_year.min()}-{d.harvest_year.max()}, n={len(d)}")
    print("percent of district: median {:.2f}, p90 {:.2f}, p99 {:.2f}, max {:.2f}".format(*np.percentile(d.x, [50, 90, 99, 100])))
    print("district-years at or above 1/5/10/20 %:", [int((d.x >= c).sum()) for c in (1, 5, 10, 20)])
    print("share of identifying variation: top 1 {:.0%}, top 5 {:.0%}, top 10 {:.0%}, top 20 {:.0%}; effective obs {:.0f}".format(
        s.sh.iloc[0], s.sh.iloc[:5].sum(), s.sh.iloc[:10].sum(), s.sh.iloc[:20].sum(), 1 / (d.sh ** 2).sum()))
    print("haor seven districts carry {:.0%}".format(d[d.district.isin(HAOR)].sh.sum()))
    print("by year:", d.groupby("harvest_year").sh.sum().round(3).sort_values(ascending=False).head(4).to_dict())
    print("top:", [(r.district, int(r.harvest_year), round(r.x, 1), round(r.sh, 3)) for r in s.head(6).itertuples()])

print("\nJRC valid observations, share of area: flash min {:.2f} median {:.2f}; monsoon min {:.2f} median {:.2f}".format(
    p.jrc_flash_obs.min(), p.jrc_flash_obs.median(), p.jrc_monsoon_obs.min(), p.jrc_monsoon_obs.median()))
print("flash obs by year:", p.groupby("harvest_year").jrc_flash_obs.mean().round(2).dropna().to_dict())

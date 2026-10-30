"""Paper 2 literature search: fixed queries against OpenAlex, logged so it can be repeated.
Writes search_log.csv (query, hits, retrieved) and candidates.csv (deduplicated records).
usage: python search.py"""
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
PER_QUERY = 40
QUERIES = {
    "A haor and Boro flooding": [
        "haor flash flood Boro rice", "flash flood rice Bangladesh damage", "Boro rice flood loss Bangladesh",
        "haor basin remote sensing flood", "2017 flash flood Bangladesh haor", "haor agriculture climate vulnerability",
        "pre-monsoon flood Bangladesh rice", "flood damage rice production Bangladesh district",
    ],
    "B area versus yield": [
        "harvested area yield decomposition extreme weather crop production",
        "flood impact crop production harvested area yield", "weather shocks harvested area abandonment panel",
        "extreme weather disasters global crop production", "climate variability harvested area versus yield",
        "flood crop loss panel fixed effects", "crop yield harvested area response flood",
    ],
    "C climate and yield in Bangladesh": [
        "climate change rice yield Bangladesh panel", "Boro rice yield temperature Bangladesh",
        "heat stress Boro rice Bangladesh", "district level rice yield climate Bangladesh",
        "climate rice production Bangladesh econometric",
    ],
    "D flood mapping and crop loss from satellites": [
        "Sentinel-1 flood mapping Bangladesh", "Sentinel-1 flood rice damage assessment",
        "satellite crop loss flood NDVI change rice", "remote sensing flood damage cropland rice",
        "JRC Global Surface Water flood agriculture", "SAR water threshold flood mapping rice paddy",
    ],
    "E vulnerability indices and spatial methods": [
        "agricultural vulnerability index Bangladesh", "composite indicator uncertainty sensitivity analysis",
        "social vulnerability index uncertainty sensitivity", "spatial autocorrelation crop yield LISA",
        "climate vulnerability exposure sensitivity adaptive capacity agriculture Bangladesh",
    ],
    "F NDVI and yield": [
        "NDVI rice yield Bangladesh", "NDVI yield relationship within field interannual irrigated rice",
        "satellite crop yield estimation smallholder district statistics",
    ],
    "G adaptation": [
        "short duration Boro rice variety flash flood haor", "flood early warning haor farmers",
        "crop insurance flood Bangladesh rice", "submergence tolerant rice Bangladesh adoption",
    ],
}
FIELDS = "id,doi,title,publication_year,cited_by_count,type,primary_location,abstract_inverted_index,authorships"


def get(query):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": query, "per-page": PER_QUERY, "select": FIELDS})
    req = urllib.request.Request(url, headers={"User-Agent": "paper2-literature-search"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def abstract(inv):
    if not inv:
        return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)


log, seen = [], {}
for theme, qs in QUERIES.items():
    for q in qs:
        d = get(q)
        rows = d["results"]
        log.append({"theme": theme, "query": q, "hits": d["meta"]["count"], "retrieved": len(rows), "date": date.today()})
        for w in rows:
            key = (w.get("doi") or w["id"]).lower()
            if key in seen:
                seen[key]["themes"].add(theme[0])
                continue
            loc = (w.get("primary_location") or {}).get("source") or {}
            a = w.get("authorships") or []
            seen[key] = {"themes": {theme[0]}, "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                         "title": re.sub(r"\s+", " ", w.get("title") or ""), "year": w.get("publication_year"),
                         "cites": w.get("cited_by_count"), "type": w.get("type"), "venue": loc.get("display_name") or "",
                         "first_author": (a[0]["author"]["display_name"] if a else ""),
                         "abstract": abstract(w.get("abstract_inverted_index"))}
        time.sleep(0.15)

with open(HERE / "search_log.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, ["theme", "query", "hits", "retrieved", "date"])
    wr.writeheader()
    wr.writerows(log)
with open(HERE / "candidates.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, ["themes", "first_author", "year", "cites", "type", "venue", "title", "doi", "abstract"])
    wr.writeheader()
    for r in seen.values():
        wr.writerow({**r, "themes": "".join(sorted(r["themes"]))})
print("queries", len(log), "| retrieved", sum(x["retrieved"] for x in log), "| unique", len(seen),
      "| with abstract", sum(bool(r["abstract"]) for r in seen.values()))

"""Second search round: targeted queries for close competitors, plus DOI checks.
Appends to search_log.csv and writes candidates_round2.csv and doi_checks.csv.
usage: python search_round2.py"""
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
QUERIES = [
    "effects of flood on agricultural productivity in Bangladesh", "satellites self-reports submersion floods Bangladesh",
    "flood rice Bangladesh difference-in-differences", "flood exposure agricultural production Bangladesh district panel",
    "Boro production loss 2017 flash flood district statistics", "flash flood early monsoon haor rice production estimate",
    "Boro rice mapping Bangladesh satellite annual", "rice area mapping Bangladesh Sentinel-1 MODIS",
    "annual paddy rice map South Asia 10 m", "pre-monsoon flood Meghna basin trend haor frequency",
    "flood positive effect dry season rice residual moisture sediment Bangladesh", "India district flood rice yield panel",
    "flood harvested area rice Vietnam Thailand Philippines panel", "typhoon rice production harvested area panel",
]
DOIS = ["10.1162/rest.90.3.414", "10.1002/jae.2508", "10.1162/REST_a_00049", "10.1257/aer.20190159", "10.1093/reep/ret016",
        "10.1162/rest.88.4.641", "10.1111/j.2517-6161.1995.tb02031.x", "10.1038/nature16467",
        "10.1016/j.eap.2014.11.004", "10.1016/j.ijdrr.2021.102247", "10.1016/j.foodpol.2021.102183",
        "10.1007/s00704-024-05270-5"]


def fetch(url, tries=3):
    req = urllib.request.Request(url, headers={"User-Agent": "paper2-literature-search"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 * (i + 1))
    return {}


def abstract(inv):
    return " ".join(w for _, w in sorted((p, w) for w, ps in inv.items() for p in ps)) if inv else ""


seen, log = {}, []
for q in QUERIES:
    d = fetch("https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": q, "per-page": 25, "select": "id,doi,title,publication_year,cited_by_count,primary_location,abstract_inverted_index,authorships"}))
    rows = d.get("results", [])
    log.append([f"Round 2", q, d.get("meta", {}).get("count", ""), len(rows), date.today()])
    for w in rows:
        key = (w.get("doi") or w["id"]).lower()
        loc = (w.get("primary_location") or {}).get("source") or {}
        a = w.get("authorships") or []
        seen.setdefault(key, {"first_author": a[0]["author"]["display_name"] if a else "", "year": w.get("publication_year"),
                              "cites": w.get("cited_by_count"), "venue": loc.get("display_name") or "",
                              "title": re.sub(r"\s+", " ", w.get("title") or ""),
                              "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                              "abstract": abstract(w.get("abstract_inverted_index"))})
    time.sleep(0.15)
with open(HERE / "search_log.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(log)
with open(HERE / "candidates_round2.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, ["first_author", "year", "cites", "venue", "title", "doi", "abstract"])
    wr.writeheader()
    wr.writerows(seen.values())

checks = []
for doi in DOIS:
    m = fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi)).get("message", {})
    s = fetch(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=abstract")
    time.sleep(1.2)
    checks.append({"doi": doi, "first_author": (m.get("author") or [{}])[0].get("family", ""),
                   "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                   "title": (m.get("title") or [""])[0], "journal": (m.get("container-title") or [""])[0],
                   "abstract": s.get("abstract") or re.sub(r"<[^>]+>", " ", m.get("abstract") or "")})
with open(HERE / "doi_checks.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, list(checks[0]))
    wr.writeheader()
    wr.writerows(checks)

print("round 2 unique records:", len(seen))
for c in checks:
    print(f"{c['first_author']} {c['year']} | {c['title'][:80]} | {c['journal'][:34]}\n   {c['abstract'][:620]}")

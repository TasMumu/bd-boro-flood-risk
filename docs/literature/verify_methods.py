"""Confirm the methods references against Crossref, so that no citation comes from memory.
usage: python verify_methods.py"""
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

REFS = [
    "Lesk Rowhani Ramankutty Influence of extreme weather disasters on global crop production",
    "Conley GMM estimation with cross sectional dependence",
    "Driscoll Kraay Consistent covariance matrix estimation with spatially dependent panel data",
    "Cameron Gelbach Miller Bootstrap-based improvements for inference with clustered errors",
    "MacKinnon Webb Wild bootstrap inference for wildly different cluster sizes",
    "MacKinnon Webb The wild bootstrap for few (treated) clusters",
    "MacKinnon Webb Randomization inference for difference-in-differences with few treated clusters",
    "Conley Taber Inference with difference in differences with a small number of policy changes",
    "Arkhangelsky Athey Hirshberg Imbens Wager Synthetic difference-in-differences",
    "Abadie Using synthetic controls: feasibility, data requirements, and methodological aspects",
    "Hsiang Climate econometrics",
    "Blanc Schlenker The use of panel models in climate impacts studies",
    "Auffhammer Hsiang Schlenker Sobel Using weather data and climate model output in economic analyses of climate change",
    "Anselin Local indicators of spatial association LISA",
    "Benjamini Hochberg Controlling the false discovery rate",
    "Santos Silva Tenreyro The log of gravity",
    "Pekel Cottam Gorelick Belward High-resolution mapping of global surface water and its long-term changes",
    "Hinkel Indicators of vulnerability and adaptive capacity: towards a clarification of the science-policy interface",
    "Barrios Diamond Imbens Kolesar Clustering, spatial correlations, and randomization inference",
]
HERE = Path(__file__).parent
rows = []
for q in REFS:
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": q, "rows": 1, "select": "DOI,title,author,issued,container-title,type"})
    req = urllib.request.Request(url, headers={"User-Agent": "paper2-literature-check"})
    with urllib.request.urlopen(req, timeout=40) as r:
        it = json.load(r)["message"]["items"][0]
    rows.append({"query": q, "first_author": (it.get("author") or [{}])[0].get("family", ""),
                 "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
                 "title": (it.get("title") or [""])[0], "journal": (it.get("container-title") or [""])[0],
                 "doi": it.get("DOI", "")})
    print(rows[-1]["first_author"], rows[-1]["year"], "|", rows[-1]["title"][:88], "|", rows[-1]["journal"][:34], "|", rows[-1]["doi"])
with open(HERE / "methods_references.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0]))
    w.writeheader()
    w.writerows(rows)

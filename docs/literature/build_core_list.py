"""Combine both search rounds, record the screening counts, and verify every core paper on Crossref.
Writes screening_summary.txt and core_papers.csv. usage: python build_core_list.py"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
ABS, FULL, NONE = "abstract", "abstract, key", "title only"
# (theme, DOI or title to look up, how much was read)
CORE = [
    ("Haor flooding", "10.3390/s17102347", FULL), ("Haor flooding", "10.1016/j.ijdrr.2021.102247", ABS),
    ("Haor flooding", "10.3329/jesnr.v12i1-2.52007", ABS), ("Haor flooding", "10.3329/jesnr.v5i1.11581", ABS),
    ("Haor flooding", "10.3329/brj.v21i1.37360", ABS), ("Haor flooding", "10.13189/ujar.2018.060106", ABS),
    ("Haor flooding", "10.3390/su152416873", ABS), ("Haor flooding", "10.1002/fes3.70028", ABS),
    ("Haor flooding", "10.1016/j.heliyon.2023.e14011", ABS), ("Haor flooding", "10.1007/s00704-024-05270-5", ABS),
    ("Floods and rice in Bangladesh", "10.1080/13600818.2010.505681", FULL), ("Floods and rice in Bangladesh", "10.4157/grj.78.783", FULL),
    ("Floods and rice in Bangladesh", "10.1016/j.ijdrr.2025.105401", NONE), ("Floods and rice in Bangladesh", "10.1257/aer.p20151095", FULL),
    ("Climate and yield in Bangladesh", "10.3390/su7010898", FULL), ("Climate and yield in Bangladesh", "10.1016/j.eap.2014.11.004", NONE),
    ("Climate and yield in Bangladesh", "10.1142/s2010007816500081", ABS), ("Climate and yield in Bangladesh", "10.1186/s40066-017-0089-5", ABS),
    ("Climate and yield in Bangladesh", "10.1017/age.2017.14", ABS),
    ("Area and yield margins", "10.1038/nature16467", FULL), ("Area and yield margins", "10.1126/sciadv.adx7799", FULL),
    ("Area and yield margins", "10.1086/709859", FULL), ("Area and yield margins", "10.1371/journal.pone.0252067", FULL),
    ("Area and yield margins", "10.1002/essoar.10510446.1", FULL), ("Area and yield margins", "10.1175/jamc-d-15-0214.1", FULL),
    ("Satellite flood and rice mapping", "title:Operational Flood Mapping Using Multi-Temporal Sentinel-1", NONE),
    ("Satellite flood and rice mapping", "10.3390/agriculture10040131", ABS), ("Satellite flood and rice mapping", "10.1007/s13753-020-00305-7", ABS),
    ("Satellite flood and rice mapping", "10.1038/s41598-023-30347-y", FULL), ("Satellite flood and rice mapping", "10.1038/s41597-019-0036-3", FULL),
    ("Satellite flood and rice mapping", "10.3390/rs11101235", FULL), ("Satellite flood and rice mapping", "10.3390/rs6031938", ABS),
    ("Satellite flood and rice mapping", "10.1038/nature20584", NONE),
    ("NDVI and yield", "10.5424/sjar/2016143-8347", ABS), ("NDVI and yield", "10.1109/igarss.2019.8899084", ABS),
    ("Indices and spatial methods", "title:Uncertainty and Sensitivity Analysis Techniques as Tools", NONE),
    ("Indices and spatial methods", "title:Social vulnerability indices: a comparative assessment", NONE),
    ("Indices and spatial methods", "title:Navigating uncertainty in environmental composite", NONE),
    ("Indices and spatial methods", "10.1016/j.gloenvcha.2010.08.002", NONE), ("Indices and spatial methods", "10.1111/j.1538-4632.1995.tb00338.x", NONE),
    ("Inference and design", "10.1016/s0304-4076(98)00084-0", NONE), ("Inference and design", "10.1162/003465398557825", NONE),
    ("Inference and design", "10.1162/rest.90.3.414", NONE), ("Inference and design", "10.1002/jae.2508", ABS),
    ("Inference and design", "10.1111/ectj.12107", ABS), ("Inference and design", "10.1016/j.jeconom.2020.04.024", ABS),
    ("Inference and design", "10.1162/REST_a_00049", ABS), ("Inference and design", "10.1257/aer.20190159", ABS),
    ("Inference and design", "10.1257/jel.20191450", NONE), ("Inference and design", "10.3386/w22181", NONE),
    ("Inference and design", "10.1093/reep/rex016", NONE), ("Inference and design", "10.1093/reep/ret016", NONE),
    ("Inference and design", "10.1162/rest.88.4.641", ABS), ("Inference and design", "10.1111/j.2517-6161.1995.tb02031.x", ABS),
    ("Inference and design", "10.3386/w15760", ABS),
    ("Adaptation", "10.1016/j.foodpol.2021.102183", NONE), ("Adaptation", "10.22434/ifamr2019.0190", ABS),
]

a = pd.read_csv(HERE / "candidates.csv").fillna("")
b = pd.read_csv(HERE / "candidates_round2.csv").fillna("")
d = pd.concat([a, b], ignore_index=True)
d["key"] = d.doi.str.lower().where(d.doi != "", d.title.str.lower())
d = d.drop_duplicates("key").copy()
d["t"] = (d.title + " " + d.abstract).str.lower()
has = lambda p: d.t.str.contains(p, regex=True)
bd, crop, flood = has(r"bangladesh|haor"), has(r"\brice\b|paddy|\bboro\b|crop|agricultur"), has(r"flood|inundat|submerg")
area = has(r"harvested area|area harvested|harvest area|cropped area|cultivated area|cultivation area|planted area|abandon|crop area|cropping area|area under cultivation")
yld, model = has(r"\byield"), has(r"panel|fixed.effect|regression|econometric|difference-in-difference")
log = pd.read_csv(HERE / "search_log.csv")
lines = [f"queries: {len(log)}", f"records retrieved: {log.retrieved.sum()}", f"unique records: {len(d)}",
         f"with abstract: {(d.abstract != '').sum()}", f"Bangladesh or haor, and crops: {(bd & crop).sum()}",
         f"  and flood: {(bd & crop & flood).sum()}", f"  and an area term: {(bd & crop & flood & area).sum()}",
         f"  and yield: {(bd & crop & flood & area & yld).sum()}", f"  and a statistical model: {(bd & crop & flood & area & yld & model).sum()}"]
(HERE / "screening_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print("records passing all terms:")
for r in d[bd & crop & flood & area & yld & model].itertuples():
    print("  ", r.first_author, r.year, "|", r.title[:90], "|", r.doi)

rows = []
for theme, ref, level in CORE:
    doi = ref
    if ref.startswith("title:"):
        doi = d[d.title.str.contains(ref[6:], case=False, regex=False)].iloc[0].doi
    req = urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi), headers={"User-Agent": "paper2-literature-check"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            m = json.load(r)["message"]
        rows.append({"theme": theme, "first_author": (m.get("author") or [{}])[0].get("family", ""),
                     "n_authors": len(m.get("author") or []), "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                     "title": (m.get("title") or [""])[0], "journal": (m.get("container-title") or [""])[0], "doi": doi, "read": level})
    except Exception as e:
        rows.append({"theme": theme, "first_author": "", "n_authors": "", "year": "", "title": f"NOT VERIFIED: {e}", "journal": "", "doi": doi, "read": level})
    time.sleep(0.1)
with open(HERE / "core_papers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print("core papers:", len(rows), "| not verified:", sum("NOT VERIFIED" in r["title"] for r in rows))
for r in rows:
    if "NOT VERIFIED" in r["title"]:
        print("  ", r["doi"], r["title"])
print(pd.DataFrame(rows).groupby("read").size().to_dict())
print([f"{r['first_author']} {r['year']}" for r in rows if r["n_authors"] in (2,)][:14])

"""Build the Paper 2 manuscript from paper/parts/*.md and the files in outputs/.
Every number in the text comes from a {{ expression }} evaluated here, so no value is typed by hand.
Citations written as [@key] become author-year citations; the reference list comes from references.json.
usage: python src/build_manuscript.py"""
import html
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = ROOT.parent / "bd-boro-data-framework"
PAPER, OUT = ROOT / "paper", ROOT / "outputs"
R = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
X = json.loads((OUT / "results_index.json").read_text(encoding="utf-8"))
D = json.loads((OUT / "dataset_summary.json").read_text(encoding="utf-8"))
P = pd.read_parquet(ROOT / "data" / "analysis_panel.parquet")
MAIN = pd.read_csv(OUT / "table_main.csv")
CK = pd.read_csv(OUT / "table_checks.csv")
SYN = pd.read_csv(OUT / "table_synthetic_control.csv")
EV = pd.read_csv(OUT / "table_haor_by_year.csv")
E17 = pd.read_csv(OUT / "table_event_2017.csv").set_index("district")
BINS = pd.read_csv(OUT / "table_flood_bins.csv")
NDVI = pd.read_csv(OUT / "table_ndvi.csv")
Q3 = pd.read_csv(OUT / "table_haor_interaction.csv")
IDX = pd.read_csv(OUT / "table_index.csv", index_col=0)
SP = pd.read_csv(OUT / "table_spatial.csv")
NAT = pd.read_csv(OUT / "table_mask_national.csv")
EARLY = pd.read_csv(OUT / "table_early_window.csv")
TIM = pd.read_csv(OUT / "table_flood_timing.csv", index_col=0)
HAOR = ["Sunamganj", "Habiganj", "Netrokona", "Kishoreganj", "Sylhet", "Moulvibazar", "Brahmanbaria"]


def minus(t):
    return re.sub(r"(?<![\w.])-(?=\d)", "−", str(t))


def f(x, d=1):
    return minus(f"{x:,.{d}f}")


def pv(p):
    if pd.isna(p):
        return "–"
    return "< 0.001" if p < 0.001 else minus(f"{p:.3f}")


def eff(source, outcome, flood="flash"):
    return MAIN[(MAIN.source == source) & (MAIN.outcome == outcome) & (MAIN.flood == flood)].iloc[0]


def chk(check, source, outcome="Harvested area"):
    return CK[(CK.check == check) & (CK.source == source) & (CK.outcome == outcome)].iloc[0]


def md_table(df):
    cols = list(df.columns)

    def width(c):
        cells = [len(str(v)) + 3 for v in df[c] if not pd.isna(v)]
        head = max(len(w) for w in str(c).split()) + 4
        return min(max([head] + cells + [6]), 26)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("-" * width(c) for c in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join("" if pd.isna(r[c]) else str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def table_sources():
    return md_table(pd.DataFrame([
        ["Boro area, yield, production", "BBS yearbooks, through the Paper 1 panel", "64 districts", "2011–2025"],
        ["Flood, Sentinel-1", "COPERNICUS/S1_GRD, VV, −18 dB", "Analysed at 60 m", "Harvest years 2015–2025"],
        ["Flood, JRC", "Global Surface Water v1.4, monthly", "30 m", "Harvest years 2011–2021"],
        ["Boro mask, crop loss, NDVI", "MODIS MOD13Q1 v061, WorldCover v200 cropland", "250 m", "2011–2025"],
        ["Weather", "ERA5-Land daily aggregates", "0.1°", "2011–2025"]],
        columns=["Variable", "Source", "Resolution", "Period"]))


def table_main():
    rows = []
    for src in ("Sentinel-1", "JRC"):
        for o in ("Harvested area", "Yield", "Production"):
            e = eff(src, o)
            rows.append([src, o, f(e.pct), pv(e.p_cluster), pv(e.p_dk), pv(e.p_conley), pv(e.p_ri), f"{int(e.n)}"])
    return md_table(pd.DataFrame(rows, columns=["Flood record", "Outcome", "Effect per 10 points (%)", "Clustered p", "Driscoll–Kraay p", "Conley p", "Randomisation p", "N"]))


def table_monsoon():
    rows = []
    for src in ("Sentinel-1", "JRC"):
        for o in ("Harvested area", "Yield", "Production"):
            e = eff(src, o, "monsoon")
            rows.append([src, o, f(e.pct), pv(e.p_cluster), pv(e.p_dk), pv(e.p_conley), pv(e.p_ri)])
    return md_table(pd.DataFrame(rows, columns=["Flood record", "Outcome", "Effect per 10 points (%)", "Clustered p", "Driscoll–Kraay p", "Conley p", "Randomisation p"]))


def table_synth():
    d = SYN[SYN.outcome.isin(["Harvested area", "Yield"])]
    rows = [[r.district, r.outcome, f(r.gap_2016), f(r.gap_2017), f(r.gap_2018), pv(r.rank_p)] for r in d.itertuples()]
    return md_table(pd.DataFrame(rows, columns=["District", "Outcome", "Gap 2016 (%)", "Gap 2017 (%)", "Gap 2018 (%)", "Placebo rank p"]))


def table_checks():
    names = ["Leave out 2016", "Leave out 2017", "Leave out 2022", "Leave out Sunamganj", "Leave out Kishoreganj", "Leave out Sylhet", "Leave out Netrokona",
             "Next year's flash flood (placebo)", "Flood after harvest (placebo)", "Rice land only", "January-February baseline, early window",
             "Sentinel-1 without 2015-2016", "Scene counts as controls"]
    rows = []
    for c in names:
        for src in ("Sentinel-1", "JRC"):
            x = CK[(CK.check == c) & (CK.source == src) & (CK.outcome == "Harvested area")]
            if len(x):
                r = x.iloc[0]
                rows.append([c.replace("January-February", "January–February").replace("2015-2016", "2015–2016"), src, f(r.pct), pv(r.p_cluster), pv(r.p_dk), "Pass" if r.passed else "Fail"])
    return md_table(pd.DataFrame(rows, columns=["Check", "Flood record", "Area effect (%)", "Clustered p", "Driscoll–Kraay p", "Result"]))


def table_reported():
    names = ["Division-by-year effects", "District linear trends", "Poisson model", "Flash flood only, 2015-2025", "Water threshold -16 dB", "Water threshold -20 dB",
             "Neighbours' flood, own effect", "Neighbours' flood, spillover"]
    rows = []
    for c in names:
        for src in ("Sentinel-1", "JRC"):
            x = CK[(CK.check == c) & (CK.source == src) & (CK.outcome == "Harvested area")]
            if len(x):
                r = x.iloc[0]
                rows.append([minus(c.replace("2015-2025", "2015–2025")), src, f(r.pct), pv(r.p_cluster), pv(r.p_dk)])
    return md_table(pd.DataFrame(rows, columns=["Variant", "Flood record", "Area effect (%)", "Clustered p", "Driscoll–Kraay p"]))


def table_top():
    d = IDX.head(10)
    rows = [[i + 1, n, "Yes" if r.haor else "No", f"{f(r.rank_p05, 0)}–{f(r.rank_p95, 0)}", f(100 * r.top10_share, 0), f(100 * r.tier_stability, 0)] for i, (n, r) in enumerate(d.iterrows())]
    return md_table(pd.DataFrame(rows, columns=["Rank", "District", "Haor", "Rank range, 5th–95th percentile", "In top ten (%)", "Same tier (%)"]))


def table_spatial():
    rows = [[r.neighbours, f(r.moran_i, 3), pv(r.p), ", ".join(eval(r.hh_005)) or "None", ", ".join(eval(r.hh_fdr)) or "None"] for r in SP.itertuples()]
    return md_table(pd.DataFrame(rows, columns=["Neighbours", "Moran's I", "p", "High-risk cluster, p < 0.05", "After false discovery rate"]))


def table_ndvi():
    rows = [[r.window, f(r.between, 2), f(r.within_district, 2), f(r.within_two_way, 2), f(r.b, 3), pv(r.p_cluster), pv(r.p_ri)] for r in NDVI.itertuples()]
    return md_table(pd.DataFrame(rows, columns=["NDVI window", "Between districts", "Within districts", "Within, year effects removed", "Effect on log yield per 0.1 NDVI", "Clustered p", "Randomisation p"]))


def table_event():
    d = E17.head(8)
    rows = [[n, f(100 * r.s1_flash_flood), f(100 * r.jrc_flash_flood), f(100 * r.loss_share), f(r.area_ha_chg_pct), f(r.yield_t_ha_chg_pct), f(r.production_t_chg_pct)] for n, r in d.iterrows()]
    return md_table(pd.DataFrame(rows, columns=["District", "Sentinel-1 flood (%)", "JRC flood (%)", "Satellite crop loss (%)", "BBS area (%)", "BBS yield (%)", "BBS production (%)"]))


def table_design():
    rows = []
    for v, lab in (("s1_flash_flood", "Flash flood, Sentinel-1"), ("jrc_flash_flood", "Flash flood, JRC"), ("s1_monsoon_flood", "Monsoon flood, Sentinel-1"), ("jrc_monsoon_flood", "Monsoon flood, JRC")):
        d = P.dropna(subset=[v]).copy()
        d["x"] = d[v] * 100
        d["r"] = d.x - d.groupby("district").x.transform("mean") - d.groupby("harvest_year").x.transform("mean") + d.x.mean()
        d["sh"] = d.r ** 2 / (d.r ** 2).sum()
        two = d[d.harvest_year.isin([2016, 2017])].sh.sum()
        rows.append([lab, f"{len(d)}", f"{1 / (d.sh ** 2).sum():.0f}", f(100 * d[d.district.isin(HAOR)].sh.sum(), 0), f(100 * two, 0)])
    return md_table(pd.DataFrame(rows, columns=["Flood variable", "District-years", "Effective observations", "From the seven haor districts (%)", "From 2016 and 2017 (%)"]))


def table_early():
    rows = [[r.source, r.outcome, r.sample, f(r.pct), pv(r.p_cluster), pv(r.p_dk), pv(r.p_conley), pv(r.p_ri)] for r in EARLY[EARLY.outcome != "Production"].itertuples()]
    return md_table(pd.DataFrame(rows, columns=["Flood record", "Outcome", "Sample", "Effect per 10 points (%)", "Clustered p", "Driscoll–Kraay p", "Conley p", "RI p"]))


def table_timing():
    rows = []
    for t in (2015, 2016, 2017, 2018, 2022):
        r = TIM.loc[t]
        rows.append([str(t), f(r.s1_early_wd), f(r.s1_late_wd), f(r.jrc_early_wd) if pd.notna(r.jrc_early_wd) else "–", f(r.jrc_late_wd) if pd.notna(r.jrc_late_wd) else "–", f(r.loss_share), f(hy("Harvested area", t))])
    return md_table(pd.DataFrame(rows, columns=["Harvest year", "Sentinel-1 early (%)", "Sentinel-1 late (%)", "JRC early (%)", "JRC late (%)", "Satellite crop loss (%)", "BBS area against 2015 (%)"]))


def table_mask():
    rows = [[str(int(r.harvest_year)), f(r.mask_mha, 2), f(r.bbs_mha, 2), f(r.shew_ghosh_mha, 2) if pd.notna(r.shew_ghosh_mha) else "–"] for r in NAT.itertuples()]
    return md_table(pd.DataFrame(rows, columns=["Harvest year", "Yearly mask (million ha)", "BBS harvested area (million ha)", "Shew and Ghosh (2019) (million ha)"]))


def hy(o, y):
    return float(EV[(EV.outcome == o) & (EV.year == y)].pct.iloc[0])


def sy(o, d, c):
    return float(SYN[(SYN.outcome == o) & (SYN.district == d)][c].iloc[0])


def er(src, o, sample):
    return EARLY[(EARLY.source == src) & (EARLY.outcome == o) & (EARLY["sample"] == sample)].iloc[0]


def bn(src, flood, o, b):
    return BINS[(BINS.source == src) & (BINS.flood == flood) & (BINS.outcome == o) & (BINS["bin"] == b)].iloc[0]


def ci(key, m):
    return R["yield_negligible"][key]["ci"][m]


TABLES = {k: v for k, v in globals().items() if k.startswith("table_") and callable(v)}


def _clean(s):
    return re.sub(r"<[^>]+>", "", html.unescape(s or "")).strip()


def _family(a):
    fam = _clean(a["family"])
    return fam.title() if fam.isupper() and len(fam) > 3 and a.get("given") else fam


def _initials(given):
    def one(tok):
        if "." in tok:
            return "".join(c + "." for c in re.findall(r"[^\W\d_]", tok) if c.isupper())
        if tok.isupper() and len(tok) <= 4:
            return "".join(c + "." for c in tok)
        return tok[0] + "."
    out = []
    for tok in re.split(r"\s+", _clean(given)):
        if tok:
            out.append("-".join(one(t) for t in tok.split("-") if t))
    return "".join(out)


def _title(t):
    t = _clean(t).rstrip(".")
    return t.capitalize() if t.isupper() else t


def cite_label(e):
    au = e["authors"]
    names = _family(au[0]) if len(au) == 1 else f"{_family(au[0])} and {_family(au[1])}" if len(au) == 2 else f"{_family(au[0])} et al."
    return names, str(e["year"])


def harvard_entry(e):
    au = e["authors"]
    names = ", ".join(f"{_family(a)}, {_initials(a['given'])}" if a.get("given") else _family(a) for a in au[:10])
    if len(au) > 10:
        names += ", et al."
    title = _title(e["title"])
    s = f"{names}, {e['year']}. {title}" + ("" if title.endswith(("?", "!")) else ".")
    t = e.get("type", "")
    if t in ("journal-article", "proceedings-article", "posted-content"):
        cont = _clean(e.get("container"))
        if cont:
            s += f" In: {cont}" if t == "proceedings-article" else f" {cont}"
        if e.get("volume"):
            s += f" {e['volume']}" + (f" ({e['issue']})" if e.get("issue") else "")
        if e.get("pages"):
            s += f", {str(e['pages']).replace('-', '–')}"
        s += "."
    elif e.get("publisher"):
        s += f" {_clean(e['publisher'])}."
    if e.get("doi"):
        s += f" https://doi.org/{e['doi']}"
    return s


def _sort_key(name):
    return "".join(c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c)).lower()


def author_year(md):
    refs = json.loads((PAPER / "references.json").read_text(encoding="utf-8"))
    cited = []

    def lab(key):
        if key not in refs:
            raise KeyError(f"unknown citation key: {key}")
        if key not in cited:
            cited.append(key)
        return cite_label(refs[key])

    def paren(m):
        groups = []
        for n, y in map(lab, [k.strip().lstrip("@") for k in m.group(1).split(";")]):
            if groups and groups[-1][0] == n:
                groups[-1][1].append(y)
            else:
                groups.append((n, [y]))
        return "(" + "; ".join(f"{n}, {', '.join(ys)}" for n, ys in groups) + ")"

    md = re.sub(r"\[(@[\w-]+(?:\s*;\s*@[\w-]+)*)\]", paren, md)
    md = re.sub(r"(?<![\w.])@([a-z][\w-]*\d{4}[a-z]?)\b", lambda m: "{} ({})".format(*lab(m.group(1))) if m.group(1) in refs else m.group(0), md)
    seen = {}
    for k in cited:
        seen.setdefault(cite_label(refs[k]), []).append(k)
    clash = {k: v for k, v in seen.items() if len(v) > 1}
    assert not clash, f"ambiguous citations: {clash}"
    order = sorted(cited, key=lambda k: (_sort_key(_family(refs[k]["authors"][0])), str(refs[k]["year"])))
    print(len(cited), "references cited; not cited:", sorted(set(refs) - set(cited)))
    return md.replace("<<REFERENCES>>", "\n\n".join(harvard_entry(refs[k]) for k in order))


def render(text):
    ns = dict(R=R, X=X, D=D, P=P, MAIN=MAIN, CK=CK, SYN=SYN, EV=EV, E17=E17, BINS=BINS, NDVI=NDVI, Q3=Q3, IDX=IDX, SP=SP, NAT=NAT, HAOR=HAOR, TIM=TIM,
              f=f, pv=pv, eff=eff, chk=chk, hy=hy, sy=sy, er=er, bn=bn, ci=ci, abs=abs, round=round, len=len, min=min, max=max, int=int, sum=sum, np=np, minus=minus,
              SA=eff("Sentinel-1", "Harvested area"), SY=eff("Sentinel-1", "Yield"), SPR=eff("Sentinel-1", "Production"),
              JA=eff("JRC", "Harvested area"), JY=eff("JRC", "Yield"), JPR=eff("JRC", "Production"),
              MSA=eff("Sentinel-1", "Harvested area", "monsoon"), MJA=eff("JRC", "Harvested area", "monsoon"), MJY=eff("JRC", "Yield", "monsoon"), MSY=eff("Sentinel-1", "Yield", "monsoon"),
              V=R["verdict_q1"], RP=R["reported_2017"], SAT=R["satellite_check"], YV=X["yield_view"], XI=X["index"])

    def ev(m):
        e = m.group(1).strip()
        return TABLES[e]() if e in TABLES else str(eval(e, ns))
    return re.sub(r"\{\{(.+?)\}\}", ev, text, flags=re.S)


def pandoc(src, dst):
    subprocess.run(["pandoc", str(src), "-o", str(dst), "--resource-path", str(OUT), "--from", "markdown+pipe_tables",
                    "--reference-doc", str(FRAMEWORK / "v2" / "paper" / "reference.docx")], check=True)
    print("wrote", dst.name)


md = "\n\n".join(render(p.read_text(encoding="utf-8")) for p in sorted((PAPER / "parts").glob("*.md")))
md = author_year(md)
abstract = md.split("# Abstract", 1)[1].split("\n# ", 1)[0].split("Keywords:", 1)[0].rstrip().rstrip("*")
print("abstract:", len(re.findall(r"\S+", abstract)), "words")
(PAPER / "Manuscript.md").write_text(md, encoding="utf-8")
pandoc(PAPER / "Manuscript.md", PAPER / "Manuscript.docx")
hl = render((PAPER / "highlights.md").read_text(encoding="utf-8"))
for line in re.findall(r"^- (.+)$", hl, flags=re.M):
    assert len(line) <= 85, f"highlight over 85 characters ({len(line)}): {line}"
(PAPER / "Highlights_rendered.md").write_text(hl, encoding="utf-8")
pandoc(PAPER / "Highlights_rendered.md", PAPER / "Highlights.docx")
print("words in the manuscript:", len(md.split()))

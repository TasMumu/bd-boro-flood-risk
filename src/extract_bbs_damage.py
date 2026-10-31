# %% [markdown]
# # 06. BBS's own reports on Boro flood damage
#
# The BBS yearbooks estimate flood damage separately from crop area. This notebook reads those
# reports, because they show how flood losses were recorded in the official statistics.
#
# It writes two tables. `data/bbs_reported_damage.csv` holds the district damage tables for the
# floods of 2016, 2017 and 2022. `outputs/table_chandpur_2017.csv` holds Chandpur's rows by rice type,
# which show the same area printed for HYV and hybrid Boro in 2016-17.
#
# Both tables are kept in the repository, so this step is skipped when the yearbook PDFs are not
# available. No value is corrected.

# %%
import re
from pathlib import Path

import pandas as pd
import pypdf

ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd().parent
PDF = ROOT.parent / "bd-boro-data-framework" / "data" / "bronze" / "bbs" / "pdfs"
ACRE_HA = 0.404686
NAMES = {"Habigang": "Habiganj", "Maulbibazar": "Moulvibazar", "Maulvibazar": "Moulvibazar", "Sunamgang": "Sunamganj", "Sylhet": "Sylhet",
         "Netrokona": "Netrokona", "Kishoregong": "Kishoreganj", "Bangladesh": "Bangladesh"}
HAVE_PDFS = (PDF / "bbs_agri_yearbook_2017.pdf").exists()
print("yearbook PDFs found:", HAVE_PDFS)

# %% [markdown]
# ## Damage tables
#
# Each table gives the area fully and partly damaged, the total in terms of full damage, and the
# production loss. The harvest year, edition, PDF page and the heading of the Total Boro block are
# listed below. The headings are spelled as printed.

# %%
TABLES = [(2016, 2017, 367, r"Tatal Boro"), (2017, 2017, 368, r"Total Boro")]
ROW = r"^\s*([A-Za-z]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s*$"
if HAVE_PDFS:
    rows = []
    for year, ed, page, mark in TABLES:
        t = pypdf.PdfReader(PDF / f"bbs_agri_yearbook_{ed}.pdf").pages[page - 1].extract_text()
        block = t[re.search(mark, t).start():]
        for m in re.finditer(ROW, block, re.M):
            if m.group(1) in NAMES:
                rows.append(dict(harvest_year=year, district=NAMES[m.group(1)], fully_ac=int(m.group(2)), partly_ac=int(m.group(3)),
                                 total_ac=int(m.group(6)), loss_t=int(m.group(8)), edition=ed, pdf_page=page))
    # The 2022 table has a different layout: area under crop, partly damaged, %, equivalent, fully, total, yield, loss
    t = pypdf.PdfReader(PDF / "bbs_agri_yearbook_2022.pdf").pages[441].extract_text()
    m = re.search(r"Boro\s+Netrokona\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", t)
    for name in ("Netrokona", "Bangladesh"):
        rows.append(dict(harvest_year=2022, district=name, fully_ac=float(m.group(5)), partly_ac=float(m.group(2)),
                         total_ac=float(m.group(6)), loss_t=float(m.group(8)), edition=2022, pdf_page=442))
    d = pd.DataFrame(rows)
    d["total_ha"] = d.total_ac * ACRE_HA
    d.to_csv(ROOT / "data" / "bbs_reported_damage.csv", index=False)
d = pd.read_csv(ROOT / "data" / "bbs_reported_damage.csv")
print(d.drop(columns=["edition", "pdf_page"]).round(0).to_string())

# %% [markdown]
# ## Chandpur's rows by rice type
#
# Chandpur's harvested area jumps in 2017 with no flood. Its total is the sum of local, HYV and
# hybrid Boro, so each is read from both editions that print the year.

# %%
if HAVE_PDFS:
    rows = []
    for ed, label in ((2017, "2015-16 and 2016-17"), (2018, "2016-17 and 2017-18")):
        r = pypdf.PdfReader(PDF / f"bbs_agri_yearbook_{ed}.pdf")
        for page, kind in ((89, "Local"), (91, "HYV"), (93, "Hybrid"), (95, "Total")):
            line = next(x for x in (r.pages[page - 1].extract_text() or "").splitlines() if "Chandpur" in x)
            n = re.findall(r"[\d.]+", line.split("Chandpur")[1])
            rows.append(dict(edition=ed, pdf_page=page, type=kind, first_year_acres=int(n[0]), second_year_acres=int(n[5]), years=label))
    pd.DataFrame(rows).to_csv(ROOT / "outputs" / "table_chandpur_2017.csv", index=False)
print(pd.read_csv(ROOT / "outputs" / "table_chandpur_2017.csv").to_string())

"""Turn the percent-format scripts in src/ into Jupyter notebooks, so each notebook holds exactly
the code that was run, with its documentation as markdown cells.
usage: python tools/py_to_notebook.py"""
import re
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
ORDER = [("extract_variables.py", "01_Extract_Variables.ipynb"), ("build_dataset.py", "02_Build_Panel.ipynb"),
         ("run_models.py", "03_Flood_Models.ipynb"), ("run_index.py", "04_Risk_Index.ipynb"),
         ("make_figures.py", "05_Figures.ipynb")]


def convert(src, dst):
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    parts = re.split(r"^# %%(.*)$", src.read_text(encoding="utf-8"), flags=re.M)
    for tag, body in zip(parts[1::2], parts[2::2]):
        body = body.strip("\n")
        if "[markdown]" in tag:
            text = "\n".join(re.sub(r"^# ?", "", ln) for ln in body.splitlines())
            nb.cells.append(nbf.v4.new_markdown_cell(text))
        elif body.strip():
            nb.cells.append(nbf.v4.new_code_cell(body))
    nbf.write(nb, dst)
    print(dst.name, len(nb.cells), "cells")


(ROOT / "notebooks").mkdir(exist_ok=True)
for s, d in ORDER:
    if (ROOT / "src" / s).exists():
        convert(ROOT / "src" / s, ROOT / "notebooks" / d)

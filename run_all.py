"""Rebuild Paper 2 from the cached extracts: panel, models, index, figures, notebooks and manuscript.
Earth Engine is contacted only if an extract is missing. usage: python run_all.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = ["extract_variables.py", "build_dataset.py", "run_models.py", "run_index.py", "make_figures.py", "build_manuscript.py"]
for s in STEPS:
    print("===", s, flush=True)
    subprocess.run([sys.executable, str(ROOT / "src" / s)], check=True, cwd=ROOT)
print("Done. After changing a script, rebuild its notebook with tools/py_to_notebook.py and execute it.")

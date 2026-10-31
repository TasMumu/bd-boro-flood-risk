# bd-boro-flood-risk

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23838852.svg)](https://doi.org/10.5281/zenodo.23838852)

Code, notebooks, outputs and manuscript for "Does yield hide flood losses? Harvested
area, flood timing and Boro rice in Bangladesh's 64 districts, 2011–2025" by Tasnim
Ahmad Mumu and Rezaul Karim.

The paper uses the Gold panel of `bd-boro-data-framework` (Zenodo
10.5281/zenodo.23795046) as a fixed input. That folder must sit next to this one. The
panel is read and never changed, and its checksum is confirmed at the start of every run. The
GADM boundaries are also needed, placed in that folder as its README explains. The yearbook
PDFs and an Earth Engine account are needed only to recompute extracts; all Earth Engine data
are public collections, and `GEE_PROJECT` in that folder's `v2/src/common.py` names the project.

## Main finding

In the 2017 flood, haor harvested area fell by about a third while yield barely moved,
and independent evidence supports the loss. As a general rule the effect is only
suggestive: it rests on 2016 and 2017, and other large floods left no fall in area.
The verdict comes from a rule written in `docs/analysis_plan.md` before the models were run. The
plan has no public timestamp from before the results, so this is not a preregistered study.

## Contents

| Folder | Contents |
|---|---|
| `paper/` | Manuscript in Word, PDF and Markdown; highlights; sources in `paper/parts/` |
| `notebooks/` | The six documented, executed notebooks |
| `src/` | The same code as scripts, in percent format |
| `docs/` | Analysis plan, journal choice, and the literature review with its search scripts |
| `outputs/` | Tables, figures and `results.json`; every number in the paper is read from here |
| `data/` | Earth Engine extracts in `data/bronze/`, and the analysis panel |
| `design_checks/` | Exposure-only checks made before any model was run |

## Notebooks

| Notebook | What it does |
|---|---|
| `01_Extract_Variables` | Boro mask, crop loss, flood timing, scenes and weather from Earth Engine |
| `02_Build_Panel` | Joins the variables to the panel; reproduces Paper 1's flood values; 18 checks |
| `03_Flood_Models` | Main models, four uncertainty methods, three designs, checks, exploratory work, verdict |
| `04_Risk_Index` | Index under 6,018 combinations of choices; spatial clusters; yield-only view |
| `05_Figures` | Every figure in the paper |
| `06_BBS_Damage` | BBS's own damage tables, and Chandpur's rows by rice type |

Each notebook is generated from the matching script by `tools/py_to_notebook.py`, so the
two cannot differ. Running the notebooks gave results identical to running the scripts.

## Citation

The release described in the manuscript is archived on Zenodo at https://doi.org/10.5281/zenodo.23838852, and
https://doi.org/10.5281/zenodo.23829198 always resolves to the latest archived version. Citation
metadata is in `CITATION.cff`.

## Licence

The code is released under the MIT License (`LICENSE`). The MIT licence does not apply to the
data: derived data remain subject to the terms of the sources they come from. Search records
that hold other authors' abstracts are not included; `docs/literature/search.py` and
`search_round2.py` regenerate them.

## Run

```bash
python run_all.py
```

This takes a few minutes and uses the cached extracts. After changing a script, rebuild the
notebooks with `python tools/py_to_notebook.py` and execute them with Jupyter. Earth Engine
is contacted only if an extract is missing; all of them together take about an hour. The
packages are those pinned in `bd-boro-data-framework/v2/requirements-lock.txt`, plus pandoc and Jupyter.

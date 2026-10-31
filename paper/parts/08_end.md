# 7. Conclusion

Using printed BBS statistics for all 64 districts and a written analysis plan, we asked whether flash floods reduce Boro rice through harvested area rather than yield. For the 2017 flood the evidence is strong: haor harvested area and production fell by about a third, yield barely moved, and BBS's damage reports and other evidence support the loss. For a general relationship the evidence is only suggestive, because the estimates rest on 2016 and 2017, their size is unstable, and the 2016 and 2022 flood years showed no comparable fall in harvested area. Flood timing is one possible reason, but that remains a hypothesis resting on one event. The practical lesson is that yield alone can miss large flood losses in this system, so flood assessment and risk indices should also use harvested area and production.

# CRediT authorship contribution statement

Tasnim Ahmad Mumu: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review & editing, Visualization. Rezaul Karim: Supervision, Methodology, Validation, Writing – review & editing.

# Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used Claude (Anthropic) to assist with code development, data validation and analysis scripts, and drafting and editing of the manuscript text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

# Data availability

The panel is archived at https://doi.org/10.5281/zenodo.23795046. The derived data remain subject to the terms of their sources. Contains modified Copernicus Sentinel data (2014–2025) and modified Copernicus Climate Change Service information (2026). The BBS yearbook PDFs and the GADM v4.1 boundaries [@gadm2022] are not redistributed and must be obtained from the Bangladesh Bureau of Statistics and gadm.org. Code, notebooks, the analysis plan and the Earth Engine extracts for this paper are in the repository given in the Software and data availability section and archived at https://doi.org/10.5281/zenodo.23829199.

# References

<<REFERENCES>>

# Appendix A. Supplementary tables

Table A.1. Other variants of the area effect, reported without a pass rule. The Poisson model [@santos2006] gives more weight to large districts.

{{ table_reported }}

Table A.2. National area of the yearly Boro mask, against BBS and published maps.

{{ table_mask }}

Table A.3. The {{ D['checks'] }} data checks run before any model, from `outputs/validation_variables.csv`.

{{ table_datachecks }}

Table A.4. Required checks of the harvested-area effect, by type.

{{ table_required_summary }}

# Appendix B. Literature search

The search used one database, OpenAlex, on 31 October 2026, with the 52 search strings in Table B.1 and up to 40 records for each of the first 38 strings and 25 for the other 14. This gave 1,870 records, of which 1,383 were unique and 1,232 had an abstract. Screening used titles and abstracts: 421 records concerned Bangladesh or the haor and crops, 182 of them also concerned flooding, and 5 of those also mentioned cultivated or harvested area. Hassan (2019) was found by a separate web search. The core list of 57 papers was confirmed on Crossref. Journals published in Bangladesh are indexed less completely, and keyword screening can miss papers that use other words. The search scripts are in the repository.

Table B.1. Search strings by theme.

{{ table_search }}

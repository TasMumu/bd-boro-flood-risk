---
title: "Does yield hide flood losses? Harvested area, flood timing and Boro rice in Bangladesh's 64 districts, 2011–2025"
---

::: {custom-style="Author"}
Tasnim Ahmad Mumu^a^, Rezaul Karim^b,\*^
:::

::: {custom-style="Affiliation"}
^a^ Department of Agronomy and Agricultural Extension, University of Rajshahi, Rajshahi 6205, Bangladesh

^b^ Department of Statistics and Data Science, University of Rajshahi, Rajshahi 6205, Bangladesh
:::

::: {custom-style="Correspondence"}
\* Corresponding author. E-mail address: mrkarim@ru.ac.bd (R. Karim); Tel.: +880 1726 433752
:::

# Abstract

Flood losses to crops are often measured through yield, but official yield comes from sample crop cuts, so a field destroyed before harvest may leave no trace in it. We tested this for Boro rice across Bangladesh's 64 districts, 2011–2025, using official statistics, Sentinel-1 and JRC flood data, and a written analysis plan. In the 2017 flash flood, harvested area in the seven haor districts fell by {{ f(abs(hy('Harvested area', 2017)), 0) }} % relative to other districts, while yield changed by {{ f(hy('Yield', 2017)) }} %. In Sunamganj, harvested area fell by {{ f(abs(E17.loc['Sunamganj', 'area_ha_chg_pct'])) }} %, while yield changed by only {{ f(E17.loc['Sunamganj', 'yield_t_ha_chg_pct']) }} %. Official damage reports, satellite greenness loss and published figures support these losses. The evidence for a general relationship is only suggestive: the harvested-area effect per 10 points of flood was {{ f(SA.pct) }} % with Sentinel-1 and {{ f(JA.pct) }} % with JRC, its size was unstable, and it was close to zero without 2016 and 2017. The 2016 and 2022 flood years showed no comparable fall. An exploratory analysis points to flood timing, but rests on 2017. Yield alone can therefore miss large losses, so damage assessment should also track harvested area and production.

**Keywords:** flood loss; flash flood; Boro rice; harvested area; crop yield statistics; Bangladesh

# Software and data availability

- Code, notebooks and outputs: https://github.com/TasMumu/bd-boro-flood-risk; the version described here is archived on Zenodo at https://doi.org/10.5281/zenodo.23838852
- Data: the panel archived at https://doi.org/10.5281/zenodo.23795046 [@mumu2026b]. The Earth Engine extracts used here are included with the code
- Software: Python 3.13 with the packages listed in the code repository, and Google Earth Engine for the new extracts

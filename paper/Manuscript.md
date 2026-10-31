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

Flood losses to crops are often measured through yield, but official yield is estimated on harvested fields, so a destroyed field may leave no trace in it. We tested this for Boro rice in Bangladesh, using a validated panel of 64 districts for 2011–2025, flood fractions from Sentinel-1 and JRC, and a written analysis plan. In the 2017 flash flood, harvested area in the seven haor districts fell by 31 % relative to other districts, while yield changed by −0.9 %. In Sunamganj, area fell by 72 % and yield by 0.8 %. A satellite crop-loss measure and published damage figures support these losses. The general result was only suggestive under the plan's rule: the area effect per 10 points of flood was −21.6 % with Sentinel-1 and −4.7 % with JRC, and it disappeared without 2016 and 2017. The 2016 and 2022 floods left no fall in area. An exploratory analysis suggests that timing matters, but rests on 2017. Yield alone can therefore miss the largest losses, so damage assessment should also track harvested area and production.

**Keywords:** flood loss; flash flood; Boro rice; harvested area; crop yield statistics; Bangladesh

# Software and data availability

- Code, notebooks and outputs: https://github.com/TasMumu/bd-boro-flood-risk [authors: add the Zenodo DOI of the archived release]
- Data: the panel archived at https://doi.org/10.5281/zenodo.23795046 (Mumu and Karim, 2026b). The Earth Engine extracts used here are included with the code
- Software: Python 3.13 with the packages listed in the code repository, and Google Earth Engine for the new extracts


# 1. Introduction

Assessing what a flood costs a farming region depends on what is measured. Most research on weather and crops has focused on yield (Cui, 2020; Wei et al., 2023), and yield is the natural outcome when a flood reduces grain per hectare. But a flood can also destroy a crop outright. If official yield is measured only on fields that were harvested, a destroyed field does not lower the yield estimate. It simply leaves the harvested area. Disaster assessments and research that look at yield alone could then miss the losses that matter most.

The evidence on this point is mixed, and the answer appears to depend on the setting. Globally, drought reduced cereal production through both area and yield, extreme heat mainly through yield, and no effect of floods could be identified in national data (Lesk et al., 2016). A recent global study reports that submergence for more than a week reduces annual rice yield by 4.3 % (Li et al., 2025). In the United States, harvested ratios fall under extreme heat (Cui, 2020), and shocks in planted and harvested area coincided with more than half of the production shocks across seven crops, although yield contributed more for some of them (Wei et al., 2023). In Kansas wheat, however, losses came from yield and not from abandonment (Obembe et al., 2021). For rice, typhoons reduced provincial production in a Philippine panel (Blanc and Strobl, 2016).

Boro rice in Bangladesh is a useful test. It is the country's main rice crop, grown in the dry season and harvested from April to May. In the haor wetlands of the north-east, early flash floods can destroy the standing crop shortly before harvest (Kamruzzaman and Shaw, 2018; Rashid and Yasmeen, 2018), and the 2017 flood alone was reported to have cost 0.88 million tonnes of Boro (Hossain et al., 2023). The Bangladesh Bureau of Statistics (BBS) estimates yield as production per harvested hectare, from crop cuts on harvested fields (Bangladesh Bureau of Statistics, 2026), so the reporting explanation can be tested directly: if destroyed fields leave no trace in yield, a flood should appear in area and production but not in yield.

We asked five questions. Q1: do flash floods reduce Boro production through harvested area rather than yield? Q2: do monsoon floods, which come before planting, act differently? Q3: are flood effects concentrated in the haor? Q4: does the vegetation index NDVI explain yield within a district? Q5: where is risk concentrated, and how stable is that ranking?

The analysis makes three contributions. It uses a validated panel of all 64 districts, with values printed by BBS and no modelled yields (Mumu and Karim, 2026a). It checks official statistics against evidence independent of them, namely two flood records, a satellite measure of crop loss, and published damage figures. And its questions, models and pass rules were written down before the models were run, so that a weak result is reported as weak (Section 4.1 gives the limits of this claim). That turned out to matter: the area effect is clear for the 2017 flood, but the evidence for a general rule is only suggestive.


# 2. Background

## 2.1 Flash floods and Boro in the haor

The haor basin is a low-lying wetland in north-eastern Bangladesh, where Boro is often the only crop of the year (Kamruzzaman and Shaw, 2018). Two hazards dominate: cold at the reproductive stage and flash flood at maturity (Rashid and Yasmeen, 2018). Floods are typically described as arriving in the first two weeks of April (Hossain et al., 2023), and the 2017 flood began on 27 March (Ahmed et al., 2017). Timing is therefore central, because the same water can destroy a standing crop or arrive after the harvest. Evidence on these losses is mostly from single events or small areas: satellite mapping of the 2017 damage (Ahmed et al., 2017), household surveys (Dey et al., 2021; Ahmed, 2024) and local studies (Khan et al., 2012; Mondal et al., 2021). The haor is also an adaptation setting, where short-duration varieties and earlier sowing are recommended (Hossain et al., 2023) and farmers report barriers to adapting (Baishakhy et al., 2023).

## 2.2 Floods and rice in Bangladesh

In Bangladesh, floods are not simply harmful. Districts more prone to flooding had higher cultivated area and productivity in 1978–2000, with yield falling in extreme floods and rising in normal floods and in the months after (Banerjee, 2010). Boro production rose after the 1988 and 1998 floods, helped by residual water, while the Aman crop fell through both area and yield (Asada et al., 2005). A district panel found meaningful flood effects on Boro production but no meaningful yield results (Hassan, 2019). Studies of climate and rice mostly examine yield, using regions, stations or national series (Sarker et al., 2014; Hasan et al., 2016; Rahman et al., 2017). One study covers both yield and cropping area, using national time series and climate variables (Amin et al., 2015). Rainfall and self-reports are weak proxies for flood exposure in Bangladesh, which supports the use of satellite data (Guiteras et al., 2015).

## 2.3 The gap

Table 1 compares the closest studies with this one. We found no study that uses a multi-year district panel with satellite flood data to split Boro flash-flood losses into harvested area and yield. This rests on a documented search of 1,383 records, screened on titles and abstracts (Appendix B). A recent study addresses monsoon flood disasters and crop production in Bangladesh (Rahman et al., 2025).

Table 1. Closest studies compared with this paper.

| Study | Flood type | Unit and period | Satellite flood data | Area and yield separated | Haor focus |
|------------|----------|---------------|----------|----------|------|
| Banerjee (2010) | Monsoon | Districts, 1978–2000 | Not stated | Partly | No |
| Asada et al. (2005) | Severe monsoon | National, long term | No | Yes, descriptive | No |
| Hassan (2019) | Flood damage indicators | Districts | Not stated | No | No |
| Amin et al. (2015) | None, climate only | National, 1972–2010 | No | Yes | No |
| Ahmed et al. (2017) | Flash, 2017 only | North-east, one event | Yes | Damaged area only | Yes |
| This paper | Flash and monsoon | 64 districts, 2011–2025 | Yes, two records | Yes | Yes |


# 3. Data

## 3.1 Panel

The analysis uses the panel built and tested in the framework paper (Mumu and Karim, 2026a) and archived separately (Mumu and Karim, 2026b): 960 district-years for all 64 districts and harvest years 2011–2025, where harvest year t is the crop sown in November of t−1 and harvested in April–May of t. Boro harvested area, yield and production are values printed in the BBS yearbooks, each with its edition and page, and no value is modelled or filled. Weather comes from ERA5-Land (Muñoz-Sabater et al., 2021). Flood fractions come from the monthly surface water record of the Joint Research Centre (JRC) (Pekel et al., 2016) and from Sentinel-1 radar (Torres et al., 2012), and are kept as separate records. Table 2 lists the sources. The seven haor districts are Sunamganj, Habiganj, Netrokona, Kishoreganj, Sylhet, Moulvibazar and Brahmanbaria, a list fixed before the models were run. They produced 17.5 % of Boro over the period.

Table 2. Data sources.

| Variable | Source | Resolution | Period |
|--------------------------|--------------------------|-------------------|--------------------------|
| Boro area, yield, production | BBS yearbooks, from the panel of Mumu and Karim (2026b) | 64 districts | 2011–2025 |
| Flood, Sentinel-1 | COPERNICUS/S1_GRD, VV, −18 dB | Analysed at 60 m | Harvest years 2015–2025 |
| Flood, JRC | Global Surface Water v1.4, monthly | 30 m | Harvest years 2011–2021 |
| Boro mask, crop loss, NDVI | MODIS MOD13Q1 v061, WorldCover v200 cropland | 250 m | 2011–2025 |
| Weather | ERA5-Land daily aggregates | 0.1° | 2011–2025 |

Flash flood is the share of district area under water in April or May of year t and not in January–March of t. Monsoon flood is the share under water in June–October of t−1 and not in January–March of t−1. JRC ends in December 2021 and Sentinel-1 begins in October 2014, so the main models use harvest years 2011–2021 for JRC and 2016–2025 for Sentinel-1.

## 3.2 Relation to the framework paper

The framework paper describes how the panel was built and tested, and uses the 2017 flood and a simple index only as brief examples (Mumu and Karim, 2026a). This paper asks a different question, and adds new variables, three designs and independent checks. Two differences need explaining. For Sunamganj in 2017, the framework paper reports −71.5 % area and −0.1 % yield against the mean of 2015–2016. Here the baseline is the mean of 2015 and 2018, giving −72.4 % and −0.8 %, because 2016 was itself a flood year. The risk index also differs. The framework paper's illustrative index has five equally weighted components with whole-district JRC flood. Ours has seven components grouped as exposure and sensitivity, flood on Boro land from both records, and stage-specific heat and cold, and it is tested under many combinations of choices, so the two top tens differ.

## 3.3 New variables

New variables were computed in Google Earth Engine (Gorelick et al., 2017). Every extract was tested for completeness, and no value was filled.

**Boro mask.** Published Boro maps cover only 2017 (Singha et al., 2019) or 2014–2018 (Shew and Ghosh, 2019), so we built a consistent mask for the whole period, following earlier MODIS mapping of Boro (Mosleh and Hassan, 2014). Using the normalised difference vegetation index (NDVI) from MODIS (Didan, 2021) on WorldCover cropland (Zanaga et al., 2022), a pixel is counted as Boro land in year t if its peak NDVI from February to mid-March reaches 0.50 and has risen by at least 0.20 since December–January. These images all end before the flood window, so the mask describes the crop before any loss. Area changes little for thresholds between 0.40 and 0.50. A stable mask, covering land that meets the rule in at least five of the 15 years, is used for flood fractions on Boro land. It covers 4.70 million ha, against about 4.8 million ha harvested in BBS statistics, and agrees with BBS area between districts (r = 0.91). The yearly mask is noisier (Table A.2) and is used only to define the land on which crop loss is measured.

**Satellite crop loss.** Following the logic of the Disaster Vegetation Damage Index (Rahman et al., 2021), we took the change in NDVI from the pre-flood peak to the two composites starting in April, and subtracted the same pixel's median change over all years. Loss is the share of Boro land with an anomaly below −0.20. This measure uses no BBS data.

**Flood timing.** The flash-flood window was split into early and late parts against a January–February baseline, so that water from a March flood is not treated as dry-season water. For Sentinel-1, early is 15 March to 15 April and late is 16 April to 15 May, each from two half-month medians. JRC is monthly, so early is March–April and late is May.

**Other variables.** We also computed flood fractions at water thresholds of −16 and −20 dB, Sentinel-1 scene counts, hot days above 35 °C from mid-March to April (Jagadish et al., 2007), and days below 20 °C from mid-February to March. The cold threshold is provisional. Adaptive capacity is not covered, because no published district series was assembled, and nothing was estimated in its place.

## 3.4 Data checks

All 18 checks passed (Table A.3). The new code recomputed the published flood fractions of the panel, and the largest difference was below 10^−9^, so the variants are computed by verified code. The panel's checksum matches the archived version.


# 4. Methods

## 4.1 Analysis plan

Questions, models, pass rules and the bound for a negligible yield effect were written in a plan before any new model was run. The plan was not registered with a public timestamp. It entered version control together with the results, in the first commit of the repository (54ca10f, 31 October 2026), so readers cannot verify the order independently, and this study should not be read as preregistered. The plan and its log of changes are in the repository. The basic models in the framework paper (Mumu and Karim, 2026a) had been seen and count as exploratory. Two changes were made before the outcome models were run, based on flood and mask data and BBS area between districts: flood fractions on rice land use a stable mask built here, because the yearly mask proved noisy and published rice maps do not cover the period; and Sentinel-1 early and late windows use half-month medians, because a single monthly median diluted a flood arriving midway. After the planned results were seen, we added the analyses in Section 5.6, one extra synthetic-control test, a variant without districts with a small Boro base, and a variant without Chandpur. These are labelled as exploratory, and they do not change the verdict.

## 4.2 Flood models

For district i in harvest year t, each outcome Y (harvested area, yield or production) is modelled as

$$\ln Y_{it} = \beta F_{it} + \gamma M_{it} + \mathbf{x}^{\prime}_{it}\boldsymbol{\delta} + \alpha_i + \tau_t + \varepsilon_{it},$$

where F is flash flood and M monsoon flood, both per 10 points of district area, **x** holds mean temperature, precipitation and hot days, and α and τ are district and year effects. Since production is area times yield, the area and yield effects must add up to the production effect; the largest gap was below 0.0001 log points. Effects are reported in per cent. This is the standard panel approach to weather effects (Hsiang, 2016; Blanc and Schlenker, 2017; Auffhammer et al., 2013). Results are estimates under the stated assumptions: floods are not randomly assigned, and we avoid causal language.

## 4.3 Three designs for flash floods

Flash floods were studied in three ways that must point the same way: the dose-response model above; a year-by-year comparison of haor and other districts relative to 2015, the last year before the two largest floods; and synthetic control (Abadie, 2021) for the five most flooded districts in 2017, where a weighted mix of non-haor districts matches each district's path in 2011–2015.

## 4.4 Uncertainty

Few districts are treated and they are atypical, a setting in which clustered errors and the wild bootstrap can fail, and randomisation inference has limits (Conley and Taber, 2011; MacKinnon and Webb, 2017, 2018, 2020). So no single method was relied on. Every main estimate is reported with errors clustered by district, Driscoll–Kraay errors (Driscoll and Kraay, 1998), Conley spatial errors (Conley, 1999) with a 100 km cut-off and two years of serial correlation, and randomisation inference that reassigns whole flood years across the panel, keeping each flood's real spatial pattern. With T years, one event alone cannot reach a p-value below 1/T, about 0.10 here, and two events below about 0.01. These limits apply only when one or two years carry all the variation. Because the flood pattern of every year is permuted, smaller p-values are possible when several years contribute, as in Table 4.

## 4.5 How results were judged

A result is called **supported** only if it has the same sign and similar size under all three designs, p < 0.05 under all four uncertainty methods in both flood records, the same direction in both records, and passes every required check. If the significance rule holds in one record it is **suggestive**, and otherwise **not supported**. Leave-out checks pass with the same sign and at least half the main size. Placebos pass if not significant at 5 % under clustered and Driscoll–Kraay errors. Satellite crop loss passes if flood raises it and it lowers BBS area, each with p < 0.05 under Driscoll–Kraay errors. Measurement checks pass with the same sign and p < 0.05 under Driscoll–Kraay errors. Synthetic control passes if the 2017 gap is negative and its size relative to the pre-flood fit ranks in the top 5 % of placebo districts.

A yield effect counts as negligible only if its 95 % interval lies within ±2 % per 10 points under every interval method. An insignificant coefficient alone is not evidence of no effect.

## 4.6 Index and spatial analysis

The risk index combines exposure (flash and monsoon flood on Boro land, heat at flowering and cold at the reproductive stage) with sensitivity (production instability, worst fall in area, low yield). In line with the handbook on composite indicators (OECD and European Commission Joint Research Centre, 2008) and uncertainty analyses of such indices (Saisana et al., 2005; Tate, 2012), we rebuilt it under 6,018 combinations of three normalisations, two aggregations and four weighting schemes, including 1,000 random draws of weights. Global Moran's I (Moran, 1950) and LISA (Anselin, 1995) were run under four neighbour definitions, with false discovery rate correction (Benjamini and Hochberg, 1995). Monsoon-flood and haor-interaction tests were corrected the same way as secondary tests.


# 5. Results

## 5.1 Few events carry the flash-flood estimates

Flash floods are concentrated in a few places and years (Fig. 1, Fig. 2). Sentinel-1 has 704 district-years but only about 11 effective observations (Table 3). Effective observations are the inverse of the sum of squared shares of the flood variation left after removing district and year means, so they fall as a few district-years dominate. Seven districts carry nearly all the variation, and two years carry most of it, so the flash-flood analysis is really a study of a few events. Monsoon floods are spread much more widely. Sentinel-1 also has a coverage break: scenes per haor district more than double after 2016 (Fig. 2b), which matters because 2016 is a key flood year.

Fig. 1. Flash flood and satellite crop loss. Panel (a) shows mean flash flood on Boro land. Panel (b) shows the share of Boro land with a sharp fall in greenness in 2017.

![](figures/fig1_map.png){width=100%}

Fig. 2. How few events carry the estimates. Panel (a) shows each year's share of flash-flood variation after removing district and year means. Panel (b) shows Sentinel-1 scenes per haor district.

![](figures/fig2_design.png){width=100%}

Table 3. Where the flood variation comes from. Effective observations are defined in the text.

| Flood variable | District-years | Effective observations | From the seven haor districts (%) | From 2016 and 2017 (%) |
|--------------------------|------------------|----------------|-------------|--------|
| Flash flood, Sentinel-1 | 704 | 11 | 88 | 68 |
| Flash flood, JRC | 704 | 23 | 90 | 56 |
| Monsoon flood, Sentinel-1 | 640 | 52 | 47 | 13 |
| Monsoon flood, JRC | 768 | 103 | 41 | 19 |

## 5.2 Main flood models

With Sentinel-1, 10 more points of flash flood went with 21.6 % less harvested area and 21.7 % less production, significant under all four methods, and with no detectable change in yield (−0.2 %) (Table 4). With JRC the area effect was much smaller (−4.7 %) and not significant under any method. Yield rose slightly with JRC (1.1 %), significant under Driscoll–Kraay errors and randomisation inference only.

Table 4. Flash-flood effects per 10 points of district area, with p-values from four methods.

| Flood record | Outcome | Effect per 10 points (%) | Clustered p | Driscoll–Kraay p | Conley p | Randomisation p | N |
|-------------|-----------------|----------|-------------|------------------|----------|-----------------|------|
| Sentinel-1 | Harvested area | −21.6 | 0.021 | < 0.001 | 0.007 | 0.002 | 640 |
| Sentinel-1 | Yield | −0.2 | 0.862 | 0.878 | 0.871 | 0.891 | 640 |
| Sentinel-1 | Production | −21.7 | 0.027 | < 0.001 | 0.010 | 0.004 | 640 |
| JRC | Harvested area | −4.7 | 0.080 | 0.140 | 0.114 | 0.238 | 704 |
| JRC | Yield | 1.1 | 0.098 | 0.022 | 0.051 | 0.013 | 704 |
| JRC | Production | −3.7 | 0.167 | 0.215 | 0.220 | 0.369 | 704 |

The yield interval was narrow but just exceeded the ±2 % bound: −2.3 to 2.0 % for Sentinel-1 under Driscoll–Kraay errors, and up to 2.4 % for JRC under clustered errors. So the planned test for a negligible yield effect was not met. Yield effects were small, and no method gave a sizeable negative one.

## 5.3 The 2017 flood

The year-by-year comparison shows why the two records differ (Fig. 3). In 2017, haor districts fell 30.6 % in area and 31.2 % in production relative to other districts and to 2015, while yield changed by −0.9 %. Area recovered at once, to 14.4 % in 2018. The other large floods left no such mark: haor area was 13.1 % in 2016 and 5.9 % in 2022. Differences before the floods reach 8.3 %, so smaller movements should not be over-read.

Fig. 3. Haor districts against other districts, relative to 2015, on one shared scale. Flood years are shaded. Intervals are clustered by district and can be too narrow with few treated districts.

![](figures/fig3_by_year.png){width=100%}

Sunamganj shows the pattern most clearly: 189 thousand ha harvested in 2016, 54 thousand ha in 2017 and 201 thousand ha in 2018. Against the mean of 2015 and 2018, its area fell by 72.4 % and its yield by 0.8 % (Table 5, Fig. 4).

Table 5. The 2017 flood in the most flooded districts. BBS changes are from the mean of 2015 and 2018.

| District | Sentinel-1 flood (%) | JRC flood (%) | Satellite crop loss (%) | BBS area (%) | BBS yield (%) | BBS production (%) |
|---------------|--------------|---------|-------------|--------|---------|--------------|
| Sunamganj | 44.7 | 37.2 | 62.8 | −72.4 | −0.8 | −72.6 |
| Kishoreganj | 27.0 | 30.0 | 38.4 | −29.2 | 1.3 | −28.2 |
| Netrokona | 17.4 | 16.2 | 14.1 | −19.4 | −1.3 | −20.5 |
| Sylhet | 12.7 | 26.7 | 58.6 | −23.1 | −3.8 | −26.1 |
| Habiganj | 10.2 | 14.1 | 20.8 | −13.2 | −3.1 | −15.9 |
| Moulvibazar | 8.4 | 9.5 | 41.4 | −24.1 | 1.3 | −23.1 |
| Lalmonirhat | 7.9 | 0.4 | 0.3 | −3.0 | 6.2 | 2.9 |
| Brahmanbaria | 5.8 | 5.7 | 5.2 | −11.8 | −0.1 | −12.0 |

Fig. 4. The 2017 flood across all 64 districts. Panel (a) sets satellite crop loss against BBS harvested area. Panel (b) sets the flood against BBS yield, on the same scale.

![](figures/fig4_event_2017.png){width=100%}

Two non-haor districts stand out in Fig. 4a, with large changes in BBS area and almost no satellite loss. Patuakhali fell by 43 %, but from a base of under 2,000 ha. Chandpur rose by 67 %: its 2017 area is 110,467 ha, against 64,424 ha in 2015 and 67,733 ha in 2018. That value is as printed in the yearbook, and we found no flood or satellite explanation for it. Both cases show that BBS area can move for reasons other than flood, by as much as the flood signal.

Synthetic control gave the same pattern. The estimated 2017 area gaps were −70.4 % in Sunamganj, −29.3 % in Kishoreganj, −17.4 % in Sylhet, −13.2 % in Netrokona and −8.5 % in Habiganj, while yield gaps stayed within 3.9 % (Table 6). The planned test was not met: no gap ranked in the top 5 % relative to its pre-flood fit. With five years to match and many donors, the pre-flood fit is almost perfect, so this ratio is unstable. An exploratory test on the gap's size alone ranks Sunamganj at p = 0.017 and Kishoreganj at p = 0.052, and the other three above 0.1.

Table 6. Synthetic control for the five most flooded districts. Placebo rank p is the planned test.

| District | Outcome | Gap 2016 (%) | Gap 2017 (%) | Gap 2018 (%) | Placebo rank p |
|--------------|-----------------|--------|--------|--------|-----------|
| Sunamganj | Harvested area | 0.8 | −70.4 | 3.5 | 0.103 |
| Kishoreganj | Harvested area | 1.6 | −29.3 | −9.1 | 0.103 |
| Netrokona | Harvested area | 3.8 | −13.2 | 2.1 | 0.776 |
| Sylhet | Harvested area | −3.3 | −17.4 | 5.1 | 0.121 |
| Habiganj | Harvested area | 1.3 | −8.5 | −1.8 | 0.603 |
| Sunamganj | Yield | 1.4 | −1.1 | 1.1 | 0.241 |
| Kishoreganj | Yield | 0.5 | 1.7 | 3.6 | 0.431 |
| Netrokona | Yield | 1.9 | −2.3 | 2.5 | 0.483 |
| Sylhet | Yield | −1.6 | −3.9 | 2.1 | 0.759 |
| Habiganj | Yield | 0.5 | −0.1 | 0.7 | 0.759 |

## 5.4 Evidence independent of BBS

The satellite measure uses no BBS data, and it passed its planned test. Each 10 points of flood raised satellite crop loss by 7.5 points with Sentinel-1 (Driscoll–Kraay p = 0.001) and 6.2 points with JRC (p = 0.005), and satellite loss lowered BBS area (p = 0.041) but not yield (p = 0.226). In 2017, satellite loss reached 63 % of Boro land in Sunamganj and 59 % in Sylhet, and at most 4.4 % outside the haor (Fig. 1b, Fig. 4a).

Published damage figures are also of the same order. Against the mean of 2015 and 2018, BBS shows a production loss of 1.08 million t in the seven haor districts in 2017, compared with 0.88 million t reported for the haor regions (Hossain et al., 2023). For Sunamganj, BBS implies 142,482 ha and 520,428 t lost, compared with 149,224 ha affected and 393,855 t damaged in a published estimate (Mondal et al., 2021).

## 5.5 Checks and verdict

The required checks gave a mixed picture (Table 7, Fig. 5). Because the main Sentinel-1 sample starts in 2016, the planned check without 2015–2016 is the same model as leaving out 2016, so it is counted once. All leave-out checks passed for Sentinel-1, and the flood-after-harvest placebo passed in both records. Next year's flood, however, failed for Sentinel-1 (11.6 %, clustered p = 0.033), possibly because haor area was high in 2016, just before the 2017 flood. For JRC, the effect disappeared without 2017 (0.6 %) or Sunamganj (−1.5 %), and was not significant on rice land only. Most importantly, without both 2016 and 2017 no effect remained in either record (0.1 % and −0.1 %). Flood size also mattered: only the largest group, 20 % or more of a district, showed clear losses (−31.9 % with Sentinel-1, from 5 district-years, and −15.7 % with JRC, from 8; Fig. 6). The size of the Sentinel-1 estimate also partly reflects small districts. Leaving out the six districts with a small Boro base gave −13.8 % with Sentinel-1 and −6.2 % with JRC, and a Poisson model, which weights by area, gave −10.9 % and −5.3 % (Table A.1). The two records are closer in both cases.

Table 7. Required checks of the area effect. Effects are per 10 points of flood.

| Check | Flood record | Area effect (%) | Clustered p | Driscoll–Kraay p | Result |
|--------------------------|-------------|----------|-------------|------------------|----------|
| Leave out 2016 | Sentinel-1 | −16.7 | 0.005 | < 0.001 | Pass |
| Leave out 2016 | JRC | −9.5 | 0.011 | 0.013 | Pass |
| Leave out 2017 | Sentinel-1 | −20.8 | 0.258 | 0.004 | Pass |
| Leave out 2017 | JRC | 0.6 | 0.688 | 0.752 | Fail |
| Leave out 2022 | Sentinel-1 | −24.4 | 0.012 | < 0.001 | Pass |
| Leave out Sunamganj | Sentinel-1 | −21.6 | 0.176 | 0.009 | Pass |
| Leave out Sunamganj | JRC | −1.5 | 0.379 | 0.533 | Fail |
| Leave out Kishoreganj | Sentinel-1 | −25.5 | 0.018 | < 0.001 | Pass |
| Leave out Kishoreganj | JRC | −5.7 | 0.073 | 0.151 | Pass |
| Leave out Sylhet | Sentinel-1 | −24.1 | 0.014 | < 0.001 | Pass |
| Leave out Sylhet | JRC | −5.6 | 0.047 | 0.101 | Pass |
| Leave out Netrokona | Sentinel-1 | −22.2 | 0.023 | < 0.001 | Pass |
| Leave out Netrokona | JRC | −5.0 | 0.070 | 0.122 | Pass |
| Next year's flash flood (placebo) | Sentinel-1 | 11.6 | 0.033 | 0.225 | Fail |
| Next year's flash flood (placebo) | JRC | 0.6 | 0.678 | 0.820 | Pass |
| Flood after harvest (placebo) | Sentinel-1 | 0.9 | 0.758 | 0.756 | Pass |
| Flood after harvest (placebo) | JRC | 2.3 | 0.328 | 0.125 | Pass |
| Rice land only | Sentinel-1 | −15.3 | 0.037 | 0.001 | Pass |
| Rice land only | JRC | −2.5 | 0.220 | 0.233 | Fail |
| January–February baseline, early window | Sentinel-1 | −14.0 | 0.077 | < 0.001 | Pass |
| January–February baseline, early window | JRC | −19.5 | 0.036 | < 0.001 | Pass |
| Scene counts as controls | Sentinel-1 | −21.5 | 0.020 | < 0.001 | Pass |

Fig. 5. How the flash-flood estimates hold up. Each row reruns the main model with one change. Intervals are 95 %, clustered by district. The shaded band marks ±2 %.

![](figures/fig5_checks.png){width=100%}

Fig. 6. Normal and extreme floods, against the group below 1 %. Intervals are 95 %, clustered by district. Under each label, n gives the district-years in the bin, Sentinel-1 first.

![](figures/fig6_bins.png){width=100%}

Under the plan's rule, the answer to Q1 is **suggestive**, not supported. The significance rule held for Sentinel-1 but not for JRC, 18 of 22 required checks passed, and the planned synthetic-control test failed. Direction and design agreed throughout. For Q3, concentration in the haor could not be tested properly: outside it, Sentinel-1 flood reached 5 % in only 1.8 % of district-years, so any slope there is an extrapolation, and no haor interaction survived false discovery rate correction.

## 5.6 Flood timing (exploratory)

Why did 2017 stand out? This analysis was added after the planned results were seen. Table 8 suggests that timing is the reason. In 2017, more water arrived early, while in 2016 most Sentinel-1 water came late. The planned early-window check had already brought the two records close together: −14.0 % with Sentinel-1 and −19.5 % with JRC per 10 points (Table 9). This is consistent with the JRC estimate in Table 4 being weak because its window mixes water before and after harvest.

This reading has clear limits. Without 2017 the early-window effect disappears or reverses in both records, so it rests on that one event. And satellite loss in 2016 (16.2 %) did not match BBS, where area rose. NDVI also falls when fields are harvested early, so satellite loss cannot separate harvest from destruction.

Table 8. Flood timing in the haor districts. Flood and loss are mean shares; BBS area is from the year-by-year model.

| Harvest year | Sentinel-1 early (%) | Sentinel-1 late (%) | JRC early (%) | JRC late (%) | Satellite crop loss (%) | BBS area against 2015 (%) |
|-----------|--------------|--------------|---------|--------|-------------|-----------|
| 2015 | 0.4 | 2.9 | 2.3 | 10.7 | 1.5 | 0.0 |
| 2016 | 1.8 | 15.9 | 8.4 | 23.6 | 16.2 | 13.1 |
| 2017 | 13.7 | 18.3 | 10.7 | 16.8 | 34.5 | −30.6 |
| 2018 | 0.2 | 3.2 | 0.0 | 12.6 | 0.9 | 14.4 |
| 2022 | 1.4 | 3.6 | – | – | 3.6 | 5.9 |

Table 9. Early-window effects per 10 points (exploratory). RI is randomisation inference.

| Flood record | Outcome | Sample | Effect per 10 points (%) | Clustered p | Driscoll–Kraay p | Conley p | RI p |
|-------------|-----------------|---------------|----------|-------------|------------------|----------|--------|
| Sentinel-1 | Harvested area | All years | −14.0 | 0.077 | < 0.001 | 0.043 | 0.079 |
| Sentinel-1 | Harvested area | Without 2017 | 9.9 | 0.085 | 0.009 | 0.068 | 0.178 |
| Sentinel-1 | Harvested area | Without 2016 | −9.6 | 0.127 | < 0.001 | 0.104 | 0.061 |
| Sentinel-1 | Yield | All years | −1.7 | 0.117 | 0.067 | 0.096 | 0.751 |
| Sentinel-1 | Yield | Without 2017 | 6.9 | 0.078 | 0.017 | 0.013 | 0.009 |
| Sentinel-1 | Yield | Without 2016 | −3.2 | 0.047 | 0.045 | 0.029 | 0.334 |
| JRC | Harvested area | All years | −19.5 | 0.036 | < 0.001 | 0.011 | 0.001 |
| JRC | Harvested area | Without 2017 | −2.5 | 0.455 | 0.486 | 0.455 | 0.641 |
| JRC | Harvested area | Without 2016 | −24.3 | 0.054 | < 0.001 | 0.008 | 0.004 |
| JRC | Yield | All years | 0.3 | 0.791 | 0.737 | 0.763 | 0.795 |
| JRC | Yield | Without 2017 | 1.4 | 0.364 | 0.448 | 0.384 | 0.411 |
| JRC | Yield | Without 2016 | 0.0 | 0.972 | 0.970 | 0.971 | 0.982 |

## 5.7 Monsoon floods (Q2)

Monsoon floods gave no clear result (Table 10). JRC pointed to more area (5.7 % per 10 points) and Sentinel-1 to less (−4.9 %), and neither was significant. With JRC, flooded years in every bin had higher yields than years below 1 % (Fig. 6a), consistent with earlier work (Banerjee, 2010; Asada et al., 2005), but Sentinel-1 showed nothing similar. The expected harm from extreme monsoon floods did not appear in either record. None of these tests survived correction.

Table 10. Monsoon-flood effects per 10 points of district area.

| Flood record | Outcome | Effect per 10 points (%) | Clustered p | Driscoll–Kraay p | Conley p | Randomisation p |
|-------------|-----------------|----------|-------------|------------------|----------|-----------------|
| Sentinel-1 | Harvested area | −4.9 | 0.350 | 0.169 | 0.306 | 0.354 |
| Sentinel-1 | Yield | 0.8 | 0.406 | 0.247 | 0.423 | 0.572 |
| Sentinel-1 | Production | −4.1 | 0.459 | 0.303 | 0.422 | 0.441 |
| JRC | Harvested area | 5.7 | 0.073 | 0.098 | 0.054 | 0.090 |
| JRC | Yield | 0.4 | 0.690 | 0.616 | 0.649 | 0.655 |
| JRC | Production | 6.1 | 0.064 | 0.103 | 0.053 | 0.074 |

## 5.8 NDVI (Q4)

NDVI tracked differences between districts and the shared rise in yield, but not year-to-year departures within a district (Table 11). Over January–April, the correlation with yield was 0.46 between districts and 0.42 within districts, and fell to −0.07 once year effects were removed. No window gave a significant effect, including peak greenness (Mosleh et al., 2016), and the result did not depend on how much of a district is rice land (a correlation of 0.05 in districts with more rice land and 0.06 in those with less). NDVI-based yield estimates at national or division level (Mosleh et al., 2016; Alam et al., 2019) may therefore capture broad differences and trends, not shocks to a district.

Table 11. NDVI and Boro yield.

| NDVI window | Between districts | Within districts | Within, year effects removed | Effect on log yield per 0.1 NDVI | Clustered p | Randomisation p |
|--------------------------|-------------|-------------|-----------|----------|-------------|-----------------|
| January–April | 0.46 | 0.42 | −0.07 | −0.027 | 0.289 | 0.211 |
| February to mid-March | 0.52 | 0.29 | 0.05 | 0.016 | 0.095 | 0.202 |
| Late March to early April | 0.15 | 0.33 | 0.04 | 0.012 | 0.217 | 0.263 |

## 5.9 Risk index and spatial patterns (Q5)

The haor dominates the index: 6 of the top ten districts are in the haor, led by Sunamganj (Table 12, Fig. 7). Six districts with a mean Boro area below 15,000 ha are flagged, a threshold set after the first results: Patuakhali, Barguna, Rangamati, Bandarban, Khagrachhari and Jhalokati. Their high ranks are not reliable. Hill districts such as Rangamati have so little rice land that their flood shares rest on few pixels, and Patuakhali and Barguna rank high because Boro expanded there from a very small base, which appears as instability but is not loss. Without these six, all 7 haor districts are in the top ten.

The ranking is not stable, however. Across 6,018 combinations, the median correlation with the base ranking was 0.66, the median district stayed in its risk tier in 35 % of cases, and no district was in the top ten in at least 90 % of them.

Table 12. The ten highest-ranked districts, with rank range and stability across all combinations.

| Rank | District | Haor | Small Boro base | Rank range, 5th–95th percentile | In top ten (%) | Same tier (%) |
|--------|--------------|--------|---------|--------------|-------|--------|
| 1 | Sunamganj | Yes | No | 1–36 | 88 | 89 |
| 2 | Sylhet | Yes | No | 2–58 | 77 | 78 |
| 3 | Patuakhali | No | Yes | 1–52 | 59 | 65 |
| 4 | Barguna | No | Yes | 2–53 | 56 | 61 |
| 5 | Kishoreganj | Yes | No | 2–30 | 78 | 81 |
| 6 | Moulvibazar | Yes | No | 2–24 | 88 | 89 |
| 7 | Rangamati | No | Yes | 1–14 | 86 | 93 |
| 8 | Habiganj | Yes | No | 4–34 | 67 | 72 |
| 9 | Meherpur | No | No | 2–51 | 34 | 42 |
| 10 | Netrokona | Yes | No | 5–46 | 60 | 65 |

Fig. 7. Risk tier and rank under all combinations. Hatched districts, starred in panel (b), have a small Boro base, so their high ranks are not reliable. Bars show the 5th to 95th percentile of rank, and dots the base ranking.

![](figures/fig7_index.png){width=100%}

Spatial clustering was clear (Table 13). Moran's I ranged from 0.31 to 0.45, and Habiganj, Moulvibazar, Netrokona, Sunamganj and Sylhet formed a high-risk cluster under all four neighbour definitions.

Table 13. Spatial clustering of the index under four neighbour definitions.

| Neighbours | Moran's I | p | High-risk cluster, p < 0.05 | After false discovery rate |
|--------------|-----------|----------|--------------------------|--------------------------|
| Contiguity | 0.451 | < 0.001 | Habiganj, Kishoreganj, Moulvibazar, Netrokona, Sunamganj, Sylhet | Habiganj, Sunamganj, Sylhet |
| 4 nearest | 0.419 | < 0.001 | Habiganj, Moulvibazar, Netrokona, Sunamganj, Sylhet | Habiganj, Moulvibazar, Sunamganj, Sylhet |
| 6 nearest | 0.313 | < 0.001 | Habiganj, Moulvibazar, Netrokona, Sunamganj, Sylhet | Habiganj, Moulvibazar, Sunamganj, Sylhet |
| 100 km band | 0.323 | < 0.001 | Habiganj, Moulvibazar, Netrokona, Sunamganj, Sylhet | Habiganj, Moulvibazar, Sunamganj, Sylhet |

A yield-only view gives a different picture. Sunamganj ranks 25th of 64 on yield instability but 3rd on production instability, and the two rankings correlate at only 0.61.


# 6. Discussion

## 6.1 What can and cannot be claimed

One claim is well supported as a description of a single event. In the 2017 flood, the loss in BBS statistics appeared in harvested area and production, and almost none in yield. The three designs agree in direction, in both flood records, although the planned synthetic-control test failed and the JRC estimate depends on 2017. A satellite measure that uses no BBS data places the loss in the same districts, and published damage figures are of the same order.

The broader claim, that flash floods generally reduce Boro through area, is not established. Under the plan's rule it is only suggestive. The estimate rests on 2016 and 2017, the 2016 and 2022 floods left no fall in area, and the two flood records differ about five-fold in their main estimates, and about two-fold once small districts are set aside. We report that plainly because a single significant estimate of about 22 % per 10 points would have told a stronger and less accurate story. This also bears on how flood effects are read elsewhere: with few events and a few treated districts, an estimate from a large panel can be one event in disguise.

## 6.2 Why area and not yield

The likely reason is how the statistics are built. Yield is estimated from crop cuts on harvested fields (Bangladesh Bureau of Statistics, 2026), so a destroyed field leaves the harvested area and never enters the yield estimate. Since Boro is planted before flash floods arrive, a same-season fall in harvested area means crop lost and not a planting decision. Crops that survive are measured as usual, which fits a yield effect near zero. The small positive yield effect with JRC could mean that weaker fields are lost first, but the evidence for this is thin.

This does not contradict Li et al. (2025), who report yield losses from submergence worldwide. Li et al. and this study measure different things in different statistical systems. Whether crop that is totally lost appears in yield or area depends on how each country's data are collected. Similarly, national data may fail to show flood effects at all (Lesk et al., 2016), because a loss such as 2017 is confined to a few districts. Our results differ from the Kansas wheat findings (Obembe et al., 2021) and resemble those on harvested ratios (Cui, 2020), which suggests that the answer depends on the crop, hazard and data system.

## 6.3 Implications

**Disaster assessment.** Yield alone is a poor signal of the largest flood losses in this system. Sunamganj lost 73 % of its production in 2017 with no visible change in yield. Assessments should track harvested area and production alongside yield, and research on Bangladesh's rice should not treat stable yields as evidence of low flood risk. Harvested area is the variable that carried the signal here, but BBS reports only harvested and not planted area. A routine estimate of planted area before the flood window would show directly what share of the crop was lost.

**Satellite monitoring.** Greenness-based crop loss located the 2017 damage without official data, as earlier work found for the same event (Ahmed et al., 2017), and similar methods have been used elsewhere (Rahman and Di, 2020; Qamer et al., 2023). It is useful for rapid assessment, but the 2016 mismatch shows that it should not be read as loss without information on harvest progress. NDVI alone should not be used to infer yield shocks in a district.

**Timing and adaptation.** If water before harvest is what matters, then the most direct response is to finish harvesting before the flood window. Earlier sowing and short-duration varieties are already recommended for this reason (Hossain et al., 2023), though farmers face barriers to adopting them (Baishakhy et al., 2023). The exploratory timing result supports this direction but does not establish it. Flood-tolerant rice has improved outcomes in north-west Bangladesh (Bairagi et al., 2021), but that evidence does not transfer directly to Boro in the haor, where the threat comes at maturity. Interest in crop insurance exists (Islam et al., 2021), and our results suggest that a payout tied to district yield would not have been triggered in 2017. Any index for the haor should be based on area or on satellite-observed loss.

## 6.4 Limitations

The study covers 15 years and few large flash floods, and one event dominates, so the findings describe these events and do not give a general law. Floods are not randomly assigned. BBS harvested area comes from official estimates, which we checked with independent evidence only partly, and only for large events, and values such as Chandpur's in 2017 remain unexplained. The analysis plan has no public timestamp from before the results. The Boro mask relies on a fixed NDVI rule and a static cropland map, is not validated with field data, and has noisy yearly totals. Sentinel-1 has fewer scenes before 2017, and optical records such as JRC can miss short floods that radar observes (Uddin et al., 2019; Twele et al., 2016). Flood fractions in the main models cover whole districts, and the required rice-only check weakened the estimates. Satellite crop loss cannot separate destruction from early harvest. Cold-stress thresholds are provisional. The risk index omits adaptive capacity and salinity (Dasgupta et al., 2018), so it is a partial picture, and its rank ranges are wide. It should guide where to look more closely, and should not be used as an allocation rule.


# 7. Conclusion

Using printed BBS statistics for all 64 districts and a written analysis plan, we asked whether flash floods reduce Boro rice through harvested area rather than yield. For the 2017 flood the answer is clearly yes: haor area and production fell by about a third, yield barely moved, and independent evidence supports the loss. As a general rule the answer is only suggestive, because the estimates rest on 2016 and 2017, and other large floods left no fall in area. Flood timing is the likely reason, but that evidence is exploratory and rests on one event. The practical lesson is that yield alone can miss the largest flood losses in this system, so flood assessment and risk indices should also use harvested area and production.

# CRediT authorship contribution statement

Tasnim Ahmad Mumu: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review & editing, Visualization. Rezaul Karim: Supervision, Methodology, Validation, Writing – review & editing.

# Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used Claude (Anthropic) to assist with code development, data validation and analysis scripts, and drafting and editing of the manuscript text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

# Data availability

The panel is archived at https://doi.org/10.5281/zenodo.23795046. The derived data remain subject to the terms of their sources. The BBS yearbook PDFs and the GADM v4.1 boundaries (GADM, 2022) are not redistributed and must be obtained from the Bangladesh Bureau of Statistics and gadm.org. Code, notebooks, the analysis plan and the Earth Engine extracts for this paper are in the repository given in the Software and data availability section.

# References

Abadie, A., 2021. Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects. Journal of Economic Literature 59 (2), 391–425. https://doi.org/10.1257/jel.20191450

Ahmed, M.R., 2024. How to Enhance Resilience Against the Adverse Effects of Climate Change: Evidence from Boro Rice Farmers in Northeast Bangladesh. Food and Energy Security 13 (6), e70028. https://doi.org/10.1002/fes3.70028

Ahmed, M., Rahaman, K., Kok, A., Hassan, Q., 2017. Remote Sensing-Based Quantification of the Impact of Flash Flooding on the Rice Production: A Case Study over Northeastern Bangladesh. Sensors 17 (10), 2347. https://doi.org/10.3390/s17102347

Alam, M.S., Kalpoma, K., Karim, M.S., Al Sefat, A., Kudoh, J.-i., 2019. Boro rice yield estimation model using MODIS NDVI data for Bangladesh. In: IGARSS 2019 - 2019 IEEE International Geoscience and Remote Sensing Symposium, 7330–7333. https://doi.org/10.1109/igarss.2019.8899084

Amin, M., Zhang, J., Yang, M., 2015. Effects of Climate Change on the Yield and Cropping Area of Major Food Crops: A Case of Bangladesh. Sustainability 7 (1), 898–915. https://doi.org/10.3390/su7010898

Anselin, L., 1995. Local Indicators of Spatial Association—LISA. Geographical Analysis 27 (2), 93–115. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x

Asada, H., Matsumoto, J., Rahman, R., 2005. Impact of Recent Severe Floods on Rice Production in Bangladesh. Geographical Review of Japan 78 (12), 783–793. https://doi.org/10.4157/grj.78.783

Auffhammer, M., Hsiang, S.M., Schlenker, W., Sobel, A., 2013. Using Weather Data and Climate Model Output in Economic Analyses of Climate Change. Review of Environmental Economics and Policy 7 (2), 181–198. https://doi.org/10.1093/reep/ret016

Bairagi, S., Bhandari, H., Kumar Das, S., Mohanty, S., 2021. Flood-tolerant rice improves climate resilience, profitability, and household consumption in Bangladesh. Food Policy 105, 102183. https://doi.org/10.1016/j.foodpol.2021.102183

Baishakhy, S.D., Islam, M.A., Kamruzzaman, M., 2023. Overcoming barriers to adapt rice farming to recurring flash floods in haor wetlands of Bangladesh. Heliyon 9 (3), e14011. https://doi.org/10.1016/j.heliyon.2023.e14011

Banerjee, L., 2010. Effects of Flood on Agricultural Productivity in Bangladesh. Oxford Development Studies 38 (3), 339–356. https://doi.org/10.1080/13600818.2010.505681

Bangladesh Bureau of Statistics, 2026. Yearbook of Agricultural Statistics-2025 (37th series). Statistics and Informatics Division, Ministry of Planning, Dhaka.

Benjamini, Y., Hochberg, Y., 1995. Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. Journal of the Royal Statistical Society Series B: Statistical Methodology 57 (1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

Blanc, E., Schlenker, W., 2017. The Use of Panel Models in Assessments of Climate Impacts on Agriculture. Review of Environmental Economics and Policy 11 (2), 258–279. https://doi.org/10.1093/reep/rex016

Blanc, E., Strobl, E., 2016. Assessing the Impact of Typhoons on Rice Production in the Philippines. Journal of Applied Meteorology and Climatology 55 (4), 993–1007. https://doi.org/10.1175/jamc-d-15-0214.1

Conley, T.G., 1999. GMM estimation with cross sectional dependence. Journal of Econometrics 92 (1), 1–45. https://doi.org/10.1016/s0304-4076(98)00084-0

Conley, T.G., Taber, C.R., 2011. Inference with “Difference in Differences” with a Small Number of Policy Changes. Review of Economics and Statistics 93 (1), 113–125. https://doi.org/10.1162/REST_a_00049

Cui, X., 2020. Beyond Yield Response: Weather Shocks and Crop Abandonment. Journal of the Association of Environmental and Resource Economists 7 (5), 901–932. https://doi.org/10.1086/709859

Dasgupta, S., Hossain, M.M., Huq, M., Wheeler, D., 2018. Climate Change, Salinization and High-Yield Rice Production in Coastal Bangladesh. Agricultural and Resource Economics Review 47 (1), 66–89. https://doi.org/10.1017/age.2017.14

Dey, N.C., Parvez, M., Islam, M.R., 2021. A study on the impact of the 2017 early monsoon flash flood: Potential measures to safeguard livelihoods from extreme climate events in the haor area of Bangladesh. International Journal of Disaster Risk Reduction 59, 102247. https://doi.org/10.1016/j.ijdrr.2021.102247

Didan, K., 2021. MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid V061. NASA Land Processes Distributed Active Archive Center. https://doi.org/10.5067/MODIS/MOD13Q1.061

Driscoll, J.C., Kraay, A.C., 1998. Consistent Covariance Matrix Estimation with Spatially Dependent Panel Data. Review of Economics and Statistics 80 (4), 549–560. https://doi.org/10.1162/003465398557825

GADM, 2022. Database of Global Administrative Areas, version 4.1. https://gadm.org.

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., Moore, R., 2017. Google Earth Engine: Planetary-scale geospatial analysis for everyone. Remote Sensing of Environment 202, 18–27. https://doi.org/10.1016/j.rse.2017.06.031

Guiteras, R., Jina, A., Mobarak, A.M., 2015. Satellites, Self-reports, and Submersion: Exposure to Floods in Bangladesh. American Economic Review 105 (5), 232–236. https://doi.org/10.1257/aer.p20151095

Hasan, M.M., Sarker, M.A.R., Gow, J., 2016. Assessment of climate change impacts on Aman and Boro rice yields in Bangladesh. Climate Change Economics 07 (03), 1650008. https://doi.org/10.1142/s2010007816500081

Hassan, S.M.K., 2019. Impacts of flooding on the rice production of Bangladesh: a panel data study. Thesis, Colorado State University. https://mountainscholar.org/handle/10217/197396.

Hossain, M., Biswas, P., Islam, M.R., 2023. Cold-Tolerant and Short-Duration Rice (Oryza sativa L.) for Sustainable Food Security of the Flash Flood-Prone Haor Wetlands of Bangladesh. Sustainability 15 (24), 16873. https://doi.org/10.3390/su152416873

Hsiang, S., 2016. Climate Econometrics. Annual Review of Resource Economics 8 (1), 43–75. https://doi.org/10.1146/annurev-resource-100815-095343

Islam, D.I., Rahman, A., Sarker, M.S.R., Luo, J., Liang, H., 2021. Factors affecting farmers’ willingness to adopt crop insurance to manage disaster risk: evidence from Bangladesh. International Food and Agribusiness Management Review 24 (3), 463–480. https://doi.org/10.22434/ifamr2019.0190

Jagadish, S., Craufurd, P.Q., Wheeler, T.R., 2007. High temperature stress and spikelet fertility in rice (Oryza sativa L.). Journal of Experimental Botany 58 (7), 1627–1635. https://doi.org/10.1093/jxb/erm003

Kamruzzaman, M., Shaw, R., 2018. Flood and Sustainable Agriculture in the Haor Basin of Bangladesh: A Review Paper. Universal Journal of Agricultural Research 6 (1), 40–49. https://doi.org/10.13189/ujar.2018.060106

Khan, M., Mia, M.Y., Hossain, M.R., 2012. Impacts of Flood on Crop Production in Haor Areas of Two Upazillas in Kishoregonj. Journal of Environmental Science and Natural Resources 5 (1), 193–198. https://doi.org/10.3329/jesnr.v5i1.11581

Lesk, C., Rowhani, P., Ramankutty, N., 2016. Influence of extreme weather disasters on global crop production. Nature 529 (7584), 84–87. https://doi.org/10.1038/nature16467

Li, Z., Rosa, L., Gorelick, S., 2025. Severe floods significantly reduce global rice yields. Science Advances 11 (46), eadx7799. https://doi.org/10.1126/sciadv.adx7799

MacKinnon, J.G., Webb, M.D., 2017. Wild Bootstrap Inference for Wildly Different Cluster Sizes. Journal of Applied Econometrics 32 (2), 233–254. https://doi.org/10.1002/jae.2508

MacKinnon, J.G., Webb, M.D., 2018. The wild bootstrap for few (treated) clusters. The Econometrics Journal 21 (2), 114–135. https://doi.org/10.1111/ectj.12107

MacKinnon, J.G., Webb, M.D., 2020. Randomization inference for difference-in-differences with few treated clusters. Journal of Econometrics 218 (2), 435–450. https://doi.org/10.1016/j.jeconom.2020.04.024

Mondal, S., Akter, L., Hiya, H.J., Farukh, M.A., 2021. Effects of 2017 Early Flash Flooding on Agriculture in Haor Areas of Sunamganj. Journal of Environmental Science and Natural Resources 12 (1-2), 117–125. https://doi.org/10.3329/jesnr.v12i1-2.52007

Moran, P.A.P., 1950. Notes on continuous stochastic phenomena. Biometrika 37 (1-2), 17–23. https://doi.org/10.1093/biomet/37.1-2.17

Mosleh, M., Hassan, Q., 2014. Development of a Remote Sensing-Based “Boro” Rice Mapping System. Remote Sensing 6 (3), 1938–1953. https://doi.org/10.3390/rs6031938

Mosleh, M.K., Hassan, Q.K., Chowdhury, E.H., 2016. Development of a remote sensing-based rice yield forecasting model. Spanish Journal of Agricultural Research 14 (3), e0907. https://doi.org/10.5424/sjar/2016143-8347

Mumu, T.A., Karim, R., 2026a. An open, tested data engineering framework for integrating official crop statistics with satellite and climate data: district-level Boro rice in Bangladesh. Manuscript submitted to Environmental Modelling & Software.

Mumu, T.A., Karim, R., 2026b. bd-boro-data-framework: an open, tested data engineering framework for integrating official crop statistics with satellite and climate data, district-level Boro rice in Bangladesh. Zenodo. https://doi.org/10.5281/zenodo.23795046

Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., et al., 2021. ERA5-Land: a state-of-the-art global reanalysis dataset for land applications. Earth System Science Data 13 (9), 4349–4383. https://doi.org/10.5194/essd-13-4349-2021

Obembe, O.S., Hendricks, N.P., Tack, J., 2021. Decreased wheat production in the USA from climate change driven by yield losses rather than crop abandonment. PLOS ONE 16 (6), e0252067. https://doi.org/10.1371/journal.pone.0252067

OECD, European Commission Joint Research Centre, 2008. Handbook on Constructing Composite Indicators: Methodology and User Guide. OECD Publishing, Paris. https://doi.org/10.1787/9789264043466-en

Pekel, J.-F., Cottam, A., Gorelick, N., Belward, A.S., 2016. High-resolution mapping of global surface water and its long-term changes. Nature 540 (7633), 418–422. https://doi.org/10.1038/nature20584

Qamer, F.M., Abbas, S., Ahmad, B., Hussain, A., Salman, A., Muhammad, S., Nawaz, M., Shrestha, S., Iqbal, B., Thapa, S., 2023. A framework for multi-sensor satellite data to evaluate crop production losses: the case study of 2022 Pakistan floods. Scientific Reports 13 (1), 4240. https://doi.org/10.1038/s41598-023-30347-y

Rahman, M.S., Di, L., 2020. A Systematic Review on Case Studies of Remote-Sensing-Based Flood Crop Loss Assessment. Agriculture 10 (4), 131. https://doi.org/10.3390/agriculture10040131

Rahman, M.A., Kang, S., Nagabhatla, N., Macnee, R., 2017. Impacts of temperature and rainfall variation on rice productivity in major ecosystems of Bangladesh. Agriculture & Food Security 6 (1), 10. https://doi.org/10.1186/s40066-017-0089-5

Rahman, M.S., Di, L., Yu, E., Lin, L., Yu, Z., 2021. Remote Sensing Based Rapid Assessment of Flood Crop Damage Using Novel Disaster Vegetation Damage Index (DVDI). International Journal of Disaster Risk Science 12 (1), 90–110. https://doi.org/10.1007/s13753-020-00305-7

Rahman, M.A., Alam, M.S., Sultana, R., Sultana, R., 2025. Assessing the interrelationship between monsoon flood disasters and major crop production in Bangladesh. International Journal of Disaster Risk Reduction 121, 105401. https://doi.org/10.1016/j.ijdrr.2025.105401

Rashid, M.M., Yasmeen, R., 2018. Cold Injury and Flash Flood Damage in Boro Rice Cultivation in Bangladesh: A Review. Bangladesh Rice Journal 21 (1), 13–25. https://doi.org/10.3329/brj.v21i1.37360

Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal Statistical Society Series A: Statistics in Society 168 (2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

Santos Silva, J.M.C., Tenreyro, S., 2006. The Log of Gravity. The Review of Economics and Statistics 88 (4), 641–658. https://doi.org/10.1162/rest.88.4.641

Sarker, M.A.R., Alam, K., Gow, J., 2014. Assessing the effects of climate change on rice yields: An econometric investigation using Bangladeshi panel data. Economic Analysis and Policy 44 (4), 405–416. https://doi.org/10.1016/j.eap.2014.11.004

Shew, A.M., Ghosh, A., 2019. Identifying Dry-Season Rice-Planting Patterns in Bangladesh Using the Landsat Archive. Remote Sensing 11 (10), 1235. https://doi.org/10.3390/rs11101235

Singha, M., Dong, J., Zhang, G., Xiao, X., 2019. High resolution paddy rice maps in cloud-prone Bangladesh and Northeast India using Sentinel-1 data. Scientific Data 6 (1), 26. https://doi.org/10.1038/s41597-019-0036-3

Tate, E., 2012. Social vulnerability indices: a comparative assessment using uncertainty and sensitivity analysis. Natural Hazards 63 (2), 325–347. https://doi.org/10.1007/s11069-012-0152-2

Torres, R., Snoeij, P., Geudtner, D., Bibby, D., Davidson, M., Attema, E., Potin, P., Rommen, B., Floury, N., Brown, M., et al., 2012. GMES Sentinel-1 mission. Remote Sensing of Environment 120, 9–24. https://doi.org/10.1016/j.rse.2011.05.028

Twele, A., Cao, W., Plank, S., Martinis, S., 2016. Sentinel-1-based flood mapping: a fully automated processing chain. International Journal of Remote Sensing 37 (13), 2990–3004. https://doi.org/10.1080/01431161.2016.1192304

Uddin, K., Matin, M.A., Meyer, F.J., 2019. Operational Flood Mapping Using Multi-Temporal Sentinel-1 SAR Images: A Case Study from Bangladesh. Remote Sensing 11 (13), 1581. https://doi.org/10.3390/rs11131581

Wei, D., Gephart, J.A., Iizumi, T., Ramankutty, N., Davis, K.F., 2023. Key role of planted and harvested area fluctuations in US crop production shocks. Nature Sustainability 6 (10), 1177–1185. https://doi.org/10.1038/s41893-023-01152-2

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., et al., 2022. ESA WorldCover 10 m 2021 v200. Zenodo. https://doi.org/10.5281/zenodo.7254221

# Appendix A. Supplementary tables

Table A.1. Other variants of the area effect, reported without a pass rule. The Poisson model (Santos Silva and Tenreyro, 2006) gives more weight to large districts.

| Variant | Flood record | Area effect (%) | Clustered p | Driscoll–Kraay p |
|--------------------------|-------------|----------|-------------|------------------|
| Division-by-year effects | Sentinel-1 | −20.4 | 0.012 | < 0.001 |
| Division-by-year effects | JRC | −6.6 | 0.003 | 0.042 |
| District linear trends | Sentinel-1 | −15.7 | 0.002 | 0.018 |
| District linear trends | JRC | −5.0 | 0.107 | 0.162 |
| Poisson model | Sentinel-1 | −10.9 | < 0.001 | – |
| Poisson model | JRC | −5.3 | < 0.001 | – |
| Districts under 15,000 ha left out | Sentinel-1 | −13.8 | 0.001 | 0.004 |
| Districts under 15,000 ha left out | JRC | −6.2 | 0.012 | 0.073 |
| Leave out Chandpur | Sentinel-1 | −21.3 | 0.023 | < 0.001 |
| Leave out Chandpur | JRC | −4.4 | 0.106 | 0.152 |
| Flash flood only, 2015–2025 | Sentinel-1 | −20.7 | 0.018 | < 0.001 |
| Water threshold −16 dB | Sentinel-1 | −20.0 | 0.035 | < 0.001 |
| Water threshold −20 dB | Sentinel-1 | −28.8 | 0.001 | < 0.001 |
| Neighbours' flood, own effect | Sentinel-1 | −21.5 | 0.049 | < 0.001 |
| Neighbours' flood, own effect | JRC | −6.2 | 0.013 | 0.052 |
| Neighbours' flood, spillover | Sentinel-1 | −0.3 | 0.972 | 0.908 |
| Neighbours' flood, spillover | JRC | 3.3 | 0.257 | 0.386 |

Table A.2. National area of the yearly Boro mask, against BBS and published maps.

| Harvest year | Yearly mask (million ha) | BBS harvested area (million ha) | Shew and Ghosh (2019) (million ha) |
|-----------|------------|-------------|------------|
| 2011 | 3.42 | 4.77 | – |
| 2012 | 3.37 | 4.81 | – |
| 2013 | 3.83 | 4.76 | – |
| 2014 | 3.79 | 4.79 | 4.29 |
| 2015 | 4.24 | 4.84 | 4.42 |
| 2016 | 4.16 | 4.77 | 4.64 |
| 2017 | 4.12 | 4.48 | 4.12 |
| 2018 | 3.65 | 4.86 | 4.41 |
| 2019 | 4.47 | 4.79 | – |
| 2020 | 4.18 | 4.76 | – |
| 2021 | 4.17 | 4.79 | – |
| 2022 | 3.73 | 4.82 | – |
| 2023 | 3.95 | 4.85 | – |
| 2024 | 3.36 | 4.88 | – |
| 2025 | 4.45 | 4.89 | – |

Table A.3. The 18 data checks run before any model, from `outputs/validation_variables.csv`.

| Check | Observed | Result |
|--------------------------|--------------------------|----------|
| Gold panel matches the archived panel | 5cbaeb1edaef | Pass |
| Boro mask and crop loss: 64 districts in every year, no missing value | 960 rows | Pass |
| Weather: 64 districts in every year, no missing value | 960 rows | Pass |
| NDVI windows: 64 districts in every year, no missing value | 960 rows | Pass |
| Sentinel-1 scene counts: 64 districts in every year, no missing value | 704 rows | Pass |
| Sentinel-1 flood: 64 districts in every year, no missing value | 704 rows | Pass |
| JRC flood: 64 districts in every year, no missing value | 704 rows | Pass |
| Sentinel-1 thresholds: 64 districts in every year, no missing value | 704 rows | Pass |
| S1_flash_wd reproduces the panel's s1_flash_flood | max difference 1.11e-16, n=704 | Pass |
| S1_monsoon_wd reproduces the panel's s1_monsoon_flood | max difference 1.11e-16, n=640 | Pass |
| Jrc_flash_wd reproduces the panel's jrc_flash_flood | max difference 4.08e-10, n=704 | Pass |
| Jrc_monsoon_wd reproduces the panel's jrc_monsoon_flood | max difference 7.75e-10, n=704 | Pass |
| All fractions lie between 0 and 1 | 0.0000 to 1.0000 | Pass |
| Boro land never exceeds district area | largest share 0.74 | Pass |
| Sentinel-1 scenes exist in every district-year | minimum 5 in Apr-May | Pass |
| Satellite crop loss is observed on most Boro land | minimum valid share 0.67 | Pass |
| Yearly mask agrees with BBS area between districts | r = 0.914 | Pass |
| Stable mask agrees with BBS area between districts | r = 0.909 | Pass |

# Appendix B. Literature search

The search used one database, OpenAlex, on 31 October 2026, with the 52 search strings in Table B.1 and up to 40 records for each of the first 38 strings and 25 for the other 14. This gave 1,870 records, of which 1,383 were unique and 1,232 had an abstract. Screening used titles and abstracts: 421 records concerned Bangladesh or the haor and crops, 182 of them also concerned flooding, and 5 of those also mentioned cultivated or harvested area. Hassan (2019) was found by a separate web search. The core list of 57 papers was confirmed on Crossref. Journals published in Bangladesh are indexed less completely, and keyword screening can miss papers that use other words. The search scripts are in the repository.

Table B.1. Search strings by theme.

| Theme | Search strings | Records retrieved |
|--------------------------|--------------------------|-------------|
| Haor and Boro flooding | haor flash flood Boro rice; flash flood rice Bangladesh damage; Boro rice flood loss Bangladesh; haor basin remote sensing flood; 2017 flash flood Bangladesh haor; haor agriculture climate vulnerability; pre-monsoon flood Bangladesh rice; flood damage rice production Bangladesh district | 320 |
| Area versus yield | harvested area yield decomposition extreme weather crop production; flood impact crop production harvested area yield; weather shocks harvested area abandonment panel; extreme weather disasters global crop production; climate variability harvested area versus yield; flood crop loss panel fixed effects; crop yield harvested area response flood | 280 |
| Climate and yield in Bangladesh | climate change rice yield Bangladesh panel; Boro rice yield temperature Bangladesh; heat stress Boro rice Bangladesh; district level rice yield climate Bangladesh; climate rice production Bangladesh econometric | 200 |
| Flood mapping and crop loss from satellites | Sentinel-1 flood mapping Bangladesh; Sentinel-1 flood rice damage assessment; satellite crop loss flood NDVI change rice; remote sensing flood damage cropland rice; JRC Global Surface Water flood agriculture; SAR water threshold flood mapping rice paddy | 240 |
| Vulnerability indices and spatial methods | agricultural vulnerability index Bangladesh; composite indicator uncertainty sensitivity analysis; social vulnerability index uncertainty sensitivity; spatial autocorrelation crop yield LISA; climate vulnerability exposure sensitivity adaptive capacity agriculture Bangladesh | 200 |
| NDVI and yield | NDVI rice yield Bangladesh; NDVI yield relationship within field interannual irrigated rice; satellite crop yield estimation smallholder district statistics | 120 |
| Adaptation | short duration Boro rice variety flash flood haor; flood early warning haor farmers; crop insurance flood Bangladesh rice; submergence tolerant rice Bangladesh adoption | 160 |
| Targeted search | effects of flood on agricultural productivity in Bangladesh; satellites self-reports submersion floods Bangladesh; flood rice Bangladesh difference-in-differences; flood exposure agricultural production Bangladesh district panel; Boro production loss 2017 flash flood district statistics; flash flood early monsoon haor rice production estimate; Boro rice mapping Bangladesh satellite annual; rice area mapping Bangladesh Sentinel-1 MODIS; annual paddy rice map South Asia 10 m; pre-monsoon flood Meghna basin trend haor frequency; flood positive effect dry season rice residual moisture sediment Bangladesh; India district flood rice yield panel; flood harvested area rice Vietnam Thailand Philippines panel; typhoon rice production harvested area panel | 350 |

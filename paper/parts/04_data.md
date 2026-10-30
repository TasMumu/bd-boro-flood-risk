# 3. Data

## 3.1 Panel

The analysis uses the Gold panel of @mumu2026: {{ f(D['n_panel'], 0) }} district-years for all 64 districts and harvest years 2011–2025, where harvest year t is the crop sown in November of t−1 and harvested in April–May of t. Boro harvested area, yield and production are values printed in the BBS yearbooks, each with its edition and page, and no value is modelled or filled. Weather comes from ERA5-Land [@munozsabater2021]. Flood fractions come from the monthly surface water record of the Joint Research Centre (JRC) [@pekel2016] and from Sentinel-1 radar [@torres2012], and are kept as separate records. Table 2 lists the sources. The seven haor districts are Sunamganj, Habiganj, Netrokona, Kishoreganj, Sylhet, Moulvibazar and Brahmanbaria, a list fixed before the models were run. They produced {{ f(100 * P[P.district.isin(HAOR)].production_t.sum() / P.production_t.sum(), 1) }} % of Boro over the period.

Table 2. Data sources.

{{ table_sources }}

Flash flood is the share of district area under water in April or May of year t and not in January–March of t. Monsoon flood is the share under water in June–October of t−1 and not in January–March of t−1. JRC ends in December 2021 and Sentinel-1 begins in October 2014, so the main models use harvest years 2011–2021 for JRC and 2016–2025 for Sentinel-1.

## 3.2 New variables

New variables were computed in Google Earth Engine [@gorelick2017]. Every extract was tested for completeness, and no value was filled.

**Boro mask.** Published Boro maps cover only 2017 [@singha2019] or 2014–2018 [@shew2019], so we built a consistent mask for the whole period, following earlier MODIS mapping of Boro [@mosleh2014]. Using the normalised difference vegetation index (NDVI) from MODIS [@didan2021] on WorldCover cropland [@zanaga2022], a pixel is counted as Boro land in year t if its peak NDVI from February to mid-March reaches 0.50 and has risen by at least 0.20 since December–January. These images all end before the flood window, so the mask describes the crop before any loss. Area changes little for thresholds between 0.40 and 0.50. A stable mask, covering land that meets the rule in at least five of the 15 years, is used for flood fractions on Boro land. It covers {{ f(D['stable_mask_mha'], 2) }} million ha, against about 4.8 million ha harvested in BBS statistics, and agrees with BBS area between districts (r = {{ f(D['r_mask_stable'], 2) }}). The yearly mask is noisier (Table A.2) and is used only to define the land on which crop loss is measured.

**Satellite crop loss.** Following the logic of the Disaster Vegetation Damage Index [@rahman2020b], we took the change in NDVI from the pre-flood peak to the two composites starting in April, and subtracted the same pixel's median change over all years. Loss is the share of Boro land with an anomaly below −0.20. This measure uses no BBS data.

**Flood timing.** The flash-flood window was split into early and late parts against a January–February baseline, so that water from a March flood is not treated as dry-season water. For Sentinel-1, early is 15 March to 15 April and late is 16 April to 15 May, each from two half-month medians. JRC is monthly, so early is March–April and late is May.

**Other variables.** We also computed flood fractions at water thresholds of −16 and −20 dB, Sentinel-1 scene counts, hot days above 35 °C from mid-March to April [@jagadish2007], and days below 20 °C from mid-February to March. The cold threshold is provisional. Adaptive capacity is not covered, because no published district series was assembled, and nothing was estimated in its place.

## 3.3 Data checks

All {{ D['checks'] }} checks passed. The new code recomputed the published flood fractions of the panel, and the largest difference was below 10^−9^, so the variants are computed by verified code. The panel's checksum matches the archived version.

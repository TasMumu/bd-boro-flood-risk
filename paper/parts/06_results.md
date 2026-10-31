# 5. Results

## 5.1 Few events carry the flash-flood estimates

Flash floods are concentrated in a few places and years (Fig. 1, Fig. 2). Sentinel-1 has 704 district-years but only about {{ f(1 / ((lambda d: ((d / d.sum()) ** 2).sum())((lambda x: (x - x.groupby(P.district).transform('mean') - x.groupby(P.harvest_year).transform('mean') + x.mean()) ** 2)(P.s1_flash_flood.dropna())) ), 0) }} effective observations (Table 3). Effective observations are the inverse of the sum of squared shares of the flood variation left after removing district and year means, so they fall as a few district-years dominate. Seven districts carry nearly all the variation, and two years carry most of it, so the flash-flood analysis is really a study of a few events. Monsoon floods are spread much more widely. Sentinel-1 also has a coverage break: scenes per haor district more than double after 2016 (Fig. 2b), which matters because 2016 is a key flood year.

Fig. 1. Flash flood and satellite crop loss. Panel (a) shows mean flash flood on Boro land. Panel (b) shows the share of Boro land with a sharp fall in greenness in 2017.

![](figures/fig1_map.png){width=100%}

Fig. 2. How few events carry the estimates. Panel (a) shows each year's share of flash-flood variation after removing district and year means. Panel (b) shows Sentinel-1 scenes per haor district.

![](figures/fig2_design.png){width=100%}

Table 3. Where the flood variation comes from. Effective observations are defined in the text.

{{ table_design }}

## 5.2 Main flood models

With Sentinel-1, 10 more points of flash flood went with {{ f(abs(SA.pct)) }} % less harvested area and {{ f(abs(SPR.pct)) }} % less production, significant under all four methods, and with no detectable change in yield ({{ f(SY.pct) }} %) (Table 4). With JRC the area effect was much smaller ({{ f(JA.pct) }} %) and not significant under any method. Yield rose slightly with JRC ({{ f(JY.pct) }} %), significant under Driscoll–Kraay errors and randomisation inference only.

Table 4. Flash-flood effects per 10 points of district area, with p-values from four methods.

{{ table_main }}

The yield interval was narrow but just exceeded the ±2 % bound: {{ f(ci('s1', 'dk')[0]) }} to {{ f(ci('s1', 'dk')[1]) }} % for Sentinel-1 under Driscoll–Kraay errors, and up to {{ f(ci('jrc', 'cluster')[1]) }} % for JRC under clustered errors. So the planned test for a negligible yield effect was not met. Yield effects were small, and no method gave a sizeable negative one.

## 5.3 The 2017 flood

The year-by-year comparison shows why the two records differ (Fig. 3). In 2017, haor districts fell {{ f(abs(hy('Harvested area', 2017))) }} % in area and {{ f(abs(hy('Production', 2017))) }} % in production relative to other districts and to 2015, while yield changed by {{ f(hy('Yield', 2017)) }} %. Area recovered at once, to {{ f(hy('Harvested area', 2018)) }} % in 2018. The other large floods left no such mark: haor area was {{ f(hy('Harvested area', 2016)) }} % in 2016 and {{ f(hy('Harvested area', 2022)) }} % in 2022. Differences before the floods reach {{ f(R['haor_pre_trend']['max_abs_pct']) }} %, so smaller movements should not be over-read.

Fig. 3. Haor districts against other districts, relative to 2015, on one shared scale. Flood years are shaded. Intervals are clustered by district and can be too narrow with few treated districts.

![](figures/fig3_by_year.png){width=100%}

Sunamganj shows the pattern most clearly: {{ f(P[(P.district == 'Sunamganj') & (P.harvest_year == 2016)].area_ha.iloc[0] / 1000, 0) }} thousand ha harvested in 2016, {{ f(P[(P.district == 'Sunamganj') & (P.harvest_year == 2017)].area_ha.iloc[0] / 1000, 0) }} thousand ha in 2017 and {{ f(P[(P.district == 'Sunamganj') & (P.harvest_year == 2018)].area_ha.iloc[0] / 1000, 0) }} thousand ha in 2018. Against the mean of 2015 and 2018, its area fell by {{ f(abs(E17.loc['Sunamganj', 'area_ha_chg_pct'])) }} % and its yield by {{ f(abs(E17.loc['Sunamganj', 'yield_t_ha_chg_pct'])) }} % (Table 5, Fig. 4).

Table 5. The 2017 flood in the most flooded districts. BBS changes are from the mean of 2015 and 2018.

{{ table_event }}

Fig. 4. The 2017 flood across all 64 districts. Panel (a) sets satellite crop loss against BBS harvested area. Panel (b) sets the flood against BBS yield, on the same scale.

![](figures/fig4_event_2017.png){width=100%}

Two non-haor districts stand out in Fig. 4a, with large changes in BBS area and almost no satellite loss. Patuakhali fell by {{ f(abs(E17.loc['Patuakhali', 'area_ha_chg_pct']), 0) }} %, but from a base of under 2,000 ha. Chandpur rose by {{ f(E17.loc['Chandpur', 'area_ha_chg_pct'], 0) }} %: its 2017 area is {{ f(P[(P.district == 'Chandpur') & (P.harvest_year == 2017)].area_ha.iloc[0], 0) }} ha, against {{ f(P[(P.district == 'Chandpur') & (P.harvest_year == 2015)].area_ha.iloc[0], 0) }} ha in 2015 and {{ f(P[(P.district == 'Chandpur') & (P.harvest_year == 2018)].area_ha.iloc[0], 0) }} ha in 2018. That value is as printed in the yearbook, and we found no flood or satellite explanation for it. Both cases show that BBS area can move for reasons other than flood, by as much as the flood signal.

Synthetic control gave the same pattern. The estimated 2017 area gaps were {{ f(sy('Harvested area', 'Sunamganj', 'gap_2017')) }} % in Sunamganj, {{ f(sy('Harvested area', 'Kishoreganj', 'gap_2017')) }} % in Kishoreganj, {{ f(sy('Harvested area', 'Sylhet', 'gap_2017')) }} % in Sylhet, {{ f(sy('Harvested area', 'Netrokona', 'gap_2017')) }} % in Netrokona and {{ f(sy('Harvested area', 'Habiganj', 'gap_2017')) }} % in Habiganj, while yield gaps stayed within {{ f(SYN[SYN.outcome == 'Yield'].gap_2017.abs().max()) }} % (Table 6). The planned test was not met: no gap ranked in the top 5 % relative to its pre-flood fit. With five years to match and many donors, the pre-flood fit is almost perfect, so this ratio is unstable. An exploratory test on the gap's size alone ranks Sunamganj at p = {{ f(sy('Harvested area', 'Sunamganj', 'gap_rank_p'), 3) }} and Kishoreganj at p = {{ f(sy('Harvested area', 'Kishoreganj', 'gap_rank_p'), 3) }}, and the other three above 0.1.

Table 6. Synthetic control for the five most flooded districts. Placebo rank p is the planned test.

{{ table_synth }}

## 5.4 Evidence independent of BBS

The satellite measure uses no BBS data, and it passed its planned test. Each 10 points of flood raised satellite crop loss by {{ f(100 * SAT['s1']['flood_to_loss']['b'], 1) }} points with Sentinel-1 (Driscoll–Kraay p = {{ pv(SAT['s1']['flood_to_loss']['p_dk']) }}) and {{ f(100 * SAT['jrc']['flood_to_loss']['b'], 1) }} points with JRC (p = {{ pv(SAT['jrc']['flood_to_loss']['p_dk']) }}), and satellite loss lowered BBS area (p = {{ pv(SAT['log_area']['p_dk']) }}) but not yield (p = {{ pv(SAT['log_yield']['p_dk']) }}). In 2017, satellite loss reached {{ f(100 * E17.loc['Sunamganj', 'loss_share'], 0) }} % of Boro land in Sunamganj and {{ f(100 * E17.loc['Sylhet', 'loss_share'], 0) }} % in Sylhet, and at most {{ f(100 * E17.drop(HAOR).loss_share.max(), 1) }} % outside the haor (Fig. 1b, Fig. 4a).

Published damage figures are also of the same order. Against the mean of 2015 and 2018, BBS shows a production loss of {{ f(RP['bbs_haor_loss_mt'], 2) }} million t in the seven haor districts in 2017, compared with 0.88 million t reported for the haor regions [@hossain2023]. For Sunamganj, BBS implies {{ f(RP['bbs_sunamganj_area_loss_ha'], 0) }} ha and {{ f(RP['bbs_sunamganj_prod_loss_t'], 0) }} t lost, compared with 149,224 ha affected and 393,855 t damaged in a published estimate [@mondal2021].

## 5.5 Checks and verdict

The required checks gave a mixed picture (Table 7, Fig. 5). Because the main Sentinel-1 sample starts in 2016, the planned check without 2015–2016 is the same model as leaving out 2016, so it is counted once. All leave-out checks passed for Sentinel-1, and the flood-after-harvest placebo passed in both records. Next year's flood, however, failed for Sentinel-1 ({{ f(chk("Next year's flash flood (placebo)", 'Sentinel-1').pct) }} %, clustered p = {{ pv(chk("Next year's flash flood (placebo)", 'Sentinel-1').p_cluster) }}), possibly because haor area was high in 2016, just before the 2017 flood. For JRC, the effect disappeared without 2017 ({{ f(chk('Leave out 2017', 'JRC').pct) }} %) or Sunamganj ({{ f(chk('Leave out Sunamganj', 'JRC').pct) }} %), and was not significant on rice land only. Most importantly, without both 2016 and 2017 no effect remained in either record ({{ f(chk('Leave out 2016 and 2017', 'Sentinel-1').pct) }} % and {{ f(chk('Leave out 2016 and 2017', 'JRC').pct) }} %). Flood size also mattered: only the largest group, 20 % or more of a district, showed clear losses ({{ f(bn('Sentinel-1', 'flash', 'Harvested area', '20+').pct) }} % with Sentinel-1, from {{ bn('Sentinel-1', 'flash', 'Harvested area', '20+').n_in_bin }} district-years, and {{ f(bn('JRC', 'flash', 'Harvested area', '20+').pct) }} % with JRC, from {{ bn('JRC', 'flash', 'Harvested area', '20+').n_in_bin }}; Fig. 6). The size of the Sentinel-1 estimate also partly reflects small districts. Leaving out the six districts with a small Boro base gave {{ f(chk('Districts under 15,000 ha left out', 'Sentinel-1').pct) }} % with Sentinel-1 and {{ f(chk('Districts under 15,000 ha left out', 'JRC').pct) }} % with JRC, and a Poisson model, which weights by area, gave {{ f(chk('Poisson model', 'Sentinel-1').pct) }} % and {{ f(chk('Poisson model', 'JRC').pct) }} % (Table A.1). The two records are closer in both cases.

Table 7. Required checks of the area effect. Effects are per 10 points of flood.

{{ table_checks }}

Fig. 5. How the flash-flood estimates hold up. Each row reruns the main model with one change. Intervals are 95 %, clustered by district. The shaded band marks ±2 %.

![](figures/fig5_checks.png){width=100%}

Fig. 6. Normal and extreme floods, against the group below 1 %. Intervals are 95 %, clustered by district. Under each label, n gives the district-years in the bin, Sentinel-1 first.

![](figures/fig6_bins.png){width=100%}

Under the plan's rule, the answer to Q1 is **{{ V['verdict'] }}**, not supported. The significance rule held for Sentinel-1 but not for JRC, {{ V['n_required_passed'] }} of {{ V['n_required'] }} required checks passed, and the planned synthetic-control test failed. Direction and design agreed throughout. For Q3, concentration in the haor could not be tested properly: outside it, Sentinel-1 flood reached 5 % in only {{ f(R['outside_haor']['s1_above_5']) }} % of district-years, so any slope there is an extrapolation, and no haor interaction survived false discovery rate correction.

## 5.6 Flood timing (exploratory)

Why did 2017 stand out? This analysis was added after the planned results were seen. Table 8 suggests that timing is the reason. In 2017, more water arrived early, while in 2016 most Sentinel-1 water came late. The planned early-window check had already brought the two records close together: {{ f(er('Sentinel-1', 'Harvested area', 'All years').pct) }} % with Sentinel-1 and {{ f(er('JRC', 'Harvested area', 'All years').pct) }} % with JRC per 10 points (Table 9). This is consistent with the JRC estimate in Table 4 being weak because its window mixes water before and after harvest.

This reading has clear limits. Without 2017 the early-window effect disappears or reverses in both records, so it rests on that one event. And satellite loss in 2016 ({{ f(TIM.loc[2016, 'loss_share']) }} %) did not match BBS, where area rose. NDVI also falls when fields are harvested early, so satellite loss cannot separate harvest from destruction.

Table 8. Flood timing in the haor districts. Flood and loss are mean shares; BBS area is from the year-by-year model.

{{ table_timing }}

Table 9. Early-window effects per 10 points (exploratory). RI is randomisation inference.

{{ table_early }}

## 5.7 Monsoon floods (Q2)

Monsoon floods gave no clear result (Table 10). JRC pointed to more area ({{ f(MJA.pct) }} % per 10 points) and Sentinel-1 to less ({{ f(MSA.pct) }} %), and neither was significant. With JRC, flooded years in every bin had higher yields than years below 1 % (Fig. 6a), consistent with earlier work [@banerjee2010; @asada2005], but Sentinel-1 showed nothing similar. The expected harm from extreme monsoon floods did not appear in either record. None of these tests survived correction.

Table 10. Monsoon-flood effects per 10 points of district area.

{{ table_monsoon }}

## 5.8 NDVI (Q4)

NDVI tracked differences between districts and the shared rise in yield, but not year-to-year departures within a district (Table 11). Over January–April, the correlation with yield was {{ f(NDVI.between.iloc[0], 2) }} between districts and {{ f(NDVI.within_district.iloc[0], 2) }} within districts, and fell to {{ f(NDVI.within_two_way.iloc[0], 2) }} once year effects were removed. No window gave a significant effect, including peak greenness [@mosleh2016], and the result did not depend on how much of a district is rice land (a correlation of {{ f(R['ndvi_purity'][0]['within_two_way'], 2) }} in districts with more rice land and {{ f(R['ndvi_purity'][1]['within_two_way'], 2) }} in those with less). NDVI-based yield estimates at national or division level [@mosleh2016; @alam2019] may therefore capture broad differences and trends, not shocks to a district.

Table 11. NDVI and Boro yield.

{{ table_ndvi }}

## 5.9 Risk index and spatial patterns (Q5)

The haor dominates the index: {{ XI['haor_in_top10'] }} of the top ten districts are in the haor, led by Sunamganj (Table 12, Fig. 7). Six districts with a mean Boro area below 15,000 ha are flagged, a threshold set after the first results: {{ ', '.join(XI['small_base'][:-1]) }} and {{ XI['small_base'][-1] }}. Their high ranks are not reliable. Hill districts such as Rangamati have so little rice land that their flood shares rest on few pixels, and Patuakhali and Barguna rank high because Boro expanded there from a very small base, which appears as instability but is not loss. Without these six, all {{ XI['haor_in_top10_large'] }} haor districts are in the top ten.

The ranking is not stable, however. Across {{ f(XI['combinations'], 0) }} combinations, the median correlation with the base ranking was {{ f(XI['spearman_median'], 2) }}, the median district stayed in its risk tier in {{ f(100 * XI['tier_stability_median'], 0) }} % of cases, and no district was in the top ten in at least 90 % of them.

Table 12. The ten highest-ranked districts, with rank range and stability across all combinations.

{{ table_top }}

Fig. 7. Risk tier and rank under all combinations. Hatched districts, starred in panel (b), have a small Boro base, so their high ranks are not reliable. Bars show the 5th to 95th percentile of rank, and dots the base ranking.

![](figures/fig7_index.png){width=100%}

Spatial clustering was clear (Table 13). Moran's I ranged from {{ f(SP.moran_i.min(), 2) }} to {{ f(SP.moran_i.max(), 2) }}, and {{ ', '.join(X['spatial']['hh_all_definitions'][:-1]) }} and {{ X['spatial']['hh_all_definitions'][-1] }} formed a high-risk cluster under all four neighbour definitions.

Table 13. Spatial clustering of the index under four neighbour definitions.

{{ table_spatial }}

A yield-only view gives a different picture. Sunamganj ranks {{ YV['sunamganj_rank_yield'] }}th of 64 on yield instability but {{ YV['sunamganj_rank_production'] }}rd on production instability, and the two rankings correlate at only {{ f(YV['spearman'], 2) }}.

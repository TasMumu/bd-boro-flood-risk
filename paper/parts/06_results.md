# 5. Results

## 5.1 Few events carry the flash-flood estimates

Flash floods are concentrated in a few places and years (Fig. 1, Fig. 2). Sentinel-1 has 704 district-years with flood data but only about {{ f(1 / ((lambda d: ((d / d.sum()) ** 2).sum())((lambda x: (x - x.groupby(P.district).transform('mean') - x.groupby(P.harvest_year).transform('mean') + x.mean()) ** 2)(P.s1_flash_flood.dropna())) ), 0) }} effective observations (Table 3). Effective observations are the inverse of the sum of squared shares of the flood variation left after removing district and year means, so they fall as a few district-years dominate. Seven districts carry nearly all the variation, and two years carry most of it, so the flash-flood analysis is really a study of a few events. Monsoon floods are spread much more widely. Sentinel-1 also has a coverage break: scenes per haor district more than double after 2016 (Fig. 2b), which matters because 2016 is a key flood year.

Fig. 1. Flash flood and satellite greenness loss. Panel (a) shows mean flash flood on Boro land. Panel (b) shows the share of Boro land with a sharp fall in greenness in 2017.

![](figures/fig1_map.png){width=100%}

Fig. 2. How few events carry the estimates. Panel (a) shows each year's share of flash-flood variation after removing district and year means. Panel (b) shows Sentinel-1 scenes per haor district.

![](figures/fig2_design.png){width=100%}

Table 3. Where the flood variation comes from. District-years are all available flood observations, before restricting to the years of each main model, so main models can have fewer (Table 4). Effective observations are defined in the text.

{{ table_design }}

## 5.2 Main flood models

With Sentinel-1, 10 more points of flash flood went with {{ f(abs(SA.pct)) }} % less harvested area and {{ f(abs(SPR.pct)) }} % less production, significant under all four methods, and with no detectable change in yield ({{ f(SY.pct) }} %) (Table 4). With JRC the area effect was much smaller ({{ f(JA.pct) }} %) and not significant under any method. Yield rose slightly with JRC ({{ f(JY.pct) }} %), significant under Driscoll–Kraay errors and randomisation inference only.

Table 4. Flash-flood effects per 10 points of district area, with p-values from four methods.

{{ table_main }}

The yield interval was narrow but just exceeded the ±2 % bound: {{ f(ci('s1', 'dk')[0]) }} to {{ f(ci('s1', 'dk')[1]) }} % for Sentinel-1 under Driscoll–Kraay errors, and up to {{ f(ci('jrc', 'cluster')[1]) }} % for JRC under clustered errors. So the planned test for a negligible yield effect was not met. Yield effects were small, and no method gave a sizeable negative one.

## 5.3 The 2017 flood

The year-by-year comparison shows why the two records differ (Fig. 3). In 2017, haor districts fell {{ f(abs(hy('Harvested area', 2017))) }} % in area and {{ f(abs(hy('Production', 2017))) }} % in production relative to other districts and to 2015, while yield changed by {{ f(hy('Yield', 2017)) }} %. Area recovered at once, to {{ f(hy('Harvested area', 2018)) }} % in 2018. The 2016 and 2022 flood years did not show a comparable decline in measured harvested area: haor harvested area was {{ f(hy('Harvested area', 2016)) }} % in 2016 and {{ f(hy('Harvested area', 2022)) }} % in 2022. Differences before the floods reach {{ f(R['haor_pre_trend']['max_abs_pct']) }} %, so smaller movements should not be over-read.

Fig. 3. Haor districts against other districts, relative to 2015, on one shared scale. Flood years are shaded. Intervals are clustered by district and can be too narrow with few treated districts.

![](figures/fig3_by_year.png){width=100%}

Sunamganj shows the pattern most clearly: {{ f(P[(P.district == 'Sunamganj') & (P.harvest_year == 2016)].area_ha.iloc[0] / 1000, 0) }} thousand ha harvested in 2016, {{ f(P[(P.district == 'Sunamganj') & (P.harvest_year == 2017)].area_ha.iloc[0] / 1000, 0) }} thousand ha in 2017 and {{ f(P[(P.district == 'Sunamganj') & (P.harvest_year == 2018)].area_ha.iloc[0] / 1000, 0) }} thousand ha in 2018. Against the mean of 2015 and 2018, its area fell by {{ f(abs(E17.loc['Sunamganj', 'area_ha_chg_pct'])) }} % and its yield by {{ f(abs(E17.loc['Sunamganj', 'yield_t_ha_chg_pct'])) }} % (Table 5, Fig. 4).

Table 5. The 2017 flood in the most flooded districts. BBS changes are from the mean of 2015 and 2018.

{{ table_event }}

Fig. 4. The 2017 flood across all 64 districts. Panel (a) sets satellite greenness loss against BBS harvested area. Panel (b) sets the flood against BBS yield, on the same scale.

![](figures/fig4_event_2017.png){width=100%}

Two non-haor districts stand out in Fig. 4a, with large changes in BBS area and almost no satellite loss. Patuakhali fell by {{ f(abs(E17.loc['Patuakhali', 'area_ha_chg_pct']), 0) }} %, but from a base of under 2,000 ha. Chandpur rose by {{ f(E17.loc['Chandpur', 'area_ha_chg_pct'], 0) }} %: its 2017 area is {{ f(P[(P.district == 'Chandpur') & (P.harvest_year == 2017)].area_ha.iloc[0], 0) }} ha, against {{ f(P[(P.district == 'Chandpur') & (P.harvest_year == 2015)].area_ha.iloc[0], 0) }} ha in 2015 and {{ f(P[(P.district == 'Chandpur') & (P.harvest_year == 2018)].area_ha.iloc[0], 0) }} ha in 2018. This appears to be a duplication in the source: the yearbooks print the same {{ f(CH.loc['HYV', 'second_year_acres'], 0) }} acres for both HYV and hybrid Boro [@bbs2018, pp. 72–74], while hybrid area was {{ f(CH.loc['Hybrid', 'first_year_acres'], 0) }} acres the year before and {{ f(CH2.loc['Hybrid', 'second_year_acres'], 0) }} acres the year after. We keep the value as printed, and leaving out Chandpur changes little (Table A.1). None of the framework's checks detected it, because it is repeated in two editions and included in the national total; a check on year-to-year jumps, or on the HYV and hybrid components, would flag it. Both districts show that BBS area can move for reasons other than flood, by as much as the flood signal.

Synthetic control gave the same pattern. The estimated 2017 area gaps were {{ f(sy('Harvested area', 'Sunamganj', 'gap_2017')) }} % in Sunamganj, {{ f(sy('Harvested area', 'Kishoreganj', 'gap_2017')) }} % in Kishoreganj, {{ f(sy('Harvested area', 'Sylhet', 'gap_2017')) }} % in Sylhet, {{ f(sy('Harvested area', 'Netrokona', 'gap_2017')) }} % in Netrokona and {{ f(sy('Harvested area', 'Habiganj', 'gap_2017')) }} % in Habiganj, while yield gaps stayed within {{ f(SYN[SYN.outcome == 'Yield'].gap_2017.abs().max()) }} % (Table 6). The planned test was not met: no gap ranked in the top 5 % relative to its pre-flood fit. With five years to match and many donors, the pre-flood fit is almost perfect, so this ratio is unstable. An exploratory test on the gap's size alone ranks Sunamganj at p = {{ f(sy('Harvested area', 'Sunamganj', 'gap_rank_p'), 3) }} and Kishoreganj at p = {{ f(sy('Harvested area', 'Kishoreganj', 'gap_rank_p'), 3) }}, and the other three above 0.1.

Table 6. Synthetic control for the five most flooded districts. Placebo rank p is the planned test.

{{ table_synth }}

## 5.4 Other evidence on the 2017 loss

BBS's own reports show how the loss was recorded. The yearbook for 2016–17 states that flash flood fully damaged Boro on 296,701 ha [@bbs2018, p. 68], and its national Boro area fell by {{ f(NATA[2016] - NATA[2017], 0) }} ha from the year before. The same report attributes a higher yield to management. Its damage table for floods in March and April (Table 4.2.11, p. 349) lists six haor districts (Table 7), where the reported damaged area is close to the fall in BBS harvested area, and its production loss of {{ f(DMG.loc[(2017, 'Bangladesh'), 'loss_t'], 0) }} t is close to the 0.88 million t in the literature [@hossain2023]. These reports come from the same agency, so they do not independently confirm the area series, but they show that in 2017 destroyed crop was recorded as lost area and not as lower yield. For the 2016 flood, BBS reported far less: a production loss of {{ f(DMG.loc[(2016, 'Bangladesh'), 'loss_t'], 0) }} t, with {{ f(DMG.loc[(2016, 'Bangladesh'), 'total_ha'], 0) }} ha damaged in its table (Table 4.2.10, p. 348 of the same yearbook) and 40,198 ha fully damaged in its crop report [@bbs2017, p. 68]. That fits the absence of a fall in area in 2016. For 2022 it reported Boro damage only in Netrokona: {{ f(DMG.loc[(2022, 'Bangladesh'), 'total_ha'], 0) }} ha and {{ f(DMG.loc[(2022, 'Bangladesh'), 'loss_t'], 0) }} t [@bbs2023, Table 4.2.8, p. 422]. So the two flood years without a fall in harvested area are also years in which BBS reported little Boro damage. Even so, Sunamganj's reported damage in 2016 ({{ f(DMG.loc[(2016, 'Sunamganj'), 'total_ha'], 0) }} ha) exceeds its fall in harvested area that year, so reported damage does not always appear in the area series.

Table 7. BBS reported damage and the fall in BBS harvested area and production in 2017, against the mean of 2015 and 2018. The last row gives the damage totals printed in the yearbook. The printed district losses add to {{ f(DMG.loc[2017].drop('Bangladesh').loss_t.sum(), 0) }} t, and the areas above add to {{ f(DMG.loc[2017].drop('Bangladesh').total_ha.round().sum(), 0) }} ha after rounding.

{{ table_damage }}

The satellite measure uses no BBS data, and it passed its planned test. Each 10 points of flood raised satellite greenness loss by {{ f(100 * SAT['s1']['flood_to_loss']['b'], 1) }} points with Sentinel-1 (Driscoll–Kraay p = {{ pv(SAT['s1']['flood_to_loss']['p_dk']) }}) and {{ f(100 * SAT['jrc']['flood_to_loss']['b'], 1) }} points with JRC (p = {{ pv(SAT['jrc']['flood_to_loss']['p_dk']) }}), and greenness loss lowered BBS harvested area (p = {{ pv(SAT['log_area']['p_dk']) }}) but not yield (p = {{ pv(SAT['log_yield']['p_dk']) }}). In 2017, greenness loss reached {{ f(100 * E17.loc['Sunamganj', 'loss_share'], 0) }} % of Boro land in Sunamganj and {{ f(100 * E17.loc['Sylhet', 'loss_share'], 0) }} % in Sylhet, and at most {{ f(100 * E17.drop(HAOR).loss_share.max(), 1) }} % outside the haor (Fig. 1b, Fig. 4a). This supports the location and scale of the loss, but it does not prove that every flagged pixel was flood-damaged, and the 2016 mismatch (Section 5.6) limits its use as a general measure of crop loss.

Published damage figures are of the same order, although areas and definitions differ, so these comparisons are of scale only. Against the mean of 2015 and 2018, the BBS series shows a production loss of {{ f(RP['bbs_haor_loss_mt'], 2) }} million t in the seven haor districts in 2017, compared with 0.88 million t reported for the haor regions [@hossain2023]. For Sunamganj, it implies {{ f(RP['bbs_sunamganj_area_loss_ha'], 0) }} ha and {{ f(RP['bbs_sunamganj_prod_loss_t'], 0) }} t lost, compared with 149,224 ha affected and 393,855 t damaged in a published estimate [@mondal2021].

## 5.5 Checks and verdict

The required checks gave a mixed picture (Table 8, Fig. 5). Because the main Sentinel-1 sample starts in 2016, the planned check without 2015–2016 is the same model as leaving out 2016, so it is counted once. All leave-out checks passed for Sentinel-1, and the flood-after-harvest placebo passed in both records. Next year's flood, however, failed for Sentinel-1 ({{ f(chk("Next year's flash flood (placebo)", 'Sentinel-1').pct) }} %, clustered p = {{ pv(chk("Next year's flash flood (placebo)", 'Sentinel-1').p_cluster) }}), possibly because haor area was high in 2016, just before the 2017 flood. For JRC, the effect disappeared without 2017 ({{ f(chk('Leave out 2017', 'JRC').pct) }} %) or Sunamganj ({{ f(chk('Leave out Sunamganj', 'JRC').pct) }} %), and was not significant on rice land only. Most importantly, the estimated effect was close to zero in both records when 2016 and 2017 were both excluded ({{ f(chk('Leave out 2016 and 2017', 'Sentinel-1').pct) }} % and {{ f(chk('Leave out 2016 and 2017', 'JRC').pct) }} %). Flood size also mattered: only the largest group, 20 % or more of a district, showed clear losses ({{ f(bn('Sentinel-1', 'flash', 'Harvested area', '20+').pct) }} % with Sentinel-1, from {{ bn('Sentinel-1', 'flash', 'Harvested area', '20+').n_in_bin }} district-years, and {{ f(bn('JRC', 'flash', 'Harvested area', '20+').pct) }} % with JRC, from {{ bn('JRC', 'flash', 'Harvested area', '20+').n_in_bin }}; Fig. 6). The size of the Sentinel-1 estimate also partly reflects small districts. Leaving out the six districts with a small Boro base gave {{ f(chk('Districts under 15,000 ha left out', 'Sentinel-1').pct) }} % with Sentinel-1 and {{ f(chk('Districts under 15,000 ha left out', 'JRC').pct) }} % with JRC, and a Poisson model, which weights by area, gave {{ f(chk('Poisson model', 'Sentinel-1').pct) }} % and {{ f(chk('Poisson model', 'JRC').pct) }} % (Table A.1). The two records are closer in both cases.

Table A.4 summarises the required checks. The JRC failures matter most for the general claim, because they show that its estimate rests on one event and one district. The rice-only JRC estimate weakened because, on rice land, flood in Sylhet in 2017 ({{ f(100 * P[(P.district == 'Sylhet') & (P.harvest_year == 2017)].jrc_flash_boro.iloc[0], 0) }} %) matched that in Sunamganj ({{ f(100 * P[(P.district == 'Sunamganj') & (P.harvest_year == 2017)].jrc_flash_boro.iloc[0], 0) }} %), while Sylhet's harvested area fell far less (Table 5).

Table 8. Required checks of the harvested-area effect, per 10 points of flood. Pass or fail follows the criterion for each check in Section 4.5, and does not indicate significance under every estimator.

{{ table_checks }}

Fig. 5. How the flash-flood estimates hold up. Each row reruns the main model with one change. Intervals are 95 %, clustered by district. The shaded band marks ±2 %.

![](figures/fig5_checks.png){width=100%}

Fig. 6. Normal and extreme floods, against the group below 1 %. Intervals are 95 %, clustered by district. Under each label, n gives the district-years in the bin, Sentinel-1 first.

![](figures/fig6_bins.png){width=100%}

Under the plan's rule, the evidence on Q1 is **{{ V['verdict'] }}** and does not establish a general relationship. The significance rule held for Sentinel-1 but not for JRC, {{ V['n_required_passed'] }} of {{ V['n_required'] }} required checks passed, and the planned synthetic-control test failed. Direction and design agreed throughout. For Q3, concentration in the haor could not be tested properly: outside it, Sentinel-1 flood reached 5 % in only {{ f(R['outside_haor']['s1_above_5']) }} % of district-years, so any slope there is an extrapolation, and no haor interaction survived false discovery rate correction.

## 5.6 Flood timing (exploratory)

Why did 2017 stand out? This analysis was added after the planned results were seen, and it offers a hypothesis for future work, not an established explanation. Table 9 suggests that timing is one possible reason. In 2017, more water arrived early, while in 2016 most Sentinel-1 water came late, and BBS dates the 2017 damage to March and April. The planned early-window check had already brought the two records close together: {{ f(er('Sentinel-1', 'Harvested area', 'All years').pct) }} % with Sentinel-1 and {{ f(er('JRC', 'Harvested area', 'All years').pct) }} % with JRC per 10 points (Table 10). This is consistent with the JRC estimate in Table 4 being weak because its window mixes water before and after harvest.

This reading has clear limits. Without 2017 the early-window effect disappears or reverses in both records, so it rests on that one event. And greenness loss in 2016 ({{ f(TIM.loc[2016, 'loss_share']) }} %) did not match BBS, where harvested area rose. NDVI also falls when fields are harvested early, so this measure cannot separate harvest from destruction.

Table 9. Flood timing in the haor districts (exploratory). Flood and greenness loss are mean shares; BBS harvested area is from the year-by-year model.

{{ table_timing }}

Table 10. Early-window effects per 10 points (exploratory). RI is randomisation inference.

{{ table_early }}

## 5.7 Monsoon floods (Q2)

Monsoon floods gave no clear result (Table 11). JRC pointed to more area ({{ f(MJA.pct) }} % per 10 points) and Sentinel-1 to less ({{ f(MSA.pct) }} %), and neither was significant. With JRC, flooded years in every bin had higher yields than years below 1 % (Fig. 6a), consistent with earlier work [@banerjee2010; @asada2005], but Sentinel-1 showed nothing similar. The expected harm from extreme monsoon floods did not appear in either record. None of these tests survived correction.

Table 11. Monsoon-flood effects per 10 points of district area.

{{ table_monsoon }}

## 5.8 NDVI (Q4)

NDVI tracked differences between districts and the shared rise in yield, but not year-to-year departures within a district (Table 12). Over January–April, the correlation with yield was {{ f(NDVI.between.iloc[0], 2) }} between districts and {{ f(NDVI.within_district.iloc[0], 2) }} within districts, and fell to {{ f(NDVI.within_two_way.iloc[0], 2) }} once year effects were removed. No window gave a significant effect, including peak greenness [@mosleh2016], and the result did not depend on how much of a district is rice land (a correlation of {{ f(R['ndvi_purity'][0]['within_two_way'], 2) }} in districts with more rice land and {{ f(R['ndvi_purity'][1]['within_two_way'], 2) }} in those with less). NDVI-based yield estimates at national or division level [@mosleh2016; @alam2019] may therefore capture broad differences and trends, not shocks to a district.

Table 12. NDVI and Boro yield.

{{ table_ndvi }}

## 5.9 Risk index and spatial patterns (Q5)

Haor districts dominate the highest-risk positions in the base index: {{ XI['haor_in_top10'] }} of the top ten are in the haor, led by Sunamganj (Table 13, Fig. 7). The index is a screening tool, and its ranks are not precise. Six districts with a mean Boro area below 15,000 ha are flagged, a threshold set after the first results: {{ ', '.join(XI['small_base'][:-1]) }} and {{ XI['small_base'][-1] }}. Their high ranks are not reliable. Hill districts such as Rangamati have so little rice land that their flood shares rest on few pixels, and Patuakhali and Barguna rank high because Boro expanded there from a very small base, which appears as instability but is not loss. Without these six, all {{ XI['haor_in_top10_large'] }} haor districts are in the top ten.

The ranking is not stable, however. Across {{ f(XI['combinations'], 0) }} combinations, the median correlation with the base ranking was {{ f(XI['spearman_median'], 2) }}, the median district stayed in its risk tier in {{ f(100 * XI['tier_stability_median'], 0) }} % of cases, and no district was in the top ten in at least 90 % of them.

Table 13. The ten highest-ranked districts, with rank range and stability across all combinations.

{{ table_top }}

Fig. 7. Risk tier and rank under all combinations. Hatched districts, starred in panel (b), have a small Boro base, so their high ranks are not reliable. Bars show the 5th to 95th percentile of rank, and dots the base ranking.

![](figures/fig7_index.png){width=100%}

Spatial clustering was clear (Table 14). Moran's I ranged from {{ f(SP.moran_i.min(), 2) }} to {{ f(SP.moran_i.max(), 2) }}, and {{ ', '.join(X['spatial']['hh_all_definitions'][:-1]) }} and {{ X['spatial']['hh_all_definitions'][-1] }} formed a high-risk cluster under all four neighbour definitions before correction. After false discovery rate correction, {{ ', '.join(FDR_ALL[:-1]) }} and {{ FDR_ALL[-1] }} remained under all four, and Moulvibazar under three.

Table 14. Spatial clustering of the index under four neighbour definitions.

{{ table_spatial }}

A yield-only view gives a different picture. Sunamganj ranks {{ YV['sunamganj_rank_yield'] }}th of 64 on yield instability but {{ YV['sunamganj_rank_production'] }}rd on production instability, and the two rankings correlate at only {{ f(YV['spearman'], 2) }}.

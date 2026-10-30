# Paper 2 literature review

Completed 31 October 2026. Step 2 of the analysis plan.

## 1. Result

**The gap looks real, with one paper still to be checked.** No study found so far
uses a multi-year district panel with satellite flood data to split Boro
flash-flood losses into harvested area and yield.

This rests on titles and abstracts, not full texts. One recent close study,
Rahman et al. (2025), is behind a paywall. Its partial public abstract points to
monsoon floods and overall land and production losses, not haor flash floods, so
it probably does not close the gap. The claim stays provisional until the full
text is read (Section 6).

The review also sharpens the paper's argument. Recent global work reports flood
damage as yield loss, while Bangladesh's statistics may record the same damage
as lost harvested area. Where the loss appears could depend on how the statistics
are collected, which is the point worth making.

## 2. How the search was done

| Stage | Records |
|---|---|
| Queries in OpenAlex (38 by theme, 14 targeted) | 52 |
| Records retrieved | 1,870 |
| Unique records | 1,383 |
| With an abstract | 1,232 |
| About Bangladesh or the haor, and crops | 421 |
| And about flooding | 182 |
| And mentioning cultivated or harvested area | 5 |

Three of those five are relevant: Asada et al. (2005), Banerjee (2010) and Amin et al.
(2015). The other two concern flood forecasts and a household survey on farm
practices. Hassan (2019), a thesis, did not appear in OpenAlex and came from an
earlier web search.

The core list has 57 papers, each confirmed on Crossref. Of these, 40 were read at
abstract level, and 17 are listed by title only, mostly standard methods references.
Full details are in `core_papers.csv`, and every step can be repeated with the
scripts in this folder.

**Limits of the search.** It uses one database, and journals published in
Bangladesh are indexed less completely. Keyword screening can miss papers whose
abstracts use other words, and 151 records had no abstract to screen.

## 3. What is known

**Flash floods in the haor.** Boro in the haor is exposed to early flash floods
just before harvest (Kamruzzaman and Shaw, 2018). The 2017 flood began on 27 March
(Ahmed et al., 2017), and floods are described as typically coming in the first two
weeks of April (Hossain et al., 2023). Cold at the reproductive stage and flash
flood at maturity are the two main threats (Rashid and Yasmeen, 2018). Evidence is
mostly single-event or local: satellite mapping of the 2017 damage (Ahmed et al.,
2017), household surveys (Dey et al., 2021; Ahmed, 2024) and small area
studies (Khan et al., 2012; Mondal et al., 2021).

**Floods and rice in Bangladesh.** Floods are not simply harmful. Banerjee (2010)
found higher cultivated area and productivity in more flood-prone districts in
1978–2000, with yield falling in extreme floods and rising in normal floods
and in the months after. Asada et al. (2005) reports that Boro production rose after the
1988 and 1998 floods, helped by residual water, while Aman fell through both area
and yield. Hassan (2019) found meaningful Boro production effects but no meaningful
yield results. Guiteras et al. (2015) show that rainfall and self-reports are weak
proxies for true flood exposure, which supports using satellite data.

**Climate and yield in Bangladesh.** Most studies focus on yield, using regions,
stations or national series (Sarker et al., 2014; Hasan et al., 2016; Rahman
et al., 2017). Amin et al. (2015) is the clearest study of both yield and cropping
area, but it uses a national time series and climate variables, not floods.

**Area and yield as separate channels.** Findings differ by setting, so no general
rule can be assumed:

| Study | Setting | Finding |
|---|---|---|
| Lesk et al. (2016) | Global, national cereals, 1964–2007 | Droughts cut area and yield, heat cut yield, and no effect of floods could be identified in national data |
| Li et al. (2025) | Global rice, 1980–2015 | Submergence for over a week reduces annual yield by 4.3 % |
| Cui (2020) | US maize and soy | Harvested ratios fall above 35 °C; ignoring them misjudges losses by over 10 % |
| Obembe et al. (2021) | Kansas wheat | Losses come from yield, not abandonment |
| Wei and Davis (2022, preprint) | US maize | Area-related disruptions explain at least as much instability as yield |
| Blanc and Strobl (2016) | Philippines, typhoons | Rice-field exposure in a spatial panel shows production loss |

**Satellite evidence of crop loss.** Remote sensing of flood crop loss is well
established (Rahman and Di, 2020, 62 case studies). Rahman et al. (2020) and
Qamer et al. (2023) offer usable methods for an independent loss estimate.
Rice-specific maps exist for Bangladesh, which is better than a general cropland
mask: 10 m seasonal maps including Boro (Singha et al., 2019) and annual 30 m
dry-season rice maps for 2014–2018 (Shew and Ghosh, 2019).

**NDVI and Boro yield.** Studies use NDVI to estimate yield at national or division
level (Mosleh et al., 2016; Alam et al., 2019). Mosleh et al. (2016) use the
initial greenness stage in early January and peak greenness from late March to
early April.

**Inference.** Clustered standard errors and the wild cluster bootstrap fail when
few clusters are treated, and randomisation inference has limits when treated
units are atypical (MacKinnon and Webb, 2017, 2018, 2020; Conley and Taber, 2011).
That describes the flash-flood data exactly, so no single method can be trusted
alone.

## 4. Closest studies compared with this paper

| | Flood type | Unit and period | Satellite flood data | Area and yield separated | Haor focus |
|---|---|---|---|---|---|
| Banerjee (2010) | Monsoon | Districts, 1978–2000 | Not stated | Partly | No |
| Asada et al. (2005) | Severe monsoon | National, long term | No | Yes, descriptive | No |
| Hassan (2019, thesis) | Flood damage indicators | Districts | Not stated | No, production and yield | No |
| Amin et al. (2015) | None (climate only) | National, 1972–2010 | No | Yes | No |
| Ahmed et al. (2017) | Flash, 2017 only | Northeast region, one event | Yes | Damaged area only | Yes |
| Rahman et al. (2025) | Monsoon | Not read | Not read | Land and production losses, from a partial abstract | Not stated |
| **This paper** | **Flash and monsoon** | **64 districts, 2011–2025** | **Yes, two records** | **Yes** | **Yes** |

## 5. What this changes in the plan

| Finding | Change to the analysis plan |
|---|---|
| Normal floods may raise productivity and extreme ones lower it (Banerjee, 2010; Asada et al., 2005) | Q2 now expects a positive effect at normal levels and a negative one at extreme levels; flood bins become required for monsoon floods |
| The 2017 flood began on 27 March (Ahmed et al., 2017) | **The JRC baseline can count early flood water as dry-season water and subtract it.** New required check with a January–February baseline and a window starting in mid-March |
| Cold matters at the reproductive stage (Rashid and Yasmeen, 2018) | Stage-specific cold moves from the seedling to the reproductive stage |
| Rice-specific maps exist (Singha et al., 2019; Shew and Ghosh, 2019) | Test a Boro mask ahead of the general cropland mask, first checking the map year: a map from a flood year could miss the lost fields |
| Harvested and planted area can behave differently (Cui, 2020; Wei and Davis, 2022) | BBS gives harvested area only, so add satellite pre-flood Boro area where possible, to estimate the share of planted area that was harvested |
| Findings differ across settings (Lesk, Li, Obembe) | The paper does not claim a general rule. It tests whether BBS records flood loss as area, given that yield comes from crop cuts on harvested fields |
| Peak greenness comes in late March to early April (Mosleh et al., 2016) | Add this window to the NDVI analysis |
| Inference is fragile with few treated districts | Keep all four methods, and check beforehand the smallest p-value randomisation inference can reach |

## 6. Still to read

Legal open copies were searched for on 31 October 2026 through OpenAlex, Semantic
Scholar, publisher pages and repositories. None of the four full texts is open, so
please try the University of Rajshahi library or ask Dr. Karim.

| Paper | What could be read | Why the full text matters | DOI |
|---|---|---|---|
| **Rahman et al. (2025), International Journal of Disaster Risk Reduction** | Partial abstract only: monsoon floods, land and production losses | Closest recent paper; must be read before the gap is claimed | 10.1016/j.ijdrr.2025.105401 |
| Banerjee (2010), Oxford Development Studies | Abstract | Closest published panel; flood data, methods and definition of extreme floods | 10.1080/13600818.2010.505681 |
| Sarker et al. (2014), Economic Analysis and Policy | Title only; the repository did not respond | Bangladesh rice panel | 10.1016/j.eap.2014.11.004 |
| Bairagi et al. (2021), Food Policy | Abstract, through RePEc: Sub1 rice in northwest Bangladesh, 2016 cross-section | Full text is no longer essential: this is not evidence for Boro in the haor, so the policy section should not use it that way | 10.1016/j.foodpol.2021.102183 |

The map year and data access for Singha et al. (2019) and Shew and Ghosh (2019) also
need checking before step 3.

## References

Full author lists, journals and DOIs for all 57 core papers are in `core_papers.csv`.
Hassan (2019) is at https://mountainscholar.org/handle/10217/197396. The formatted
list will be built from these records when the paper is written.

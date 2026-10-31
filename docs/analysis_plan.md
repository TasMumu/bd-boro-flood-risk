# Paper 2 analysis plan

Draft of 31 October 2026, updated after the literature review
(`literature/literature_review.md`), for discussion with Dr. Rezaul Karim.

This plan fixes the questions, models and pass criteria before any new outcome
model is run. The basic area, yield and production models already seen for
Paper 1 count as exploratory. Everything below is new work, and results are
reported whichever way they come out.

## 1. Questions

**Working title:** Does yield hide flood losses? Flood exposure, harvested area
and yield of Boro rice across Bangladesh's 64 districts, 2011–2025.

| | Question | Expectation to test |
|---|---|---|
| Q1 (main) | Do flash floods reduce Boro production through harvested area rather than yield? | Negative effect on area; yield effect within the negligible range (Section 5) |
| Q2 | Do monsoon floods, which come before planting, act differently? | Positive at normal levels, negative at extreme levels (Banerjee, 2010; Asada et al., 2005) |
| Q3 | Are flood effects concentrated in the haor districts? | Larger effect in the haor |
| Q4 | Why does NDVI not explain yield within a district? | Explained in Section 7 |
| Q5 | Where is risk concentrated, and how stable is that ranking? | Assessed in Section 6 |

## 2. What the design checks found

These checks used the flood variables and Sentinel-1 scene counts only. No yield,
area or production value was read. Scripts and outputs are in `design_checks/`.

**The flash-flood estimates rest on very few events.**

| Flood variable | District-years | Effective observations | Share from seven haor districts | Share from 2016 and 2017 |
|---|---|---|---|---|
| Flash flood, Sentinel-1 | 704 | 11 | 88 % | 68 % |
| Flash flood, JRC | 704 | 23 | 90 % | 56 % |
| Monsoon flood, Sentinel-1 | 640 | 52 | 47 % | not concentrated |
| Monsoon flood, JRC | 768 | 103 | 41 % | not concentrated |

Effective observations are the inverse of the summed squared shares of the flood
variation left after removing district and year means. Sunamganj 2017 alone is
25 % of the Sentinel-1 flash-flood variation.

So the flash-flood analysis is really a study of about three events (2016, 2017,
2022) in a few atypical districts, not a panel of 704 independent observations.
Ordinary standard errors can overstate certainty in that setting, and the
different methods already disagree once 2017 is removed. Monsoon floods vary much
more widely, so a standard panel suits them.

**Sentinel-1 coverage has a break between 2016 and 2017.** The series is almost
entirely Sentinel-1A over Bangladesh, so losing Sentinel-1B in December 2021 had
little effect here. The change is earlier:

| Scenes over the haor basin | 2015 | 2016 | 2017–2025 |
|---|---|---|---|
| April–May | 22 | 17 | 24–33 |
| January–March (dry baseline) | 25 | 20 | 39–46 |

Counts are scenes touching a box around the basin, so they are approximate. This
matters because 2016 is a key flood year. Its Sentinel-1 value rests on about half
the baseline scenes of later years.

## 3. Data

**Fixed input.** The Gold panel of Paper 1 (960 district-years, 2011–2025), Zenodo
10.5281/zenodo.23795046, panel SHA-256 starting `5cbaeb1edaef`. It is read and
never changed. Yields are BBS printed values only: no proxy, interpolated or
imputed values.

**New variables, built with the same checks as Paper 1:**

| Variable | Why it is needed |
|---|---|
| Flood fractions on Boro rice land, using Singha et al. (2019) or Shew and Ghosh (2019) if suitable, otherwise WorldCover cropland | Whole-district fractions include rivers and non-crop land. A map from a flood year could miss the lost fields, so the map year is checked first |
| Mid-March to mid-April, and later, separately | Floods can begin in late March (27 March in 2017), and damage depends on whether water arrives before harvest |
| Satellite pre-flood Boro area, where it can be mapped | BBS gives harvested area only; this allows the share of planted area that was harvested to be estimated |
| Sentinel-1 scene count per district-year | Measures the coverage break directly |
| Satellite crop loss: fall in cropland NDVI from before to after the flood | An independent check on the BBS area loss, using no BBS data |
| Heat at flowering and cold at the reproductive stage | The current seasonal weather measures may miss sensitive stages (Rashid and Yasmeen, 2018) |
| Irrigation, salinity and similar district data | Only where published by district; never estimated or filled |

**Haor definition, fixed now:** Sunamganj, Habiganj, Netrokona, Kishoreganj, Sylhet,
Moulvibazar and Brahmanbaria. An alternative using the share of each district
inside the haor basin will be tested if a suitable boundary exists.

## 4. Models

**Outcomes:** log harvested area, log yield, log production. Since production is
area times yield, the area and yield effects must add up to the production effect.
This is checked in every model.

**Reading the area effect:** Boro is planted before flash floods arrive, so a
same-season fall in harvested area means crop lost, not a planting decision. BBS
yield comes from crop cuts on harvested fields, so a destroyed field may leave no
trace in yield. The paper tests this reporting explanation and does not claim a
general rule, since other settings find the opposite (Obembe et al., 2021; Li et
al., 2025).

**Monsoon floods (Q2):** two-way fixed effects for district and year, with
temperature, rainfall and hot days as controls, and flood fractions in bins as well
as a straight line, to separate normal from extreme floods. JRC and Sentinel-1 are
run separately and never spliced.

**Flash floods (Q1, Q3):** three designs that must point the same way.

1. Dose-response: two-way fixed effects on the flood fraction, using all districts.
2. Year-by-year comparison of haor and other districts across 2011–2025. This shows
   any trend before a flood, the size of each drop, and whether area recovers.
3. Synthetic control for the most flooded districts in 2017, built from non-haor
   districts.

**Uncertainty:** every main estimate is reported with all four of the following.

- Standard errors clustered by district.
- Driscoll–Kraay standard errors, which allow for shocks shared across districts.
- Conley spatial standard errors, which allow nearby districts to be correlated.
- Randomisation inference, reassigning whole flood years across the panel so that
  the real spatial pattern of each flood is kept.

With so few flood years, randomisation inference has a floor on how small its
p-value can be. That floor is calculated before any model is run. If it is above
0.05, the rule in Section 5 uses the exact randomisation p-value and reports the
floor, so the test is not set up to fail. Each method has known weaknesses with few
treated districts (MacKinnon and Webb, 2017, 2020), which is why none is used alone.

## 5. How results will be judged

A result is called **supported** only if all of these hold. Otherwise it is
reported as **suggestive** or **not supported**.

- Same sign and similar size under all three flash-flood designs.
- p < 0.05 under all four uncertainty methods.
- Same direction in JRC and Sentinel-1 over their overlap.
- It passes the required checks marked below.

**Negligible yield effect:** the yield claim needs positive evidence, not just an
insignificant coefficient. It holds only if the 95 % interval lies within ±2 % per
10 points of flood fraction. *This bound was fixed on 31 October 2026, before any
model was run.*

| Check | What it rules out | Required |
|---|---|---|
| Leave out each of 2016, 2017 and 2022 | One event driving the result | Yes |
| Leave out each district, especially Sunamganj | One district driving the result | Yes |
| Next year's flood as a placebo | Effects that are really trends | Yes |
| Flood after harvest (June–October of t) as a placebo | Spurious timing | Yes |
| Satellite crop loss agrees with BBS area loss | An artefact of BBS reporting | Yes |
| Rice-only instead of whole-district fractions | Water on non-crop land | Yes |
| January–February baseline and a window from mid-March | Early flood water being counted as dry-season water, which is a risk for JRC | Yes |
| Sentinel-1 without 2015–2016, and with scene count as a control | The coverage break | Yes |
| Division-by-year fixed effects | Regional shocks | Reported |
| District-specific linear trends | Different long-run paths | Reported |
| Poisson model for area and production | Dependence on the log form | Reported |
| Flood fraction in bins | A threshold rather than a straight line | Reported |
| Water thresholds of −16, −18 and −20 dB | Dependence on one threshold | Reported |
| Neighbouring districts' flood | Spillovers between districts | Reported |
| Comparison with published damage reports for 2017 | Implausible size | Reported |

Secondary tests are corrected with false discovery rate control.

**Exact pass rules, fixed on 31 October 2026 before any model was run:**

- **Main flood models:** the flood variable, the other flood variable and the weather
  controls enter together, as in Paper 1. Sentinel-1 uses 2016–2025 and JRC 2011–2021.
  The main exposure is the whole-district fraction; rice-only is a required check.
- **Supported:** the p < 0.05 rule must hold in both flood sources. If it holds in one,
  the result is suggestive.
- **Leave-out checks:** same sign, and at least half the size of the main estimate.
- **Placebos:** not significant at 5 % under clustered and Driscoll–Kraay errors.
- **Satellite crop loss:** flood raises satellite loss and satellite loss lowers BBS
  area, each with p < 0.05 under Driscoll–Kraay errors.
- **Rice-only, early window and scene checks:** same sign, p < 0.05 under
  Driscoll–Kraay errors. The size is not compared, because the units differ.
- **Synthetic control:** the 2017 gap is negative, and its size relative to the fit
  before the flood ranks in the top 5 % of placebo districts.
- **Conley errors:** 100 km distance cut-off and 2 years of serial correlation.

## 6. Vulnerability index and spatial analysis

The index in Paper 1 covers exposure and production sensitivity only. Paper 2
goes further:

- Structure it as exposure, sensitivity and adaptive capacity, as far as published
  district data allow.
- Test normalisation (min–max, z-score, rank), aggregation (arithmetic, geometric)
  and weights (equal, random, data-driven).
- Run Moran's I and LISA under several neighbour definitions, with false discovery
  rate correction.
- Report tier stability: how often each district stays in its risk tier.

The index describes where to look more closely. It is not an allocation rule, and
it is not evidence that the data are correct.

## 7. NDVI

Tests fixed in advance: the correlation with yield between districts and within
districts; the effect of removing year effects; different windows, including peak
greenness from late March to early April (Mosleh et al., 2016); and whether the
result depends on how pure the cropland is.

## 8. Known limits

- Fifteen years and few large flash floods. The findings describe these events, and
  should not be presented as a general law.
- Floods are not randomly assigned, so results are stated as estimates under the
  listed assumptions.
- BBS harvested area comes from official estimates, which is why the satellite
  crop-loss check is required.
- There is no annual Boro-specific field map; the cropland mask is a stand-in.

## 9. Order of work

1. Agree this plan. Done on 31 October 2026, including the ±2 % bound and the haor
   definition.
2. Complete the literature review. Done at abstract level (52 queries, 1,383 unique
   records). No study found separates haor flood losses into area and yield in a
   district panel. Rahman et al. (2025) and three other full texts must still be
   read before the gap is stated in the paper.
3. Build and validate the new variables. Done: 18 of 18 checks pass, and the new code
   reproduces Paper 1's flood values to rounding error.
4. Run the models in the order above. Done. Verdict on Q1 under the rule: suggestive.
5. Write the paper, with every number read from output files. Done: `paper/`.
6. Choose the journal. Done: see `journal_choice.md`.

## 10. Changes made after this plan was written

**Before any outcome model was run**, based on flood and mask data and on BBS area between
districts:

- Published rice maps cover only 2017 or 2014–2018, so a yearly MODIS mask was built, and a
  stable mask (at least 5 of 15 years) is used for flood fractions, because the yearly mask
  is noisy. Thresholds are in `data/bronze/parameters.json`.
- Sentinel-1 early and late windows use two half-month medians, because a single median
  diluted a flood arriving midway.
- Adaptive capacity is left out: no published district series was assembled, and the plan
  rules out estimating it. The 20 °C cold threshold is provisional.

**After the planned results were seen**, labelled exploratory in the paper and not part of
the verdict:

- The early-window effect with and without 2016 and 2017, and a table of flood timing.
- A synthetic-control test on the size of the gap alone. The planned ratio test failed, and
  the pre-flood fit is almost perfect, so that ratio is unstable.

**After external review, 31 October 2026:**

- The check "Sentinel-1 without 2015-2016" is the same model as leaving out 2016, because
  the main sample starts in 2016, so it is counted once: 18 of 22 required checks pass.
- Districts with a mean Boro area below 15,000 ha are flagged in the index, and a variant
  without them is reported, as is a variant without Chandpur.
- This plan has no public timestamp from before the results. It entered git in the first
  commit (54ca10f, 2026-10-31 02:48 +0600), together with the results, so that commit cannot
  prove the order. The paper says so, and it must not be described as preregistered.

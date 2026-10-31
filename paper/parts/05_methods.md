# 4. Methods

## 4.1 Analysis plan

Questions, models, pass rules and the bound for a negligible yield effect were written in a plan before any new model was run. The plan was not registered with a public timestamp. It entered version control together with the results, in the first commit of the repository (54ca10f, 31 October 2026), so readers cannot verify the order independently, and this study should not be read as preregistered. The plan and its log of changes are in the repository. The basic models in the framework paper [@mumu2026a] had been seen and count as exploratory. Two changes were made before the outcome models were run, based on flood and mask data and BBS area between districts: flood fractions on rice land use a stable mask built here, because the yearly mask proved noisy and published rice maps do not cover the period; and Sentinel-1 early and late windows use half-month medians, because a single monthly median diluted a flood arriving midway. After the planned results were seen, we added the analyses in Section 5.6, one extra synthetic-control test, a variant without districts with a small Boro base, and a variant without Chandpur. These are labelled as exploratory, and they do not change the verdict.

## 4.2 Flood models

For district i in harvest year t, each outcome Y (harvested area, yield or production) is modelled as

$$\ln Y_{it} = \beta F_{it} + \gamma M_{it} + \mathbf{x}^{\prime}_{it}\boldsymbol{\delta} + \alpha_i + \tau_t + \varepsilon_{it},$$

where F is flash flood and M monsoon flood, both per 10 points of district area, **x** holds mean temperature, precipitation and hot days, and α and τ are district and year effects. Since production is area times yield, the area and yield effects must add up to the production effect; the largest gap was below {{ f(0.0001, 4) }} log points. Effects are reported in per cent. This is the standard panel approach to weather effects [@hsiang2016; @blanc2017; @auffhammer2013]. Results are estimates under the stated assumptions: floods are not randomly assigned, and we avoid causal language.

## 4.3 Three designs for flash floods

Flash floods were studied in three ways that must point the same way: the dose-response model above; a year-by-year comparison of haor and other districts relative to 2015, the last year before the two largest floods; and synthetic control [@abadie2021] for the five most flooded districts in 2017, where a weighted mix of non-haor districts matches each district's path in 2011–2015.

## 4.4 Uncertainty

Few districts are treated and they are atypical, a setting in which clustered errors and the wild bootstrap can fail, and randomisation inference has limits [@conley2011; @mackinnon2017; @mackinnon2018; @mackinnon2020]. So no single method was relied on. Every main estimate is reported with errors clustered by district, Driscoll–Kraay errors [@driscoll1998], Conley spatial errors [@conley1999] with a 100 km cut-off and two years of serial correlation, and randomisation inference that reassigns whole flood years across the panel, keeping each flood's real spatial pattern. With T years, one event alone cannot reach a p-value below 1/T, about {{ f(R['ri_floor']['s1']['one_event'], 2) }} here, and two events below about {{ f(R['ri_floor']['s1']['two_events'], 2) }}. These limits apply only when one or two years carry all the variation. Because the flood pattern of every year is permuted, smaller p-values are possible when several years contribute, as in Table 4.

## 4.5 How results were judged

A result is called **supported** only if it has the same sign and similar size under all three designs, p < 0.05 under all four uncertainty methods in both flood records, the same direction in both records, and passes every required check. If the significance rule holds in one record it is **suggestive**, and otherwise **not supported**. Leave-out checks pass with the same sign and at least half the main size. Placebos pass if not significant at 5 % under clustered and Driscoll–Kraay errors. Satellite crop loss passes if flood raises it and it lowers BBS area, each with p < 0.05 under Driscoll–Kraay errors. Measurement checks pass with the same sign and p < 0.05 under Driscoll–Kraay errors. Synthetic control passes if the 2017 gap is negative and its size relative to the pre-flood fit ranks in the top 5 % of placebo districts.

A yield effect counts as negligible only if its 95 % interval lies within ±2 % per 10 points under every interval method. An insignificant coefficient alone is not evidence of no effect.

## 4.6 Index and spatial analysis

The risk index combines exposure (flash and monsoon flood on Boro land, heat at flowering and cold at the reproductive stage) with sensitivity (production instability, worst fall in area, low yield). In line with the handbook on composite indicators [@oecd2008] and uncertainty analyses of such indices [@saisana2005; @tate2012], we rebuilt it under {{ f(XI['combinations'], 0) }} combinations of three normalisations, two aggregations and four weighting schemes, including 1,000 random draws of weights. Global Moran's I [@moran1950] and LISA [@anselin1995] were run under four neighbour definitions, with false discovery rate correction [@benjamini1995]. Monsoon-flood and haor-interaction tests were corrected the same way as secondary tests.

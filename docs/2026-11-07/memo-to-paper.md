# From the Oct 22 Methods Memo to the paper

Each place the final analysis differs from the memo, with a sentence the paper can use. Full register: `EXPERIMENTS.md` §0 and §9b. Proposed memo text: `docs/2026-11-02/memo-corrections.md`.

| # | Memo | Final analysis | Sentence for the paper |
|---|---|---|---|
| 1 | Report W·AI (theta) as the spillover | Direct, indirect and total impacts | "Because neighbors' outcomes feed back through the spatial lag, we report direct, indirect and total effects (LeSage and Pace 2009) rather than the W·AI coefficient alone." |
| 2 | H2a mediator is HMA | tech_share main; HMA kept as the memo version | "HMA is built from AI, so its first stage is positive by construction; we use the tech-job share as the main mediator and report HMA for comparison." |
| 3 | No quadratic term | AI² with a Lind-Mehlum test | "We test nonlinearity with a quadratic in AI and a Lind-Mehlum test." |
| 4 | Price as a control | With and without price | "Because data centers may raise electricity prices, we also estimate the model without price." |
| 5 | Subgroup regressions | Interactions in one model | "We test heterogeneity with interactions in one model, so differences between groups are tested directly." |
| 6 | Three core outcomes | Added solar, wind, new capacity, CO2, coal share | "We add outcomes by source and a coal-share check." |
| 7 | No dynamics | 2017-2025 distributed lags and a long difference | "We examine dynamics with distributed lags on 2017-2025 and a 2015-2025 long difference." |
| 12 | Not stated | ctrl4 is the baseline; tech_share is never a control | "We don't control for the tech-job share, because it is the H2a mediator." |
| 15 | No SDM estimator named | SDPDm, LYtrans=FALSE, for all three outcomes | "We use one estimator for all outcomes, because the bias-corrected version gave rho above one for renew_share." |
| 21 | "RPS" control | Larger of RPS and CES, from LBNL's June 2026 file | "We control for the LBNL current RPS/CES schedule; because LBNL revises past years, it doesn't show what earlier law required." |
| 24 | AI is employment in NAICS 518210 | Private jobs only | "Our measure is private data-center jobs per 1,000 workers; adding published government jobs changes no result." |
| 25 | Population from Census and BEA | BEA for all years | "Population is BEA's series for all years, whose source is the Census Bureau's midyear estimates." |
| 26 | Census 2010 land area | 2020 Gazetteer | "Land area is from the 2020 Census Gazetteer; state fixed effects absorb the difference." |
| 27 | TIGER boundary file for W | Gazetteer county points; 2023 adjacency | "State centroids are land-weighted averages of county points from the 2020 Gazetteer; the border matrix uses the 2023 county adjacency file." |
| 28 | Not in memo | Spillover placebo | "We test the spillover's timing with neighbors' next-year AI." |
| 30 | Hansen threshold as a stretch | Dropped | "We don't estimate a threshold model; the quadratic model addresses nonlinearity." |
| F | Not in memo | The Fang et al. (2025) test | "We also test Fang et al. (2025) on their variables, and show one change at a time how the answer moves toward our design." |
| 11 | Not in memo | Georgia solar module | "We add a learning-curve calculation for Georgia, which is arithmetic rather than a test of AI." |

## Added 2026-11-07 (prompts 08 and 09)
- **Fang's outcome:** the main old basis is SEDS as published in June 2023; the year-by-year heat-rate rebuild replaces the single k (kept as a check).
- **Fang's method set:** subgroup splits with interaction tests, the fossil-fuel negative indicator, an extreme-weather split (our NOAA Storm Events counting rule) and an event study are now run. The June 2023 subgroup rows were added after seeing Table 2 (F27) and are exploratory.
- **Extensions not in the memo:** by-type outcomes, other outcomes (sales by sector, prices, mix, additions, imports, CO2), a measured-drivers model of the national trend, an "infrastructure + talent" AI index with a relevance test, groupings by AI investment and a land moderator. All registered in `EXPERIMENTS.md` section 14 before running; deviations X1-X5.
- **Not run:** the innovation dimension (no inventor locations), the Queued Up outcome (no scripted download), and Fang's Table A1 and Supplement B comparisons (supplement not received).

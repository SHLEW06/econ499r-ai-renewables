# Stretch goals: RECEIPT, 2026-11-04
Driver: `code/R/04e3_stretch.R --date 2026-11-04`. Tables and chart: `code/python/04e3_stretch_tables.py --date 2026-11-04`. Spec: EXPERIMENTS.md section 10. Log: `logs/2026-11-04/04e3_stretch.log`. Zhang spec throughout: ctrl4, AI(t-1) winsorized, two-way FE, clustered by state, 50 states.

## Gate
The baseline on this panel matches the 4e rows within 1e-8 (`gate.csv`).

## Shift-share IV: uninformative
- **Instrument:** each state's 2015 share of national 518210 jobs x national jobs in t-1 excluding that state, indexed to 2015, x 1,000.
- **First stage:** 0.0116 (SE 0.0069, p = 0.100). **KP F = 2.81, below 10, so the instrument is weak and the IV estimates are uninformative.** KP rank LM = 3.05 (p = 0.081).
- **Check:** a 2014 base, outside the sample, is weaker: KP F = 2.28.
- **KP rank LM is computed directly.** `fixest`'s `kpr` errors with clustered SEs in version 0.14.2. With one endogenous variable and one instrument, this statistic is the cluster-robust score test of the first-stage coefficient.
- **Reduced form:** reported for completeness. new_renew_mw is positive and significant (16.58, p < 0.001), but it can't be scaled into an AI effect with this first stage.

So the IV doesn't answer the reverse-timing question from the placebo.

## Moderation
No AI x broadband or AI x R&D interaction is significant for any of the four outcomes (smallest p = 0.110, new_renew_mw x broadband). `rd_share_pct` = R&D / panel nominal GDP, to keep one GDP vintage. Broadband: 2016-2024, no 2020, N = 400. R&D: 2017-2023, N = 350.

## Not run
- **Hansen threshold:** dropped by team decision.
- **AI x EPU in the Zhang spec:** run in the Fang test instead.

## Files
`stretch.csv` (74 rows), `gate.csv`, `iv_first_stage.csv/.tex`, `iv_table.csv/.tex`, `moderation_table.csv/.tex`, `../figures/04e_stretch_moderation.png`

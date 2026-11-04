# H3 SDM main-spec revision: RECEIPT, 2026-11-03
Driver: `code/R/04d2_sdm_mainspec.R --date 2026-11-03`. Spec: EXPERIMENTS.md section 0 items 15-16. The 4d files in `results/2026-11-03/h3/` are unchanged.

## Rule and outcome
- (a) LYtrans=TRUE, demn=TRUE on invdist-50: rho = 0.814 (ln_ec), 0.610 (ln_ee), 1.406 (renew_share). The valid interval is (-4.74, 1), and renew_share is outside it, so (a) fails.
- (b) **Main spec = LYtrans=FALSE for all three outcomes.** renew_share with LYtrans=TRUE, demn=FALSE stays as a labeled check.

## Estimator labels
- `ML`: LYtrans=FALSE
- `LY-bias`: LYtrans=TRUE, demn=FALSE (the 4d "main")
- `LY-demn`: LYtrans=TRUE, demn=TRUE

## Impacts
- Point estimate (`plugin`): impacts computed at the estimated rho, b1, theta1.
- `se_draws`, `ci_lo`, `ci_hi`: from 2,000 draws using the same scheme and seeds as `impactsSDPDm`. `p` = two-sided normal p of plugin / se_draws. CIs are draw percentiles.
- `mean_draws` is what 4d reported as the estimate.
- `rho_draws_out` counts draws with rho outside the valid interval. Where it is above 0, draw SEs are dominated by a few extreme draws (near-pole values), so read the percentile CI instead. This affects ln_ec and ln_ee in the main spec.

## Checks
- The first 500 draws reproduce `impactsSDPDm(NSIM=500)` to 1e-15.
- Means of draws reproduce the 4d impacts to 1e-15 on the same estimators and W.
- 4d called rho > 1 under LY-bias a "convergence failure." It is really the one-step bias formula overshooting: rho_ML + T*Var(rho)/(1-rho) predicts the LY-bias rho (`rho_overshoot_check.csv`). The rho SE is about 0.6-0.75 for ln_ec and ln_ee on inverse-distance W, so the correction is large.
- `splm_leeyu_check.csv`: splm's `LeeYu=TRUE` gives rho = 0.152, -0.136, -0.319, far from SDPDm's Lee-Yu versions, so it does not confirm them. b1 and theta1 stay close to the ML values. The plain ML fit is the one that matched splm in 4d.

## Run note
The first run of this script today did not apply demn on invdist-50: SDPDm silently drops demn unless rows sum to exactly 1, and the CSV has rounding error below 1e-5. The script now normalizes W exactly for LY-demn only and stops if demn is not applied. These files are from the corrected run.

## Files
- `sdm_core.csv`, `sdm_impacts.csv`: every estimator x W x outcome (rows with rho outside the interval have status FAILED).
- `wai_variation.csv`: SD of W*AI and own AI, raw and after FE.
- `indirect_per_1sd.csv`: renew_share indirect effect per one within-state SD of W*AI.
- `rho_overshoot_check.csv`, `splm_leeyu_check.csv`, `MAIN_SPEC.txt`.

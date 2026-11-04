# H3 spillover placebo: RECEIPT, 2026-11-04
Driver: `code/R/04e2_spillover_placebo.R --date 2026-11-04`. Spec: EXPERIMENTS.md section 0 item 28. Log: `logs/2026-11-04/04e2_spillover_placebo.log`.

## Gate
39 of 39 checks pass (`gate.csv`). On the full sample, the driver reproduces the stored SLX (invdist-50) within 1e-8 and the stored SDM main spec: rho, b1, theta1 and plug-in impacts within 1e-5, and simulated SEs within 1%. SDM versions here use `SDPDm(model="sar")` with W*X columns built by the driver, so W*AI(t+1) can enter without W*AI(t-1).

## Design
- **Sample:** 2015-2023, N = 450 on invdist-50 and N = 432 on border-48. W*AI(t+1) in 2024 would need 2025 AI for AK, ND, SD and WY, which BLS suppresses. Inverse-distance W gives every state weight on them, so 2024 is dropped to keep the panel balanced. The own-AI placebo in 4e has N = 496, so the two samples differ.
- **The lead** is winsorized as in the own-AI placebo.
- **W:** invdist-50 is the main W; border-48 is a check.

| Version | Terms |
|---|---|
| `a_lag` | AI(t-1), W*AI(t-1): the original model on this sample |
| `b_lead` | AI(t+1), W*AI(t+1): full swap |
| `c_ownlag_wlead` | AI(t-1), W*AI(t+1) |
| `d_both` | AI(t-1), W*AI(t-1), W*AI(t+1) |
| `e_both_ownlead` | `d_both` plus AI(t+1) |

## How to read the SDM rows
- **Use the percentile CIs (`ci_lo`, `ci_hi`) where `rho_draws_out` is above 0.** The draw SEs and `p` are then dominated by draws with rho outside its valid range. That applies to every invdist-50 row (255-694 of 2,000 draws) and to border-48 `ln_ec`. They're reliable for border-48 `ln_ee` and `renew_share`, where no draws fall outside.
- **rho is much less precise on this sample on invdist-50.** For renew_share, its SE is 0.743 at N = 450, against 0.075 at N = 550 (`placebo_sdm_core.csv`).

## Results
- **Dropping 2024-2025 alone removes the main-spec renew_share spillover.** Indirect effect on invdist-50: -0.161 (N = 550, CI excludes 0) becomes -0.082 (N = 450, CI -0.588 to 0.447).
- **invdist-50: uninformative.** Neither W*AI(t-1) nor W*AI(t+1) can be told apart from zero for renew_share, in the SLX or the SDM. W*AI(t+1) has little independent variation.
- **border-48: same pattern as the own-AI placebo, for renew_share.** With both in one model, the lead is significant and the lag is about zero: SLX theta -0.0406 (p = 0.028) vs 0.0098 (p = 0.584); SDM indirect -0.0432 (p = 0.025) vs -0.0011 (p = 0.978).
- **ln_ec and ln_ee:** no lead is significant. With both in one model, SLX W*AI(t-1) has the harmful sign and is significant in 3 of 4 rows (`ln_ec` on both W; `ln_ee` on border-48), but the same-sample lag-only rows aren't significant and the SDM CIs include zero. Treat this as exploratory.

## Wording
On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate (-0.161, p = 0.035) can't be separated from this reverse timing. H3 is not supported.

## Files
`gate.csv`, `placebo_slx.csv`, `placebo_sdm_core.csv`, `placebo_sdm_impacts.csv`, `lead_lag_variation.csv`

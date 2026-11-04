# Phase 4e robustness: RECEIPT, 2026-11-04
Driver: `code/R/04e_robustness.R --date 2026-11-04`. Spec curve: `code/python/04e_spec_curve.py --date 2026-11-04`. Spec: EXPERIMENTS.md section 9 and section 0 items 21 and 24. Log: `logs/2026-11-04/04e_robustness.log`. Stretch goals not run.

## Gate
18 of 18 checks reproduce the stored 4b and 4d estimates and SEs within 1e-8 (`gate.csv`).

## Rerun against 2026-11-03
All 111 rows that ran on Nov 3 are identical, with no difference in any estimate or SE. The panel fix changed only `dc_wages_usd`, which no model uses (`logs/2026-11-04/c1b_dc_wages.log`). The Nov 3 files stay in place.

## New rows
- **A5, RPS control:** main = `target_pct`, the "LBNL current RPS/CES schedule." Checks: RPS target only; June 2023 edition, 2015-2025 and 2015-2023; current schedule on 2015-2023 to compare; without NY. Each row is paired with a `-coef` row for the control's own coefficient.
- **All-ownership AI:** private + published government 518210 jobs (`data/ai_allown_518210.csv`), winsorized by the same rule as the baseline. Suppressed government rows count as 0.

## Results to read first
- **RPS:** the AI coefficient barely moves, and the control is never significant at 5%. EXPERIMENTS.md expected it to shrink; it didn't.
- **All-ownership:** nearly the same as the baseline on all four outcomes. Within-state correlation with the private measure is 0.999.
- **Placebo:** AI(t+1) is significant for renew_share (-0.0197, p = 0.006) and new_renew_mw (86.8, p = 0.028). With lead and lag in one renew_share model, the lead keeps the effect (-0.0210, p = 0.007) and the lag is about zero (0.0015, p = 0.827).

## Not run
Data-center MW (A2): no state-year series exists.

## Choices made in the driver
As in the Nov 3 receipt: the lead is winsorized at 1/99 (`placebo-nowins` shows the alternative); distributed lags shift `ai_dc_per1000_lag1`, so 2014 AI is usable; P2 uses HC1 SEs, with classical SEs also reported.

## Conley (A8, check only)
1,000 km: all five VCOVs are not positive definite and were eigenvalue-fixed, so treat those rows as unreliable (`conley_vcov_check.csv`).

## Files
`robustness.csv` (178 rows: 175 ok, 3 NOT_RUN), `gate.csv`, `spec_curve.csv`, `spec_curve.tex`, `PROVENANCE.md`, `conley_*.csv`, `../figures/04e_spec_curve.png`

# Phase 4e robustness: RECEIPT, 2026-11-03
Driver: `code/R/04e_robustness.R --date 2026-11-03`. Spec curve: `code/python/04e_spec_curve.py --date 2026-11-03`. Spec: EXPERIMENTS.md section 9. Stretch goals not run.

## Gate
18 of 18 checks reproduce the stored 4b and 4d estimates and SEs within 1e-8 (`gate.csv`): core and DK, new_renew_mw, per-capacity, fossil_to_renew, border SLX b1 and theta1, and 4b's long difference (version with the bug).

## Not run
- **Data-center MW (A2):** no state-year series exists.
- **RPS control (A5):** no LBNL file in `data/raw/lbnl/` and no `data/lbnl_rps_targets.csv` at run time. The driver runs it automatically once the CSV exists. Coding rules: EXPERIMENTS.md section 0 item 18.

## Choices made in the driver
- The lead is winsorized at 1/99, because `load_panel.R` leaves it unwinsorized. `placebo-nowins` shows the unwinsorized version.
- Distributed lags are built by shifting `ai_dc_per1000_lag1`, so 2014 AI is usable and the lags are winsorized like the baseline. `load_panel.R`'s lag2 and lag3 start from 2015 and are not winsorized.
- P2 uses HC1 SEs; classical SEs are also reported, for comparison with 4b.

## Placebo: read this first
AI(t+1) is significant for renew_share (-0.0198, p = 0.006) and new_renew_mw (86.8, p = 0.028). Diagnostics, added after seeing this and labeled as such:
- renew_share holds without winsorizing (-0.0191, p = 0.003). With lead and lag in one model, the lead keeps the effect (-0.0210, p = 0.007) and the lag is about zero (0.0015, p = 0.827).
- new_renew_mw is less clear: p = 0.087 without winsorizing, and neither term is significant in one model. Within-state corr(lead, lag) = 0.716.

## Conley (A8, check only)
- A 1 km cutoff gives SEs close to clustering by state, so `fixest` Conley includes the same state across years (`conley_check.csv`).
- 500 km: positive definite. About 3.9 other states are within the cutoff on average; 4 states have none (`conley_neighbors.csv`).
- 1,000 km: **all five VCOVs are not positive definite** and were eigenvalue-fixed. Treat those rows as unreliable (`conley_vcov_check.csv`).

## Files
`robustness.csv` (119 rows: 111 ok, 8 NOT_RUN), `gate.csv`, `spec_curve.csv`, `spec_curve.tex`, `PROVENANCE.md`, `conley_*.csv`, `../figures/04e_spec_curve.png`

# RECEIPT.md: h1 corrected copies
Date: 2026-11-09
No model was run. These are corrected copies of two files in `results/2026-11-02/h1/`, which stay unchanged (append-only). Details: `docs/2026-11-09/lm-proper-header-fix.md`.

| File | Source | Correction |
|---|---|---|
| `lm_proper.csv` | `results/2026-11-02/h1/lm_proper.csv` | Header gains `controls` (17 columns). The 8 rows from `04b_step1_twfe_checks.R` get `controls = ctrl5`; the 8 ctrl4 rows already had it. Values unchanged |
| `dynamics.csv` | `results/2026-11-02/h1/dynamics.csv` | In the 3 `dyn_longdiff_..._ctrl4_...` rows, `status` and `lag_k` swapped back to the header's order. Values unchanged |

Both files equal, byte for byte, what `04b_step1_twfe.R`, `04b_step1_twfe_checks.R` and `04b_step1_twfe_ctrl4.R` (fixed 2026-11-09) write when run in that order in a clean clone.
Status: ok

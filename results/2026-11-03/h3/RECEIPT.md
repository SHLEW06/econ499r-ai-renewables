# Phase 4d RECEIPT — 2026-11-03
Run completed: 2026-11-03 16:09:58.791618

## W matrices
  invdist-50: W_inverse_distance_rowstd.csv (50x50, row-std as-is)
  invdist-48: subset invdist-50 drop AK+HI, re-row-normalized
  border-48:  W_border_binary.csv subset drop AK+HI, row-standardized

## SDPDm notes
  LYtrans=TRUE: Lee-Yu (2010) bias correction for two-way FE panel (main)
  LYtrans=FALSE: uncorrected ML (for splm comparison)
  demn=FALSE: effect='twoways' handles FE removal internally
  SEs: asymptotic ML (not clustered); NSIM=500 for impactsSDPDm

## Outputs
  h3_moran.csv:        231 rows
  h3_lm_tests.csv:     12 rows
  h3_slx.csv:          9 rows (3 outcomes x 3 W)
  h3_sdm_core.csv:     12 rows
  h3_sdm_impacts.csv:  12 rows
  h3_splm_check.csv:   3 rows
  figures:             results/2026-11-03/figures/*.png

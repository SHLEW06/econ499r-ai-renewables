# RECEIPT — Phase 4c mediation
Date: 2026-11-03
Script: code/R/04c_step2_mediation.R --date 2026-11-03

## Inputs
  data/out/state_panel_2015_2025.csv (via load_panel.R)
  results/2026-11-02/h1/h1_core.csv (a1 values for share-mediated)

## Outputs
  results/2026-11-03/h2/h2_results.csv
  results/2026-11-03/h2/ln_ea_redundancy.csv
  results/2026-11-03/tables/h2_tech_share_c.csv + .tex
  results/2026-11-03/tables/h2_hma.csv + .tex
  results/2026-11-03/tables/h2_ln_ea.csv + .tex
  results/2026-11-03/tables/PROVENANCE.md
  results/2026-11-03/figures/h2_path_*.pdf + .png (3 diagrams)

## Sample
  N = 550 (50 states, 2015-2025, DC dropped, lag1 complete cases)
  tech_share: mean-centered; hma, ln_ea: as-is from panel

## Controls
  ctrl4 = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth
  (H1 baseline; EXPERIMENTS.md §6/§7 tags corrected from ctrl5 to ctrl4)

## Bootstrap
  999 reps (pairs cluster bootstrap, resample by state), seed=42
  a1 values used for share-mediated: ln_ec=-0.0015655  ln_ee=0.0022056  renew_share=-0.0101293

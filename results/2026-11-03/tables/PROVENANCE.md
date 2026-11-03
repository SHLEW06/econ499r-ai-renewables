# PROVENANCE — H2 tables
Generated: 2026-11-03
Script: code/R/04c_step2_mediation.R --date 2026-11-03
Panel: data/out/state_panel_2015_2025.csv (via load_panel.R)
H1 a1 source: results/2026-11-02/h1/h1_core.csv (ctrl4, CRV1-state rows)
Controls: ctrl4 = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth
SE: clustered by state (CRV1) for all three equations
Bootstrap: 999 reps, seed=42, cluster-by-state (pairs cluster bootstrap)
tech_share: mean-centered (grand mean subtracted)
Equations: (a) M ~ AI + ctrl4 + FE; (b) Y ~ M + ctrl4 + FE; (c) Y ~ M + AI + ctrl4 + FE

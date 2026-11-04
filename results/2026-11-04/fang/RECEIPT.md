# Fang test, Part B: RECEIPT, 2026-11-04
Driver: `code/R/04h_fang_test.R --date 2026-11-04`. Tables and chart: `code/python/04h_fang_tables.py --date 2026-11-04`. Spec: EXPERIMENTS.md section 9b. Log: `logs/2026-11-04/04h_fang_test.log`.

## Gate
All checks pass (`gate.csv`): N = 204 and 153; fixest matches least squares with state dummies; `fang_panel.csv` matches the master panel; the jobs lag is consistent; the 2021 postings total matches.

## Which postings series is main
"Lightcast's own series" is the share history in `fig_4.4.12` (2026 edition) and its earlier versions. It covers only CA, NY, TX and WA, so it can't be the main measure. The stitched series stays main (`prompts/06_finish.md` section 2).

## Replication
Doesn't reproduce on current SEDS: column 6 is -0.0188 (p = 0.317) against Fang's +0.0531.

**Most likely reason, and how far it goes:** EIA moved SEDS to the captured-energy approach for wind, solar, hydro and geothermal in Oct 2023, for all years. A labeled rebuild of approximately the old basis (biomass + k x the other four) brings back the positive sign:

| Version | Column 2 | Column 6 |
|---|---|---|
| Fang, published | +0.0452*** | +0.0531*** |
| Current SEDS | -0.0100 | -0.0188 |
| Approx. old SEDS, k = 2.3 | +0.0284* | +0.0165 |
| Approx. old SEDS, k = 2.6 | +0.0342** | +0.0216 |
| Approx. old SEDS, k = 2.9 | +0.0393** | +0.0262 |

The rebuild is approximate: one k stands in for each year's heat rate, and direct-use solar and geothermal are treated like electricity. k isn't taken from an EIA table. It's a range around the ratio of a typical fossil heat rate to 3,412 Btu/kWh. **This shows the change is large enough to flip the sign. It doesn't reproduce Fang's numbers,** and we couldn't test Fang's data vintage directly.

Using each year's postings as first published doesn't help: -0.0414 (p = 0.014) in column 6.

## Choices and limits
- **SEs:** conventional in the replication, since the paper says only "standard errors." Clustered versions are in `fang_results.csv`.
- **Share-of-national row:** with year FE it equals the postings row by construction, so it isn't a test.
- **Heterogeneity:** exploratory, many tests, no multiplicity correction. Fang's "mean" groups look like median splits; both are shown. Extreme weather: not run.
- **RPS control:** in percent, not logged, because of zeros.
- **Not winsorized,** matching Fang. The Zhang test winsorizes.

## Files
`fang_results.csv` (560 rows, status ok), `gate.csv`, `split_groups.csv`, `tables/` (replication, bridge, moderation, by_type, heterogeneity, regions, placebo, robustness; CSV and .tex), `PROVENANCE.md`, `../figures/04h_bridge.png`

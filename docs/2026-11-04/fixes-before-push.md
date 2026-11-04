# Fixes before push, 2026-11-04

The team's review of the finish run asked for five fixes. All are done, and nothing was pushed.

## 1. Exploratory SLX note
`findings.md` now matches the PDF. With lead and lag in one model, neighbors' past AI is significant for ln_ec (p = 0.034 inverse distance, 0.024 border) and for border-weights ln_ee (p = 0.033). The SDM doesn't confirm it, and with this many tests a few p < 0.05 are expected by chance. `04g_results_pack.py` stops if those SDM CIs ever exclude zero.

## 2. New H1 chart
`fig_h1_coefficients.png` now shows estimates per one within-state SD of AI (0.5212), one panel per unit: percent, percentage points, MW. It's Figure 1 of the PDF. The old file stays at `results/2026-11-02/figures/h1_coef_plot_ctrl4.png`.

## 3. Citations
**Georgia commitments trace to a filing on disk, so the numbers stay.** Georgia Power, Quarterly Large Load Economic Development Report, Q2 2026, filed Aug. 17, 2026, Georgia PSC Docket 55378, PDF p. 8: "Customer commitments expanded from 3,600 MW to 15,600 MW." File: `DKT 55378 Lg Load Econ Dev Rept Q2 2026 PD.pdf` inside `data/raw/georgia/dkt55378_large_load_report_q2_2026.zip`. `build_georgia_tables.py` now checks that sentence on that page. The cover letter is captioned Docket 55378; the page headers say Docket 56002.

**EIA notice.** https://www.eia.gov/state/seds/seds-change/index.php is cited wherever the Fang sign flip is discussed, and k = 2.3-2.9 is labeled our approximation of the old accounting.

**IEA WEO 2025, Annex A, solar PV capacity.** Checked on the PDF on Nov 4; the PDF isn't stored.

| Path | Scenario | Table, page | 2024 GW | 2035 GW |
|---|---|---|---:|---:|
| Low | Current Policies | A.3a, p. 417 | 2,164 | 8,067 |
| Central | Stated Policies | A.3b, p. 423 | 2,164 | 8,855 |
| High | Net Zero Emissions by 2050 | A.3c, p. 429 | 2,164 | 12,499 |

## 4. Net producer
Documented in `EXPERIMENTS.md` F15 and F19, `data/receipts/seds_fang.md` and `results/2026-11-04/fang/RECEIPT.md`. Fang's rule is electricity production above consumption from EIA, series not stated (PDF p. 4).

| Rule | State-years | Gap between groups, Fang's spec, postings |
|---|---:|---|
| Fang, published | 76 | not reported |
| EIA generation above retail sales (ours) | 120 | 0.0864, p = 0.003 |
| SEDS total energy production above consumption | 40 | 0.0336, p = 0.316 |
| SEDS net interstate electricity flow below zero | 104 | 0.0368, p = 0.177 |

Total energy is closer by count (36 away, against 44), so it's added as a check. It isn't Fang's concept. Interstate flow wasn't asked for, but it's the closest electricity rule tried, so it's reported too.

## 5. NOAA weather check
`data/noaa_degree_days.csv`, 48 states, 2015-2025. Climate at a Glance matches the nClimDiv monthly files exactly on all 528 state-years. `code/R/04e4_weather_check.R`; logged first in `EXPERIMENTS.md` section 0, item 31.

| Sample and controls | AI(t-1) on ln_ec | N |
|---|---|---:|
| Baseline, 50 states | -0.0016 (p = 0.795) | 550 |
| Same 48 states, no weather | -0.0009 (p = 0.880) | 528 |
| 48 states, + HDD and CDD | -0.0021 (p = 0.711) | 528 |

HDD and CDD are both significant (p < 0.001). The AI coefficient doesn't change.

## Also corrected, found while tracing
- **"After Fang's data."** Our text said EIA's change came after Fang's data, as a fact. Fang's paper was received Dec 2, 2024, and names no SEDS release. New wording uses what supports the old basis: Fang says EIA's data ended in 2021 (PDF p. 3), and its Table 2 constants imply a mean log outcome of 11.79, which fits the old basis (11.78-11.90) and not the current one (11.44). `results/2026-11-04/fang/seds_basis_level_check.csv`.
- **`data/receipts/georgia_psc.md`.** It listed a "~40 GW" queue and a data-center "majority" that aren't in the cited report, and read 2,600 MW as load growth when it's the rise in peak demand. No result used them. The table now holds traced figures.
- **"Cross-source checks all green."** One yellow row now exists (no rule reaches Fang's 76), so the text says so.
- **`fang_split_vars.csv`.** The `extreme_weather_note` no longer says NOAA wasn't available. The split stays not run: it counts occurrences, and degree days don't replace that.

## Rebuild
```
python3 econ499r_starter/scripts/download_noaa_degree_days.py data/raw/noaa data/noaa_degree_days.csv
python3 econ499r_starter/scripts/build_net_producer_defs.py data/raw/eia/seds data/fang_split_vars.csv data/fang_net_producer_definitions.csv
Rscript code/R/04e4_weather_check.R --date 2026-11-04
Rscript code/R/04h2_fang_net_producer.R --date 2026-11-04
```
Then the commands in `data/receipts/master_workbook.md`, `04g`, `04j` and `04k`, and both packaging scripts.

# Receipt: Fang test panel and split variables

**Built by:** `econ499r_starter/scripts/build_fang_tables.py data/raw data logs/2026-11-04`. Doesn't change the master panel.

## Outputs
| File | Rows | Contents |
|---|---|---|
| `data/fang_panel.csv` | 561 (51 x 2015-2025) | Everything the Fang test needs; blanks stay blank |
| `data/fang_split_vars.csv` | 561 | Fang's split variables |

## Sources
| Variable | Source | Receipt |
|---|---|---|
| `re_bbtu` and types, `ep_tetcd`, `total_energy_bbtu` | EIA SEDS | `seds_fang.md` |
| `edu_bach_per1000` | NCSES | `ncses.md` |
| `ai_postings`, shares, vintage | AI Index | `ai_index.md` |
| `gdp_real_musd2017`, `population` | BEA, via the master panel. **Chained 2017 dollars; Fang uses 2012** | `bea.md` |
| `epu_composite`, `epu_national`, `epu_state` | Annual means | `epu.md` |
| `dc_jobs`, `dc_jobs_lag1`, `ai_dc_per1000` and lag | QCEW private 518210, via the panel. The 2015 lag reads the 2014 raw file | `bls_qcew.md` |
| `elec_consumption_mwh`, `elec_price_c_kwh` | EIA retail sales, via the panel | `eia_state.md` |
| `net_producer` | 1 if `gen_total_mwh` > retail sales | `eia_state.md` |
| `rd_total_musd` | NSF, 2017-2023 | `nsf.md` |
| `income_pc_usd` | BEA SAINC1 line 3, current dollars | `bea.md` |
| `census_region` | Census four regions: Northeast 9, Midwest 12, South 17, West 13 | Fixed list |
| `target_pct` | LBNL current RPS/CES schedule | `lbnl_rps.md` |
| ctrl4 variables | Master panel | |

**Extreme weather: not run.** NOAA isn't available, so `fang_split_vars.csv` carries a blank column with that note.

**Split groups** (above or below mean) are built in Part B, from each state's 2018-2021 average.

## Checks
- 561 rows, no duplicate keys.
- Fang's sample is complete: 204 of 204 state-years in 2018-2021 have all of the paper's variables.
- Coverage by variable and year: `logs/2026-11-04/fang_coverage.csv`.

# Receipt: SEDS renewables on the old (fossil-fuel-equivalence) basis

**Status: done, 2026-11-07. Used for the Fang test (prompt 08, section 1; `EXPERIMENTS.md` section 9b, F23-F27) and prompt 09.** Output: `data/seds_old_basis.csv` (51 states x 2015-2024, 510 rows, no blanks in the rebuilt series). Script: `python3 -I econ499r_starter/scripts/build_finalize_tables.py data/raw data logs/2026-11-07`. Downloads: `python3 -I econ499r_starter/scripts/download_finalize_sources.py data/raw logs/2026-11-07/finalize_downloads.csv` (retrieved 2026-11-07).

## Why
In October 2023 EIA changed how SEDS counts electricity from wind, solar, hydro and geothermal: from fossil fuel equivalency (the national fossil-fueled plant heat rate) to captured energy (3,412 Btu/kWh). Notice: https://www.eia.gov/state/seds/seds-change/index.php (saved as `data/raw/eia/seds/seds_change_notice.html`). Fang's data end in 2021 and were published before the change.

## Sources
| File (`data/raw/`) | URL | Bytes | sha256 | Kept |
|---|---|---:|---|---|
| `eia/seds_archive/complete_seds_2021.zip` | https://www.eia.gov/state/seds/archive/complete_seds_2021.zip | 7,814,638 | `46646ef548bc6bdc6a5cd3a3e3ac6f66d165b1779faecd60a766032ce0ac4ca1` | RETCB, WYTCB, HYTCB, SOTCB, GETCB, BMTCB, TETCB for 2015-2021; FFETK (US). The CSV inside is dated 2023-06-22, before the change |
| `eia/seds_archive/archive_index.html` | https://www.eia.gov/state/seds/archive/ | 78,361 | `d8b96e788418f77fd9795573399f3e074c16c5a38de9796e34fc4e8fb758bfcd` | Citation only |
| `eia/mer/TOTAL.zip` | https://api.eia.gov/bulk/TOTAL.zip (EIA bulk Monthly Energy Review series, no key) | 3,245,210 | `0d9e1069bfc4fab83d69ce1ceafdb072342607ada6651b084992ea393d379b26` | Annual WYFFBUS, WYTCBUS, HVFFBUS, HVTCBUS, REFFBUS, RETCBUS |
| `eia/seds/use_all_phy.csv` | https://www.eia.gov/state/seds/sep_use/total/csv/use_all_phy.csv | 2,715,056 | `efd03111cc2b5b5bc25d94e97340bf19ddad260e81874e4ed6c8d59fcf199f57` | SOR7P (residential small-scale solar PV generation, million kWh) |
| `eia/seds/seds_change_notice.html` | https://www.eia.gov/state/seds/seds-change/index.php | 48,375 | `c20b0ec08b1e22445678c334f3a76c2472af5a64dd3431d3d4ba70cd6adeefc4` | Citation only |
| `eia/mer/mer_A_FULL.pdf` | https://www.eia.gov/totalenergy/data/monthly/pdf/mer_A_FULL.pdf | 1,099,621 | `2bcc0414f73dc1346e01495ac6c62a73028c4b6a5027074ab9c57e3cc16367f7` | Table A6 source notes (PDF p. 15: "Approximate Heat Rates for Electricity Net Generation, Total Fossil Fuels") |
| `eia/mer/_to_delete/MER_TA6.xlsx` | https://www.eia.gov/totalenergy/data/monthly/query/mer_data_excel.asp?table=TA6 | 77,294 | `f321c39a22530e5e7e5319b40a8bb560fcdd4c5ac4869be4c1fd36099ca813aa` | **Unused.** Despite the URL it holds MER Table 1.1 |
| `eia/mer/_to_delete/mer_a.pdf` | https://www.eia.gov/totalenergy/data/monthly/pdf/mer_a.pdf | 155,748 | `b58902260c1fc066204689e0bec34dda04b6a19de97aa612bcb7c871fd2207c0` | **Unused.** Appendix tables are renumbered; this is population and GDP |
| `eia/mer/_to_delete/full_data_MER.zip` | https://www.eia.gov/totalenergy/data/monthly/full_data_MER.zip | 13,984,834 | `ef91e697ba8c5d193b8a848d5dbad54c62be121fd18521b3247299c1ee8fc926` | **Unused.** EV-charging microdata (MER Appendix F) |

The three unused files were moved to `data/raw/eia/mer/_to_delete/` on 2026-11-07 (team decision), not deleted.

## Heat rate
MER Table A6's annual values couldn't be pulled by script: the browser's CSV and XLSX exports for TA6 returned empty files. EIA's bulk MER series carry both the fossil-fuel-equivalent and the captured-energy values for each fuel, so HR_t = 3.412 x WYFFBUS / WYTCBUS (thousand Btu/kWh). Hydro gives the same value to 0.002. **It equals the archived SEDS FFETK ("fossil-fueled steam-electric power plant conversion factor") to 0.001 in every year 2015-2021.**

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|
| HR, thousand Btu/kWh | 9.314 | 9.228 | 9.208 | 9.098 | 8.899 | 8.767 | 8.844 | 8.813 | 8.630 | 8.617 |

## Rebuild rule
Comparing the archive with current SEDS component by component (2015 and 2021) shows which parts EIA converted. These scale by exactly HR_t / 3.412: WYTCB, HYTCB, GEEGB (geothermal used for electricity), SOEGB, SOCCB and SOICB. GECCB, GEICB and GERCB (geothermal direct use and heat pumps) are unchanged. SORCB is partly converted: small-scale PV is, solar thermal isn't. So:

old = BMTCB + k_t x (WYTCB + HYTCB + GEEGB + SOEGB + SOCCB + SOICB + PVres) + (GECCB + GEICB + GERCB) + (SORCB - PVres), with k_t = HR_t / 3.412 and PVres = 3.412 x SOR7P.

Prompt 08 says to convert wind, solar, hydro and geothermal. This rule applies that to their electricity only, which is what EIA did. The all-components version is kept as `re_bbtu_rebuilt_allconv`, a check.

## Checks (`logs/2026-11-07/finalize_tables_build.log`, `seds_rebuild_check.csv`, `seds_rebuild_national.csv`)
- **Against the archive, 2015-2021, 357 state-years:** with the archive's own biomass, the rebuild matches to a median 0.00% (90th percentile 0.01%, max 0.19%). The method reproduces EIA's old accounting. With current biomass (EIA has revised wood, waste and biofuels since 2023), the median gap is 0.57%, the 90th percentile 4.83% and the max 23.1%, all from biomass revisions. The single-k version (k = 2.6) has a median gap of 1.62%.
- **National:** the 51-state sum is within 0.03-0.51% of EIA's national fossil-fuel-equivalent renewables (REFFBUS) in every year 2015-2024.
- **Current basis identity:** WY + HY + SO + GE + BM = RETCB within 2 billion Btu.
- **Biomass split:** WWTCB + BFTCB = BMTCB except in 2.0% of state-years, which are off by more than 1%. The largest gap is 901 billion Btu.

**Rating: green.**

## Columns in `seds_old_basis.csv`
`re_bbtu_current` (RETCB), `re_bbtu_rebuilt` (main old basis), `re_bbtu_rebuilt_allconv` (check), `re_bbtu_k26` (single k, as on 11-04), `RETCB_arch2021` (archive as published, 2015-2021 only), components WYTCB, HYTCB, SOTCB, GETCB, BMTCB, WWTCB (wood and waste), BFTCB (biofuels, including losses and co-products), EMTCB (fuel ethanol), BDTCB (biodiesel), B1TCB (renewable diesel), SOR7P, `fossil_bbtu` (FFTCB), TETCB, `fossil_share_total`, and two current-basis totals: without all biomass and without biofuels.

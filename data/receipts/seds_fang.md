# Receipt: SEDS renewable consumption and energy price (Fang test)

**Source:** U.S. Energy Information Administration, *State Energy Data System*. Consumption: `data/raw/eia/seds/use_all_btu.csv` (see `eia_seds.md`). Prices: https://www.eia.gov/state/seds/sep_prices/total/csv/pr_all.csv
**How:** `download_fang_sources.py` and `build_fang_tables.py`, 2026-11-04.

## What was kept
`data/seds_renewables_state.csv`: 510 rows, 51 areas x 2015-2024. All codes confirmed against EIA's code list.

| Column | MSN | EIA description | Unit |
|---|---|---|---|
| `re_bbtu` | RETCB | Renewable energy total consumption | Billion Btu |
| `wind_bbtu` | WYTCB | Wind energy total consumption | Billion Btu |
| `solar_bbtu` | SOTCB | Solar energy total consumption | Billion Btu |
| `geothermal_bbtu` | GETCB | Geothermal energy total consumption | Billion Btu |
| `hydro_bbtu` | HYTCB | Hydropower total consumption | Billion Btu |
| `biomass_bbtu` | BMTCB | Biomass total consumption | Billion Btu |
| `total_energy_bbtu` | TETCB | Total energy consumption | Billion Btu |
| `ep_tetcd` | TETCD | Total energy average price | Dollars per million Btu |

## Steps
Keep the 8 codes and 51 areas (drop `US`), 2015-2024, and reshape. **Rows:** 8 series x 52 areas in; 510 out. No NA.

## Checks
- **Internal:** the five types sum to RETCB within 0.04%.
- **Against the panel:** TETCB matches panel `seds_total_energy_bbtu` exactly on all 510 rows.
- **Against Fang's Ns, nonzero state-years 2018-2021:** renewables, solar, geothermal and biomass 204 (Fang 204); hydro 192 (Fang 192); wind 165 (Fang 164). The one-state-year wind gap is probably a later SEDS revision; I didn't confirm that.

## Quirks
**Accounting change in the outcome.** In Oct 2023, EIA moved SEDS from the fossil fuel equivalency approach to the captured-energy approach for wind, solar, hydro and geothermal electricity, at 3,412 Btu/kWh, for all years ([SEDS change note](https://www.eia.gov/state/seds/seds-change/index.php); [MER Appendix E](https://www.eia.gov/totalenergy/data/monthly/pdf/mer_e.pdf)). Fang's data end in 2021, before this. Biomass isn't affected, so it now makes up about 59-68% of U.S. `RETCB` in 2018-2024, and total renewables follow it more closely. By-type series change little in logs. See `results/2026-11-04/fang/RECEIPT.md`.

Zero cells 2015-2024: wind 97, hydro 30. Fang drops these in by-type models because of logs. SEDS ends in 2024, so 2025 is NA in `fang_panel.csv`.

**Rating: green.**

## Raw file hashes
| File | Bytes | SHA-256 | Source |
|---|---:|---|---|
| `pr_all.csv` | 2,060,495 | `c80d9bca62b347514f43ca577f722d38988874e3db34bfce178bb45aef23ab78` | https://www.eia.gov/state/seds/sep_prices/total/csv/pr_all.csv |
| `Codes_and_Descriptions.xlsx` | 68,741 | `c34324b0ae9c793b45261a1377a2d4fb1ad002d27b54195329bed6514897169f` | https://www.eia.gov/state/seds/CDF/Codes_and_Descriptions.xlsx |

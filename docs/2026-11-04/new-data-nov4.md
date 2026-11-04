# Handoff: new data, Nov 4

## Status
Steps 2-7 are done, except NOAA, which is not done because NCEI was unreachable. No models were run, and the master panel wasn't changed.

| Side table | Rows | Rating |
|---|---|---|
| `data/lbnl_rps_targets.csv` | 561 | Yellow |
| `data/acs_broadband.csv` | 510 | Yellow |
| `data/nsf_state_rd.csv` | 357 | Yellow |
| `data/epu_state_annual.csv` | 2,091 | Green |
| `data/owid_global_solar_capacity.csv` | 52 | Green |
| `data/lbnl_utility_solar.csv` | 2,005 | Green |
| `data/epoch_ai_campuses_by_state.csv` | 29 | Green, context only |
| `data/noaa_degree_days.csv` | none | Not done |

Ratings and checks: `data/DATA_VALIDATION.md`, "New data, Nov 4." Workbook: `outputs/ECON499R_Data_Workbook_2026-11-04.xlsx`; the Nov 1 copy is unchanged.

## Team decisions, 2026-11-04
1. **`target_pct` is the larger of RPS and CES each year.** `rps_target_pct` stays as a check.
2. **The RPS control uses the "LBNL current RPS/CES schedule."** Use that label everywhere. Checks: the June 2023 edition (`target_pct_ed2023`) and a version without NY.
3. **NOAA is not done,** and CPC files are not substituted.
4. **B1 broadband uses 2016-2024,** without 2015 and 2020.

## What to know before using these
- **ACS 2015:** code `S2801_C02_012E`, and not comparable with later years.
- **NSF:** divide `rd_total_musd` by panel `gdp_nom_musd`, rather than using NSF's intensity, to keep one GDP vintage.

## Open
- **Google Kansas City East:** state unresolved in the Epoch table.
- **Not committed, by design:** raw data, side tables, the workbook.

## How to rebuild (from project root)
```bash
python3 econ499r_starter/scripts/download_nsf_tab10.py data/raw/nsf
python3 econ499r_starter/scripts/download_acs_broadband.py .env data/raw/acs data/acs_broadband.csv logs/2026-11-04/acs_spot_check.csv
python3 econ499r_starter/scripts/check_rps_vintages.py "data/raw/lbnl/RPS & CES Targets and Demand_June 2026.xlsx" <scratch_dir> logs/2026-11-04/rps_vintage_check.csv
python3 econ499r_starter/scripts/build_side_tables_nov4.py data/raw data logs/2026-11-04/rps_vintage_check.csv data/out/state_panel_2015_2025.csv
python3 econ499r_starter/scripts/build_file_inventory.py data/raw logs/2026-11-04/raw_sha256_manifest.csv data/FILE_INVENTORY.csv
python3 econ499r_starter/scripts/add_side_tabs_nov4.py outputs/ECON499R_Data_Workbook_2026-11-01.xlsx data outputs/ECON499R_Data_Workbook_2026-11-04.xlsx
```

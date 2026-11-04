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

## What to know before using these
1. **RPS targets aren't targets in force.** See `data/receipts/lbnl_rps.md`. Target Achievement has no target levels, and LBNL revises past years (MD 2020: 30.5 then 18.1).
2. **`target_pct` is the larger of RPS and CES.** This is my choice, and it matters only for MA and VA, 2021-2025. `rps_target_pct` is there if the team prefers RPS only.
3. **Rerunning `code/R/04e_robustness.R` now runs A5.** The script runs the RPS control whenever `data/lbnl_rps_targets.csv` exists. The current A5 rows say NOT_RUN. Decide on item 2 first.
4. **ACS 2015:** code `S2801_C02_012E`, and not comparable with later years.
5. **NSF:** divide `rd_total_musd` by panel `gdp_nom_musd`, rather than using NSF's intensity, to keep one GDP vintage.

## Open
- **NOAA:** rerun `download_noaa_degree_days.py` when NCEI responds, or download by hand (links in `data/receipts/noaa.md`). Its parser hasn't run on real output.
- **Google Kansas City East:** state unresolved in the Epoch table.
- **Not committed, by design:** raw data, side tables, the workbook.
- **Not committed, not mine:** the changes to `CLAUDE.md` and `EXPERIMENTS.md`, the 4e robustness files, `data/INDEPENDENT_AUDIT_2026-11-04.md`, and `logs/2026-11-04/raw_sha256_manifest.csv`, which `build_file_inventory.py` needs as its baseline.
- **`CLAUDE.md` §7 is out of date:** it still lists RPS, NSF and Epoch as needed.

## How to rebuild (from project root)
```bash
python3 econ499r_starter/scripts/download_nsf_tab10.py data/raw/nsf
python3 econ499r_starter/scripts/download_acs_broadband.py .env data/raw/acs data/acs_broadband.csv logs/2026-11-04/acs_spot_check.csv
python3 econ499r_starter/scripts/check_rps_vintages.py "data/raw/lbnl/RPS & CES Targets and Demand_June 2026.xlsx" <scratch_dir> logs/2026-11-04/rps_vintage_check.csv
python3 econ499r_starter/scripts/build_side_tables_nov4.py data/raw data logs/2026-11-04/rps_vintage_check.csv data/out/state_panel_2015_2025.csv
python3 econ499r_starter/scripts/build_file_inventory.py data/raw logs/2026-11-04/raw_sha256_manifest.csv data/FILE_INVENTORY.csv
python3 econ499r_starter/scripts/add_side_tabs_nov4.py outputs/ECON499R_Data_Workbook_2026-11-01.xlsx data outputs/ECON499R_Data_Workbook_2026-11-04.xlsx
```

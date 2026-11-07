# Data receipts: index and rebuild steps

Each receipt records a source's link, files, SHA-256 hashes, what was kept, steps, row counts and checks. Validation ratings are in `data/DATA_VALIDATION.md`. Every raw file is listed in `data/FILE_INVENTORY.csv`.

## Where things are

| Looking for | Where it actually is |
|---|---|
| **Codebook** | `data/variable_registry.csv`, with `data/DATA_DICTIONARY.md` and the Variable Finder tab of `outputs/ECON499R_Master_Data_2026-11-04.xlsx` generated from it. Rebuild steps: `master_workbook.md`. There's no `data/codebook.csv` |
| **Cleaning code** | `econ499r_starter/scripts/build_panel.py` builds the panel. `build_side_tables_nov4.py` and `build_ai_allown.py` build the side tables. There's no `code/python/clean/` |
| **Methods Memo** | `notes/Methods_Memo_AI_Renewable_Energy_US_Test_Zhang_2026.pdf`. A byte-identical copy is `econ499r_starter/reference/Methods_Memo.pdf`. There's no `admin/` folder |
| **Download script** | `econ499r_starter/download_all.py`, not under `scripts/` |
| **Registered deviations from the memo** | `EXPERIMENTS.md` §0; proposed wording in `docs/2026-11-02/memo-corrections.md` |

## Index

### Phase 2 sources (master panel and finance tables)
| Receipt | Source | Raw folder | Used for |
|---|---|---|---|
| [eia_state.md](eia_state.md) | EIA state generation, capacity, sales, emissions | `data/raw/eia/` | Panel |
| [eia_seds.md](eia_seds.md) | EIA SEDS | `data/raw/eia/seds/` | Panel, `seds_mmbtu_pc` |
| [eia_forms.md](eia_forms.md) | EIA Forms 860, 861, 923 | `data/raw/eia_forms/` | Reference; identifies 2017 blank-fuel rows |
| [bls_qcew.md](bls_qcew.md) | BLS QCEW NAICS 518210, 5415, 10 | `data/raw/bls/` | Panel; all-ownership check |
| [bea.md](bea.md) | BEA state GDP and personal income | `data/raw/bea/` | Panel |
| [census.md](census.md) | Census Gazetteer and county adjacency | `data/raw/census/` | Panel, W matrices |
| [census_pop.md](census_pop.md) | Census state population estimates | `data/raw/census_pop/` | Check of BEA population only |
| [ferc_pudl.md](ferc_pudl.md) | FERC Form 1 via PUDL | `data/raw/pudl/` | Finance tables |
| [rmi.md](rmi.md) | RMI Utility Transition Hub | `data/raw/rmi/` | Optional finance |
| [lazard.md](lazard.md) | Lazard LCOE+ | `data/raw/costs/` | Georgia case box |
| [georgia_psc.md](georgia_psc.md) | Georgia Power IRP and large-load filings | `data/raw/georgia/` | Georgia case box |

### Added Nov 4 (side tables in `data/`; the panel doesn't use them)
| Receipt | Source | Raw folder | Output |
|---|---|---|---|
| [lbnl_rps.md](lbnl_rps.md) | LBNL current RPS/CES schedule, target achievement | `data/raw/lbnl/` | `lbnl_rps_targets.csv` |
| [lbnl_solar.md](lbnl_solar.md) | LBNL Utility-Scale Solar | `data/raw/lbnl/` | `lbnl_utility_solar.csv` |
| [owid.md](owid.md) | IRENA solar capacity via OWID | `data/raw/owid/` | `owid_global_solar_capacity.csv` |
| [epu.md](epu.md) | State EPU | `data/raw/epu/` | `epu_state_annual.csv` |
| [nsf.md](nsf.md) | NSF National Patterns Table 10 | `data/raw/nsf/` | `nsf_state_rd.csv` |
| [acs.md](acs.md) | ACS S2801 broadband | `data/raw/acs/` | `acs_broadband.csv` |
| [epoch.md](epoch.md) | Epoch AI data centers (context only) | `data/raw/epoch/` | `epoch_ai_campuses_by_state.csv` |
| [noaa.md](noaa.md) | NOAA degree days; one check only | `data/raw/noaa/` | `noaa_degree_days.csv` |

### Added for the Fang test (Phase 4h; side tables in `data/`; the panel doesn't use them)
| Receipt | Source | Raw folder | Output |
|---|---|---|---|
| [ai_index.md](ai_index.md) | Stanford AI Index job postings by state | `data/raw/aiindex/` | `ai_job_postings_state.csv` |
| [seds_fang.md](seds_fang.md) | SEDS renewables and energy price | `data/raw/eia/seds/` | `seds_renewables_state.csv` |
| [ncses.md](ncses.md) | NCSES bachelor's degrees indicator | `data/raw/ncses/` | `ncses_bachelors_state.csv` |
| [fang_panel.md](fang_panel.md) | Fang panel and split variables | Several | `fang_panel.csv`, `fang_split_vars.csv` |

### Added Nov 7 (prompts 08 and 09; side tables in `data/`; the panel doesn't use them)
| Receipt | Source | Raw folder | Output |
|---|---|---|---|
| [seds_old_basis.md](seds_old_basis.md) | EIA SEDS archive (June 2023), bulk MER, SEDS physical units | `data/raw/eia/seds_archive/`, `data/raw/eia/mer/`, `data/raw/eia/seds/` | `seds_old_basis.csv` |
| [noaa_storm_events.md](noaa_storm_events.md) | NOAA Storm Events details files | `data/raw/noaa/storm_events/` | `storm_events_state.csv` |
| [extend_outcomes.md](extend_outcomes.md) | EIA capacity, EIA-861 and SEDS (already downloaded) | `data/raw/eia/`, `data/raw/eia_forms/` | `extend_outcomes.csv`, `extend_restructured.csv` |
| [drivers_sources.md](drivers_sources.md) | P.L. 117-169 (govinfo), EIA Henry Hub; CRS and LBNL wind blocked | `data/raw/crs/`, `data/raw/eia/henry_hub/` | `extend_drivers_national.csv`, `extend_drivers_state.csv` |
| [crs_reports.md](crs_reports.md) | CRS R43453, IF10479, R46865 (mirrors; hand download) | `data/raw/crs/` | Tax-credit coding, section 4 |
| [lbnl_wind.md](lbnl_wind.md) | LBNL Land-Based Wind data, 2026 edition (hand download) | `data/raw/lbnl/` | Wind cost, section 4 |
| [bls_oews.md](bls_oews.md) | BLS OEWS state files 2015-2024 (hand download) | `data/raw/bls/oews/` | Section 5 talent dimension |
| [ai_index_section5.md](ai_index_section5.md) | QCEW 518210, OEWS, AI postings, BTOS, Quid via AI Index 2026, AIPD (unused) | `data/raw/bls/`, `data/raw/census_btos/`, `data/raw/aiindex/`, `data/raw/uspto_aipd/` | `ai_index_components.csv`, `ai_index_state.csv`, `ai_index_crossstate.csv` |
| [fang_supplement.md](fang_supplement.md) | Fang et al. (2025) supplementary material (hand download, Emory) | `literature/` (not in git) | Table A1 and Supplement B comparisons |
| [qcew_placebo.md](qcew_placebo.md) | BLS QCEW, two placebo industries | `data/raw/bls/placebo/` | read directly by `09a_fang_crosscheck.R` |

**Moved, not deleted (team decision, 2026-11-07):** `data/raw/eia/mer/_to_delete/` holds `MER_TA6.xlsx` (actually MER Table 1.1), `mer_a.pdf` (Appendix A tables, renumbered) and `full_data_MER.zip` (EV-charging microdata). They were downloaded by mistake on 2026-11-07 and aren't used. Hashes are in `seds_old_basis.md`.

**Filed 2026-11-07 (hand downloads; moves in `logs/2026-11-07/filing_moves.csv`):** the three receipts above. `data/raw/_to_delete/` holds three exact duplicates: `R46865 (1).pdf`, `State_Policy_Uncertainty.xlsx` (same SHA-256 as `data/raw/epu/State_Policy_Uncertainty.xlsx`) and `Fang Supplement.pdf`. The latter has the same SHA-256 as `literature/Assessing_AI_Impact_on_Renewable_Energy_Transition.pdf`, the article itself, **not the supplement**. The real supplement arrived later the same day as `fang supplement.docx` and is filed as `literature/Fang_Lee_Li_2025_supplement.docx` (`fang_supplement.md`).

## Rebuild steps (from the project root)

`data/raw/` is read-only. These commands rebuild everything derived from it; they don't change raw files, except that steps marked *download* add files.

```bash
S=econ499r_starter/scripts

# 1. Master panel, W matrices, centroids (about 30 seconds)
python3 -I $S/build_panel.py data/raw data/out

# 2. Finance tables and preliminary results, used by the workbook
python3 -I $S/ferc_fin.py data/raw/pudl data/out
python3 -I $S/prelim.py data/out
# SEC needs the SEC_USER_AGENT environment variable: sec_fin.py <cache_dir> <out_csv>

# 3. Side tables
python3 $S/download_nsf_tab10.py data/raw/nsf                # download
python3 $S/download_acs_broadband.py .env data/raw/acs data/acs_broadband.csv logs/2026-11-04/acs_spot_check.csv   # download; key from .env only
python3 $S/check_rps_vintages.py "data/raw/lbnl/RPS & CES Targets and Demand_June 2026.xlsx" <scratch_dir> logs/2026-11-04/rps_vintage_check.csv
python3 $S/build_side_tables_nov4.py data/raw data logs/2026-11-04/rps_vintage_check.csv data/out/state_panel_2015_2025.csv
python3 $S/build_ai_allown.py data/raw data/out/state_panel_2015_2025.csv data/ai_allown_518210.csv logs/2026-11-04/gov_518210_shares.csv

# 4. Inventory and workbook
python3 $S/build_file_inventory.py data/raw logs/2026-11-04/raw_sha256_manifest.csv data/FILE_INVENTORY.csv
python3 -I $S/build_xlsx.py data/out <scratch_dir>/wb_base.xlsx
python3 $S/add_side_tabs_nov4.py <scratch_dir>/wb_base.xlsx data outputs/ECON499R_Data_Workbook_2026-11-04.xlsx

# Fang test (Phase 4h)
python3 -I $S/download_fang_sources.py data/raw logs/2026-11-04/fang_downloads.csv   # download
python3 -I $S/build_fang_tables.py data/raw data logs/2026-11-04

# Finalize and extend (prompts 08 and 09, Nov 7)
python3 -I $S/download_finalize_sources.py data/raw logs/2026-11-07/finalize_downloads.csv   # download
python3 -I $S/build_finalize_tables.py data/raw data logs/2026-11-07
python3 -I $S/build_extend_tables.py data/raw data logs/2026-11-07
python3 -I $S/download_extend_sources.py data/raw logs/2026-11-07/extend_downloads.csv drivers   # download
python3 -I $S/build_drivers_tables.py data/raw data logs/2026-11-07
python3 -I $S/download_extend_sources.py data/raw logs/2026-11-07/extend_downloads.csv index   # download
python3 -I $S/download_extend_sources.py data/raw logs/2026-11-07/extend_downloads.csv addon   # download
python3 -I $S/build_ai_index.py data/raw data logs/2026-11-07

# 5. Compare two builds, cell by cell (C.1b)
python3 $S/compare_panel_builds.py <before_dir> data/out <out_csv>
```

## Checking raw files

`logs/2026-11-04/raw_sha256_manifest.csv` is the audit's baseline of 1,664 files. `build_file_inventory.py` stops if any of them has changed or is missing. Files added later carry their hashes in their own receipts and in `data/FILE_INVENTORY.csv`.

# Data bundle: unused raw files left out, 2026-11-09

`release/data_bundle_2026-11-09.zip` replaces the 2026-11-07 bundle. It leaves out the raw files that no script reads: 1,631 files, 1.13 GB, listed with size and source URL in `data/raw_unused.csv`. They stay on disk. Bundle: 320 files, 457 MB zipped, 985 MB unzipped (was 1,951 files, 1,529 MB zipped).

## How "no script reads it" was decided

1. **Python, traced.** Every Python script that can read `data/raw/` was run in a clean clone under an audit hook that logs each file opened and each file passed to a subprocess (`pdftotext`, `unzip`): `code/python/trace_raw_reads.py`. Scripts: `build_panel`, `ferc_fin`, `check_rps_vintages`, `build_side_tables_nov4`, `build_ai_allown`, `build_fang_tables`, `build_finalize_tables`, `build_extend_tables`, `build_drivers_tables`, `build_ai_index`, `build_net_producer_defs`, `validate_panel`, `build_cross_source_checks`, `build_georgia_tables`, `04f_georgia_solar`, `build_raw_file_shapes`, `build_master_workbook`, `check_master_workbook`. All exited 0.
2. **R and notebooks, read.** No R driver builds raw paths indirectly. The R drivers read `bls/placebo/qcew_<year>_{312140,812910}.csv`, `bls/qcew_2019_518210.csv`, `eia/seds/use_all_btu.csv` and `eia/seds_archive/complete_seds_2021.zip`. Notebook 02 only prints raw file names.
3. **Not counted as a read:** scripts that open every raw file only to describe or hash it. These are `build_raw_file_shapes.py` (the workbook's Raw Files tab), `build_file_inventory.py`, `build_data_bundle.py` and `verify_data.py`; `check_master_workbook.py` and `validate_panel.py` read nothing outside the used set. The download scripts write raw files but don't read them back.
4. **Parquet:** pyarrow opens files outside Python's audit hook, so the five PUDL files were checked in `ferc_fin.py`'s code. All five are used.

Per-file result: `logs/2026-11-09/raw_reads_trace.csv` (path, status, scripts that read it). Of 1,911 raw files: 171 used, 1,631 unused, 109 kept although no script opens them.

## Kept although no script opens them

| Files | Why |
|---|---|
| `acs/s2801_*.json`, `acs/s2801_variable_codes.csv` (10) | The saved Census API responses `download_acs_broadband.py` turned into `data/acs_broadband.csv`. Rebuilding needs a key |
| `noaa/<ST>_{hdd,cdd}_2015_2025.csv` (96) | The saved NOAA responses behind `data/noaa_degree_days.csv` |
| `noaa/state-readme.txt` | NOAA's documentation for the climate-division files `build_cross_source_checks.py` reads |
| `epoch/README.md`, `owid/readme.md` | License (CC BY) and citation terms for data in the bundle |

## Read by hand

Some unused files were read by a person, not a script: the CRS reports and public laws (tax-credit coding), the Georgia 2023 IRP Update and the Lazard LCOE+ PDF (Georgia box), EIA-860 2017 (the NE and NM blank-fuel rows) and the 20 unchosen QCEW placebo candidates (choosing the two placebo industries). `data/raw_unused.csv` says so in its `note` column, and the README table repeats it.

## Effects

- `verify_data.py` skips files listed in `data/raw_unused.csv` when listing extras, so a machine that has them still passes cleanly.
- `build_raw_file_shapes.py` reports a missing data file as "unreadable" on the Raw Files tab; nothing else in the workbook changes.
- The receipts and `data/FILE_INVENTORY.csv` still list every file with its hash, so a re-download can be checked.

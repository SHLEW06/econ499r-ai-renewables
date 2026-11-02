# Phase 2A handoff — data audit
**Date:** 2026-11-01  
**Project:** ECON 499R — AI and Renewable Energy, U.S. states 2015–2025  
**Team:** Shunji Lewandowski (modeling) · Alexander Hendricks (data and finance)  
**Next prompt:** `prompts/02_data_audit_cleaning_excel.md` PART B (after Shunji's OK)

---

## 1. What was done

Completed PART A of `02_data_audit_cleaning_excel.md`: mapped every file in `data/` to its script target, verified readability by magic bytes, built a full requirements matrix, and wrote `data/DATA_AUDIT.md`.

No files were moved, cleaned, downloaded, or modified. No models were run.

---

## 2. What we have

### Ready to use (after moving to `data/raw/<source>/` in PART B)

| Source | Files | Coverage | Script target prefix |
|---|---|---|---|
| EIA state generation | `eia_generation_state_annual.xlsx` | 1990–2025 | `raw/eia/` |
| EIA state capacity | `eia_existing_capacity_annual.xlsx` | 1990–2025 | `raw/eia/` |
| EIA Form 861 sales | `eia_form861_electricity_sales_2010_plus.xlsx` | 2010–2025 | `raw/eia/` |
| EIA emissions | `eia_emissions_annual.xlsx` | 1990–2024 | `raw/eia/` |
| EIA SEDS | `eia_seds_energy_use_all_btu.csv` | 1960–2024 | `raw/eia/seds/` |
| EIA planned capacity | `eia_planned_capacity_annual.xlsx` | — | `raw/eia/` |
| BEA SAGDP | `bea_sagdp_state_gdp.zip` | 1997–2025 | `raw/bea/` |
| BEA SAINC | `bea_sainc_state_income.zip` | 1929–2025 | `raw/bea/` |
| Census Gazetteer | `census_2020_gazetteer_counties.zip` | 2020 | `raw/census/` |
| FERC Form 1 (4 tables) | `ferc1_*.parquet` ×4 | Through 2025 | `raw/pudl/` |
| Georgia PSC IRPs | 4 PDFs | 2023, 2025 | `raw/georgia/` |
| Georgia PSC large-load | Q1 + Q2 2026 (PDF, zip) | 2026 Q1–Q2 | `raw/georgia/` |
| Georgia PSC tech. appendix | `irp_2025_public_disclosure.zip` | 2025 | Extra — keep in `data/georgia_psc/` |
| RMI Transition Hub | `data_download_all_pt1.zip` (10 CSVs) | — | `raw/rmi/` after extraction |
| Lazard LCOE+ 2026 | `literature/Lazard_LCOE_Plus.pdf` | 2026 | `raw/costs/` (wrong location now) |
| BLS QCEW (2025 only) | 3 CSVs | **2025 only** | `raw/bls/qcew_2025_*.csv` |

### Pre-built (from prior session — reference only)

`outputs/ECON499R_csv_for_R/`: state panel (561 rows × 80 cols), W matrices, FERC financials, SEC company financials. Use as check against the PART B rebuild; do not treat as raw inputs.

---

## 3. Critical gaps (block the methods)

These must be resolved before PART B can produce a complete panel:

| # | Gap | Steps blocked | How to fix |
|---|---|---|---|
| 1 | BLS QCEW 518210, years 2014–2024 (11 files) | Steps 1–3 (no AI measure) | `python econ499r_starter/download_all.py --core-only` |
| 2 | BLS QCEW industry 10, years 2014–2024 (11 files) | Steps 1–3 (no denominator) | Same run as above |
| 3 | BLS QCEW 5415, years 2014–2024 (11 files) | Step 2a (no tech_share / HMA) | Same run as above |
| 4 | Census county adjacency 2023 (1 file) | Step 3 (no W-border) | Same run as above |
| 5 | LBNL RPS/CES spreadsheet | Step 4 robustness (RPS control) | Browser download |
| 6 | Q1–Q4 2024 large-load reports (4 PDFs) | Georgia case box completeness | Browser, Docket 55378 |

Items 1–4 are a single script run. Total download: ~34 files, mostly small CSVs + one .txt.

---

## 4. Setup gaps (needed before PART B)

The following files that `02_data_audit_cleaning_excel.md` references do not yet exist:

| File | Purpose |
|---|---|
| `prompts/00_START_HERE.md` | Phase orientation prompt |
| `CLAUDE.md` | Project conventions — git, folder layout, deviation logging |
| `EXPERIMENTS.md` | Divergence register (memo spec vs. what we actually run) |

These should be created (or confirmed not needed) before PART B starts. The audit prompt also assumes a `code/python/` directory for scripts; the actual scripts are in `econ499r_starter/`. PART B will need to either move them or adjust references.

The `data/raw/` directory structure does not yet exist. All current data files are in `data/<source>/`. PART B step 1 ("Place the files") will create `data/raw/<source>/` and move files there.

---

## 5. Optional additions (strengthen the methods)

Ordered by impact:

1. **NOAA HDD/CDD** — weather control in robustness; 96 files; script
2. **NSF R&D Table 10, 2017–2023** — R&D moderator; 7 xlsx; script
3. **Epoch AI frontier data centers** — alt. AI/load measure; 1 CSV; script
4. **SEC company financials** — 58 utility/energy filers; run `sec_fin.py` with `SEC_USER_AGENT` set
5. **7 optional PUDL tables** — utility rate base, revenues, RUS co-ops; script
6. **Census ACS S2801 broadband** — broadband moderator; script with free `CENSUS_KEY`
7. **LBNL Utility-Scale Solar** — Georgia solar cost projection; browser
8. **AI patents (USPTO + PatentsView)** — alt. AI measure; browser (~764 MB)
9. **Bloomberg stock prices** — utility returns; Goizueta Business Library; licensed

---

## 6. How to resume (PART B)

1. Confirm with Shunji which gaps to fill first.
2. Create `CLAUDE.md`, `EXPERIMENTS.md`, and `prompts/00_START_HERE.md` (or confirm they are not needed).
3. Run `python econ499r_starter/download_all.py --core-only` to fetch the 33 missing BLS files + county adjacency. Place output in `data/raw/` (or adjust script's `RAW` path to `data/raw`).
4. Download LBNL RPS/CES by hand; drop in `data/raw/lbnl/`.
5. Download Q1–Q4 2024 large-load reports by hand; drop in `data/georgia_psc/`.
6. Then follow `02_data_audit_cleaning_excel.md` PART B: move all files to `data/raw/<source>/`, log moves, catalog, clean, build workbook and receipts, run walkthrough notebook.

Full detail in `data/DATA_AUDIT.md`.

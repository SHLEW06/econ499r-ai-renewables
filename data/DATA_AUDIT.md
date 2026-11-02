# Data Audit — ECON 499R
**As of:** 2026-11-01  
**Auditor:** Claude Code (Phase 2A)  
**Scope:** inventory, readability, completeness against methods. No cleaning or downloading done.

---

## 0. Setup notes

Four files referenced in `02_data_audit_cleaning_excel.md` do not yet exist and must be created before PART B:

| File | Status | Needed for |
|---|---|---|
| `prompts/00_START_HERE.md` | Missing | Phase orientation |
| `CLAUDE.md` | Missing | Project conventions, git setup |
| `EXPERIMENTS.md` | Missing | Divergence register |
| `docs/` directory | Created now (2026-11-01) | Handoffs |

The script is at `econ499r_starter/download_all.py`, not `code/python/download_all.py`. The `--raw-dir` and `--list` flags do not exist. Path layout from reading the script directly: files land in `raw/<source>/` relative to wherever the script runs.

Current data files sit in `data/<source>/` (Phase 1 organization). PART B will need to move them into `data/raw/<source>/` to match what `build_panel.py` expects.

---

## 1. File map — what we have vs. what the script expects

### 1a. EIA state-level files (core panel)

| Current path | Script target (`raw/`) | Size | Years | Readable | Notes |
|---|---|---|---|---|---|
| `data/eia/eia_generation_state_annual.xlsx` | `eia/annual_generation_state.xlsx` | 2.7 MB | 1990–2025 | ✓ | Covers 2015–2025 needed |
| `data/eia/eia_existing_capacity_annual.xlsx` | `eia/existcapacity_annual.xlsx` | 2.6 MB | 1990–2025 | ✓ | Covers 2015–2025 needed |
| `data/eia/eia_planned_capacity_annual.xlsx` | `eia/plancapacity_annual.xlsx` | 40 KB | Unknown | ✓ | Georgia outlook only |
| `data/eia/eia_form861_electricity_sales_2010_plus.xlsx` | `eia/HS861_2010-.xlsx` | 488 KB | 2010–2025 | ✓ | EC, EE, price control |
| `data/eia/eia_emissions_annual.xlsx` | `eia/emission_annual.xlsx` | 2.1 MB | 1990–2024 | ✓ | Ends 2024 (known) |
| `data/eia/eia_seds_energy_use_all_btu.csv` | `eia/seds/use_all_btu.csv` | 4.3 MB | 1960–2024 | ✓ | Ends 2024 (known) |
| — | `eia/annual_consumption_state.xlsx` | — | — | ✗ | **Missing** (optional fuel-use check) |

### 1b. BLS QCEW

| Current path | Script target (`raw/`) | Years have | Years needed | Readable | Notes |
|---|---|---|---|---|---|
| `data/bls/bls_qcew_518210_data_center_hosting.csv` | `bls/qcew_2025_518210.csv` | **2025 only** | 2014–2025 | ✓ | **11 years missing** |
| `data/bls/bls_qcew_5415_computer_systems_design.csv` | `bls/qcew_2025_5415.csv` | **2025 only** | 2014–2025 | ✓ | **11 years missing** |
| `data/bls/bls_qcew_10_all_industries.csv` | `bls/qcew_2025_10.csv` | **2025 only** | 2014–2025 | ✓ | **11 years missing** |
| — | `bls/qcew_{2014..2024}_518210.csv` (×11) | — | — | ✗ | **Missing** |
| — | `bls/qcew_{2014..2024}_5415.csv` (×11) | — | — | ✗ | **Missing** |
| — | `bls/qcew_{2014..2024}_10.csv` (×11) | — | — | ✗ | **Missing** |

**Total BLS gap: 33 files.** All fetchable by script (`download_all.py --core-only`, loops `range(2014, 2026)`).

### 1c. BEA

| Current path | Script target (`raw/`) | Size | Years | Readable | Notes |
|---|---|---|---|---|---|
| `data/bea/bea_sagdp_state_gdp.zip` | `bea/SAGDP.zip` | 10.4 MB | 1997–2025 (570 CSVs) | ✓ | GDP, manuf share |
| `data/bea/bea_sainc_state_income.zip` | `bea/SAINC.zip` | 17.6 MB | 1929–2025 (1017 CSVs) | ✓ | Population |

### 1d. Census

| Current path | Script target (`raw/`) | Size | Readable | Notes |
|---|---|---|---|---|
| `data/census/census_2020_gazetteer_counties.zip` | `census/gaz_counties.zip` | 142 KB | ✓ | Land area + centroids for W-distance |
| — | `census/county_adj.txt` | — | ✗ | **Missing — county adjacency for W-border** |

### 1e. FERC Form 1 (PUDL)

| Current path | Script target (`raw/`) | Size | Readable | Notes |
|---|---|---|---|---|
| `data/ferc/ferc1_income_statements_sched114.parquet` | `pudl/out_ferc1__yearly_income_statements_sched114.parquet` | 2.7 MB | ✓ | |
| `data/ferc/ferc1_plant_in_service_sched204.parquet` | `pudl/out_ferc1__yearly_plant_in_service_sched204.parquet` | 6.1 MB | ✓ | |
| `data/ferc/ferc1_all_plants.parquet` | `pudl/out_ferc1__yearly_all_plants.parquet` | 7.8 MB | ✓ | |
| `data/ferc/ferc1_steam_plants_fuel_sched402.parquet` | `pudl/out_ferc1__yearly_steam_plants_fuel_by_plant_sched402.parquet` | 1.1 MB | ✓ | |
| — | `pudl/out_ferc1__yearly_utility_plant_summary_sched200.parquet` | — | ✗ | Optional |
| — | `pudl/out_ferc1__yearly_rate_base.parquet` | — | ✗ | Optional |
| — | `pudl/out_ferc1__yearly_operating_revenues_sched300.parquet` | — | ✗ | Optional |
| — | `pudl/out_eia__yearly_utilities.parquet` | — | ✗ | Optional |
| — | `pudl/out_eia__yearly_plants.parquet` | — | ✗ | Optional |
| — | `pudl/out_rus12__yearly_statement_of_operations.parquet` | — | ✗ | Optional |
| — | `pudl/out_rus7__yearly_statement_of_operations.parquet` | — | ✗ | Optional |

### 1f. Georgia PSC

| Current path | Script target (`raw/`) | Readable | Notes |
|---|---|---|---|
| `data/georgia_psc/irp_2025_main_document.pdf` | `georgia/2025_IRP_Main_Document.pdf` | ✓ | |
| `data/georgia_psc/irp_2025_table_of_contents.pdf` | `georgia/2025_IRP_TOC.pdf` | ✓ | |
| `data/georgia_psc/irp_2025_one_page_summary.pdf` | `georgia/2025_IRP_one_page_summary.pdf` | ✓ | |
| `data/georgia_psc/irp_2023_update_main_document.pdf` | `georgia/2023_IRP_Update_Main_Document.pdf` | ✓ | |
| `data/georgia_psc/dkt55378_large_load_report_q1_2026.pdf` | `georgia/LargeLoad_Report_Q1_2026.pdf` | ✓ | Probable duplicate of script target |
| `data/georgia_psc/dkt55378_large_load_report_q1_2026_attachment.xlsx` | *(not in script)* | ✓ | Extra — browser download from PSC |
| `data/georgia_psc/dkt55378_large_load_report_q2_2026.zip` | *(not in script)* | ✓ | **Bonus.** 6 files: PDF + xlsx + assertion + cover letter. Q2 2026 is present. |
| `data/georgia_psc/irp_2025_public_disclosure.zip` | *(not in script)* | ✓ | **Bonus.** 81 files: full technical appendix volumes 1–3 |
| — | Q1–Q4 2024 large-load reports | ✗ | **Missing** (4 PDFs, browser, Docket 55378) |
| — | Q3 2026 large-load report | ? | Possibly not filed yet |
| — | Dockets 56298, 56310 (10,000 MW cert.) | ✗ | **Missing** (browser) |

### 1g. Other files present

| Current path | What it is | Notes |
|---|---|---|
| `data/data_download_all_pt1.zip` | RMI Utility Transition Hub (10 CSVs) | Browser download; not in script. Contents: customers_sales, operations_emissions, operations_emissions_by_tech, reliability, emissions_targets, assets_earnings_investments, housing_units_income, debt_equity_returns, net_plant_balance, expenditure_bills_burden. Assign to `data/raw/rmi/` in PART B. |
| `literature/Lazard_LCOE_Plus.pdf` | Lazard LCOE+ 2026 | Should be `data/raw/costs/Lazard_LCOEplus_2026.pdf` per script. Currently in wrong location. |
| `outputs/ECON499R_csv_for_R/` | Pre-built panel and W matrices | From prior session (Oct 30 / Nov 1 rebuild). Use only as a reference check — not a substitute for a clean rebuild. |
| `econ499r_starter/reference/` | Check values, prelim results, memo, Zhang paper | Use as ground truth for rebuild validation. |

---

## 2. Readability check

All files tested by magic-byte check (ZIP = `PK\x03\x04`, Parquet = `PAR1`, CSV = text header). All non-zip data files passed. Zip contents confirmed via `zipfile.ZipFile.namelist()`.

| File | Result |
|---|---|
| All 6 EIA xlsx/csv | ✓ OK |
| Both BEA zips (SAGDP, SAINC) | ✓ OK — valid zip, correct internal CSV naming |
| Census Gazetteer zip | ✓ OK |
| All 4 FERC parquets | ✓ OK (PAR1 magic bytes confirmed) |
| Both Georgia PSC zips | ✓ OK — real PDFs and xlsx inside |
| RMI zip | ✓ OK — 10 CSVs inside |
| BLS 3 CSV files | ✓ OK — correct QCEW column headers |
| EIA Form zips (860, 861, 923) | Not opened (form-level files, not needed for panel build) |

No corrupted, empty, or "Request Rejected" files found.

---

## 3. Completeness matrix

One row per required input. Status key: ✓ Ready · ⚠ Partial · ✗ Missing

### Steps 1–4 core

| Method step | Variable(s) | Source | File in `data/` | Years needed | Years have | Status | Gap |
|---|---|---|---|---|---|---|---|
| Step 1 outcome | ln_ec | EIA Form 861 | eia_form861_electricity_sales_2010_plus.xlsx | 2015–2025 | 2010–2025 | ✓ | — |
| Step 1 outcome | ln_ee | EIA Form 861 + BEA SAGDP | same + bea_sagdp_state_gdp.zip | 2015–2025 | Both ready | ✓ | — |
| Step 1 outcome | renew_share | EIA State Generation | eia_generation_state_annual.xlsx | 2015–2025 | 1990–2025 | ✓ | — |
| Step 1 outcome (extra) | solar_share | EIA State Generation | eia_generation_state_annual.xlsx | 2015–2025 | 1990–2025 | ✓ | — |
| Step 1 outcome (extra) | new_renew_mw | EIA Capacity | eia_existing_capacity_annual.xlsx | 2015–2025 | 1990–2025 | ✓ | — |
| **Step 1 cause (AI)** | **ai_dc_per1000** | **BLS QCEW 518210** | **bls_qcew_518210_data_center_hosting.csv** | **2014–2025** | **2025 only** | **✗** | **11 files** |
| **Step 1 AI denom.** | **total jobs** | **BLS QCEW ind. 10** | **bls_qcew_10_all_industries.csv** | **2014–2025** | **2025 only** | **✗** | **11 files** |
| Step 1 control | ln_gdp_pc | BEA SAGDP | bea_sagdp_state_gdp.zip | 2015–2025 | 1997–2025 | ✓ | — |
| Step 1 control | manuf_share | BEA SAGDP | bea_sagdp_state_gdp.zip | 2015–2025 | 1997–2025 | ✓ | — |
| Step 1 control | price_c_kwh | EIA Form 861 | eia_form861_electricity_sales_2010_plus.xlsx | 2015–2025 | 2010–2025 | ✓ | — |
| Step 1 control | pop_growth | BEA SAINC | bea_sainc_state_income.zip | 2015–2025 | 1929–2025 | ✓ | — |
| **Step 2a mediator** | **tech_share** | **BLS QCEW 5415** | **bls_qcew_5415_computer_systems_design.csv** | **2014–2025** | **2025 only** | **✗** | **11 files** |
| Step 2a mediator | hma | Derived (AI × tech_share) | Blocked by 5415 gap | 2015–2025 | — | ✗ | Blocked |
| Step 2b mediator | ln_ea (GDP/land area) | BEA SAGDP + Census Gaz. | Both ready | 2015–2025 | Both ready | ✓ | — |
| Step 3 spatial W | W-inverse-distance | Census Gazetteer (centroids) | census_2020_gazetteer_counties.zip | 2020 vintage | Present | ✓ | — |
| **Step 3 spatial W** | **W-border** | **Census County Adjacency** | **MISSING** | **2023** | **None** | **✗** | **1 file** |
| Step 4 robustness | fossil_to_renew | EIA State Generation | eia_generation_state_annual.xlsx | 2015–2025 | 1990–2025 | ✓ | — |
| Step 4 robustness | seds_mmbtu_pc | EIA SEDS | eia_seds_energy_use_all_btu.csv | 2015–2024 | 1960–2024 | ✓ (ends 2024) | — |
| **Step 4 robustness** | **RPS mandate** | **LBNL RPS/CES** | **MISSING** | **2015–2025** | **None** | **✗** | **Browser** |
| **Step 4 robustness** | **data_center_mw** | **Epoch / Cleanview** | **MISSING** | **2015–2025** | **None** | **✗** | **Script/Browser** |

### Financials

| Item | Source | File | Status | Gap |
|---|---|---|---|---|
| FERC income statements | PUDL | ferc1_income_statements_sched114.parquet | ✓ | — |
| FERC plant in service | PUDL | ferc1_plant_in_service_sched204.parquet | ✓ | — |
| FERC all plants | PUDL | ferc1_all_plants.parquet | ✓ | — |
| FERC steam plant fuel | PUDL | ferc1_steam_plants_fuel_sched402.parquet | ✓ | — |
| FERC optional tables (7) | PUDL | Missing | Optional ✗ | Script |
| SEC company facts (58 cos.) | SEC XBRL | Missing | Optional ✗ | `sec_fin.py` (needs `SEC_USER_AGENT`) |
| RMI Utility Transition Hub | RMI | data_download_all_pt1.zip (needs extraction) | ⚠ In zip | Move to `raw/rmi/` |
| Lazard LCOE+ 2026 PDF | Lazard | literature/Lazard_LCOE_Plus.pdf | ⚠ Wrong location | Move to `raw/costs/` |
| Bloomberg stock prices | Bloomberg | Missing | Optional ✗ | Browser (Emory license) |

### Georgia case box

| Item | File | Status | Gap |
|---|---|---|---|
| 2025 IRP main document | irp_2025_main_document.pdf | ✓ | — |
| 2025 IRP technical appendices | irp_2025_public_disclosure.zip | ✓ (bonus) | — |
| 2023 IRP Update | irp_2023_update_main_document.pdf | ✓ | — |
| Q1 2026 large-load report | dkt55378_large_load_report_q1_2026.pdf | ✓ | — |
| Q2 2026 large-load report | dkt55378_large_load_report_q2_2026.zip | ✓ (bonus) | — |
| Q1–Q4 2024 large-load reports | Missing | ✗ | 4 PDFs, browser (Docket 55378) |
| Q3 2026 large-load report | Missing | ? | May not be filed yet |
| Dockets 56298, 56310 (10k MW cert.) | Missing | Optional ✗ | Browser |

### Stretch variables

| Variable | Source | Status | Gap |
|---|---|---|---|
| NOAA HDD/CDD (48 states × 2) | NOAA NCEI | ✗ Missing | 96 CSV files, script |
| NSF R&D Table 10, 2017–2023 | NSF NCSES | ✗ Missing | 7 xlsx, script |
| Census ACS S2801 broadband | Census API | ✗ Missing | Script, needs `CENSUS_KEY` |
| AI patents (USPTO dataset) | USPTO | ✗ Missing | Browser (~764 MB) |
| PatentsView inventor locations | USPTO | ✗ Missing | Browser |
| Stanford AI Index job postings | Stanford HAI | ✗ Missing | Browser (selected states only) |
| LBNL Utility-Scale Solar | LBNL | ✗ Missing | Browser |
| Epoch frontier data centers | Epoch AI | ✗ Missing | Script |
| Cleanview data center tracker | Cleanview | ✗ Missing | Browser (may need account) |

---

## 4. Gap lists

### 4a. Required but missing or broken — ordered by which step they block first

| Priority | What | Blocks | Fetch method | Link from data_links.md |
|---|---|---|---|---|
| 1 | **BLS QCEW 518210, years 2014–2024** (11 files) | Steps 1–3: no AI measure | Script: `download_all.py --core-only` | `https://data.bls.gov/cew/data/api/{year}/a/industry/518210.csv` |
| 2 | **BLS QCEW industry 10, years 2014–2024** (11 files) | Steps 1–3: no AI denominator | Script: same run | `https://data.bls.gov/cew/data/api/{year}/a/industry/10.csv` |
| 3 | **BLS QCEW 5415, years 2014–2024** (11 files) | Step 2a: no tech_share | Script: same run | `https://data.bls.gov/cew/data/api/{year}/a/industry/5415.csv` |
| 4 | **Census county adjacency 2023** (1 file) | Step 3: no W-border matrix | Script: `download_all.py --core-only` | `https://www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2023.txt` |
| 5 | **LBNL RPS/CES spreadsheet** | Step 4 robustness (RPS control) | Browser | `https://emp.lbl.gov/projects/renewables-portfolio` |
| 6 | **Q1–Q4 2024 large-load reports** (4 PDFs) | Georgia case box completeness | Browser | Docket 55378: `https://psc.ga.gov/search/facts-docket/?docketId=55378` |

Items 1–4 can all be fetched with a single `python econ499r_starter/download_all.py --core-only` run (from the project root, after placing files in `data/raw/`).

### 4b. Optional additions — ordered by methods impact, then by effort

| Priority | What | What it adds | Effort | Fetch method | Link |
|---|---|---|---|---|---|
| 1 | **NOAA HDD/CDD** (96 files) | Weather control in robustness | Low — script | Script | NOAA Climate-at-a-Glance |
| 2 | **NSF R&D Table 10, 2017–2023** (7 xlsx) | R&D moderator (stretch H) | Low — script | Script | NSF NCSES |
| 3 | **Epoch AI frontier data centers** (1 CSV) | Alt. AI measure — large AI campuses only | Low — script | Script | `https://epoch.ai/data/data_centers/data_centers.csv` |
| 4 | **SEC company financials** (58 filers) | Finance side — utility balance sheets | Medium — run `sec_fin.py`, set `SEC_USER_AGENT` | Script | SEC XBRL API |
| 5 | **7 optional PUDL tables** | Utility rate base, revenues, RUS co-ops | Low — script | Script | `pudl.catalyst.coop/stable/` |
| 6 | **Census ACS S2801 broadband** | Broadband moderator (stretch G) | Low — script, needs free `CENSUS_KEY` | Script | `https://api.census.gov/data/key_signup.html` |
| 7 | **LBNL Utility-Scale Solar** | Georgia solar cost projection module | Medium — read, extract GA data | Browser | `https://emp.lbl.gov/utility-scale-solar` |
| 8 | **AI patents (USPTO + PatentsView)** | Alternative AI measure (through 2023) | High — large download (~764 MB), joins needed | Browser | USPTO Open Data Portal |
| 9 | **Cleanview data center tracker** | Alt. AI/load measure — 50-state capacity | Medium — may need account | Browser | `https://www.cleanview.co/data-centers` |
| 10 | **Stanford AI Index job postings** | Alt. AI measure — selected states only | Low — but limited state coverage | Browser | `https://hai.stanford.edu/ai-index` |
| 11 | **Bloomberg stock prices** | Finance side — utility returns | Medium — by hand at Goizueta | Browser (licensed) | Emory Goizueta Business Library |

---

## 5. Pre-built outputs (prior session)

`outputs/ECON499R_csv_for_R/` contains a complete set of processed files from the Oct 30 / Nov 1 build. Do not treat these as raw data. Use them only to validate the rebuild:

| File | Rows | Columns | Note |
|---|---|---|---|
| `state_panel_2015_2025.csv` | 561 | 80 | 50 states + DC × 11 years |
| `ferc1_cost_by_technology.csv` | — | — | From `ferc_fin.py` |
| `ferc1_plant_costs.csv` | — | — | From `ferc_fin.py` |
| `ferc1_utility_financials.csv` | — | — | From `ferc_fin.py` |
| `sec_company_financials.csv` | — | — | 58 SEC filers |
| `state_centroids_land.csv` | — | — | From Census Gazetteer |
| `W_border_binary.csv` | — | — | Border W |
| `W_distance_miles.csv` | — | — | Distance W |
| `W_inverse_distance_rowstd.csv` | — | — | Row-standardized inverse-distance W |

Check values are in `econ499r_starter/reference/expected_values.md`, `prelim_means_by_year.csv`, `prelim_morans_i.csv`, and `prelim_step1_slx.csv`.

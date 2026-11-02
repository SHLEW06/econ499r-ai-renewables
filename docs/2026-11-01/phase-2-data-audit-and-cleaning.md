# Phase 2 handoff — data audit and cleaning
**Date:** 2026-11-01  
**Project:** ECON 499R — AI and Renewable Energy, U.S. states 2015–2025  
**Team:** Shunji Lewandowski (modeling) · Alexander Hendricks (data and finance)  
**Next prompt:** `prompts/04_models.md` (Phase 4 — R models)

---

## 1. What was done

### Phase 2A — Data audit
- Mapped every file in `data/` to its script target; verified readability; built requirements matrix.
- Found critical gap: BLS QCEW files for 2014–2024 missing (only 2025 present); Census county adjacency missing.
- Wrote `data/DATA_AUDIT.md` and `docs/2026-11-01/phase-2a-data-audit.md`.

### Phase 2B — File placement, downloads, build
- Created `data/raw/<source>/` directory structure.
- Copied 26 existing files from `data/<source>/` to `data/raw/<source>/` with script-expected names.
- Downloaded 33 missing BLS QCEW files (years 2014–2024 for NAICS 518210, 5415, and industry 10) directly into `data/raw/bls/`.
- Downloaded Census county adjacency 2023 (`county_adj.txt`) into `data/raw/census/`.
- Downloaded `out_eia__yearly_utilities.parquet` (needed by `ferc_fin.py`) into `data/raw/pudl/`.
- Extracted BEA zips to `data/raw/bea/sagdp/` and `data/raw/bea/sainc/`.
- Extracted Census Gazetteer zip; extracted RMI CSVs to `data/raw/rmi/`.
- Moved Lazard PDF from `literature/` to `data/raw/costs/`.
- Logged all moves and downloads in `logs/2026-11-01/phase2_moves.csv` (61 entries with SHA256).

### Panel build
Ran `python3 econ499r_starter/scripts/build_panel.py data/raw data/out`.

**Output: `data/out/state_panel_2015_2025.csv` — 561 rows × 80 columns.**

Validation against expected values (context handoff):

| Check | Expected | Got | Pass? |
|---|---|---|---|
| Shape | (561, 80) | (561, 80) | ✓ |
| GA renew_share 2015 | 6.1% | 6.09% | ✓ |
| GA renew_share 2025 | 12.9% | 12.87% | ✓ |
| GA solar_share 2025 | 7.7% | 7.68% | ✓ |
| GA 2025 generation mix (gas/nuclear/coal/solar) | 38.6 / 35.2 / 13.7 / 7.7% | exact match | ✓ |
| Suppressed cells (AK, ND, SD, WY 2025) | 4 | 4 | ✓ |
| CO2 / SEDS 2025 missing | 51 each | 51 each | ✓ |

Also built:
- `data/out/W_distance_miles.csv` (50×50 great-circle distance matrix)
- `data/out/W_inverse_distance_rowstd.csv` (50×50 row-standardized)
- `data/out/W_border_binary.csv` (50×50 binary contiguity)
- `data/out/state_centroids_land.csv`
- `data/out/ferc1_utility_financials.csv` (2,366 rows × 25 cols)
- `data/out/ferc1_plant_costs.csv` (21,332 rows × 24 cols)
- `data/out/ferc1_cost_by_technology.csv` (153 rows × 10 cols)

### Documentation built
- `CLAUDE.md` — project conventions, folder layout, rebuild commands, known caveats
- `EXPERIMENTS.md` — divergence register (EXP-001 through EXP-006)
- `data/DATA_INDEX.md` — index of all raw and built files
- `data/DATA_AUDIT.md` — updated from Phase 2A
- `data/receipts/<source>.md` — per-source receipts (bls_qcew, eia_state, bea, census, ferc_pudl, georgia_psc, lazard, rmi, eia_forms)
- `outputs/ECON499R_Data_Workbook_2026-11-01.xlsx` — 12-tab Excel workbook for Alexander (README, Core Panel with live formulas, Full Panel, Codebook, Prelim Results, FERC1 Utilities, FERC1 Cost by Tech, FERC1 Plants, SEC Companies, W Inverse Distance, W Border, Sources)
- `notebooks/02_data_and_methods_walkthrough.ipynb` — Jupyter walkthrough

---

## 2. What's still missing

### Blocks Step 4 robustness
- **LBNL RPS/CES spreadsheet** — needed for RPS control variable (EXP-003). Browser download: https://emp.lbl.gov/projects/renewables-portfolio ("RPS & CES Targets and Demand" XLSX). Drop in `data/raw/lbnl/`.

### Georgia case box (not blocking models)
- Q1–Q4 2024 large-load reports (4 PDFs). Browser: Docket 55378 at https://psc.ga.gov/search/facts-docket/?docketId=55378
- Q3 2026 large-load report (may not be filed yet; check same docket page)

### Optional / stretch
- NOAA HDD/CDD: `python econ499r_starter/download_all.py` (non-core, 96 CSV files)
- NSF R&D Table 10: same run
- Epoch AI frontier data centers: same run
- SEC company financials: `python econ499r_starter/scripts/sec_fin.py data/raw/sec data/out/sec_company_financials.csv` (set `SEC_USER_AGENT="Shunji Lewandowski your@email"` first). Current `data/out/sec_company_financials.csv` is from the Oct 30 prior session.
- Census ACS S2801 broadband: script, needs free `CENSUS_KEY`
- Bloomberg stock prices: browser, Goizueta Business Library

---

## 3. Deviations from Methods Memo (see EXPERIMENTS.md)

EXP-001 (tech_share vs. HMA): under review — run both in Step 2, log.  
EXP-002 (SDM impacts): adopted — report direct/indirect/total, not just theta.  
EXP-003 (RPS control): under review — blocked by missing LBNL file.  
EXP-004 (AI squared): under review — include as extra robustness column.  
EXP-005 (alternative AI measure): under review — needs patent/posting data.

---

## 4. Key Georgia Power data points (FERC Form 1, 2025)

| Item | Value |
|---|---|
| Electric operating revenue | $12,264M |
| Electric operating income | $3,398M |
| Operating margin | 27.7% |
| Net income | $2,851M |
| Total plant in service | $61,250M |
| Nuclear plant | $13,016M |
| Production fossil share | 48.1% |
| Production renewable share | 6.7% (FERC definition, excludes wood biomass) |

---

## 5. How to resume — Phase 4 (R models)

1. The panel is ready: `data/out/state_panel_2015_2025.csv` (561 × 80).
2. The W matrices are ready: `data/out/W_inverse_distance_rowstd.csv` and `W_border_binary.csv`.
3. Open `econ499r_starter/R/econ499r_step1_to_3.R` and update the paths to point to `data/out/`.
4. Before running, match the Python prelim results in `data/out/prelim_step1_slx.csv` and `prelim_morans_i.csv`.
5. Follow `prompts/04_models.md` (to be created) — or adapt from `econ499r_starter/CLAUDE_CODE_PROMPT.md` tasks B through D.
6. Log any spec deviations in `EXPERIMENTS.md` before running.
7. Deadline: Steps 1–3 done by **Nov 17, 2026**.

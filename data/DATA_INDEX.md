# Data Index

All paths are relative to the project root.
Last updated: 2026-11-01.

---

## 1. Raw Data (`data/raw/`)

| Folder | File(s) | What it is | Years | Used for | Script to rebuild | Receipt |
|--------|---------|------------|-------|----------|-------------------|---------|
| `data/raw/eia/` | `annual_generation_state.xlsx`, `existcapacity_annual.xlsx`, `plancapacity_annual.xlsx`, `emission_annual.xlsx`, `HS861_2010-.xlsx` | EIA state electricity: generation, existing capacity, planned capacity, emissions, retail sales | 1990–2025 (emissions ends 2024) | `renew_share`, `solar_share`, `new_renew_mw`, `ln_ec`, `ln_ee`, `price_c_kwh`, `fossil_to_renew` | `download_all.py` | [receipts/eia_state.md](receipts/eia_state.md) |
| `data/raw/eia/seds/` | `use_all_btu.csv` | EIA SEDS total energy consumption by state | 1960–2024 | `seds_mmbtu_pc` (Step 4 robustness) | `download_all.py` | [receipts/eia_seds.md](receipts/eia_seds.md) |
| `data/raw/bls/` | `qcew_{2014..2025}_{518210,5415,10}.csv` (36 files) | BLS QCEW annual employment by NAICS code | 2014–2025 | `ai_dc_per1000`, `tech_share`, `total_jobs` | `download_all.py` | [receipts/bls_qcew.md](receipts/bls_qcew.md) |
| `data/raw/bea/` | `SAGDP.zip` + `sagdp/*.csv`, `SAINC.zip` + `sainc/*.csv` | BEA State GDP and State Personal Income | 1997–2025 (GDP), 1929–2025 (income) | `ln_gdp_pc`, `manuf_share`, `pop_growth`, `ln_ea` | `download_all.py` | [receipts/bea.md](receipts/bea.md) |
| `data/raw/census/` | `gaz_counties.zip`, `2020_Gaz_counties_national.txt`, `county_adj.txt` | Census 2020 county Gazetteer + 2023 county adjacency file | 2020 / 2023 | `land_sqmi`, W-distance matrix, W-border matrix | `download_all.py` | [receipts/census.md](receipts/census.md) |
| `data/raw/pudl/` | `out_ferc1__yearly_*.parquet` (4 files) + `out_eia__yearly_utilities.parquet` | FERC Form 1 via Catalyst Cooperative PUDL | 2015–2025 | Utility financials, plant costs, finance side | `download_all.py` | [receipts/ferc_pudl.md](receipts/ferc_pudl.md) |
| `data/raw/georgia/` | `2025_IRP_Main_Document.pdf`, `2025_IRP_TOC.pdf`, `2025_IRP_one_page_summary.pdf`, `2023_IRP_Update_Main_Document.pdf`, `LargeLoad_Report_Q1_2026.pdf` | Georgia Power IRP filings and Large Load reports | 2023, 2025, Q1 2026 | Georgia case box | `download_all.py` (main docs) + browser (Q2 extras) | [receipts/georgia_psc.md](receipts/georgia_psc.md) |
| `data/raw/costs/` | `Lazard_LCOEplus_2026.pdf` | Lazard LCOE+ 2026 report | 2026 | Cost benchmarks for case box | `download_all.py` | [receipts/lazard.md](receipts/lazard.md) |
| `data/raw/rmi/` | 10 CSVs (`customers_sales`, `operations_emissions`, etc.) | RMI Utility Transition Hub | Through ~2024 | Finance side (optional) | Browser download | [receipts/rmi.md](receipts/rmi.md) |
| `data/raw/eia_forms/` | `eia8602025.zip`, `f8612025.zip`, `f923_2025.zip`, `september_generator2026.xlsx` | EIA Forms 860 / 861 / 923 (plant- and utility-level) | 2025–2026 | Plant-level detail (optional) | `download_all.py --with-eia-forms` | [receipts/eia_forms.md](receipts/eia_forms.md) |

---

## 2. Built Outputs (`data/out/`)

| File | Rows x Cols | Built by | Description |
|------|-------------|----------|-------------|
| `state_panel_2015_2025.csv` | 561 x 80 | `build_panel.py` | Main state-year panel (50 states + DC, 2015–2025). All model variables. |
| `W_distance_miles.csv` | 50 x 50 | `build_panel.py` | Pairwise great-circle distances (miles) between state centroids, 50 states only (no DC). |
| `W_inverse_distance_rowstd.csv` | 50 x 50 | `build_panel.py` | Row-standardized inverse-distance weight matrix W. |
| `W_border_binary.csv` | 50 x 50 | `build_panel.py` | Binary contiguity matrix (1 if states share a county border). AK and HI have no neighbors. |
| `state_centroids_land.csv` | 50 x 3 | `build_panel.py` | Population-weighted state centroids (lat, lon) and land area (sq miles). |
| `ferc1_utility_financials.csv` | 2,366 x 25 | `ferc_fin.py` | Annual utility-level financials from FERC Form 1 (revenue, expenses, plant value by type). |
| `ferc1_plant_costs.csv` | 21,332 x 24 | `ferc_fin.py` | Plant-level capital and operating costs, 2015–2025. |
| `ferc1_cost_by_technology.csv` | 153 x 10 | `ferc_fin.py` | Technology-level cost summary (capex/kW, opex/MWh, capacity factor) by year. |

---

**Note on reference outputs:** `outputs/ECON499R_csv_for_R/` contains a prior session build (Oct 30 / Nov 1). Use only to cross-check the rebuild — do not treat these as inputs to any script.

# Receipt: RMI Utility Transition Hub

**Source:** Rocky Mountain Institute, Utility Transition Hub  
**Link:** https://utilitytransitionhub.rmi.org/data-download/  
**How:** Browser download (site blocks scripts). Obtained as `data_download_all_pt1.zip`.  
**Downloaded:** Prior to 2026-11-01 (exact date unknown)  
**File:** `data/data_download_all_pt1.zip` → extracted to `data/raw/rmi/` (10 CSV files)

## Files inside the zip

| File | Description |
|---|---|
| `customers_sales.csv` | Utility customers and electricity sales by customer class |
| `operations_emissions.csv` | Generation, fuel mix, and CO2 emissions |
| `operations_emissions_by_tech.csv` | Same, broken out by technology |
| `reliability.csv` | System average interruption metrics (SAIDI/SAIFI) |
| `emissions_targets.csv` | Utility-reported emissions reduction targets |
| `assets_earnings_investments.csv` | Utility assets, net income, capex |
| `housing_units_income.csv` | Customers by income tier and housing type |
| `debt_equity_returns.csv` | Utility capital structure and ROE |
| `net_plant_balance.csv` | Net plant in service by category |
| `expenditure_bills_burden.csv` | Bill burden metrics by income decile |

## What we kept

All 10 files extracted and available for the finance side of the analysis (optional). Not yet integrated into the panel or any model step.

## Known quirks

- Coverage is investor-owned utilities only; co-ops and municipals not included.
- Vintage and exact release date unknown from the zip. Check the RMI website for the current data version before citing.
- Two macOS artifact files (`._*.csv`) in the zip were excluded during extraction.

## Output

`data/raw/rmi/*.csv` — 10 flat files, available for Phase 2B catalog and any financial analysis. No panel-level output yet.

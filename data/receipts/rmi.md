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

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 12 files.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/rmi/._operations_emissions.csv` | 829 | `f5694ed69413fff3e01e24ec9620c487a718c9671f4ebd7db58fb323e63903c1` |
| `data/raw/rmi/._operations_emissions_by_tech.csv` | 313 | `aacd5fde0c1f606d7f07c127cede539c4d904cf796e0aae4780c907f90dedd60` |
| `data/raw/rmi/assets_earnings_investments.csv` | 89,642,705 | `31d27728fd7b0f96fde13d2ce0dbe324972106c8e5f59254f5c8769bd05e7d0f` |
| `data/raw/rmi/customers_sales.csv` | 4,020,732 | `7c773bef3770ff12da8bc8ca95cf882db9ad6ee33c75a886b1e808f3e9bf2b71` |
| `data/raw/rmi/debt_equity_returns.csv` | 2,138,518 | `e54c4914af5b30d7bdfc85c2f3a227bf99cb6e4b8f78e611cedc658604109cbf` |
| `data/raw/rmi/emissions_targets.csv` | 1,727,385 | `2b21a74050993238db5938305d333ac6932ed4fbc01266cd477fa2b10c515341` |
| `data/raw/rmi/expenditure_bills_burden.csv` | 31,326,325 | `00751d4bdd71e92e5011c6e52c40a1c0c9aaf7865c14f8d722e7de0692e7eb83` |
| `data/raw/rmi/housing_units_income.csv` | 2,001,126 | `cbefe972eefe8c77d4a11f60473670763f72d7d44bf8804340c4515c1de6b906` |
| `data/raw/rmi/net_plant_balance.csv` | 3,040,809 | `61534f51d8eac14758797441c655b0ed21aad20f5f54ce4389cbbb6778386093` |
| `data/raw/rmi/operations_emissions.csv` | 122,758,176 | `18321a2e8f971940b4e6097d3d2ca410eaa2bfb46e2f78d3429f87ae4cd29eb9` |
| `data/raw/rmi/operations_emissions_by_tech.csv` | 241,934,274 | `991387b996f9cd4d7cd25851968ffaea46339aa5ba2ddf37112b4293611fc84a` |
| `data/raw/rmi/reliability.csv` | 4,167,111 | `04ff7c30bc8522ababf871ab420c1f9d099c5f67eb4b1935a854ba582a6db5d5` |

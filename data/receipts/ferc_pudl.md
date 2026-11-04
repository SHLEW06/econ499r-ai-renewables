# Receipt: FERC Form 1 via Catalyst Cooperative PUDL

## Source

Catalyst Cooperative, Public Utility Data Liberation (PUDL) project.
Stable release S3 bucket: `s3://pudl.catalyst.coop/stable/`
Direct HTTPS access: `https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/`

FERC Form 1 is a mandatory annual report filed by major US electric utilities covering income,
balance sheet, plant in service, fuel costs, and more.

## Raw Files

| File | Description | Approx. size | Downloaded |
|---|---|---|---|
| `data/raw/pudl/out_ferc1__yearly_income_statements_sched114.parquet` | Utility income and expense statements (FERC Sched 114) | ~15 MB | 2026-11-01 |
| `data/raw/pudl/out_ferc1__yearly_plant_in_service_sched204.parquet` | Plant-in-service balances by account (FERC Sched 204) | ~25 MB | 2026-11-01 |
| `data/raw/pudl/out_ferc1__yearly_all_plants.parquet` | All plant records with technology type | ~30 MB | 2026-11-01 |
| `data/raw/pudl/out_ferc1__yearly_steam_plants_fuel_by_plant_sched402.parquet` | Steam plant fuel receipts and costs (FERC Sched 402) | ~10 MB | 2026-11-01 |
| `data/raw/pudl/out_eia__yearly_utilities.parquet` | EIA utility metadata (crosswalk to FERC respondent IDs) | ~2 MB | 2026-11-01 |

Script: `download_all.py`.

## Coverage

- FERC Form 1 filers: large electric utilities (generally >1 TWh annual sales).
- Years in PUDL stable release: 2015–2025 (earlier years available but not extracted here).

## Key Tables and Variables

**Income statements (Sched 114)**
- `operating_revenues` — total utility operating revenues
- `operating_expenses` — total O&M, depreciation, taxes
- `net_income` — bottom-line net income

**Plant in service (Sched 204)**
- Accounts map to technology categories (steam/nuclear/hydro/other production/transmission/distribution)
- Used to compute plant value by type for each utility-year

**All plants**
- `capacity_mw`, `net_generation_mwh`, `fuel_type_code_pudl` — plant-level generation and capacity
- `utility_id_ferc1`, `plant_id_ferc1`, `report_year`

**Steam plant fuel (Sched 402)**
- `fuel_cost_per_mmbtu`, `fuel_mmbtu_per_unit` — fuel cost inputs for thermal efficiency metrics

## Deduplication Strategy

PUDL produces both `reported_value` and `calculated_value` columns for some fields.

- Keep `reported_value` over `calculated_value` when both are non-null.
- Drop rows where `record_type = 'correction'` (these are amendments that PUDL tags separately;
  the original reported row is kept).
- For plant records, drop duplicates on `(utility_id_ferc1, plant_id_ferc1, report_year)`
  keeping the most recently filed record.

## Transformations

1. Join all-plants to EIA utility crosswalk via `utility_id_ferc1` → `utility_id_eia` to get
   state and ownership type.
2. Aggregate plant-level data to utility-year level for `ferc1_utility_financials.csv`.
3. Compute technology-level averages (`ferc1_cost_by_technology.csv`) by grouping on
   `fuel_type_code_pudl` and `report_year`.
4. All dollar values are as-reported (nominal). For real comparisons, deflate externally using
   the GDP deflator from BEA.

## Rows In / Out

| Parquet file | Input rows (approx.) | Output rows |
|---|---|---|
| income_statements | ~35,000 | — |
| all_plants | ~280,000 | 21,332 (plant-cost file) |
| plant_in_service | ~95,000 | — |
| Combined utility-year | — | 2,366 (financials file) |
| Tech-year aggregate | — | 153 (cost-by-tech file) |

## Known Quirks

- FERC Form 1 filers represent roughly 60–70% of total US utility-scale generation; smaller
  cooperatives and municipal utilities are excluded.
- PUDL may restate historical values between stable releases. The 2026-11-01 download should
  be used consistently; do not mix with older downloads.
- A small number of utilities report in fiscal years not aligned to calendar year — PUDL
  normalizes these to calendar year but flags them with `is_noncalendar_year`.

## Output Files

| File | Rows x Cols | Description |
|---|---|---|
| `data/out/ferc1_utility_financials.csv` | 2,366 x 25 | Annual utility-level revenues, expenses, plant value by type |
| `data/out/ferc1_plant_costs.csv` | 21,332 x 24 | Plant-level capital and operating costs, 2015–2025 |
| `data/out/ferc1_cost_by_technology.csv` | 153 x 10 | Capex/kW, opex/MWh, capacity factor by technology and year |

## Script

`scripts/ferc_fin.py`, after `download_all.py`.

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 5 files.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/pudl/out_eia__yearly_utilities.parquet` | 1,678,289 | `cb8298ee84242808dadeae309bd398b256f64804881ac444230d681ecaf8e276` |
| `data/raw/pudl/out_ferc1__yearly_all_plants.parquet` | 7,799,175 | `a5c3085527e70e6e721e6de3243dcc49ae7fd0a003b79e263aea0d55616a856a` |
| `data/raw/pudl/out_ferc1__yearly_income_statements_sched114.parquet` | 2,668,969 | `e586a147267ad9a02ac1cae3137d3acd53dfab1e630fdb22855068ac1ba99efe` |
| `data/raw/pudl/out_ferc1__yearly_plant_in_service_sched204.parquet` | 6,142,375 | `de406e1cfdee90cbdca1e5f1c70c808a5e72a8a0fda89530c57a991bb1f23e82` |
| `data/raw/pudl/out_ferc1__yearly_steam_plants_fuel_by_plant_sched402.parquet` | 1,052,704 | `4fa8fce9462f109ac8372eda4385b3f36ac63a14386a70f97f8dd7438876606a` |

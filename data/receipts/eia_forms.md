# Receipt: EIA Forms 860, 861, and 923

## Source

U.S. Energy Information Administration, Electric Power Survey forms.
- Form EIA-860 (Annual Electric Generator Report): `https://www.eia.gov/electricity/data/eia860/`
- Form EIA-861 (Annual Electric Power Industry Report): `https://www.eia.gov/electricity/data/eia861/`
- Form EIA-923 (Power Plant Operations Report): `https://www.eia.gov/electricity/data/eia923/`

## Added 2026-11-04

`data/raw/eia_forms/eia8602017.zip`, 16,181,258 bytes, sha256 `da9f1a1f8528324ff47019229d0f3648efe8c5997f18449f10d6aad2daa68e5c`, from https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602017.zip . Used only to identify the 2017 blank-fuel rows (`data/receipts/eia_state.md`). It doesn't enter the panel.

## Raw Files

| File | Description | Approx. size | Downloaded |
|---|---|---|---|
| `data/raw/eia_forms/eia8602025.zip` | EIA-860 2025 annual data (generator, plant, utility schedule) | ~15 MB | 2026-11-01 |
| `data/raw/eia_forms/f8612025.zip` | EIA-861 2025 annual data (retail sales, customers, revenue by utility) | ~5 MB | 2026-11-01 |
| `data/raw/eia_forms/f923_2025.zip` | EIA-923 2025 monthly generation and fuel data | ~20 MB | 2026-11-01 |
| `data/raw/eia_forms/september_generator2026.xlsx` | EIA-860M monthly update, September 2026 generator inventory | ~3 MB | 2026-11-01 |

Script: `download_all.py --with-eia-forms` (flag required; not downloaded in default run).

## Coverage

- EIA-860 / 861 / 923: full-year 2025 data.
- EIA-860M (September 2026): plant-level generator inventory as of September 2026, including
  planned additions and retirements through the forecast horizon.

## Contents Overview

**EIA-860 (Form 860)** — Plant and generator characteristics:
- Generator schedule: unit-level nameplate capacity, prime mover, energy source, online/retirement dates.
- Plant schedule: plant location (lat/lon, state, county), ownership.
- Utility schedule: utility type and ownership.

**EIA-861 (Form 861)** — Retail sales and revenue:
- Sales (MWh), revenue ($), and customers by utility, state, and sector.
- Note: the state-level version of this data is already in `data/raw/eia/HS861_2010-.xlsx`
  (see `receipts/eia_state.md`). The zipped form here provides utility-level granularity.

**EIA-923 (Form 923)** — Monthly plant operations:
- Net generation by plant, prime mover, and fuel type.
- Fuel receipts, quantities, and costs (Schedule 2).
- Boiler fuel consumption (Schedule 3).

**EIA-860M (September 2026)** — Forward-looking generator inventory:
- All operating, planned, and retired generators as of the most recent monthly update.
- Useful for tracking announced renewable additions in the pipeline.

## Status: Optional

These files provide plant-level detail not needed for the main state-year panel. They are
downloaded and available for:
- Cross-checking `renew_share` and `new_renew_mw` against plant-level rollups.
- Building a plant-level panel for robustness or mechanism analysis.
- Identifying data-center-adjacent generation additions at the county level.

No script currently processes these into `data/out/` files. If plant-level analysis is
added in Phase 2B, a new script (`build_plant_panel.py` or similar) should be created.

## Known Quirks

- EIA-860 and EIA-923 use different plant ID formats in some years. Always join on
  `Plant_Code` (EIA plant ID), not on plant name strings.
- The September 2026 EIA-860M is a preliminary monthly snapshot. Generator status fields
  (`Operating Status`) may differ from the final 2025 annual release in `eia8602025.zip`.
- EIA-923 Schedule 2 (fuel receipts) covers only steam-electric plants above 50 MW and
  combined-cycle plants above 100 MW; smaller generators are excluded.
- Zips must be fully extracted before reading; nested ZIPs occur in some 923 releases.

## Output

No current tabular output in `data/out/`. Files available in `data/raw/eia_forms/` for
future plant-level analysis.

## Script

`download_all.py --with-eia-forms` fetches the four files. No processing script yet.

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 4 files.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/eia_forms/eia8602025.zip` | 23,622,347 | `2b27929d26cc1da9ad6a530da1cac6718cd8496098ee560c4d47cfffd96d08ba` |
| `data/raw/eia_forms/f8612025.zip` | 4,756,816 | `f59f6c732bf685fe0a1591b32227f5ce572dc0dfd26bb5caaeed128ac4e3a396` |
| `data/raw/eia_forms/f923_2025.zip` | 23,340,452 | `1bff7092a86f6678c069c986829da5a23104048fc1aafb65b0776e3c904284de` |
| `data/raw/eia_forms/september_generator2026.xlsx` | 14,013,970 | `bcef74e1af991680731aeecfda967f5950db4ce739bb584edd8b8774c7e6da17` |

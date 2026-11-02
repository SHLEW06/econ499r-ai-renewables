# Receipt: EIA State Electricity Data

## Source

U.S. Energy Information Administration, Electricity Data by State.
URL: `https://www.eia.gov/electricity/data/state/`

## Raw Files

| File | Description | Approx. size | Downloaded |
|---|---|---|---|
| `data/raw/eia/annual_generation_state.xlsx` | Annual net generation by state, fuel, and sector | ~4 MB | 2026-11-01 |
| `data/raw/eia/existcapacity_annual.xlsx` | Existing nameplate capacity by state, fuel, and sector | ~2 MB | 2026-11-01 |
| `data/raw/eia/plancapacity_annual.xlsx` | Planned capacity additions and retirements | ~1 MB | 2026-11-01 |
| `data/raw/eia/emission_annual.xlsx` | CO2, SO2, NOx emissions by state and fuel | ~1 MB | 2026-11-01 |
| `data/raw/eia/HS861_2010-.xlsx` | Form EIA-861 retail sales, revenue, and customers by state | ~5 MB | 2026-11-01 |

Script: `download_all.py`.

## Coverage

- Generation, capacity, sales: 1990–2025.
- Emissions: 1990–2024 (2025 not yet published as of download date).

## Filters Applied

**Generation and capacity files:** Keep rows where `SECTOR` (or equivalent column) equals
`'Total Electric Power Industry'`. This aggregates across utility, independent power producer,
and combined-heat-and-power sectors.

**Emissions file:** Keep state-level rows; drop rows for individual facilities or fuel subtypes
not needed for the panel.

**Sales/revenue (EIA-861):** Keep state totals for all sectors; use to compute
`price_c_kwh = revenue_000usd / sales_mwh * 100`.

## Key Transformations

1. **Generation pivot:** Pivot fuel-source rows into columns. Aggregate renewable fuels
   (wind, utility-scale solar PV, conventional hydroelectric, geothermal, biomass) into
   `renew_gen_mwh`; aggregate fossil fuels (coal, natural gas, petroleum) into `fossil_gen_mwh`.
2. `renew_share = renew_gen_mwh / total_gen_mwh`
3. `solar_share = solar_gen_mwh / total_gen_mwh`
4. `fossil_to_renew = fossil_gen_mwh / renew_gen_mwh` (set to NA if `renew_gen_mwh = 0`)
5. **Capacity:** From `existcapacity_annual.xlsx`, compute `new_renew_mw` as the year-on-year
   change in renewable nameplate capacity per state. From `plancapacity_annual.xlsx`, extract
   announced renewable additions as a forward-looking variable.
6. **Electricity consumption:** From `HS861_2010-.xlsx`, extract total retail sales (MWh) for
   `ln_ec` (log electricity consumption) and compute `ln_ee` (log electricity intensity) by
   dividing by state real GDP.
7. **Emissions:** Compute `ln_co2` from `emission_annual.xlsx` CO2 totals by state.

## Known Quirks

- **Rooftop solar excluded:** The generation file covers utility-scale plants only. Residential
  and commercial rooftop solar is not captured in `renew_gen_mwh` or `solar_share`. This
  understates renewable generation in states with high rooftop adoption (CA, NJ, MA).
  Note this limitation when discussing `solar_share`.
- **Fuel category labels vary by year:** Pre-2008 files use slightly different fuel string
  labels. Harmonize via a lookup dictionary in `build_panel.py`.
- **EIA-861 sector breakdown changed in 2013:** Prior to 2013, some states report combined
  residential+commercial totals. Use the "Total" row to avoid breaks.

## Output Columns

`renew_share`, `solar_share`, `fossil_to_renew`, `new_renew_mw`, `ln_ec`, `ln_ee`,
`price_c_kwh`, `ln_co2`

## Script

`scripts/build_panel.py` (EIA electricity section), after `download_all.py`.

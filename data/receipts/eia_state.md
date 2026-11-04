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

- Generation and capacity: 1990–2025. Sales: 2010–2025 (`HS861_2010-.xlsx`).
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

1. **Generation pivot:** pivot fuel-source rows into columns. `gen_renew_mwh` = hydro + wind + solar + geothermal + wood + other biomass. `gen_fossil_mwh` = coal + natural gas + petroleum + Other Gases.
2. `renew_share = gen_renew_mwh / gen_total_mwh`
3. `solar_share = gen_solar_mwh / gen_total_mwh`
4. `fossil_to_renew = gen_fossil_mwh / gen_renew_mwh` (NA if `gen_renew_mwh = 0`)
5. **Capacity:** from `existcapacity_annual.xlsx`, `new_renew_mw` is the year-on-year change in renewable nameplate capacity by state. `plancapacity_annual.xlsx` is downloaded but not used in the panel.
6. **Electricity consumption:** from `HS861_2010-.xlsx`, `ln_ec = log(sales_mwh / population)`.
7. **Efficiency:** `ee_usd_per_mwh = gdp_real_musd2017 * 1e6 / sales_mwh`; `ln_ee = log(ee_usd_per_mwh)`. This is log real GDP per MWh sold (`build_panel.py` lines 158-159). Higher means more output per unit of electricity. It is the inverse of electricity intensity.
8. **Emissions:** `co2_power_t` is the CO2 total, and `co2_per_mwh_t = co2_power_t / gen_total_mwh`. No `ln_co2` variable exists.

**Corrected 2026-11-04:** an earlier version called `ln_ee` electricity intensity (sales over GDP), listed an `ln_co2` output, and named columns and a planned-capacity variable that don't exist.

## Known Quirks

- **Rooftop solar excluded:** The generation file covers utility-scale plants only. Residential
  and commercial rooftop solar is not captured in `renew_gen_mwh` or `solar_share`. This
  understates renewable generation in states with high rooftop adoption (CA, NJ, MA).
  Note this limitation when discussing `solar_share`.
- **Fuel labels:** `build_panel.py` uses one fixed mapping of the file's labels for 2010-2025. There's no year-by-year lookup.
- **Blank fuel, 2017:** `existcapacity_annual.xlsx` has blank-fuel rows for NE (190.8 MW) and NM (7.2 MW). EIA-860 2017 identifies both as natural gas, so `new_renew_mw` isn't affected. See "Blank-fuel capacity rows" below.
- **Gavins Point, 2016-2017:** this 132.3 MW hydro plant is counted in SD in those years and in NE otherwise, so NE and SD `new_renew_mw` have offsetting false changes in 2016 and 2018. See below.
- **EIA-861 sector breakdown changed in 2013:** Prior to 2013, some states report combined
  residential+commercial totals. Use the "Total" row to avoid breaks.

## Output Columns

`renew_share`, `solar_share`, `wind_share`, `clean_share`, `fossil_to_renew`, `new_renew_mw`, `ln_ec`, `ln_ee`,
`price_c_kwh`, `co2_power_t`, `co2_per_mwh_t`

## Script

`scripts/build_panel.py` (EIA electricity section), after `download_all.py`.

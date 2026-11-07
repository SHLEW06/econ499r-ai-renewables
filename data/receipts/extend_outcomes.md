# Receipt: outcomes for prompt 09 sections 2-3 (`data/extend_outcomes.csv`, `data/extend_restructured.csv`)

**Status: done, 2026-11-07.** Built only from files already in `data/raw/`; nothing was downloaded. Script: `python3 -I econ499r_starter/scripts/build_extend_tables.py data/raw data logs/2026-11-07` (log: `logs/2026-11-07/extend_tables_build.log`). Registered in `EXPERIMENTS.md` sections 14.2-14.3.

**Inputs:** `data/out/state_panel_2015_2025.csv` (generation, sales, CO2, population); `data/raw/eia/existcapacity_annual.xlsx` (nameplate capacity, Total Electric Power Industry, 2014-2025, the same filter as `build_panel.py`); `data/raw/eia/HS861_2010-.xlsx` (EIA-861 prices by sector; Energy Only Providers); `data/raw/eia_forms/f8612025.zip` (`Sales_Ult_Cust_2025.xlsx`, ownership, for the restructuring check); `data/seds_old_basis.csv` (SEDS by type).

**Columns:** shares of in-state generation for wind, utility solar, hydro, geothermal, biomass (wood + other biomass), gas, coal and nuclear. ln generation for the five renewable types (blank where zero). MW added (net change in nameplate) per 1,000 MW of 2015 total capacity for wind, solar, hydro, geothermal, biomass and gas. ln sales per person for the residential, commercial and industrial sectors. Price by sector (EIA-861, cents/kWh). Net imports = (retail sales - in-state generation) / retail sales. ln power-sector CO2. SEDS ln wood and waste, ln biofuels, ln renewables without all biomass, ln renewables without biofuels, ln total.

**Not available, so skipped (the prompt allows this):** small-scale solar (EIA's state generation file is utility-scale) and battery storage (EIA's state capacity file has no storage category).

**Checks:** MW added for solar and wind equal the panel's `new_solar_mw` and `new_wind_mw` exactly. EIA-861 total sales equal the panel's `sales_mwh` exactly. The commercial price matches the panel's `price_com_c_kwh` to 0.005 cents (rounding). Nonzero generation state-years (50 states): wind 456, solar 499, hydro 528, geothermal 76 (7 states), biomass 526.

**Restructured classification:** pre-registered rule (Energy-Only Providers' share of 2015 retail sales >= 10%) plus Texas (deviation X1). 15 of the 50 states are restructured: CA, CT, DE, IL, MA, MD, ME, MT, NH, NJ, NY, OH, PA, RI, TX. Near the cutoff: CA 11.0, MI 9.1, NV 6.4. Check rule: retail power marketers' share of 2025 sales >= 10%, which drops CA and MT.

**Rating: green** (all from official EIA files, with exact matches to the panel).

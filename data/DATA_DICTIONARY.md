# Data dictionary

Generated from `data/variable_registry.csv` by `code/python/build_master_workbook.py`, as of 2026-11-07. Don't edit by hand. The workbook's Variable Finder tab comes from the same registry.

Ratings come from `data/DATA_VALIDATION.md`. "Not rated" means no Part C or Nov 4 rating exists for that table.

## Core Panel

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  | Value from the panel |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  | Value from the panel |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| population | Resident population | persons | Value from the panel | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| sales_mwh | Retail electricity sales, all sectors | MWh | Value from the panel | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| revenue_kusd | Retail electricity revenue, all sectors | thousand $ | Value from the panel | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_real_musd2017 | Real GDP, chained 2017 dollars | $ million (2017) | Value from the panel | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| gdp_nom_musd | GDP, all industries, current dollars | $ million | Value from the panel | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_farm_musd | GDP, farms | $ million | Value from the panel | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_manuf_musd | GDP, manufacturing | $ million | Value from the panel | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_total_mwh | Net generation, all sources, Total Electric Power Industry | MWh | Value from the panel | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| gen_renew_mwh | Hydro + wind + solar + geothermal + wood + other biomass generation (memo definition) | MWh | Value from the panel | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_fossil_mwh | Coal + natural gas + petroleum + other gases generation | MWh | Value from the panel | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_solar_mwh | Net generation from solar | MWh | Value from the panel | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| cap_renew_mw | Nameplate capacity of renewable sources in service | MW | Value from the panel | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| dc_jobs | NAICS 518210 annual average employment, private only. Government rows exist and are excluded; see the AI All Ownerships tab | jobs | Value from the panel | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang / Fang | green | Ready |
| tech5415_jobs | NAICS 5415 computer systems design employment, private | jobs | Value from the panel | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| total_jobs | All-industry employment, total covered (industry 10, own 0) | jobs | Value from the panel | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| land_sqmi | Land area (sum of 2020 county land areas) | sq mi | Value from the panel | Census 2020 county Gazetteer | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ai_dc_per1000_lag1 | AI measure lagged one year; the regressor in Step 1 | per 1,000 workers | Value from the panel | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| sales_mwh_pc | MWh sold per person | MWh/person | D2/C2 | EIA retail sales and revenue (Form EIA-861) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ln_ec | H1 consumption outcome: ln(sales_mwh_pc) | log | LN(T2) | EIA retail sales and revenue (Form EIA-861) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ee_usd_per_mwh | Real GDP per MWh sold | 2017 $/MWh | F2*1000000/D2 | BEA GDP by state (SAGDP2, SAGDP9) + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ln_ee | H1 efficiency outcome: ln(ee_usd_per_mwh) | log | LN(V2) | BEA GDP by state (SAGDP2, SAGDP9) + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| renew_share | H1 energy-structure outcome: gen_renew_mwh / gen_total_mwh | share | K2/J2 | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| solar_share | Solar generation / total generation | share | M2/J2 | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| fossil_to_renew | Paper-matching check: fossil MWh / renewable MWh (lower = cleaner) | ratio | IF(K2>0,L2/K2,"") | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ai_dc_per1000 | AI measure: private data-center jobs per 1,000 workers = 1,000 x dc_jobs / total_jobs (memo Section 3; private only by team decision) | per 1,000 workers | IF(O2="","",1000*O2/Q2) | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang / Fang | green | Ready |
| tech_share | H2a mediator: tech5415_jobs / total_jobs | share | IF(P2="","",P2/Q2) | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| price_c_kwh | Control: average retail price = revenue / sales | cents/kWh | 100*E2/D2 | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| ln_gdp_pc | Control: ln real GDP per person | log | LN(F2*1000000/C2) | BEA GDP by state (SAGDP2, SAGDP9) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| manuf_share | Control: manufacturing share of nominal GDP | share | I2/G2 | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| ea_nonfarm_gdp_per_sqmi | H2b mediator input: nonfarm nominal GDP / land area | $/sq mi | (G2-H2)*1000000/R2 | BEA GDP by state (SAGDP2, SAGDP9) + Census 2020 county Gazetteer | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_wind_mwh | Net generation from wind | MWh | Value from the panel | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_coal_mwh | Net generation from coal | MWh | Value from the panel | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| co2_power_t | CO2 from the electric power industry | metric tons | Value from the panel | EIA estimated emissions by state | 2015-2025 | 51 areas | 51: EIA emissions end in 2024 | Zhang | yellow | Ready |
| population_prev | Prior-year population. 2015 row is a value (2014 population backed out of pop_growth); later rows point to the row above | persons | 2015: value; later: =C{r-1} | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| cap_renew_prev | Prior-year renewable capacity. 2015 row is a value (cap_renew_mw - new_renew_mw); later rows point to the row above | MW | 2015: value; later: =N{r-1} | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ln_ea | H2b mediator: ln of ea_nonfarm_gdp_per_sqmi | log | LN(AF2) | BEA GDP by state (SAGDP2, SAGDP9) + Census 2020 county Gazetteer | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| pop_growth | Control: population growth from prior year | share | C2/AJ2-1 | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| wind_share | Wind generation / total generation | share | AG2/J2 | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| coal_share | Coal generation / total generation. Added for the workbook; not in the panel file | share | AH2/J2 | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| co2_per_mwh | CO2 per MWh generated. Same as the panel's co2_per_mwh_t | t/MWh | IF(AI2="","",AI2/J2) | EIA estimated emissions by state + EIA net generation by state | 2015-2025 | 51 areas | 51: EIA emissions end in 2024 | not used | yellow | Ready |
| new_renew_mw | Renewable build-out outcome: change in cap_renew_mw from prior year (can be negative after retirements) | MW | N2-AK2 | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| net_exporter_2015 | 1 if the state generated more than it sold at retail in 2015. Fixed per state; the split used in H1 heterogeneity | 0/1 | IF(INDEX($J$1:$J$562,ROW()-(B2-2015))>INDEX($D$1:$D$562,ROW()-(B2-2015)),1,0) | EIA net generation by state + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| energy_equity | State share of U.S. GDP / state share of U.S. retail MWh. Threshold variable for the Hansen test, which was dropped | ratio | (G2/SUMIF($B$2:$B$562,B2,$G$2:$G$562))/(D2/SUMIF($B$2:$B$562,B2,$D$2:$D$562)) | BEA GDP by state (SAGDP2, SAGDP9) + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | not used | green | Ready |
| in_zhang_sample | 1 for the 50 states; DC is excluded in the Zhang test | 0/1 | IF(A2<>"DC",1,0) |  | 2015-2025 | 51 areas |  | not used | green | Ready |
| in_fang_sample | 1 for 2018-2021, the Fang replication sample (includes DC) | 0/1 | IF(AND(B2>=2018,B2<=2021),1,0) |  | 2015-2025 | 51 areas |  | not used | green | Ready |

## Full Panel

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| gen_total_mwh | Net generation, all sources, Total Electric Power Industry | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| gen_coal_mwh | Net generation from coal | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_gas_mwh | Net generation from gas | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| gen_petroleum_mwh | Net generation from petroleum | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| gen_othergas_mwh | Net generation from othergas | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| gen_nuclear_mwh | Net generation from nuclear | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| gen_hydro_mwh | Net generation from hydro | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_wind_mwh | Net generation from wind | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_solar_mwh | Net generation from solar | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_geothermal_mwh | Net generation from geothermal | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_wood_mwh | Net generation from wood | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_otherbio_mwh | Net generation from otherbio | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_pumpedstorage_mwh | Net generation from pumpedstorage | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| gen_other_mwh | Net generation from other | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| gen_renew_mwh | Hydro + wind + solar + geothermal + wood + other biomass generation (memo definition) | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gen_fossil_mwh | Coal + natural gas + petroleum + other gases generation | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| renew_share | H1 energy-structure outcome: gen_renew_mwh / gen_total_mwh | share |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| solar_share | Solar generation / total generation | share |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| wind_share | Wind generation / total generation | share |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| clean_share | (Renewables + nuclear) / total generation | share |  | EIA net generation by state | 2015-2025 | 51 areas |  | not used | green | Ready |
| fossil_to_renew | Paper-matching check: fossil MWh / renewable MWh (lower = cleaner) | ratio |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| cap_total_mw | Nameplate capacity, total | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| cap_coal_mw | Nameplate capacity, coal | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_gas_mw | Nameplate capacity, gas | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_petroleum_mw | Nameplate capacity, petroleum | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_nuclear_mw | Nameplate capacity, nuclear | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_hydro_mw | Nameplate capacity, hydro | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_wind_mw | Nameplate capacity, wind | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_solar_mw | Nameplate capacity, solar | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_geothermal_mw | Nameplate capacity, geothermal | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_wood_mw | Nameplate capacity, wood | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_otherbio_mw | Nameplate capacity, otherbio | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_other_mw | Nameplate capacity, other | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_pumpedstorage_mw | Nameplate capacity, pumpedstorage | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_othergas_mw | Nameplate capacity, othergas | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| cap_renew_mw | Nameplate capacity of renewable sources in service | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| new_renew_mw | Renewable build-out outcome: change in cap_renew_mw from prior year (can be negative after retirements) | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| new_solar_mw | Change in solar nameplate capacity from prior year | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| new_wind_mw | Change in wind nameplate capacity from prior year | MW |  | EIA existing capacity by state (Form EIA-860) | 2015-2025 | 51 areas |  | not used | green | Ready |
| sales_mwh | Retail electricity sales, all sectors | MWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| sales_res_mwh | Residential retail sales | MWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | not used | green | Ready |
| sales_com_mwh | Commercial retail sales (data centers mostly here) | MWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | not used | green | Ready |
| sales_ind_mwh | Industrial retail sales | MWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | not used | green | Ready |
| revenue_kusd | Retail electricity revenue, all sectors | thousand $ |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| price_c_kwh | Control: average retail price = revenue / sales | cents/kWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| price_com_c_kwh | Commercial average price | cents/kWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | not used | green | Ready |
| co2_power_t | CO2 from the electric power industry | metric tons |  | EIA estimated emissions by state | 2015-2025 | 51 areas | 51: EIA emissions end in 2024 | Zhang | yellow | Ready |
| co2_per_mwh_t | CO2 per MWh generated | t/MWh |  | EIA estimated emissions by state + EIA net generation by state | 2015-2025 | 51 areas | 51: EIA emissions end in 2024 | Zhang | yellow | Ready |
| seds_total_energy_bbtu | Total energy consumption, all fuels (SEDS series TETCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | yellow | Ready |
| dc_jobs | NAICS 518210 annual average employment, private only. Government rows exist and are excluded; see the AI All Ownerships tab | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang / Fang | green | Ready |
| dc_suppressed | 1 if BLS suppressed 518210 for the state-year | 0/1 |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| dc_wages_usd | NAICS 518210 total annual wages, private. Blank where dc_suppressed = 1 | $ |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | not used | green | Ready |
| tech5415_jobs | NAICS 5415 computer systems design employment, private | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| tech5415_suppressed | 1 if BLS suppressed 5415 | 0/1 |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | not used | green | Ready |
| total_jobs | All-industry employment, total covered (industry 10, own 0) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ai_dc_per1000 | AI measure: private data-center jobs per 1,000 workers = 1,000 x dc_jobs / total_jobs (memo Section 3; private only by team decision) | per 1,000 workers |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang / Fang | green | Ready |
| tech_share | H2a mediator: tech5415_jobs / total_jobs | share |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_nom_musd | GDP, all industries, current dollars | $ million |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_farm_musd | GDP, farms | $ million |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_manuf_musd | GDP, manufacturing | $ million |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| gdp_real_musd2017 | Real GDP, chained 2017 dollars | $ million (2017) |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| population | Resident population | persons |  | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| land_sqmi | Land area (sum of 2020 county land areas) | sq mi |  | Census 2020 county Gazetteer | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| sales_mwh_pc | MWh sold per person | MWh/person |  | EIA retail sales and revenue (Form EIA-861) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ln_ec | H1 consumption outcome: ln(sales_mwh_pc) | log |  | EIA retail sales and revenue (Form EIA-861) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ee_usd_per_mwh | Real GDP per MWh sold | 2017 $/MWh |  | BEA GDP by state (SAGDP2, SAGDP9) + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ln_ee | H1 efficiency outcome: ln(ee_usd_per_mwh) | log |  | BEA GDP by state (SAGDP2, SAGDP9) + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| seds_mmbtu_pc | Paper-matching consumption check: SEDS total energy per person | MMBtu/person |  | EIA SEDS consumption + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Zhang | yellow | Ready |
| ln_gdp_pc | Control: ln real GDP per person | log |  | BEA GDP by state (SAGDP2, SAGDP9) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| manuf_share | Control: manufacturing share of nominal GDP | share |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| pop_growth | Control: population growth from prior year | share |  | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| ea_nonfarm_gdp_per_sqmi | H2b mediator input: nonfarm nominal GDP / land area | $/sq mi |  | BEA GDP by state (SAGDP2, SAGDP9) + Census 2020 county Gazetteer | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| ln_ea | H2b mediator: ln of ea_nonfarm_gdp_per_sqmi | log |  | BEA GDP by state (SAGDP2, SAGDP9) + Census 2020 county Gazetteer | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| energy_equity | State share of U.S. GDP / state share of U.S. retail MWh. Threshold variable for the Hansen test, which was dropped | ratio |  | BEA GDP by state (SAGDP2, SAGDP9) + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | not used | green | Ready |
| hma | Paper eq. 2 coupling index of range-standardized AI and tech_share (0 to 1) | index |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang | yellow | Ready |
| ai_dc_per1000_lag1 | AI measure lagged one year; the regressor in Step 1 | per 1,000 workers |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| contig48 | 1 if in the contiguous 48 (+DC) | 0/1 |  |  | 2015-2025 | 51 areas |  | Zhang | green | Ready |
| is_dc | 1 for District of Columbia (drop for the 50-state sample) | 0/1 |  |  | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |

## Fang Panel

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| gdp_real_musd2017 | Real GDP, chained 2017 dollars | $ million (2017) |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| population | Resident population | persons |  | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| dc_jobs | NAICS 518210 annual average employment, private only. Government rows exist and are excluded; see the AI All Ownerships tab | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang / Fang | green | Ready |
| total_jobs | All-industry employment, total covered (industry 10, own 0) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| ai_dc_per1000 | AI measure: private data-center jobs per 1,000 workers = 1,000 x dc_jobs / total_jobs (memo Section 3; private only by team decision) | per 1,000 workers |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang / Fang | green | Ready |
| ai_dc_per1000_lag1 | AI measure lagged one year; the regressor in Step 1 | per 1,000 workers |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| dc_suppressed | 1 if BLS suppressed 518210 for the state-year | 0/1 |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| ln_gdp_pc | Control: ln real GDP per person | log |  | BEA GDP by state (SAGDP2, SAGDP9) + BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| manuf_share | Control: manufacturing share of nominal GDP | share |  | BEA GDP by state (SAGDP2, SAGDP9) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| price_c_kwh | Control: average retail price = revenue / sales | cents/kWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| pop_growth | Control: population growth from prior year | share |  | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| is_dc | 1 for District of Columbia (drop for the 50-state sample) | 0/1 |  |  | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| dc_jobs_lag1 | dc_jobs lagged one year; 2015 reads the 2014 raw file | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| re_bbtu | Renewable energy total consumption (RETCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| wind_bbtu | Wind (WYTCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| solar_bbtu | Solar (SOTCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| geothermal_bbtu | Geothermal (GETCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| hydro_bbtu | Hydropower (HYTCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| biomass_bbtu | Biomass (BMTCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| total_energy_bbtu | Total energy consumption (TETCB) | billion Btu |  | EIA SEDS consumption | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| ep_tetcd | Total energy average price (TETCD) | $/MMBtu |  | EIA SEDS prices | 2015-2025 | 51 areas | 51: SEDS ends in 2024 | Fang | green | Ready |
| edu_bach_per1000 | Bachelor's degrees conferred per 1,000 individuals age 18-24 | per 1,000 |  | NCSES State Indicators: bachelor's degrees per 1,000 age 18-24 | 2015-2025 | 51 areas | 51: NCSES table ends in 2024 | Fang | green | Ready |
| epu_composite | Annual mean of monthly composite state EPU | index |  | State Economic Policy Uncertainty | 2015-2025 | 51 areas |  | Fang | green | Ready |
| epu_national | Annual mean of monthly national-policy EPU for the state | index |  | State Economic Policy Uncertainty | 2015-2025 | 51 areas |  | Fang | green | Ready |
| epu_state | Annual mean of monthly state-policy EPU | index |  | State Economic Policy Uncertainty | 2015-2025 | 51 areas |  | Fang | green | Ready |
| ai_postings | AI job postings; see the AI Job Postings tab | count |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| ai_share_us_pct | State share of U.S. AI postings | percent |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| ai_share_source | Published or derived share | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| ai_share_of_state_pct | AI share of the state's own postings | percent |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| ai_edition | AI Index edition | year |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| ai_vendor | Data vendor for the edition | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| ai_vintage | Break group for postings | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2015-2025 | 51 areas | 153: No state postings published before 2018 | Fang | yellow | Ready |
| target_pct | LBNL current RPS/CES schedule | percent |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang / Fang | yellow | Ready |
| elec_consumption_mwh | Retail sales, from the panel | MWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| elec_price_c_kwh | Average retail price, from the panel | cents/kWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| net_producer | 1 if gen_total_mwh > retail sales | 0/1 |  | EIA net generation by state + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| rd_total_musd | Total R&D, NSF, 2017-2023 | $ million, current |  | NSF National Patterns Table 10, seven editions | 2015-2025 | 51 areas | 204: The NSF editions used cover 2017-2023 | Zhang / Fang | yellow | Ready |
| income_pc_usd | Per capita personal income, BEA SAINC1 line 3 | $, current |  | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| census_region | Census four regions | text |  | Census region lookup (four regions) | 2015-2025 | 51 areas |  | Fang | green | Ready |

## RPS Targets

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Key | yellow | Ready |
| target_pct | Larger of rps_target_pct and ces_target_pct. Differs from the RPS only in MA and VA, 2021-2025. LBNL current RPS/CES schedule, not targets in force | percent |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang / Fang | yellow | Ready |
| rps_target_pct | "Total RPS" row, times 100 | percent |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |
| ces_target_pct | "Total CES" row, times 100 | percent |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |
| target_pct_ed2023 | Same rule from the June 2023 edition. Check only | percent |  | LBNL RPS & CES targets, June 2023 edition | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |
| target_basis | LBNL current RPS/CES schedule, or "not in LBNL file; set to 0" for the 18 states not in the file | text |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |
| ta_status | reported, no_obligation, no_data, not_applicable or state_not_in_file | text |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |
| ta_achievement_pct | Share of the target achieved. Not a target | percent |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas | 267: LBNL gives no achievement value; ta_status says why | Zhang | yellow | Ready |
| obligation_check | Target Achievement compared with the schedule; counts in lbnl_rps.md | text |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |
| revised_vs_older_edition | 1 if an older edition printed a different value for that year or a later one | 0/1 |  | LBNL RPS & CES Targets and Demand | 2015-2025 | 51 areas |  | Zhang | yellow | Ready |

## ACS Broadband

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas |  | Key | yellow | Ready |
| broadband_pct | Share of households with a broadband subscription (S2801) | percent |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas | 51: No ACS 1-year release for 2020 | Zhang | yellow | Ready |
| broadband_pct_moe | Margin of error of broadband_pct | percentage points |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas | 51: No ACS 1-year release for 2020 | Stretch | yellow | Ready |
| broadband_households | Households with broadband | households |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas | 51: No ACS 1-year release for 2020 | Stretch | yellow | Ready |
| total_households | Total households | households |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas | 51: No ACS 1-year release for 2020 | Stretch | yellow | Ready |
| census_var | Census variable read for that year | code |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas | 51: No ACS 1-year release for 2020 | Stretch | yellow | Ready |
| note | 2015 not comparable; 2020 has no 1-year release | text |  | Census ACS 1-year S2801 broadband | 2015-2024 | 51 areas | 408: Text column; blank means no note | Zhang / Fang | yellow | Ready |

## EPU Annual

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | State Economic Policy Uncertainty | 1985-2025 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  | State Economic Policy Uncertainty | 1985-2025 | 51 areas |  | Key | green | Ready |
| epu_composite | Annual mean of monthly composite state EPU | index |  | State Economic Policy Uncertainty | 1985-2025 | 51 areas | 382: Blank in the publisher's file before the state's series starts; complete in 2015-2025 | Fang | green | Ready |
| epu_national | Annual mean of monthly national-policy EPU for the state | index |  | State Economic Policy Uncertainty | 1985-2025 | 51 areas | 382: Blank in the publisher's file before the state's series starts; complete in 2015-2025 | Fang | green | Ready |
| epu_state | Annual mean of monthly state-policy EPU | index |  | State Economic Policy Uncertainty | 1985-2025 | 51 areas | 382: Blank in the publisher's file before the state's series starts; complete in 2015-2025 | Fang | green | Ready |
| n_months_state | Months with a state EPU value that year | count |  | State Economic Policy Uncertainty | 1985-2025 | 51 areas |  | Stretch | green | Ready |

## NSF State RD

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Key | yellow | Ready |
| nsf_edition | NSF publication number the year comes from | code |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| rd_total_musd | Total R&D performed in the state | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Zhang / Fang | yellow | Ready |
| rd_federal_musd | R&D performed by federal intramural | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| rd_ffrdc_musd | R&D performed by FFRDCs | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| rd_business_musd | R&D performed by business | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| rd_higher_ed_musd | R&D performed by higher education | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| rd_nonprofit_musd | R&D performed by nonprofits | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas | 9: NSF printed a non-numeric cell; text in published_not_numeric | Stretch | yellow | Ready |
| rd_state_internal_musd | R&D performed by state government | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas | 51: NSF printed a non-numeric cell; text in published_not_numeric | Stretch | yellow | Ready |
| gdp_nsf_musd | GDP as printed in NSF's table | $ million, current |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| rd_intensity_pct | R&D as a share of GDP, as published | percent |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas |  | Stretch | yellow | Ready |
| published_not_numeric | Published text kept where a cell is non-numeric | text |  | NSF National Patterns Table 10, seven editions | 2017-2023 | 51 areas | 299: Filled only where a cell is non-numeric | Stretch | yellow | Ready |

## OWID Solar

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| entity | Country or region | text |  | Solar PV capacity (IRENA via Our World in Data) | 2000-2025 |  |  | Georgia | green | Ready |
| code | ISO code | text |  | Solar PV capacity (IRENA via Our World in Data) | 2000-2025 |  |  | Georgia | green | Ready |
| year | Calendar year |  |  | Solar PV capacity (IRENA via Our World in Data) | 2000-2025 |  |  | Georgia | green | Ready |
| solar_pv_ongrid_gw | Cumulative on-grid solar PV capacity | GW |  | Solar PV capacity (IRENA via Our World in Data) | 2000-2025 |  |  | Georgia | green | Ready |
| source | Source label | text |  | Solar PV capacity (IRENA via Our World in Data) | 2000-2025 |  |  | Georgia | green | Ready |

## LBNL Solar Projects

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| eia_id | EIA plant ID | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 3: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| project_name | Project name | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| solar_cod | Commercial operation date | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| solar_cod_year | Commercial operation year | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| region | Region | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| state | Two-letter state code (50 states + DC) |  |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| latitude | Latitude | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| longitude | Longitude | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| avg_ghi | Average global horizontal irradiance | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| solar_tech_main | Main solar technology | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| solar_tech_sub | Sub-technology | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 10: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| solar_capacity_mw_dc | Capacity, MW-DC | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 24: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| solar_capacity_mw_ac | Capacity, MW-AC | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| ilr | Inverter loading ratio | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 24: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| mount | Mount type | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| tracking_type | Tracking type | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas |  | Georgia | green | Ready |
| tilt | Tilt | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 328: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| azimuth | Azimuth | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 9: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| hybrid | Hybrid flag | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1794: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| storage_tech | Storage technology | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1763: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| storage_coupling | Storage coupling | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1745: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| storage_cod_year | Storage operation year | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1751: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| storage_capacity_mw | Storage power, MW | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1751: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| storage_energy_mwh | Storage energy, MWh | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1750: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2025_energy_value_mwh | 2025 energy value, $/MWh | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 306: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2025_capacity_value_mwh | 2025 capacity value, $/MWh | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 306: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| pv_lcoe_no_tax_credits_2025_mwh | LCOE without tax credits, 2025 $/MWh | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 343: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| pv_lcoe_with_federal_tax_credits_2025_mwh | LCOE with federal tax credits, 2025 $/MWh | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 343: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| offtaker_type | Offtaker type | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 201: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| levelized_pv_ppa_2025_mwh | Levelized PPA price, 2025 $/MWh | see definition |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1517: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2008_capacity_factor | Capacity factor, 2008 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 2000: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2009_capacity_factor | Capacity factor, 2009 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1999: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2010_capacity_factor | Capacity factor, 2010 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1997: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2011_capacity_factor | Capacity factor, 2011 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1989: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2012_capacity_factor | Capacity factor, 2012 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1960: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2013_capacity_factor | Capacity factor, 2013 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1920: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2014_capacity_factor | Capacity factor, 2014 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1878: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2015_capacity_factor | Capacity factor, 2015 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1819: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2016_capacity_factor | Capacity factor, 2016 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1736: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2017_capacity_factor | Capacity factor, 2017 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1590: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2018_capacity_factor | Capacity factor, 2018 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1442: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2019_capacity_factor | Capacity factor, 2019 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1346: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2020_capacity_factor | Capacity factor, 2020 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1241: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2021_capacity_factor | Capacity factor, 2021 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 1084: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2022_capacity_factor | Capacity factor, 2022 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 952: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2023_capacity_factor | Capacity factor, 2023 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 764: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2024_capacity_factor | Capacity factor, 2024 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 549: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |
| 2025_capacity_factor | Capacity factor, 2025 | share |  | LBNL Utility-Scale Solar, 2026 Edition |  | 48 areas | 327: Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year) | Georgia | green | Ready |

## Epoch by State

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |
| n_sites | Epoch sites in the state | count |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |
| n_operating | Sites with current power above 0 | count |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |
| current_it_mw | Sum of Epoch's Current power (MW) | MW |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |
| planned_it_mw | Sum over sites of the largest IT power on the timeline | MW |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |
| planned_facility_mw | Sum over sites of the largest facility power on the timeline | MW |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |
| note | Context only; not a model variable | text |  | Epoch AI data centers |  | 29 areas |  | Georgia | green, context only | Ready |

## AI All Ownerships

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Key | not rated | Ready |
| year | Calendar year |  |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Key | not rated | Ready |
| dc_jobs_private | Private 518210 jobs; same as the panel's dc_jobs | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang | not rated | Ready |
| dc_jobs_gov_federal | Federal 518210 jobs (own code 1) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |
| dc_jobs_gov_state | State government 518210 jobs (own code 2) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |
| dc_jobs_gov_local | Local government 518210 jobs (own code 3) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |
| n_gov_rows_suppressed | Government rows BLS suppressed | count |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |
| total_jobs | All-industry employment, total covered | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |
| dc_jobs_gov_published | Sum of published government 518210 rows | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |
| dc_jobs_allown | Private + published government | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang | not rated | Ready |
| gov_share_pct | Government share of all-ownership 518210 jobs | percent |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang | not rated | Ready |
| ai_allown_per1000 | All-ownership data-center jobs per 1,000 workers | per 1,000 workers |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas | 4: BLS suppressed AK, ND, SD and WY in 2025 | Zhang | not rated | Ready |
| ai_allown_per1000_lag1 | Same, lagged one year | per 1,000 workers |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) | 2015-2025 | 51 areas |  | Zhang | not rated | Ready |

## AI Job Postings

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Key | yellow | Ready |
| postings | AI job postings in the state | count |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| share_pct | State share of U.S. AI postings | percent |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| share_source | "published" for 2022-2025; "derived: state / sum of 51" for 2018-2021 | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| ai_share_of_state_postings_pct | AI share of the state's own postings. A different measure | percent |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| edition | AI Index edition | year |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Zhang / Fang | yellow | Ready |
| vendor | Data vendor for the edition | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| vintage | Break group: each edition is its own; 2019-2021 is the only multi-year group | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| figure | Figure in the report | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Zhang / Fang | yellow | Ready |
| page | PDF page. Blank for 2019-2020, which no report prints | page |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas | 102: No report prints 2019-2020 | Fang | yellow | Ready |
| source_file | Raw file read | path |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas |  | Fang | yellow | Ready |
| note | Notes on the row | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2018-2025 | 51 areas | 357: Text column; blank means no note | Zhang / Fang | yellow | Ready |

## AI Postings Overlap

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Key |  |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2019-2020 | 51 areas |  | Fang (check) | yellow | Ready |
| year | Key |  |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2019-2020 | 51 areas |  | Fang (check) | yellow | Ready |
| postings | AI postings as printed in the other edition | count |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2019-2020 | 51 areas |  | Fang (check) | yellow | Ready |
| st_share | State share | percent |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2019-2020 | 51 areas |  | Fang (check) | yellow | Ready |
| edition | Edition | year |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2019-2020 | 51 areas |  | Fang (check) | yellow | Ready |
| note | Note | text |  | AI Index 2019, Chapter on the economy; postings year(s) 2018 + AI Index 2021, Chapter on the economy; postings year(s) check of 2019-2021 text + AI Index 2022, Chapter on the economy; postings year(s) 2019-2021 + 4 more | 2019-2020 | 51 areas |  | Fang (check) | yellow | Ready |

## SEDS Renewables

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Key | green | Ready |
| re_bbtu | Renewable energy total consumption (RETCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| wind_bbtu | Wind (WYTCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| solar_bbtu | Solar (SOTCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| geothermal_bbtu | Geothermal (GETCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| hydro_bbtu | Hydropower (HYTCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| biomass_bbtu | Biomass (BMTCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| total_energy_bbtu | Total energy consumption (TETCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |
| ep_tetcd | Total energy average price (TETCD) | $/MMBtu |  | EIA SEDS prices | 2015-2024 | 51 areas |  | Fang | green | Ready |

## NCSES Bachelors

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | NCSES State Indicators: bachelor's degrees per 1,000 age 18-24 | 2015-2024 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  | NCSES State Indicators: bachelor's degrees per 1,000 age 18-24 | 2015-2024 | 51 areas |  | Key | green | Ready |
| edu_bach_per1000 | Bachelor's degrees conferred per 1,000 individuals age 18-24 | per 1,000 |  | NCSES State Indicators: bachelor's degrees per 1,000 age 18-24 | 2015-2024 | 51 areas |  | Fang | green | Ready |
| degrees | Bachelor's degrees conferred | count |  | NCSES State Indicators: bachelor's degrees per 1,000 age 18-24 | 2015-2024 | 51 areas |  | Fang | green | Ready |
| pop_18_24 | Population age 18-24 | persons |  | NCSES State Indicators: bachelor's degrees per 1,000 age 18-24 | 2015-2024 | 51 areas |  | Fang | green | Ready |

## Fang Split Vars

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  |  | 2015-2025 | 51 areas |  | Key | green | Ready |
| elec_consumption_mwh | Retail sales, from the panel | MWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| elec_price_c_kwh | Average retail price, from the panel | cents/kWh |  | EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| gen_total_mwh | Total generation, from the panel | MWh |  | EIA net generation by state | 2015-2025 | 51 areas |  | Zhang / Fang | green | Ready |
| net_producer | 1 if gen_total_mwh > retail sales | 0/1 |  | EIA net generation by state + EIA retail sales and revenue (Form EIA-861) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| rd_total_musd | Total R&D, NSF, 2017-2023 | $ million, current |  | NSF National Patterns Table 10, seven editions | 2015-2025 | 51 areas | 204: The NSF editions used cover 2017-2023 | Zhang / Fang | yellow | Ready |
| income_pc_usd | Per capita personal income, BEA SAINC1 line 3 | $, current |  | BEA state personal income and population (SAINC1) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| census_region | Census four regions | text |  | Census region lookup (four regions) | 2015-2025 | 51 areas |  | Fang | green | Ready |
| extreme_weather | Not run: Fang's count of extreme hot and cold occurrences wasn't built. Column is blank | n/a |  | NOAA heating and cooling degree days | 2015-2025 | 51 areas | 561: Not run: Fang's count of extreme hot and cold occurrences wasn't built | Fang | not run | Not available |
| extreme_weather_note | Reason the column is blank | text |  | NOAA heating and cooling degree days | 2015-2025 | 51 areas |  | Fang | not run | Not available |

## Net Producer Defs

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Key | yellow | Ready |
| gen_total_mwh | Total generation, from the panel | MWh |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| retail_sales_mwh | Retail sales, from the panel | MWh |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| seds_net_interstate_flow_bbtu | SEDS net interstate flow of electricity and associated losses (ELISB); negative is flow out of state | billion Btu |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| seds_total_consumption_bbtu | SEDS total energy consumption (TETCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| seds_total_production_bbtu | SEDS total primary energy production (TEPRB) | billion Btu |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| gen_gt_sales | 1 if 2018-2021 average generation is above retail sales: our main rule | 0/1 |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| teprb_gt_tetcb | 1 if 2018-2021 average SEDS total energy production is above consumption | 0/1 |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |
| elisb_negative | 1 if 2018-2021 average SEDS net interstate electricity flow is below zero | 0/1 |  | EIA SEDS consumption + EIA SEDS production + EIA net generation by state + 1 more | 2018-2021 | 51 areas |  | Fang (check) | yellow | Ready |

## NOAA Degree Days

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | NOAA heating and cooling degree days | 2015-2025 | 48 areas |  | Key | green | Ready |
| year | Calendar year |  |  | NOAA heating and cooling degree days | 2015-2025 | 48 areas |  | Key | green | Ready |
| cdd | Cooling degree days, base 65F, January-December. State value population-weighted by NOAA (2010 Census) | degree days |  | NOAA heating and cooling degree days | 2015-2025 | 48 areas |  | Zhang (check) | green | Ready |
| hdd | Heating degree days, base 65F, January-December. State value population-weighted by NOAA (2010 Census) | degree days |  | NOAA heating and cooling degree days | 2015-2025 | 48 areas |  | Zhang (check) | green | Ready |

## SEDS Old Basis

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Key | green | Ready |
| hr_kbtu_kwh | EIA fossil-fueled plant heat rate, from bulk MER (equals archived FFETK 2015-2021) | thousand Btu/kWh |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| k_t | hr_kbtu_kwh / 3.412 | ratio |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| re_bbtu_current | Renewable consumption, current SEDS (RETCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| re_bbtu_rebuilt | Renewables rebuilt year by year on the old fossil-fuel-equivalence basis (electricity parts only) | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| re_bbtu_rebuilt_allconv | Same, converting all of wind, solar, hydro and geothermal (check) | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| re_bbtu_k26 | Biomass + 2.6 x (wind + solar + hydro + geothermal); check only | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| RETCB_arch2021 | RETCB as published in the June 2023 SEDS release (2015-2021); main old basis | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas | 153: RETCB_arch2021 covers 2015-2021 only (June 2023 release); other blanks are blank in SEDS | Fang (08) | green | Ready |
| WYTCB | Wind, current SEDS | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| HYTCB | Hydro, current SEDS | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| SOTCB | Solar, current SEDS | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| GETCB | Geothermal, current SEDS | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| BMTCB | Biomass, current SEDS | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| WWTCB | Wood and waste | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| BFTCB | Biofuels incl. losses and co-products | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| EMTCB | Fuel ethanol excl. denaturant | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| BDTCB | Biodiesel | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| B1TCB | Renewable diesel | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| SOR7P | Residential small-scale solar PV generation | million kWh |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| pv_res_bbtu | SOR7P x 3.412 | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| noncomb_elec_bbtu_current | Wind + hydro + geothermal and solar electricity, captured basis | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| fossil_bbtu | Fossil fuels total consumption (FFTCB) | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| TETCB | Total energy consumption | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| fossil_share_total | FFTCB / TETCB | share |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| re_excl_biomass_current | RETCB - BMTCB | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |
| re_excl_biofuels_current | RETCB - BFTCB | billion Btu |  | EIA SEDS consumption + EIA SEDS archived release, consolidated file, data through 2021 (published June 2023) + EIA Monthly Energy Review bulk series (TOTAL.zip) + 1 more | 2015-2024 | 51 areas |  | Fang (08) | green | Ready |

## Storm Events

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Key | yellow | Ready |
| events_heat | Records of Excessive Heat or Heat | count |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Fang (08) | yellow | Ready |
| events_cold | Records of Extreme Cold/Wind Chill or Cold/Wind Chill | count |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Fang (08) | yellow | Ready |
| extreme_events | events_heat + events_cold | count |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Fang (08) | yellow | Ready |
| episodes_heat | Distinct heat episodes | count |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Fang (08) | yellow | Ready |
| episodes_cold | Distinct cold episodes | count |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Fang (08) | yellow | Ready |
| extreme_episodes | Heat + cold episodes | count |  | NOAA Storm Events Database, details files 2015-2024 | 2015-2024 | 51 areas |  | Fang (08) | yellow | Ready |

## Extend Outcomes

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Key | green | Ready |
| year | Calendar year |  |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Key | green | Ready |
| is_dc | 1 for DC | flag |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| population | Population (BEA) | persons |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| gen_total_mwh | Total in-state generation | MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| sales_mwh | Retail sales | MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| sales_res_mwh | Residential retail sales | MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| sales_com_mwh | Commercial retail sales | MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| sales_ind_mwh | Industrial retail sales | MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| co2_power_t | Power-sector CO2 | metric tons |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: EIA emissions end in 2024 | Extensions (09) | green | Ready |
| co2_per_mwh_t | Power-sector CO2 per MWh | tons/MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: EIA emissions end in 2024 | Extensions (09) | green | Ready |
| share_wind | Share of in-state generation from wind | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_gen_wind | ln generation from wind; blank where zero | log MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 105: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| share_solar | Share of in-state generation from utility-scale solar | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_gen_solar | ln generation from utility-scale solar; blank where zero | log MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 55: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| share_hydro | Share of in-state generation from conventional hydro | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_gen_hydro | ln generation from conventional hydro; blank where zero | log MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 33: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| share_geo | Share of in-state generation from geothermal | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_gen_geo | ln generation from geothermal; blank where zero | log MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 485: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| share_bio | Share of in-state generation from biomass (wood + other biomass) | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_gen_bio | ln generation from biomass (wood + other biomass); blank where zero | log MWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 24: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| share_gas | Share of in-state generation from natural gas | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| share_coal | Share of in-state generation from coal | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| share_nuclear | Share of in-state generation from nuclear | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_sales_res_pc | ln residential retail sales per person | log MWh per person |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_sales_com_pc | ln commercial retail sales per person | log MWh per person |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_sales_ind_pc | ln industrial retail sales per person | log MWh per person |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| net_imports | (retail sales - generation) / retail sales | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_co2_power | ln power-sector CO2 | log |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| add_wind_per1000 | Net change in wind nameplate capacity per 1,000 MW of 2015 total capacity | MW per 1,000 MW |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| add_solar_per1000 | Net change in utility-scale solar nameplate capacity per 1,000 MW of 2015 total capacity | MW per 1,000 MW |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| add_hydro_per1000 | Net change in conventional hydro nameplate capacity per 1,000 MW of 2015 total capacity | MW per 1,000 MW |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| add_geo_per1000 | Net change in geothermal nameplate capacity per 1,000 MW of 2015 total capacity | MW per 1,000 MW |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| add_bio_per1000 | Net change in biomass (wood + other biomass) nameplate capacity per 1,000 MW of 2015 total capacity | MW per 1,000 MW |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| add_gas_per1000 | Net change in natural gas nameplate capacity per 1,000 MW of 2015 total capacity | MW per 1,000 MW |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| price_res_c_kwh | Residential price, EIA-861 | cents/kWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| price_com861_c_kwh | Commercial price, EIA-861 | cents/kWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| price_ind_c_kwh | Industrial price, EIA-861 | cents/kWh |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas |  | Extensions (09) | green | Ready |
| ln_seds_woodwaste | ln SEDS wood and waste | log |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| ln_seds_biofuels | ln SEDS biofuels | log |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 57: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| ln_seds_re_exbiomass | ln SEDS renewables excl. biomass | log |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| ln_seds_re_exbiofuels | ln SEDS renewables excl. biofuels | log |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |
| ln_seds_re_total | ln SEDS renewables total | log |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) + EIA retail sales and revenue (Form EIA-861) + 3 more | 2015-2025 | 51 areas | 51: ln columns are blank where generation is zero; SEDS and CO2 end in 2024; blank in EIA's file otherwise | Extensions (09) | green | Ready |

## Restructured

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Key | yellow | Ready |
| energy_only_sales_mwh_2015 | Sales by EIA-861 Energy-Only Providers, 2015 | MWh |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| total_sales_mwh_2015 | Total retail sales, 2015 | MWh |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| energy_only_share_pct_2015 | Energy-only share of 2015 sales | percent |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| restructured | Main classification: share >= 10% plus Texas (deviation X1) | flag |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| near_cutoff_flag | Within 5 points of the 10% cutoff | flag |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| restructured_prereg_rule | Pre-registered rule alone (Texas = 0) | flag |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| rpm_share_pct_2025 | Retail power marketers' share of 2025 sales (EIA-861 detail) | percent |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| restructured_check_rpm2025 | Check rule: rpm share >= 10% | flag |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| near_cutoff_flag_check | Check rule within 5 points of cutoff | flag |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |
| source | Source note | text |  | EIA retail sales and revenue (Form EIA-861) + Form EIA-861 data files, 2025 |  | 51 areas |  | Extensions (09) | yellow | Ready |

## Drivers National

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| year | Calendar year |  |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Key | green | Ready |
| itc_pct | Solar ITC by year construction begins | percent |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| itc_source | Citation, printed page [PDF page] | text |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| ptc_pct_of_full | Wind PTC as a share of the full credit, by construction-start year | percent |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| ptc_source | Citation, printed page [PDF page] | text |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| wind_lcoe_2025usd_mwh | LBNL generation-weighted wind LCOE by COD year | 2025 $/MWh |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| wind_lcoe_source | Source note | text |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| solar_lcoe_2025usd_mwh | LBNL MW-weighted PV LCOE without tax credits by COD year | 2025 $/MWh |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| solar_lcoe_projects | Projects in the solar LCOE mean | count |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| solar_lcoe_mw_ac | MW-AC in the solar LCOE mean | MW |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| hh_usd_mmbtu | Henry Hub spot price, annual average | $/MMBtu |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| us_dc_jobs_50 | Sum of 50-state private 518210 jobs | jobs |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| n_states_dc | States with data | count |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |
| us_ai_postings_50 | Sum of 50-state AI postings | count |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  | 3: Postings start in 2018; text columns blank where not needed | Extensions (09) | green | Ready |
| n_states_post | States with data | count |  | CRS R43453, The Renewable Electricity Production Tax Credit: In Brief (Apr. 29, 2020) + CRS IF10479, The Energy Credit or Energy Investment Tax Credit (ITC) (Apr. 23, 2021) + Consolidated Appropriations Act, 2021, P.L. 116-260 + 5 more | 2015-2025 |  |  | Extensions (09) | green | Ready |

## Drivers State

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas |  | Key | yellow | Ready |
| wind_cf | Wind capacity factor, first full year with >= 10 MW (deviation X4) | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas |  | Extensions (09) | yellow | Ready |
| wind_cf_year | Year used | year |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas | 10: Year blank where the state never has 10 MW of that type | Extensions (09) | yellow | Ready |
| wind_cf_flag | Note | text |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas | 36: Year blank where the state never has 10 MW of that type | Extensions (09) | yellow | Ready |
| solar_cf | Solar capacity factor, same rule | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas |  | Extensions (09) | yellow | Ready |
| solar_cf_year | Year used | year |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas | 3: Year blank where the state never has 10 MW of that type | Extensions (09) | yellow | Ready |
| solar_cf_flag | Note | text |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas | 23: Year blank where the state never has 10 MW of that type | Extensions (09) | yellow | Ready |
| gas_share_2015 | Gas share of 2015 generation | share |  | EIA net generation by state + EIA existing capacity by state (Form EIA-860) |  | 50 areas |  | Extensions (09) | yellow | Ready |

## AI Index Components

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Key | yellow | Ready |
| dc_jobs | Private 518210 jobs (panel) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| total_jobs | Total covered jobs (panel) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| population | Population (panel) | persons |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| sales_mwh | Retail sales (panel) | MWh |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| land_sqmi | Land area | sq mi |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| qcew_estabs | Private 518210 establishments | count |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| qcew_jobs | Private 518210 jobs (QCEW) | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| qcew_wages | Private 518210 total wages | $ |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| oews_rsci | OEWS computer and information research scientists | jobs |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas | 138: QCEW non-disclosed, OEWS ** or #, or postings before 2018 | Extensions (09) | yellow | Ready |
| oews_code | SOC code used | code |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas | 114: QCEW non-disclosed, OEWS ** or #, or postings before 2018 | Extensions (09) | yellow | Ready |
| ai_postings | AI job postings | count |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas | 150: No state postings published before 2018 | Extensions (09) | yellow | Ready |
| c_jobs | ln 518210 jobs per 1,000 workers | log |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| c_estab | ln establishments per million residents | log |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| c_wage | ln 518210 wages per worker | log |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas |  | Extensions (09) | yellow | Ready |
| c_post | ln postings per 1,000 workers | log |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas | 150: QCEW non-disclosed, OEWS ** or #, or postings before 2018 | Extensions (09) | yellow | Ready |
| c_rsci | ln research scientists per 1,000 workers | log |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 + 1 more | 2015-2024 | 50 areas | 138: QCEW non-disclosed, OEWS ** or #, or postings before 2018 | Extensions (09) | yellow | Ready |

## AI Index

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Key | yellow | Ready |
| year | Calendar year |  |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Key | yellow | Ready |
| sub_infra | Infrastructure sub-index: mean z of jobs, establishments, wages | z |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Extensions (09) | yellow | Ready |
| sub_talent | Talent sub-index: mean z of postings, research scientists | z |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Extensions (09) | yellow | Ready |
| index_a | Index A: mean of the two sub-indices | z |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Extensions (09) | yellow | Ready |
| index_b | Index B: first principal component | score |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Extensions (09) | yellow | Ready |
| version | main_2018_2023, main_scored_2024 or check_2015_2023_no_postings | text |  | BLS QCEW annual averages (NAICS 518210, 5415, all industries) + BLS Occupational Employment and Wage Statistics, state files, May 2015-May 2024 + AI Index 2026, Chapter on the economy; postings year(s) 2025 | 2015-2024 | 44 areas |  | Extensions (09) | yellow | Ready |

## AI Index Cross-State

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| state | Two-letter state code (50 states + DC) |  |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Key | yellow | Ready |
| sales_mwh | 2015 retail sales | MWh |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |
| dc_jobs | 2015 private 518210 jobs | jobs |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |
| land_sqmi | Land area | sq mi |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |
| btos_ai_use_2024_pct | BTOS share of firms using AI, 2024 average | percent |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 7: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| btos_periods_2024 | Periods averaged | count |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |
| current_it_mw | Epoch current IT MW | MW |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 22: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| quid_invest_2025_usd | Quid private AI investment, 2025 | $ |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 4: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| index_a_2024 | Index A, 2024 (scored) | z |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 16: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| index_b_2024 | Index B, 2024 (scored) | score |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 16: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| index_a_2023 | Index A, 2023 | z |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 12: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| invest_per_twh_2015 | 2025 investment per TWh of 2015 sales | $/TWh |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 4: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| jobs518210_per_twh_2015 | 2015 518210 jobs per TWh of 2015 sales | jobs/TWh |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |
| land_sqmi_per_twh_2015 | Land per TWh of 2015 sales | sq mi/TWh |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |
| grp_invest | Investment group (fixed before results) | group |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 4: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| grp_invest_per_twh | Tertile of investment per TWh | group |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas | 4: BTOS suppressed; Epoch covers 29 states; Quid missing for AR, OK, SD and WV; index needs all components | Extensions (09) | yellow | Ready |
| grp_jobs_per_twh | Tertile of jobs per TWh | group |  | Census Business Trends and Outlook Survey, AI questions, state estimates + Private AI investment by U.S. state, 2025 (Quid, via AI Index 2026, Fig. 4.2.15) + Epoch AI data centers + 2 more |  | 50 areas |  | Extensions (09) | yellow | Ready |

## FERC1 Utilities

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| utility_id_ferc1 | FERC respondent ID | id |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| utility_id_pudl | PUDL utility ID | id |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| utility_name | Utility name | text |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| hq_state_eia | Headquarters state from EIA | text |  | FERC Form 1 via PUDL | 2015-2025 |  | 722: Blank in PUDL for that filer-year | finance | not rated | Ready |
| entity_type_eia | Entity type from EIA | text |  | FERC Form 1 via PUDL | 2015-2025 |  | 1288: Blank in PUDL for that filer-year | finance | not rated | Ready |
| year | Calendar year |  |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| elec_net_operating_income_musd | Electric net operating income | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 1263: Blank in PUDL for that filer-year | finance | not rated | Ready |
| elec_operating_revenue_musd | Electric operating revenue | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 24: Blank in PUDL for that filer-year | finance | not rated | Ready |
| elec_operating_expense_musd | Electric operating expenses | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 6: Blank in PUDL for that filer-year | finance | not rated | Ready |
| net_income_musd | Net income | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 43: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_distribution_musd | Plant in service, distribution | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 796: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_total_musd | Plant in service, total | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 130: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_storage_musd | Plant in service, storage. 2021 on | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 2237: Accounts for solar, wind, storage and other renewable start in 2021 | finance | not rated | Ready |
| plant_hydro_musd | Plant in service, hydro | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 1736: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_nuclear_musd | Plant in service, nuclear | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 1974: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_other_production_musd | Plant in service, other production | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 1181: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_other_renewable_musd | Plant in service, other renewable. 2021 on | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 2287: Accounts for solar, wind, storage and other renewable start in 2021 | finance | not rated | Ready |
| plant_production_musd | Plant in service, production total | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 997: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_solar_musd | Plant in service, solar. 2021 on | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 2223: Accounts for solar, wind, storage and other renewable start in 2021 | finance | not rated | Ready |
| plant_steam_musd | Plant in service, steam | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 1293: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_transmission_musd | Plant in service, transmission | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 413: Blank in PUDL for that filer-year | finance | not rated | Ready |
| plant_wind_musd | Plant in service, wind. 2021 on | $ million |  | FERC Form 1 via PUDL | 2015-2025 |  | 2260: Accounts for solar, wind, storage and other renewable start in 2021 | finance | not rated | Ready |
| production_fossil_share | Fossil share of production plant | share |  | FERC Form 1 via PUDL | 2015-2025 |  | 1120: Blank in PUDL for that filer-year | finance | not rated | Ready |
| production_renewable_share | Renewable share of production plant | share |  | FERC Form 1 via PUDL | 2015-2025 |  | 1728: Accounts for solar, wind, storage and other renewable start in 2021 | finance | not rated | Ready |
| operating_margin | Net operating income / operating revenue | share |  | FERC Form 1 via PUDL | 2015-2025 |  | 1271: Blank in PUDL for that filer-year | finance | not rated | Ready |

## FERC1 Cost by Tech

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| tech_class | Technology class | text |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| year | Calendar year |  |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| plants | Plants in the cell | count |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| capacity_mw | Capacity | MW |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| net_generation_mwh | Net generation | MWh |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| book_capex_usd_per_kw | Book capital cost per kW | $/kW |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| nonfuel_opex_usd_per_mwh | Non-fuel operating cost per MWh | $/MWh |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| fuel_usd_per_mwh | Fuel cost per MWh | $/MWh |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| total_opex_usd_per_mwh | Total operating cost per MWh | $/MWh |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| capacity_factor | Generation / (capacity x hours) | share |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |

## FERC1 Plants

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| year | Calendar year |  |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| utility_id_ferc1 | FERC respondent ID | id |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| utility_name_ferc1 | Utility name | text |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| plant_id_pudl | PUDL plant ID | id |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| plant_name_ferc1 | Plant name | text |  | FERC Form 1 via PUDL | 2015-2025 |  | 5: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| tech_group | Technology group | text |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| tech_class | Technology class | text |  | FERC Form 1 via PUDL | 2015-2025 |  |  | finance | not rated | Ready |
| plant_type | Plant type as reported | text |  | FERC Form 1 via PUDL | 2015-2025 |  | 3299: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| fuel_type | Fuel type | text |  | FERC Form 1 via PUDL | 2015-2025 |  | 8111: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| construction_type | Construction type | text |  | FERC Form 1 via PUDL | 2015-2025 |  | 10029: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| construction_year | Year built | year |  | FERC Form 1 via PUDL | 2015-2025 |  | 1224: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| capacity_mw | Capacity | MW |  | FERC Form 1 via PUDL | 2015-2025 |  | 918: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| net_generation_mwh | Net generation | MWh |  | FERC Form 1 via PUDL | 2015-2025 |  | 2514: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| capacity_factor | Capacity factor | share |  | FERC Form 1 via PUDL | 2015-2025 |  | 9192: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| capex_total | Book capital cost | $ |  | FERC Form 1 via PUDL | 2015-2025 |  | 1363: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| capex_per_mw | Book capital cost per MW | $/MW |  | FERC Form 1 via PUDL | 2015-2025 |  | 3148: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| capex_annual_addition | Capital added in the year | $ |  | FERC Form 1 via PUDL | 2015-2025 |  | 11539: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| opex_fuel | Fuel cost | $ |  | FERC Form 1 via PUDL | 2015-2025 |  | 11020: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| opex_total_nonfuel | Non-fuel operating cost | $ |  | FERC Form 1 via PUDL | 2015-2025 |  | 568: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| opex_all | All operating cost | $ |  | FERC Form 1 via PUDL | 2015-2025 |  | 568: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| opex_per_mwh | Operating cost per MWh | $/MWh |  | FERC Form 1 via PUDL | 2015-2025 |  | 8955: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| fuel_cost_per_mwh | Fuel cost per MWh | $/MWh |  | FERC Form 1 via PUDL | 2015-2025 |  | 12876: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| fuel_cost_per_mmbtu | Fuel cost per MMBtu | $/MMBtu |  | FERC Form 1 via PUDL | 2015-2025 |  | 20278: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |
| avg_num_employees | Average employees | count |  | FERC Form 1 via PUDL | 2015-2025 |  | 12017: Blank in PUDL or not computable for that plant-year | finance | not rated | Ready |

## SEC Companies

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| ticker | Stock ticker | text |  | SEC XBRL company facts | 2015-2025 |  |  | finance | not rated | Ready |
| cik | SEC company ID | id |  | SEC XBRL company facts | 2015-2025 |  |  | finance | not rated | Ready |
| company | Company name | text |  | SEC XBRL company facts | 2015-2025 |  |  | finance | not rated | Ready |
| group | Company group | text |  | SEC XBRL company facts | 2015-2025 |  |  | finance | not rated | Ready |
| note | Notes on the company | text |  | SEC XBRL company facts | 2015-2025 |  | 396: Text column; blank means no note | finance | not rated | Ready |
| year | Calendar year |  |  | SEC XBRL company facts | 2015-2025 |  |  | finance | not rated | Ready |
| revenue_musd | Revenue | $ million |  | SEC XBRL company facts | 2015-2025 |  | 7: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| operating_income_musd | Operating income | $ million |  | SEC XBRL company facts | 2015-2025 |  | 110: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| net_income_musd | Net income | $ million |  | SEC XBRL company facts | 2015-2025 |  | 6: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| capex_musd | Capital spending | $ million |  | SEC XBRL company facts | 2015-2025 |  | 71: No fact under the XBRL tags used. NEE, DTE and HASI capex use company-specific tags | finance | not rated | Ready |
| depreciation_musd | Depreciation | $ million |  | SEC XBRL company facts | 2015-2025 |  | 65: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| operating_cash_flow_musd | Operating cash flow | $ million |  | SEC XBRL company facts | 2015-2025 |  | 13: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| total_assets_musd | Total assets | $ million |  | SEC XBRL company facts | 2015-2025 |  | 10: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| ppe_net_musd | Net property, plant and equipment | $ million |  | SEC XBRL company facts | 2015-2025 |  | 66: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| long_term_debt_musd | Long-term debt | $ million |  | SEC XBRL company facts | 2015-2025 |  | 42: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| equity_musd | Shareholders' equity | $ million |  | SEC XBRL company facts | 2015-2025 |  | 12: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |
| revenue_tag | XBRL tag used for revenue | text |  | SEC XBRL company facts | 2015-2025 |  | 7: No fact under the XBRL tags used, or field not applicable | finance | not rated | Ready |

## State Centroids

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| USPS | State code |  |  | Census 2020 county Gazetteer |  |  |  | Zhang | green | Ready |
| lat | Land-weighted latitude of county centroids | degrees |  | Census 2020 county Gazetteer |  |  |  | Zhang | green | Ready |
| lon | Land-weighted longitude of county centroids | degrees |  | Census 2020 county Gazetteer |  |  |  | Zhang | green | Ready |
| land_sqmi | Land area | sq mi |  | Census 2020 county Gazetteer |  |  |  | Zhang | green | Ready |

## W Inverse Distance

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| W Inverse Distance (50 state columns) | Row-standardized inverse-distance weight between two states | weight |  | Census 2020 county Gazetteer |  | 50 areas |  | Zhang | green | Ready |

## W Border

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| W Border (50 state columns) | 1 if two states share a border, from county adjacency | weight |  | Census county adjacency file |  | 50 areas |  | Zhang | green | Ready |

## W Distance Miles

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| W Distance Miles (50 state columns) | Distance between state centroids | miles |  | Census 2020 county Gazetteer |  | 50 areas |  | Zhang | green | Ready |

## Georgia

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| GA vs U.S. median | Georgia and the median of the 50 states, by year | see section | from Full Panel | EIA net generation by state |  | GA |  | Georgia | green | Ready |
| Large-load Table 2 | Pipeline, commitments and broken ground, approximate MW; Q2 2026 report, Table 2, PDF p. 8 | see section | as filed | Georgia Power large-load economic development reports, Q1 and Q2 2026 |  | GA |  | Georgia | yellow | Ready |
| Large-load attachment by stage and segment | Projects and announced load by stage and segment; from the attachment, tab Main | see section | summed by build_georgia_tables.py | Georgia Power large-load economic development reports, Q1 and Q2 2026 |  | GA |  | Georgia | yellow | Ready |
| Cited filing figures | Figures from the IRP and large-load reports with document and PDF page | see section | as filed; each checked against its page | Georgia Power 2025 IRP and 2023 IRP Update |  | GA |  | Georgia | yellow | Ready |
| Epoch Georgia sites | Epoch AI sites in Georgia, latest timeline row | see section | from raw Epoch files | Epoch AI data centers |  | GA |  | Georgia | green | Ready |

## Raw EIA Generation

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| YEAR | Column as published in annual_generation_state.xlsx. Not cleaned | As published |  | EIA net generation by state |  |  |  | Input to Full Panel | not rated | Ready |
| STATE | Column as published in annual_generation_state.xlsx. Not cleaned | As published |  | EIA net generation by state |  |  |  | Input to Full Panel | not rated | Ready |
| TYPE OF PRODUCER | Column as published in annual_generation_state.xlsx. Not cleaned | As published |  | EIA net generation by state |  |  |  | Input to Full Panel | not rated | Ready |
| ENERGY SOURCE | Column as published in annual_generation_state.xlsx. Not cleaned | As published |  | EIA net generation by state |  |  |  | Input to Full Panel | not rated | Ready |
| GENERATION (Megawatthours) | Column as published in annual_generation_state.xlsx. Not cleaned | As published |  | EIA net generation by state |  |  |  | Input to Full Panel | not rated | Ready |

## Raw EIA Capacity

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Year | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| State Code | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| Producer Type | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| Fuel Source | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| Generators | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| Facilities | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| Nameplate Capacity (Megawatts) | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |
| Summer Capacity (Megawatts) | Column as published in existcapacity_annual.xlsx. Not cleaned | As published |  | EIA existing capacity by state (Form EIA-860) |  |  |  | Input to Full Panel | not rated | Ready |

## Raw EIA Sales

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| (column A, no header) | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| (column B, no header) | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Revenues | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Sales | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Customers | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Price | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Revenues | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Sales | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Customers | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Price | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Revenues | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Sales | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Customers | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Price | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Revenues | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Sales | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Customers | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Price | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Revenues | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Sales | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Customers | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |
| Price | Column as published in HS861_2010-.xlsx. Not cleaned | As published |  | EIA retail sales and revenue (Form EIA-861) |  |  |  | Input to Full Panel | not rated | Ready |

## Raw EIA Emissions

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Year | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |
| State | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |
| Producer Type | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |
| Energy Source | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |
| CO2 (Metric Tons) | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |
| SO2 (Metric Tons) | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |
| NOx (Metric Tons) | Column as published in emission_annual.xlsx. Not cleaned | As published |  | EIA estimated emissions by state |  |  |  | Input to Full Panel | not rated | Ready |

## Raw EIA Plan Capacity

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Planned Year | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| State Code | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| Producer Type | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| Fuel Source | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| Generators | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| Facilities | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| Nameplate Capacity (Megawatts) | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |
| Summer Capacity (Megawatts) | Column as published in plancapacity_annual.xlsx. Not cleaned | As published |  | EIA planned capacity by state |  |  |  | Not used | not rated | Ready |

## Raw SEDS Use

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Data_Status | Column as published in use_all_btu.csv. Not cleaned | As published |  | EIA SEDS consumption |  |  |  | Input to Full Panel and SEDS Renewables | not rated | Ready |
| State | Column as published in use_all_btu.csv. Not cleaned | As published |  | EIA SEDS consumption |  |  |  | Input to Full Panel and SEDS Renewables | not rated | Ready |
| MSN | Column as published in use_all_btu.csv. Not cleaned | As published |  | EIA SEDS consumption |  |  |  | Input to Full Panel and SEDS Renewables | not rated | Ready |
| 1960-2024 (year columns) | Column as published in use_all_btu.csv. Not cleaned | As published |  | EIA SEDS consumption |  |  |  | Input to Full Panel and SEDS Renewables | not rated | Ready |

## Raw SEDS Prices

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Data_Status | Column as published in pr_all.csv. Not cleaned | As published |  | EIA SEDS prices |  |  |  | Input to SEDS Renewables | not rated | Ready |
| State | Column as published in pr_all.csv. Not cleaned | As published |  | EIA SEDS prices |  |  |  | Input to SEDS Renewables | not rated | Ready |
| MSN | Column as published in pr_all.csv. Not cleaned | As published |  | EIA SEDS prices |  |  |  | Input to SEDS Renewables | not rated | Ready |
| 1970-2024 (year columns) | Column as published in pr_all.csv. Not cleaned | As published |  | EIA SEDS prices |  |  |  | Input to SEDS Renewables | not rated | Ready |

## Raw BEA SAGDP2

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| GeoFIPS | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| GeoName | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| Region | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| TableName | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| LineCode | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| IndustryClassification | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| Description | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| Unit | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| 1997-2025 (year columns) | Column as published in SAGDP2__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |

## Raw BEA SAGDP9

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| GeoFIPS | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| GeoName | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| Region | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| TableName | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| LineCode | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| IndustryClassification | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| Description | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| Unit | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |
| 1997-2025 (year columns) | Column as published in SAGDP9__ALL_AREAS_1997_2025.csv. Not cleaned | As published |  | BEA GDP by state (SAGDP2, SAGDP9) |  |  |  | Input to Full Panel | not rated | Ready |

## Raw BEA SAINC1

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| GeoFIPS | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| GeoName | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| Region | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| TableName | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| LineCode | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| IndustryClassification | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| Description | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| Unit | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |
| 1929-2025 (year columns) | Column as published in SAINC1__ALL_AREAS_1929_2025.csv. Not cleaned | As published |  | BEA state personal income and population (SAINC1) |  |  |  | Input to Full Panel | not rated | Ready |

## Raw Census Pop V2025

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| SUMLEV | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| REGION | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DIVISION | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| STATE | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NAME | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| ESTIMATESBASE2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| POPESTIMATE2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| POPESTIMATE2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| POPESTIMATE2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| POPESTIMATE2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| POPESTIMATE2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| POPESTIMATE2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NPOPCHG_2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NPOPCHG_2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NPOPCHG_2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NPOPCHG_2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NPOPCHG_2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NPOPCHG_2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| BIRTHS2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| BIRTHS2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| BIRTHS2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| BIRTHS2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| BIRTHS2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| BIRTHS2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DEATHS2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DEATHS2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DEATHS2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DEATHS2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DEATHS2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DEATHS2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NATURALCHG2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NATURALCHG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NATURALCHG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NATURALCHG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NATURALCHG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NATURALCHG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| INTERNATIONALMIG2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| INTERNATIONALMIG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| INTERNATIONALMIG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| INTERNATIONALMIG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| INTERNATIONALMIG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| INTERNATIONALMIG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DOMESTICMIG2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DOMESTICMIG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DOMESTICMIG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DOMESTICMIG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DOMESTICMIG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| DOMESTICMIG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NETMIG2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NETMIG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NETMIG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NETMIG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NETMIG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| NETMIG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RESIDUAL2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RESIDUAL2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RESIDUAL2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RESIDUAL2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RESIDUAL2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RESIDUAL2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATESBASE2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATES2020 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATES2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATES2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATES2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATES2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| GQESTIMATES2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RBIRTH2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RBIRTH2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RBIRTH2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RBIRTH2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RBIRTH2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDEATH2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDEATH2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDEATH2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDEATH2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDEATH2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNATURALCHG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNATURALCHG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNATURALCHG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNATURALCHG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNATURALCHG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RINTERNATIONALMIG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RINTERNATIONALMIG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RINTERNATIONALMIG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RINTERNATIONALMIG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RINTERNATIONALMIG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDOMESTICMIG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDOMESTICMIG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDOMESTICMIG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDOMESTICMIG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RDOMESTICMIG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNETMIG2021 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNETMIG2022 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNETMIG2023 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNETMIG2024 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |
| RNETMIG2025 | Column as published in NST-EST2025-ALLDATA.csv. Not cleaned | As published |  | Census state population estimates (Vintage 2025; 2010-2020 intercensal) |  |  |  | Check of population | not rated | Ready |

## Raw Census Gazetteer

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| USPS | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| GEOID | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| ANSICODE | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| NAME | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| ALAND | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| AWATER | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| ALAND_SQMI | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| AWATER_SQMI | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| INTPTLAT | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |
| INTPTLONG | Column as published in 2020_Gaz_counties_national.txt. Not cleaned | As published |  | Census 2020 county Gazetteer |  |  |  | Input to land_sqmi and centroids | not rated | Ready |

## Raw Census Adjacency

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| County Name | Column as published in county_adj.txt. Not cleaned | As published |  | Census county adjacency file |  |  |  | Input to W Border | not rated | Ready |
| County GEOID | Column as published in county_adj.txt. Not cleaned | As published |  | Census county adjacency file |  |  |  | Input to W Border | not rated | Ready |
| Neighbor Name | Column as published in county_adj.txt. Not cleaned | As published |  | Census county adjacency file |  |  |  | Input to W Border | not rated | Ready |
| Neighbor GEOID | Column as published in county_adj.txt. Not cleaned | As published |  | Census county adjacency file |  |  |  | Input to W Border | not rated | Ready |

## Raw EPU Monthly

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| year | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| month | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalAK | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateAK | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeAK | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalAL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateAL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeAL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalAR | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateAR | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeAR | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalAZ | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateAZ | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeAZ | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalCA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateCA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeCA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalCO | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateCO | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeCO | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalCT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateCT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeCT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalDC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateDC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeDC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalDE | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateDE | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeDE | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalFL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateFL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeFL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalGA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateGA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeGA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalHI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateHI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeHI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalIA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateIA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeIA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalID | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateID | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeID | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalIL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateIL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeIL | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalIN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateIN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeIN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalKS | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateKS | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeKS | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalKY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateKY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeKY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalLA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateLA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeLA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMD | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMD | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMD | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalME | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateME | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeME | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMO | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMO | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMO | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMS | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMS | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMS | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalMT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateMT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeMT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalND | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateND | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeND | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNE | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNE | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNE | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNH | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNH | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNH | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNJ | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNJ | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNJ | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNM | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNM | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNM | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNV | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNV | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNV | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalNY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateNY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeNY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalOH | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateOH | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeOH | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalOK | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateOK | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeOK | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalOR | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateOR | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeOR | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalPA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StatePA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositePA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalRI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateRI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeRI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalSC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateSC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeSC | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalSD | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateSD | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeSD | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalTN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateTN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeTN | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalTX | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateTX | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeTX | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalUT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateUT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeUT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalVA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateVA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeVA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalVT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateVT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeVT | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalWA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateWA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeWA | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalWI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateWI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeWI | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalWV | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateWV | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeWV | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_NationalWY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_StateWY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |
| EPU_CompositeWY | Column as published in State_Policy_Uncertainty.xlsx. Not cleaned | As published |  | State Economic Policy Uncertainty |  |  |  | Input to EPU Annual | not rated | Ready |

## Raw OWID Solar

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Entity | Column as published in solar-pv-cumulative-capacity.csv. Not cleaned | As published |  | Solar PV capacity (IRENA via Our World in Data) |  |  |  | Input to OWID Solar | not rated | Ready |
| Code | Column as published in solar-pv-cumulative-capacity.csv. Not cleaned | As published |  | Solar PV capacity (IRENA via Our World in Data) |  |  |  | Input to OWID Solar | not rated | Ready |
| Year | Column as published in solar-pv-cumulative-capacity.csv. Not cleaned | As published |  | Solar PV capacity (IRENA via Our World in Data) |  |  |  | Input to OWID Solar | not rated | Ready |
| Solar photovoltaic | Column as published in solar-pv-cumulative-capacity.csv. Not cleaned | As published |  | Solar PV capacity (IRENA via Our World in Data) |  |  |  | Input to OWID Solar | not rated | Ready |

## Raw Epoch Sites

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Name | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Current H100 equivalents | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Current power (MW) | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Current total capital cost (2025 USD billions) | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Owner | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Users | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Selected Sources | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Calculations sheet | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Project | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Current chip types | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| All chip types | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Investors | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Construction companies | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Energy companies | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Country | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Address | Column as published in data_centers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |

## Raw Epoch Timelines

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Data center | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Date | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Construction status | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Buildings operational | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| IT power (MW) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Power (MW) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| H100 equivalents | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Performance (8-bit OP/s) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Total capital cost (2025 USD billions) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Compute cost (2025 USD billions) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Construction cost (2025 USD billions) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Annual operating cost (2025 USD billions) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Water use (MGD) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |
| Current H100 equivalents (from Data center) | Column as published in data_center_timelines.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Input to Epoch by State; Georgia | not rated | Ready |

## Raw Epoch Chips

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Handle | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Date | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Chip type | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Number of Units | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Chip type source | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Number of Units source | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Owner | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| User | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Notes | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Data center | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Timeline | Column as published in data_center_chip_quantities.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |

## Raw Epoch Chip Types

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Name | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| ML Hardware (linked) | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Designer | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Primarily for Chinese market | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| TDP (W) (from ML Hardware (linked)) | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| 16-bit FLOP/s | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| 8-bit OP/s | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Notes | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Memory | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Memory bandwidth | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| H100e | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Cost per chip (approx.) | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Release date | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Unofficial estimated TDP (W) | Column as published in chip_types.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |

## Raw Epoch Chillers

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Model | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Manufacturer | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Type | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Cooling capacity (kW) | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Number of fans | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Length (m) | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Width (m) | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Area (m^2) | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Source | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Link | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Spot check | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Notes | Column as published in data_center_chillers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |

## Raw Epoch Cooling Towers

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Model | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Manufacturer | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Length (m) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Width (m) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Height (m) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Area (m^2) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Cooling capacity (stated, kW) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Cooling capacity (central estimate, kW) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Source | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Link | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Spot check | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Notes | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Fan Diameter (m) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Number of Fans | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Fan estimate diameter (m) | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Type | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |
| Motor Horsepower | Column as published in data_center_cooling_towers.csv. Not cleaned | As published |  | Epoch AI data centers |  |  |  | Not used | not rated | Ready |

## Raw RMI Customers Sales

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| parent_name | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_name | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_id_ferc1 | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| year | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| customer_type | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| customer_type_rmi | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| customers | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| sales | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| revenue | Column as published in customers_sales.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |

## Raw RMI Net Plant

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| parent_name | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_name | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_id_ferc1 | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| year | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| technology_ferc | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| technology | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| original_cost | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| accum_depr | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| net_plant_balance | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| arc_gross | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| arc_accum_depr | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| arc_net | Column as published in net_plant_balance.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |

## Raw RMI Reliability

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| parent_name | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_name | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_id_eia | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_type_rmi | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| year | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| state | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| reliability_standard | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| outage_conditions | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| customers | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| interruptions | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| minutes | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| saidi | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| saifi | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| caidi | Column as published in reliability.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |

## Raw RMI Housing Income

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| parent_name | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_name | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| respondent_id | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| year | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| percent_AMI | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| ownership | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| housing_units | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| income | Column as published in housing_units_income.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |

## Raw RMI Emission Targets

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| owned_delivered | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| parent_name | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_name_irp | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_type_rmi | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| year | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| emissions_co2_historical | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| emissions_co2_target | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| emissions_co2_irp | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| emissions_co2_1point5c | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| net_generation_mwh | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| net_generation_mwh_1point5c | Column as published in emissions_targets.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |

## Raw RMI Debt Equity

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| parent_name | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| ticker | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_name | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| utility_id_ferc1 | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| year | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| rate_case_data_year | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| rate_base_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| equity_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| debt_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| equity_ratio_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| returns_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| earnings_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| interest_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| fed_tax_expense_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| pre_tax_net_income_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| ror_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| roe_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| interest_rate_realized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| equity_ratio | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| ror | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| roe | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| interest_rate | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| effective_fed_tax_rate | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| equity_authorized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| debt_authorized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| returns_authorized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| earnings_authorized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| interest_authorized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |
| interest_rate_authorized | Column as published in debt_equity_returns.csv. Not cleaned | As published |  | RMI Utility Transition Hub |  |  |  | Not used | not rated | Ready |

## none

| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| large_load_q1_q4_2024 | Georgia Power large-load reports for Q1-Q4 2024 |  |  | Georgia Power large-load reports, Q1-Q4 2024 |  |  | Need a browser download; the PSC list returns 404 to scripts | Georgia | not run | Pending |

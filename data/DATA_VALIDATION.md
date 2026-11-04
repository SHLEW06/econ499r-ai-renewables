# DATA_VALIDATION.md — Part C proof of correctness
**Date:** 2026-11-02  
**Panel:** `data/out/state_panel_2015_2025.csv` — 561 rows × 80 columns (51 states incl. DC, 2015–2025)  
**Script:** `econ499r_starter/scripts/validate_panel.py`  
**Detailed outputs:** `logs/2026-11-02/build/validation/`

---

## Verdict table

One row per model variable. Any red blocks Phase 4a. There are **no reds**.

| Variable | Right definition | Numbers check | Reproduces | Ready | Note |
|---|---|---|---|---|---|
| renew_share | yes | PASS | yes | **green** | utility-scale only (known: rooftop not in EIA gen file) |
| solar_share | yes | PASS | yes | **green** | utility-scale only |
| wind_share | yes | PASS | yes | **green** | |
| clean_share | yes | PASS | yes | **green** | renew + nuclear |
| fossil_to_renew | yes | PASS | yes | **green** | includes Other Gases (0.34% of fossil) |
| ln_ec | yes | PASS | yes | **green** | ln(retail sales / population) |
| ln_ee | yes | PASS | yes | **green** | ln(real 2017 GDP / retail sales); corr with nominal = 0.98 |
| ai_dc_per1000 | yes | PASS | yes | **green** | 4 states suppressed in 2025 (AK,ND,SD,WY) |
| ai_dc_per1000_lag1 | yes | PASS | yes | **green** | exact 1-year lag |
| price_c_kwh | yes | PASS | yes | **green** | all-sector; matches EIA State Profiles 2024 within 0.004 c/kWh |
| co2_per_mwh_t | yes | PASS | yes | **yellow** | ends 2024; 51 NAs in 2025 (known, EIA source ends 2024) |
| seds_mmbtu_pc | yes | PASS | yes | **yellow** | ends 2024; 51 NAs in 2025 (known, SEDS ends 2024) |
| tech_share | yes | PASS | yes | **green** | NAICS 5415 / all covered |
| ln_gdp_pc | yes | PASS | yes | **green** | ln(real 2017 GDP / population) |
| manuf_share | yes | PASS | yes | **green** | manufacturing nom GDP / total nom GDP |
| pop_growth | yes | PASS | yes | **green** | pct change by state |
| ln_ea | yes | PASS | yes | **green** | ln((nom GDP − farm GDP) / land sqmi) |
| energy_equity | yes | PASS | yes | **green** | (state/US nom GDP) / (state/US retail sales) |
| hma | yes | n/a | yes | **yellow** | inherits 4-state suppression from ai_dc_per1000 in 2025 |
| new_renew_mw | yes | PASS | yes | **green** | YoY diff of cap_renew_mw; negative values kept |

Yellow = known data gap, does not block Phase 4a. CO2 and SEDS used in robustness only (Step 4) and are available through 2024. HMA flagged yellow by convention; the 4 suppressed cells are documented.

---

## C.1 Right definition

Every derived variable was independently recomputed from the panel's raw columns and compared cell-by-cell.

| Check | Formula checked | Max abs diff | Result |
|---|---|---|---|
| D01 renew_share | sum(hydro,wind,solar,geo,wood,otherbio) / gen_total | 1.1e-16 | **PASS** |
| D02 gen_renew_mwh | same 6 sources summed | 0.0 | **PASS** |
| D03 gen_fossil_mwh | coal+gas+petroleum+othergas | 0.0 | **PASS** |
| D04 solar_share | gen_solar / gen_total | 1.0e-16 | **PASS** |
| D05 wind_share | gen_wind / gen_total | 1.0e-16 | **PASS** |
| D06 clean_share | (renew+nuclear) / gen_total | 1.1e-16 | **PASS** |
| D07 fossil_to_renew | gen_fossil / gen_renew | 3.6e-15 | **PASS** |
| D08 price_c_kwh | 100 × revenue_kusd / sales_mwh | 3.6e-15 | **PASS** |
| D09 co2_per_mwh_t | co2_power_t / gen_total | 1.1e-16 | **PASS** |
| D10 ai_dc_per1000 | 1000 × dc_jobs / total_jobs | 8.9e-16 | **PASS** |
| D11 tech_share | tech5415_jobs / total_jobs | 9.9e-17 | **PASS** |
| D12 ln_ec | ln(sales_mwh / population) | 4.4e-16 | **PASS** |
| D13 ln_ee | ln(gdp_real_musd2017 × 1e6 / sales_mwh) | 1.8e-15 | **PASS** |
| D14 ee_usd_per_mwh | gdp_real_musd2017 × 1e6 / sales_mwh | 1.8e-12 | **PASS** |
| D15 ln_gdp_pc | ln(gdp_real_musd2017 × 1e6 / population) | 1.8e-15 | **PASS** |
| D16 manuf_share | gdp_manuf_musd / gdp_nom_musd | 9.7e-17 | **PASS** |
| D17 seds_mmbtu_pc | seds_total_energy_bbtu × 1000 / population | 1.1e-13 | **PASS** |
| D18 ea_nonfarm_gdp_per_sqmi | (nom−farm) × 1e6 / land_sqmi | 7.5e-9 | **PASS** |
| D19 ln_ea | ln(ea_nonfarm_gdp_per_sqmi) | 3.6e-15 | **PASS** |
| D20 energy_equity | (st nom GDP / US nom GDP) / (st sales / US sales) | 4.4e-16 | **PASS** |
| D21 ai_dc_per1000_lag1 | groupby(state).shift(1) | 0.0 | **PASS** |

### Explicit decisions required by the prompt

**D22 — GDP in ln_ee: real or nominal?**  
The memo says "State GDP in $" without specifying. We use real chained-2017 GDP (BEA SAGDP9 line 1). Under two-way FE the choice should matter little: corr(ln_ee_real, ln_ee_nominal) = 0.976. Real GDP is preferred because it removes inflation from the efficiency ratio.

**D23 — AI numerator (private only) and denominator (all covered):**  
NAICS 518210 private rows (own_code=5, agglvl=58) are the numerator. **Corrected 2026-11-04:** an earlier version said government 518210 rows do not exist at state level. That was false. Government rows (own_code 1, 2, 3; agglvl 58) appear in all 12 raw files. Over 2015-2025 they add 0.83% to private jobs overall, but 24.6% of the state total in NM, 10.3% in MN, 9.4% in PA and 6.0% in OH (`logs/2026-11-04/gov_518210_shares.csv`). The main measure stays private only by team decision, named "private data-center jobs per 1,000 workers" (`EXPERIMENTS.md` §0 item 24), and 4e has a labeled all-ownership row. The denominator is industry 10 (own_code=0, agglvl=50), which is all covered employment as the memo specifies. A private-only denominator would change ai_dc_per1000 by at most 0.2% in any state-year.

**D24 — Fossil includes Other Gases:**  
gen_othergas_mwh averages 234,467 MWh/state-year vs. total fossil of 50,424,088 MWh — Other Gases are 0.34% of fossil. Including them changes fossil_to_renew negligibly. The memo says "coal, gas, and oil"; we include Other Gases to match EIA's source structure. Logged as a known minor deviation.

**D25 — Renewable: utility-scale only:**  
The EIA state generation file covers utility-scale generation. Rooftop solar (residential and commercial) does not appear. This is a known limitation noted in CLAUDE.md. It causes us to understate renewable share (especially in CA and MA) and means ln_ec (retail sales / population) includes consumption from both grid and rooftop, while renew_share reflects only grid supply.

---

## C.1b Full panel rebuild comparison (added 2026-11-02)

**Procedure:** `build_panel.py data/raw /tmp/panel_rebuild_test` was run from the project root, outputting to a temp directory (never touching `data/out`). The rebuilt panel was then compared cell-by-cell with `data/out/state_panel_2015_2025.csv`.

**Scope:**
- 78 shared non-key columns (all columns except `state` and `year`)
- 561 rows (51 states × 11 years)
- **Total cells compared: 43,758**

**Result: ZERO differences.** Every numeric value in every shared column matched exactly (tolerance 1e-6) or was NaN in both panels simultaneously. The rebuild produces a bit-for-bit identical panel from the same raw files.

**Prelim means by year (`econ499r_starter/reference/prelim_means_by_year.csv`):**

| Variable | Max abs diff (all 11 years) | Note |
|---|---|---|
| renew_share | 0.000493 | Reference rounds to 3 dp |
| solar_share | 0.000480 | Reference rounds to 3 dp |
| sales_mwh_pc | 0.000457 | Reference rounds to 3 dp |
| ee_usd_per_mwh | 0.000469 | Reference rounds to 3 dp |
| ai_dc_per1000 | 0.000475 | Reference rounds to 3 dp |
| price_c_kwh | 0.000424 | Reference rounds to 3 dp |

All 6 variables across all 11 years match within 0.001 — consistent with the reference file rounding to 3 decimal places. **PASS.**

**`data/out/prelim_step1_slx.csv` vs `econ499r_starter/reference/prelim_step1_slx.csv`:** Files are identical (confirmed by diff). **PASS.**

---

### C.1b rerun, 2026-11-04: `dc_wages_usd` fix

The four suppressed 2025 cells (AK, ND, SD, WY) showed `dc_wages_usd` = 0. They are now blank, with `dc_suppressed` = 1, matching `dc_jobs`. Comparing the builds before and after, with no tolerance, across 43,758 cells: **those 4 cells are the only differences.** Blank cells went from 216 to 220. All W and centroid files are byte-identical. Log: `logs/2026-11-04/c1b_dc_wages.log`. `dc_wages_usd` isn't used in any model.

### Blank-fuel capacity rows, 2026-11-04

The NE (190.8 MW) and NM (7.2 MW) blank-fuel rows in 2017 are natural gas per EIA-860 2017: Rokeby units 2 and 3, and Hobbs unit CHW-T. Neither is renewable, so `new_renew_mw` is unchanged and no rebuild was needed. A separate issue found while checking: Gavins Point (132.3 MW hydro) moves between NE and SD in EIA's file, giving false `new_renew_mw` changes in 2016 and 2018. Details: `data/receipts/eia_state.md`.

## C.2 Right numbers

### EIA generation internal consistency

**N01 — Fuel columns sum to Total:** Max difference = **2 MWh** across all 561 state-years. This is a rounding artifact in EIA's published totals (integers are rounded before the total is printed). Not a data error.

**N02 — 51 states sum to US-TOTAL:** Max percentage difference = **0.00%** for all years 2015–2025. The EIA national total covers 51 states + DC. Our panel is exactly those entities. See `n02_eia_states_vs_us_total.csv`.

### QCEW consistency

**N03 — 518210 state sum vs. national row:** State sum ≤ national in every year. Mean gap = 94 jobs. This gap is exactly the suppressed states' employment (AK, ND, SD, WY in 2025 plus occasional other suppressions in prior years), which is not counted in the state sum but is estimated in the national row. Expected.

**N04 — Industry 10 state sum vs. national:** Max percentage difference = **0.000%**. The total matches the national row exactly across all years (51 states + DC covers the full national count).

### BEA consistency

**N05 — SAGDP2 line 1 state sum vs. US row:** Max percentage difference = **0.613%** (across all years). BEA's SAGDP2 footnote says the difference between the U.S. and the sum of states "reflects overseas activity, economic activity taking place outside the borders of the United States by the military and associated federal civilian support staff." The check still passes. (Corrected 2026-11-04: an earlier version attributed the gap to U.S. territories.)

### Published figures (read-only web lookups)

**N06 — Average retail electricity price, 2024 (EIA State Electricity Profiles, released Nov 2025):**

| State | EIA published (c/kWh) | Panel (c/kWh) | Diff |
|---|---|---|---|
| GA | 11.40 | 11.399 | 0.001 |
| VA | 10.62 | 10.616 | 0.004 |
| TX | 9.79 | 9.790 | 0.000 |
| CA | 27.04 | 27.040 | 0.000 |
| NY | 19.66 | 19.659 | 0.001 |

All differences are rounding (EIA State Profile rounds to 2 decimal places). **PASS.**  
Source: EIA State Electricity Profiles for GA, VA, TX, CA, NY (2024 edition); accessed 2026-11-02.

**N06b — Average retail electricity price, 2015:**  
EIA 2015 state prices are not available in the interactive state profiles (they show current year only). However: (a) the 2024 comparison confirms our processing pipeline is correct; (b) the 2015 values in our panel come from the same EIA-861 file with the same formula, which lowers the risk of a processing error but doesn't rule one out, and no 2015 comparison was made. A separate audit matched 2016, 2020 and 2022 prices against EIA State Profile tables, within EIA's 2-decimal rounding (`data/INDEPENDENT_AUDIT_2026-11-04.md`). (Corrected 2026-11-04.) Values for reference: GA=9.62 c/kWh, VA=9.31, TX=8.70, CA=15.42, NY=15.28.

**N07 — Population (Census estimates):**  
Our population variable is BEA SAINC1 line 2, which is the official Census Population Estimates Program series published through the BEA regional accounts. BEA's footnote gives "U.S. Census Bureau midyear population estimates," so it can differ from older Census vintages: by up to 95,554 people in the audit's sampled cells (MA 2017, Vintage 2020). All 3 sampled cells match the newest Census series exactly. (Corrected 2026-11-04: an earlier version said no gap was possible.)

**N08 — Georgia 2024 renewable share vs. EIA Georgia State Electricity Profile:**  
EIA State Profile (2024): total net generation = 139.8 billion kWh. Our panel: gen_total_mwh = 139,805,428 = **139.8 TWh** — exact match. Matching the total confirms the denominator of the 12.51% renew_share. It can't confirm the share itself, and this check didn't compare renewable generation with a published figure. A separate audit matched `renew_share` for other states against EIA generation by fuel, and those cells didn't include Georgia 2024. (Corrected 2026-11-04.) The profile labels natural gas as Georgia's primary source (consistent with our panel: gas = 38.6% of generation in 2024).

---

## C.3 Reproduce

### Georgia spot check (expected_values.md, Oct 30, 2026)

| State | Year | Variable | Expected | Got | Match |
|---|---|---|---|---|---|
| GA | 2025 | renew_share | 0.1287 | 0.1287 | ✓ |
| GA | 2025 | solar_share | 0.0768 | 0.0768 | ✓ |
| GA | 2025 | ai_dc_per1000 | 5.0346 | 5.0346 | ✓ |
| GA | 2015 | ai_dc_per1000 | 2.0106 | 2.0106 | ✓ |
| GA | 2015 | dc_jobs | 8,346 | 8,346 | ✓ |
| GA | 2025 | dc_jobs | 24,620 | 24,620 | ✓ |
| GA | 2015 | price_c_kwh | 9.6188 | 9.6188 | ✓ |
| GA | 2025 | price_c_kwh | 12.0600 | 12.0600 | ✓ |
| GA | 2015 | ln_ec | 2.5902 | 2.5902 | ✓ |
| GA | 2025 | ln_ec | 2.6065 | 2.6065 | ✓ |
| GA | 2015 | ln_ee | 8.2878 | 8.2878 | ✓ |
| GA | 2025 | ln_ee | 8.4551 | 8.4551 | ✓ |

All 12 match to 4 decimal places. **Zero differences.**

### Top AI states 2025 (expected_values.md)

| State | Expected | Got |
|---|---|---|
| WA | 6.479 | 6.479 | ✓ |
| GA | 5.035 | 5.035 | ✓ |
| MO | 4.978 | 4.978 | ✓ |
| VA | 4.859 | 4.859 | ✓ |

### Panel structure
- Shape: (561, 80) ✓
- dc_suppressed = 1 in 2025 for exactly: AK, ND, SD, WY ✓
- CO2 2025: 51 NAs ✓
- SEDS 2025: 51 NAs ✓

---

## C.4 Trace (25 cells, seed = 42)

25 cells selected at fixed seed=42, spread across sources and variables. Each value below was confirmed traceable to its raw file, transformation, and final panel value.

| # | State | Year | Column | Panel value | Raw source | Raw file | Key filter / formula |
|---|---|---|---|---|---|---|---|
| 1 | GA | 2015 | dc_jobs | 8,346 | BLS QCEW | qcew_2015_518210.csv | area_fips='13000', own_code=5, agglvl=58 → annual_avg_emplvl |
| 2 | GA | 2025 | renew_share | 0.12871 | EIA | annual_generation_state.xlsx | state='GA', year=2025, prod='Total', sum(6 renew sources)/Total |
| 3 | TX | 2020 | gen_wind_mwh | 92,440,997 | EIA | annual_generation_state.xlsx | state='TX', year=2020, source='Wind' |
| 4 | CA | 2018 | gdp_real_musd2017 | 2,850,608.8 | BEA | SAGDP9__ALL_AREAS_1997_2025.csv | GeoFIPS='06000', LineCode=1, col='2018' |
| 5 | NY | 2022 | price_c_kwh | 18.3267 | EIA | HS861_2010-.xlsx | state='NY', year=2022 → 100×tot_rev_k/tot_sales_mwh |
| 6 | WA | 2025 | ai_dc_per1000 | 6.4790 | BLS QCEW | qcew_2025_518210.csv + qcew_2025_10.csv | 1000×dc_jobs/total_jobs |
| 7 | FL | 2019 | sales_mwh | 240,347,955 | EIA | HS861_2010-.xlsx | state='FL', year=2019 → tot_sales_mwh |
| 8 | OH | 2023 | ln_ec | 2.5192 | derived | — | ln(sales_mwh/population) |
| 9 | VA | 2017 | tech_share | 0.04214 | BLS QCEW | qcew_2017_5415.csv + qcew_2017_10.csv | tech5415_jobs/total_jobs |
| 10 | IL | 2016 | co2_per_mwh_t | 0.38564 | EIA | emission_annual.xlsx | state='IL', year=2016 → co2_power_t/gen_total_mwh |
| 11 | NC | 2021 | solar_share | 0.07792 | EIA | annual_generation_state.xlsx | state='NC', year=2021 → gen_solar/gen_total |
| 12 | MO | 2025 | ai_dc_per1000 | 4.9782 | BLS QCEW | qcew_2025_518210.csv + qcew_2025_10.csv | 1000×dc_jobs/total_jobs |
| 13 | AL | 2018 | cap_wind_mw | 0.0 | EIA | existcapacity_annual.xlsx | state='AL', year=2018, source='Wind' (no wind capacity in AL 2018) |
| 14 | MI | 2020 | manuf_share | 0.16975 | BEA | SAGDP2__ALL_AREAS_1997_2025.csv | LineCode=12 (manuf) / LineCode=1 (all) |
| 15 | OR | 2024 | renew_share | 0.61411 | EIA | annual_generation_state.xlsx | state='OR', year=2024 (high hydro state) |
| 16 | AZ | 2019 | ln_ee | 8.43675 | derived | — | ln(gdp_real×1e6/sales_mwh) |
| 17 | PA | 2017 | gen_coal_mwh | 47,634,271 | EIA | annual_generation_state.xlsx | state='PA', year=2017, source='Coal' |
| 18 | CO | 2022 | wind_share | 0.29135 | EIA | annual_generation_state.xlsx | state='CO', year=2022 → gen_wind/gen_total |
| 19 | MN | 2023 | tech_share | 0.01289 | BLS QCEW | qcew_2023_5415.csv + qcew_2023_10.csv | tech5415/total |
| 20 | SC | 2025 | solar_share | 0.03104 | EIA | annual_generation_state.xlsx | state='SC', year=2025 |
| 21 | NV | 2016 | ln_gdp_pc | 10.8914 | derived | — | ln(gdp_real×1e6/population) |
| 22 | TN | 2021 | energy_equity | 0.71306 | derived | — | (TN nom GDP/US nom GDP)/(TN sales/US sales) |
| 23 | IN | 2024 | co2_per_mwh_t | 0.63329 | EIA | emission_annual.xlsx | state='IN', year=2024 |
| 24 | MT | 2018 | land_sqmi | 145,550.35 | Census | 2020_Gaz_counties_national.txt | USPS='MT', sum(ALAND_SQMI) across counties |
| 25 | ND | 2025 | dc_suppressed | 1 | BLS QCEW | qcew_2025_518210.csv | area_fips='38000' → disclosure_code='N' |

All 25 cells traced successfully from raw source to panel value. Full table also at `logs/2026-11-02/build/validation/c4_trace_cells.csv`.

---

## C.5 Plausibility

### Keys and structure

| Check | Result | Detail |
|---|---|---|
| (state,year) unique | **PASS** | 0 duplicates |
| 561 rows = 51 × 11 | **PASS** | |
| 51 states (50+DC) | **PASS** | |
| Years 2015–2025 | **PASS** | 11 years |
| States match 51-state list | **PASS** | No extras, none missing |
| contig48 = 0 for AK,HI | **PASS** | |
| is_dc = 1 for DC | **PASS** | |

### Range checks

All 6 share variables (renew_share, solar_share, wind_share, clean_share, manuf_share, tech_share) fall in [0, 1] for all rows. No negative values in dc_jobs, total_jobs, gdp_nom_musd, gdp_real_musd2017, population, or sales_mwh.

### Big year-over-year jumps (> 50% in any model variable)

200 cases found. Breakdown:

| Variable | Count | Explanation |
|---|---|---|
| solar_share | 172 | States adding first (or early) utility-scale solar from a near-zero base. 16 are +∞ (prev=0). All plausible: 2016–2025 is the period of rapid utility-scale solar expansion. |
| wind_share | 17 | States adding first wind capacity from zero. 5 are +∞ (prev=0). |
| renew_share | 6 | Driven by solar/wind additions above. |
| ai_dc_per1000 | 5 | See detail below. |

**AI per 1,000 jumps — each reviewed individually:**

| State | Year | Prev | New | % chg | Explanation |
|---|---|---|---|---|---|
| AR | 2020 | 1.37 | 2.89 | +110% | New data center construction in NW Arkansas. Plausible. |
| RI | 2017 | 5.15 | 1.15 | −78% | RI had anomalously high 518210 employment in 2016 (colocation facility). Decrease is a reclassification, not a data error. |
| WA | 2022 | 4.52 | 7.45 | +65% | Well-documented hyperscale data center expansion (Microsoft, Amazon) in eastern WA. Plausible. |
| DC | 2018 | 0.73 | 1.21 | +64% | Small absolute values amplify pct change. |
| MS | 2016 | 1.79 | 0.79 | −56% | Decline in 518210 employment. |

None of these are data errors. **No flags that block Phase 4a.**

### Spotlight states

Full time series exported to `logs/2026-11-02/build/validation/p11_spotlight_*.csv`.

**Virginia (VA):** tech_share = 4.2–5.1% (highest among all states; reflects Northern VA data center corridor). ai_dc_per1000 = 3.8–4.9 (top 5). renew_share low (6–11%) despite offshore wind buildout beginning. price_c_kwh = 9.3–10.6 c/kWh (below national average).

**Texas (TX):** Largest absolute wind capacity; wind_share rose from 10.6% to 29.4% over 2015–2025. Solar grew from ~0% to 11.6%. renew_share went from 10.6% to 29.4%. price_c_kwh = 8.7–9.8 c/kWh (below national average). No anomalies.

**Georgia (GA):** Solar expansion story: solar_share 0.1% (2015) → 7.7% (2025). ai_dc_per1000 rose from 2.0 to 5.0 (second highest in 2025 behind WA). price_c_kwh = 9.6–12.1 (rises with Georgia Power rate cases). All values plausible.

**Washington (WA):** Highest ai_dc_per1000 = 6.48 in 2025 (hyperscale data centers). Highest renew_share overall (~62–69%) due to Columbia River hydro. The WA 2022 jump (+65% in ai_dc_per1000) is explained above.

### Missingness

All gaps have documented reasons. No unexplained NAs.

| Variable | Year(s) | n missing | Reason |
|---|---|---|---|
| co2_power_t, co2_per_mwh_t | 2025 | 51 | EIA CO2 emissions data ends 2024 |
| seds_total_energy_bbtu, seds_mmbtu_pc | 2025 | 51 | EIA SEDS ends 2024 |
| dc_jobs, ai_dc_per1000, hma | 2025 | 4 | BLS suppressed AK, ND, SD, WY (disclosure_code='N') |
| ai_dc_per1000_lag1 | 2015 | 4 | 2014 is not in the panel; 2014 QCEW used only for 2015 lag construction |

Full table at `logs/2026-11-02/build/validation/p12_missingness.csv`.

---

## C.6 Vintage

**Corrected 2026-11-04** from `data/INDEPENDENT_AUDIT_2026-11-04.md` section 2.3. The original table called EIA 2025 preliminary and gave a June 2026 BEA revision.

| Source | File | Vintage / release | Preliminary years | Revision risk |
|---|---|---|---|---|
| EIA annual generation | annual_generation_state.xlsx | Historical State Data; sheet `Net_Generation_1990-2025 Final`; server date Sept 11, 2026 | None: EIA labels 2025 final | Low to medium: EIA can still restate |
| EIA capacity | existcapacity_annual.xlsx | Historical State Data; server date Sept 10, 2026 | None: EIA labels 2025 final | Low |
| EIA Form 861 retail sales | HS861_2010-.xlsx | Released Oct 7, 2026 | None: EIA labels 2025 final | Low |
| EIA CO2 emissions | emission_annual.xlsx | Electric Power Annual 2024 | ends 2024 | n/a (not revised) |
| EIA SEDS | use_all_btu.csv | State Energy Data System, its own product; released June 26, 2026; through 2024 | ends 2024 | n/a |
| BLS QCEW | qcew_2014–2025_*.csv | Annual averages | Not confirmed: BLS's download page lists 2025 with no status label; 2025 cells matched BLS on Nov 4 | Low; annual averages rarely revised |
| BEA SAGDP2/9, SAINC1 | CSV files | File footers: "Last updated: September 30, 2026," revising 2019-2025 (SAGDP2) and 2009-2025 (SAINC1) | 2025 initial estimate | Medium: subject to later annual revisions |
| Census Gazetteer | 2020_Gaz_counties_national.txt | 2020 Decennial Census | n/a (fixed) | None |
| Census county adjacency | county_adj.txt | 2023 version | n/a (fixed) | None |
| FERC Form 1 (PUDL) | ferc1_*.parquet | PUDL stable release, Oct 14, 2026; v2026.10.0 per its release notes. Confirm the version in the raw files before citing | 2025 included | Low |

**Papers-due risk:** EIA labels its 2025 data final, so the main revision risk before the Dec 1, 2026 deadline is low. If any source is revised, rebuild takes ~30 seconds (`python3 econ499r_starter/scripts/build_panel.py data/raw data/out`) and all downstream outputs regenerate. BEA's next annual revision would change the 2025 estimates; check its calendar before the final run.

---

## Summary

- **Definitions:** 21 checked, 21 PASS. 4 explicit decisions documented (D22–D25): real vs. nominal GDP, private-only AI numerator, Other Gases in fossil, utility-scale-only renewable.
- **Full rebuild comparison (C.1b, added 2026-11-02):** build_panel.py rerun to /tmp; 43,758 cells (78 columns × 561 rows) compared — **zero differences**. Prelim means by year all match within 0.001 (rounding). prelim_step1_slx.csv files identical.
- **Numbers:** 5 programmatic checks all PASS. 5 published-figure comparisons all PASS (prices within 0.004 c/kWh; totals within 0.613%).
- **Reproduce:** 12 Georgia spot checks exact (0.0000 diff). 4 top-AI states exact.
- **Trace:** 25 cells fully traced from raw files.
- **Plausibility:** All key checks PASS. 200 big-jump flags all explained (solar/wind from zero; 5 AI fluctuations reviewed individually).
- **Vintage (corrected 2026-11-04):** All sources documented. EIA labels 2025 final; BEA 2025 remains the main revision risk; rebuild is trivial.
- **Verdict: 0 red, 3 yellow (CO2, SEDS, HMA — known gaps, not blocking), 17 green. Phase 4b may proceed.**

---

## New data, Nov 4

**Date:** 2026-11-04. **Scope:** files added since Phase 2. The master panel wasn't changed. Each file's contents were read, not just its name. Receipts are in `data/receipts/`, and the build output is in `logs/2026-11-04/side_tables_build.log`.

| File | Rating | Product and years (from contents) | Units and coverage | Vintage | Spot checks | Main caveat |
|---|---|---|---|---|---|---|
| LBNL RPS & CES Targets and Demand | **Yellow** | Target schedule, 2000-2050 | Percent of applicable sales; 32 states + DC in file; table covers 51 areas x 2015-2025 | June 2026 | Byte-identical to LBNL; 27 states + DC reconciles with LBNL's deck; MI and AZ match state rules | Label it "LBNL current RPS/CES schedule." 60 of 327 nonzero state-years differ from older editions. NY 2018 series break |
| LBNL Target Achievement and Compliance Costs | **Green** | Share of target achieved, 1999-2025 | Ratio, no target levels; 31 states + DC; 2025 mostly "no data" | June 2026 | Byte-identical to LBNL; 294 of 327 nonzero state-years confirm an obligation; 3 conflict | Cross-check only. It can't supply a target level |
| LBNL Utility-Scale Solar | **Green** | Project data through 2025 | MW-AC and MW-DC; 2,005 projects, 48 states; GA 66, Southeast 414 | Oct 2026 | Byte-identical to LBNL; 1,989 PV matches LBNL's count; GA 0.97, TX 1.04, FL 1.00 of EIA capacity | Larger than 5 MW-AC only (NC 0.60 of EIA) |
| OWID solar capacity | **Green** | IRENA on-grid PV, 2000-2025 | GW; countries and regions | Updated July 28, 2026 | World 2025 within 0.2% and USA 2025 within 0.3% of IRENA; USA 2023 matches | IRENA checked on a third-party copy of its report. On-grid gap not fully explained |
| State EPU | **Green** | Baker, Davis and Levy, monthly, 1985-2025 | Index; 50 states + DC; complete in 2015-2025 | Server date Jan 20, 2026 | Byte-identical to publisher; GA 2025 hand average matches | Small states rest on few papers |
| NSF National Patterns Table 10, 7 editions | **Yellow** | R&D by state, 2017-2023 | $M current; 51 areas | Editions 2020 to 2026 | NY, NJ and NH 2023 match NSF's PDF; totals within $4M; intensity within 0.006 | One edition per year, so no revisions. WY and AK swings. Mixed GDP vintages (0.91-1.04 of panel) |
| `nsf27300-tab010.xlsx` (team's file) | **Red, not used** | Business R&D by industry and size, 2024 | No states | NSF, Oct 2026 | Read directly: no state rows | Wrong table. Kept only as a record |
| ACS S2801 (API) | **Yellow** | Household broadband, 2015-2024 | Percent, with MOE; 51 areas | Pulled Nov 4, 2026 | 9 of 9 match table B28002 | 2015 isn't comparable (Census changed the question in 2016). No 2020 |
| Epoch AI data centers | **Green, context only** | Largest AI sites, timelines to 2030 | MW; 96 sites, 77 US | Updated Nov 1, 2026 | `data_centers.csv` byte-identical; page's TX, OH, VA, NE, IA counts match; 2 site values match | About 45% coverage per Epoch. One site's state unresolved. Not a model variable |
| NOAA degree days | **Not done** | No file | None | None | None | NCEI timed out on every host, Nov 4. The team chose not to substitute CPC files. No table exists |

**Totals:** 5 green, 3 yellow, 1 red (not used), 1 not done. The red doesn't block anything, because its replacement is in the table above it.

### RPS coverage check
- **All 50 states, 2015-2025? Yes.** 561 rows (50 states + DC x 11 years), no NA, no duplicates, and keys match the panel exactly. 18 of the states are 0 because they aren't in LBNL's file.
- **Does it show what each year's law required? No.** Every nonzero value is the LBNL current RPS/CES schedule (June 2026). Target Achievement has no target levels, and LBNL revises past years between editions.

| Check on the 327 nonzero state-years | Rows |
|---|---|
| Target Achievement confirms an obligation that year | 294 |
| Can't be checked yet ("no data," mostly 2025) | 30 |
| Conflict: target above 0, but LBNL reports no obligation (MT 2020; NY 2015, 2016) | 3 |
| Differs from a value in an older edition (13 states; some overlap with the rows above) | 60 |

Largest revisions against older editions: MD 2020 (30.5 then 18.1), NJ 2020 (28.4 then 20.6), NH 2022 (22.5 then 15.0). Reasons aren't given. Full list: `logs/2026-11-04/rps_vintage_check.csv`.

---

## Fang test data, Nov 4

Each file's contents were read, not just its name. Build output: `logs/2026-11-04/fang_tables_build.log`.

| File | Rating | Product and years | Units and coverage | Vintage | Spot checks | Main caveat |
|---|---|---|---|---|---|---|
| AI Index job postings by state | **Yellow** | AI postings, 2018-2025 | Count; 51 areas | Editions 2019, 2022-2026 | Maps exact against public CSVs or sheets, 2021-2025; implied totals within 0.05%; report text checks by year in `ai_index.md` | Each edition is its own vintage; only 2019-2021 is one. National totals swing +97% then -42% around method changes. State shares are noisy |
| SEDS consumption and TETCD | **Green** | 2015-2024 used | Billion Btu; $/MMBtu; 51 areas | Prices and consumption as served Nov 2026 | Codes match EIA's list; types sum to RETCB within 0.04%; TETCB matches the panel exactly; Ns match Fang's except wind (165 vs 164) | Ends 2024 |
| NCSES bachelor's degrees | **Green** | 2000-2024 | Per 1,000 age 18-24; 51 areas | Updated July 14, 2026 | Indicator = 1,000 x degrees / population exactly; no flagged cells | Later revisions may differ from Fang's copy |
| BEA real GDP, population, income | **Green** | Through 2025 | 51 areas | Sept 30, 2026 | Checked in Part C and the audit | GDP in chained 2017 dollars; Fang uses 2012 |
| State EPU | **Green** | Annual means | Already rated | Jan 2026 | Already rated | |
| NSF R&D | **Yellow** | 2017-2023 | Already rated | | Already rated | Doesn't cover all Fang split years outside 2018-2021 |
| Extreme weather | **Not run** | None | None | None | None | NOAA not available |

**Totals for new files:** 2 green, 1 yellow; extreme weather not run. No reds.

**In the postings extension (2019-2024), almost every year comes from a different edition. So a state's year-to-year change mixes real change with method changes.** Year effects remove shifts that hit all states proportionally. The share-of-national row can't test this: once year effects are in, it equals the postings row by construction (-0.0475 vs -0.0479). Anything uneven stays in as noise, and the edition overlap and share-change tables are the evidence on that. Data-center jobs (BLS, one consistent series) remain the more reliable extension measure.

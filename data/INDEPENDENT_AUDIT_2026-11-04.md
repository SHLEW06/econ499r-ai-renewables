# Independent data audit, 2026-11-04

**Result: every sampled value checked is correct, and no raw file changed. The issues are in decisions and documentation.** All 30 sampled cells match the raw files. The 25 cells with a same-measure published value also match the agency's number, apart from published rounding. Three cells could only be checked on a different capacity measure, and two real GDP cells could not be checked online.

The issues that matter most:
1. **Government jobs:** `DATA_VALIDATION.md` D23 says state-level government rows for NAICS 518210 don't exist. They do, in every year. Leaving them out is a defensible choice, but it was justified by a false statement, and it can move the AI measure by up to 0.36 per 1,000 jobs.
2. **Receipts:** `bea.md` and `eia_state.md` describe variables differently from the code. For example, `bea.md` defines `ln_ea` as an agricultural earnings share.
3. **`DATA_VALIDATION.md`:** besides D23, the claims in N05, N07, N06b, N08 and C.6 don't hold up as written (section 2.3).

This report changes nothing. Nothing was fixed, and nothing in `data/` or `results/` was edited other than adding this file.

## How independent this audit is
- **Not a fresh reviewer.** This audit ran in the same working session as the Phase 4d and 4e analysis, so I had already seen the project and its notes. I didn't build the panel. I rechecked claims against sources instead of relying on the notes, but someone new should treat this as a careful self-check, not outside review.
- **My own earlier changes.** Earlier in this session I moved three Georgia files into `data/raw/georgia/` and edited `data/receipts/georgia_psc.md` and `data/DATA_INDEX.md`, at the team's request. Those are disclosed in section 5.
- **Files named in the request that don't exist:**

| Named path | What I used instead |
|---|---|
| `data/codebook.csv` | The `Codebook` sheet of `outputs/ECON499R_Data_Workbook_2026-11-01.xlsx` |
| `data/receipts/README.md` | The ten individual receipts in `data/receipts/` |
| `code/python/clean/` | `econ499r_starter/scripts/build_panel.py`, the only panel build code |
| `admin/` (Methods Memo) | `notes/Methods_Memo_AI_Renewable_Energy_US_Test_Zhang_2026.pdf`, byte-identical to the copy in `econ499r_starter/reference/` |

The workbook's `Full Panel` sheet matches `data/out/state_panel_2015_2025.csv` on all 78 non-key columns (largest difference 4.8e-07).

## Result by variable

| Variable | Sampled cells | Against agency site | Against raw file | Code vs memo and codebook | Result |
|---|---|---|---|---|---|
| `renew_share` | 3 | 3 of 3 match | 3 of 3 | Match | **Pass** |
| `solar_share` | 2 | 2 of 2 match | 2 of 2 | Match | **Pass** |
| `wind_share` | 3 | 3 of 3 match | 3 of 3 | Match | **Pass** |
| `price_c_kwh` | 3 | 3 of 3, within published 2-decimal rounding | 3 of 3 | Match | **Pass** |
| `sales_mwh` | 3 | 3 of 3 exact | 3 of 3 | Match | **Pass** |
| `population` | 3 | 3 of 3 exact, on the newest Census series | 3 of 3 | Source differs from memo | **Issue (minor):** values correct; BEA is the source, not Census, and N07 is wrong |
| `gdp_real_musd2017` | 2 | Not checked online | 2 of 2 | Match (real is a documented choice) | **Pass on raw file only** |
| `dc_jobs` | 2 | 2 of 2 exact | 2 of 2 | Private only; memo doesn't say | **Issue:** values correct; D23 is false |
| `total_jobs` | 3 | 3 of 3 exact | 3 of 3 | Match | **Pass** |
| `tech5415_jobs` | 3 | 3 of 3 exact | 3 of 3 | Match | **Pass** |
| `new_renew_mw` | 3 | Different measure: net summer capacity matches the raw summer column in 3 of 3 | 3 of 3 (nameplate) | Follows memo p. 10 | **Issue (minor):** nameplate not confirmed online; blank-fuel rows; net change |

Variables outside the 30-cell sample got a code check only (no cell comparison):

| Variable | Code vs memo and codebook | Result |
|---|---|---|
| `ai_dc_per1000`, `ai_dc_per1000_lag1` | Formula matches; numerator is private only | **Issue:** inherits the `dc_jobs` issue |
| `tech_share` | Match | **Pass** |
| `hma` | Matches memo eq. 2. Range uses all 51 areas, but DC doesn't set either AI or tech minimum or maximum | **Pass** |
| `ln_ec`, `pop_growth`, `manuf_share`, `ln_gdp_pc` | Match | **Pass** |
| `ln_ee` | Real GDP is a documented choice; `eia_state.md` describes it backwards | **Pass on code; issue in receipt** |
| `fossil_to_renew`, `clean_share` | Adds Other Gases (documented). `clean_share` isn't in the memo (added variable) | **Pass, deviation documented** |
| `ln_ea`, `land_sqmi` | 2020 Gazetteer, not the memo's 2010 file; `bea.md` defines `ln_ea` wrongly | **Issue (minor)** |
| `energy_equity` | Match | **Pass** |
| `co2_per_mwh_t`, `seds_mmbtu_pc` | Match codebook; end in 2024 | **Pass** |
| `dc_wages_usd` | 0 for the four suppressed cells, not blank | **Issue (minor):** not used in any model |
| W matrices | Centroid and border sources differ from memo; rows rounded | **Issue (minor)** |

---

## 1. Thirty random cells (seed 2026)

**How the sample was drawn:** `numpy.random.default_rng(2026)`, before looking at any values. Each of the 11 variables got 2 cells, the other 8 cells were assigned at random, and state (51 including DC) and year (2015–2025) were then drawn at random. The sample happened to include no DC cells and no suppressed cells.

**How to read the table:**
- "Raw" is an independent read of the raw file that doesn't use `build_panel.py`.
- The share variables are computed from published generation by fuel, because EIA doesn't publish these shares directly.
- EIA API links need a free key added (`&api_key=YOUR_KEY`). I used EIA's public demo key, which hit its limit after 7 cells, so the other 11 EIA cells use EIA's State Electricity Profile tables, through 2024.

**Totals:** 25 checked online on the same measure, 3 online on a different measure, 2 not checked online. All 30 match the raw file.

| # | Variable | State | Year | Panel | Published | Difference | Raw | Check | URL |
|---|---|---|---|---|---|---|---|---|---|
| 1 | renew_share | FL | 2024 | 0.081887 | 0.081887 | -3.7e-10 | 0.081887 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=FL&facets[sectorid][]=99&start=2024&end=2024&length=100` |
| 2 | renew_share | NC | 2016 | 0.079527 | 0.079527 | -2.4e-09 | 0.079527 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=NC&facets[sectorid][]=99&start=2016&end=2016&length=100` |
| 3 | renew_share | IA | 2016 | 0.390507 | 0.390507 | -4.7e-09 | 0.390507 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=IA&facets[sectorid][]=99&start=2016&end=2016&length=100` |
| 4 | solar_share | WI | 2023 | 0.020423 | 0.020423 | -3.8e-09 | 0.020423 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=WI&facets[sectorid][]=99&start=2023&end=2023&length=100` |
| 5 | solar_share | VA | 2018 | 0.007990 | 0.007990 | -8.4e-13 | 0.007990 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=VA&facets[sectorid][]=99&start=2018&end=2018&length=100` |
| 6 | wind_share | NY | 2021 | 0.033312 | 0.033312 | 8.0e-12 | 0.033312 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=NY&facets[sectorid][]=99&start=2021&end=2021&length=100` |
| 7 | wind_share | PA | 2016 | 0.016165 | 0.016165 | -2.7e-11 | 0.016165 | online | `https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=generation&facets[location][]=PA&facets[sectorid][]=99&start=2016&end=2016&length=100` |
| 8 | wind_share | MT | 2022 | 0.148470 | 0.148470 | 0 | 0.148470 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20MT.xlsx` |
| 9 | price_c_kwh | TN | 2022 | 10.8942 | 10.8900 | -0.0042 | 10.8942 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20TN.xlsx` |
| 10 | price_c_kwh | MI | 2020 | 12.2114 | 12.2100 | -0.0014 | 12.2114 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20MI.xlsx` |
| 11 | price_c_kwh | KY | 2016 | 8.4176 | 8.4200 | +0.0024 | 8.4176 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20KY.xlsx` |
| 12 | retail sales MWh | IN | 2016 | 103,704,821 | 103,704,821 | 0 | 103,704,821 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20IN.xlsx` |
| 13 | retail sales MWh | HI | 2024 | 8,952,134 | 8,952,134 | 0 | 8,952,134 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20HI.xlsx` |
| 14 | retail sales MWh | MT | 2016 | 14,100,601 | 14,100,601 | 0 | 14,100,601 | online | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20MT.xlsx` |
| 15 | population | MA | 2017 | 6,959,114 | 6,959,114 | 0 | 6,959,114 | online | `https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/intercensal/state/asrh/sc-est2020int-alldata6.csv` |
| 16 | population | NC | 2024 | 11,052,061 | 11,052,061 | 0 | 11,052,061 | online | `https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/totals/NST-EST2025-ALLDATA.csv` |
| 17 | population | AL | 2020 | 5,032,962 | 5,032,962 | 0 | 5,032,962 | online | `https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/totals/NST-EST2025-ALLDATA.csv` |
| 18 | real GDP ($M 2017) | MI | 2025 | 575,397.4 | n/a | n/a | 575,397.4 | not checked online | raw file: `data/raw/bea/sagdp/SAGDP9__ALL_AREAS_1997_2025.csv` |
| 19 | real GDP ($M 2017) | LA | 2016 | 235,554.2 | n/a | n/a | 235,554.2 | not checked online | raw file: `data/raw/bea/sagdp/SAGDP9__ALL_AREAS_1997_2025.csv` |
| 20 | dc_jobs | FL | 2020 | 20,336 | 20,336 | 0 | 20,336 | online | `https://data.bls.gov/cew/data/api/2020/a/industry/518210.csv` |
| 21 | dc_jobs | NJ | 2018 | 10,064 | 10,064 | 0 | 10,064 | online | `https://data.bls.gov/cew/data/api/2018/a/industry/518210.csv` |
| 22 | total_jobs | MI | 2022 | 4,300,943 | 4,300,943 | 0 | 4,300,943 | online | `https://data.bls.gov/cew/data/api/2022/a/industry/10.csv` |
| 23 | total_jobs | IA | 2025 | 1,558,465 | 1,558,465 | 0 | 1,558,465 | online | `https://data.bls.gov/cew/data/api/2025/a/industry/10.csv` |
| 24 | total_jobs | GA | 2025 | 4,890,150 | 4,890,150 | 0 | 4,890,150 | online | `https://data.bls.gov/cew/data/api/2025/a/industry/10.csv` |
| 25 | tech_jobs (`tech5415_jobs`) | UT | 2025 | 34,750 | 34,750 | 0 | 34,750 | online | `https://data.bls.gov/cew/data/api/2025/a/industry/5415.csv` |
| 26 | tech_jobs (`tech5415_jobs`) | SC | 2020 | 18,399 | 18,399 | 0 | 18,399 | online | `https://data.bls.gov/cew/data/api/2020/a/industry/5415.csv` |
| 27 | tech_jobs (`tech5415_jobs`) | NJ | 2017 | 70,022 | 70,022 | 0 | 70,022 | online | `https://data.bls.gov/cew/data/api/2017/a/industry/5415.csv` |
| 28 | new_renew_mw | KY | 2020 | 3.0 | -12.1 | -15.1 | 3.0 | online, different measure | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20KY.xlsx` |
| 29 | new_renew_mw | WV | 2023 | 0.0 | 0.0 | 0 | 0.0 | online, different measure | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20WV.xlsx` |
| 30 | new_renew_mw | NV | 2021 | 657.5 | 635.5 | -22.0 | 657.5 | online, different measure | `https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20NV.xlsx` |

**Notes on the differences:**
- **Shares:** differences are at most 4.7e-09, from the API's precision.
- **Prices:** EIA publishes 2 decimals, and the differences are at most 0.0042 cents.
- **Population:** two of the three cells differed from the first Census file I tried, and all three match exactly on the newest series:

| Cell | Older Census series | Difference from panel | Series that matches the panel |
|---|---|---|---|
| MA 2017 | Vintage 2020: 6,863,560 | −95,554 (−1.4%) | 2010–2020 intercensal |
| NC 2024 | Vintage 2024: 11,046,024 | −6,037 | Vintage 2025 |
| AL 2020 | Vintage 2024: 5,033,094 | +132 | Vintage 2025 |

- **`new_renew_mw`:** the panel uses nameplate capacity, but the state lookups I could use publish net summer capacity. EIA's net summer figures (−12.1, 0, 635.5 MW) match the raw summer column exactly, so the raw file is confirmed, but the nameplate panel values were matched only to the raw file. KY 2020 also shows the measure can change the sign: +3.0 nameplate vs −12.1 net summer.
- **Real GDP:** BEA's API needs a key, its GDP page doesn't show state levels, and I didn't try its interactive tables, which need a browser. I checked these two cells against the raw file only. That file's footer reads "Last updated: September 30, 2026," and its size matches the file currently on BEA's site (section 5).

---

## 2. Code vs memo and codebook

The code reviewed is `build_panel.py`. Line numbers refer to that file.

### 2.1 Code vs memo or codebook

| Variable | Memo or codebook says | Code does | Effect | Status |
|---|---|---|---|---|
| `dc_jobs`, AI measure | Memo p. 4: employment in NAICS 518210. No ownership stated. Codebook: private | Private rows only (line 104); denominator is all ownership (line 106) | See below. Up to 0.36 per 1,000 jobs | Matches codebook; memo silent; **D23 is false** |
| `dc_wages_usd` | Workbook README: suppressed 518210 cells "are blank, not zero" | Wages stay 0 for AK, ND, SD, WY in 2025 (line 112; only jobs are blanked, line 117) | Unused in models, but a trap if someone uses it | **Mismatch** |
| `population`, `pop_growth` | Memo pp. 9, 11: Census county data for 2020–2025 and BEA through 2024; "population growth (Census)" | BEA SAINC1 line 2 for all years (lines 137–143) | None on values: all 3 cells match Census | **Mismatch with memo**; codebook agrees with code |
| `land_sqmi`, `ln_ea` | Memo p. 11: Census 2010 state area (Georgia 57,513 sq mi) | Sum of 2020 county land areas (Georgia 57,716.962) | +0.35% for Georgia; constant over time, so absorbed by state FE | **Mismatch with memo**; codebook agrees with code |
| W matrices | Memo p. 11: Census TIGER state boundary file | Land-weighted county points from the 2020 Gazetteer; 2023 county adjacency (lines 146–151, 196–202) | Not measured | **Mismatch with memo**; receipt agrees with code |
| W inverse distance | Row-standardized | Rounded to 6 decimals after standardizing (line 195). Row sums run 0.999995 to 1.000004, and 44 of 50 aren't exactly 1 | Small, but SDPDm silently ignored `demn=TRUE` on this W until 4d's rerun normalized it exactly | **Minor** |
| `new_renew_mw` | Memo p. 3: new capacity "added." Memo p. 10: "the change from the year before" | Year-on-year change in nameplate (line 59), so 42 of 561 cells are negative | Net of retirements, not gross additions | Follows p. 10; memo is inconsistent; EIA State Profile Table 4B has gross additions and retirements |
| `new_renew_mw` | All renewable capacity counted | `existcapacity_annual.xlsx` has blank fuel on NE 2017 (190.8 MW) and NM 2017 (7.2 MW). These count in `cap_total_mw` but no fuel column | If renewable, `new_renew_mw` is off by that amount in 2017 and 2018. The fuel can't be determined from this file | **Source-file quirk; undocumented** |
| `fossil_to_renew` | Memo p. 3: coal, gas, oil | Adds Other Gases (line 37) | 0.34% of fossil per D24 | Documented deviation |
| `ln_ee` | Memo p. 3: "State GDP in $" | Real chained-2017 GDP (line 158) | Correlation with nominal version 0.976 per D22 (not recomputed) | Documented choice |
| Real GDP for 2025 | Memo p. 10: quarterly series, so 2025 is four quarters | Annual SAGDP9 (line 136) | None expected | Minor; annual table exists |

**Government jobs in NAICS 518210.** Government-owned rows (`own_code` 1, 2, 3) exist at state level in all 12 raw files:
- **Scale:** 112 state-years over 2014–2025 have government jobs above zero, totaling 2,836 to 4,050 jobs a year.
- **Largest:** PA, about 1,200 jobs (11–13% on top of its private count in 2015–2020); NM, up to 49% of its private count in 2014.
- **Effect on AI:** adding them would raise `ai_dc_per1000` by up to 0.356 (MN 2017), with a median of 0.10 where they exist. The within-state SD quoted in `CLAUDE.md` is 0.57.
- **Timing:** rows with government jobs rise from 5 in 2021 to 17 in 2022 and 20 by 2025. I didn't determine why; the 2022 NAICS change is one possibility to check.

Private-only is defensible, but the reason given in D23 is wrong, so the team should make this choice with these numbers in view.

### 2.2 Receipts vs code
These are documentation errors. The panel doesn't use what the receipts describe.

| Receipt | Says | Actually |
|---|---|---|
| `bea.md` | `ln_ea = log(earnings_ag_musd / total_earnings_musd)`, from SAINC5 lines 10 and 70 | `ln_ea` is log nonfarm GDP per square mile (lines 164–165). SAINC5 isn't used |
| `bea.md` | Deflator applied; `(D)` rows dropped | Neither is in the code |
| `bea.md` | `SAGDP.zip` ~120 MB, `SAINC.zip` ~80 MB | 10.4 MB and 17.6 MB |
| `eia_state.md` | `ln_ee` is log electricity intensity, sales divided by GDP | It's GDP per MWh, the inverse (lines 158–159) |
| `eia_state.md` | Outputs `ln_co2`; columns `renew_gen_mwh`, `fossil_gen_mwh`; planned-capacity variable; lookup dictionary in `build_panel.py` | None exist |
| `eia_state.md` | Fossil = coal, gas, petroleum; all sales data 1990–2025 | Fossil includes Other Gases; `HS861_2010-.xlsx` starts in 2010 |
| `census.md` | Adjacency link `.../reference/county_adjacency.txt` | That's a 2015 file of 726,724 bytes. The raw file (1,116,106 bytes) matches `.../county_adjacency/county_adjacency2023.txt` |
| `DATA_INDEX.md` | Centroids are population-weighted | They're land-weighted (lines 150–151). `census.md` already notes this |
| `ferc_pudl.md` | File names such as `out_ferc1__yearly_income_statements.parquet` | The actual names differ (`..._sched114.parquet`) |
| `bls_qcew.md` | Code verifies 51 rows per file | The code has no such check; own-code 5 files have 53 state-level rows (the filter drops PR and VI) |

### 2.3 `DATA_VALIDATION.md` claims that don't hold up

| Item | Claim | What I found |
|---|---|---|
| D23 | "Government 518210 rows do not appear at state level in any year" | False (section 2.1) |
| N05 | The 0.613% gap between states and the U.S. "reflects U.S. territories" | BEA's SAGDP2 footnote says the gap "reflects overseas activity" by the military and federal civilian staff. The check still passes |
| N07 | BEA population is "identical to the Census state population estimates by construction... No comparison gap possible" | It differs from older Census vintages by up to 95,554. It matched the newest series in all 3 cells, but the claim needs that qualifier |
| N06b | "No systematic error is possible" for 2015 prices | An overclaim, and no earlier-year comparison was made. This audit's 2016, 2020 and 2022 price cells do match |
| N08 | Matching total generation "confirms" Georgia's `renew_share` | Totals alone can't confirm a share. Sampled shares for other states do match |
| C.6 | EIA 2025 generation, capacity and sales are "preliminary" | EIA's page says "Final annual data for 2025," and the generation sheet is named `Net_Generation_1990-2025 Final` |
| C.6 | BEA: "June 2026 comprehensive revision" | File footers read "Last updated: September 30, 2026" |
| C.6 | SEDS is a "Monthly Energy Review supplement"; "PUDL 2025 release" | SEDS is its own product, released June 26, 2026. PUDL's current release is v2026.10.0 |
| QCEW status | C.6 says no preliminary years for 2025 | Not confirmed either way: BLS's download page lists 2025 with no status label. The 2025 cells matched BLS today |

---

## 3. Full-panel rebuild comparison (C.1b)

**As reported in `DATA_VALIDATION.md`:** 43,758 cells compared (78 non-key columns × 561 rows), with **zero differences**.

**As rechecked today:** I reran `build_panel.py data/raw <scratch>` rather than relying on that note, because C.1b's output went to `/tmp` and no log was kept.

| Measure | Result |
|---|---|
| Cells compared | 43,758 |
| Value differences | 0 (largest absolute difference 0.0, with no tolerance) |
| Missing-value pattern differences | 0 (216 cells are blank in both) |
| `state_panel_2015_2025.csv` | Byte-identical |
| `W_inverse_distance_rowstd.csv`, `W_distance_miles.csv`, `W_border_binary.csv`, `state_centroids_land.csv` | Byte-identical |

The 216 blanks are the expected gaps: 51 each for CO2 (2 columns) and SEDS (2 columns), and 4 each for `dc_jobs`, `ai_dc_per1000` and `hma`.

---

## 4. Sources: primary or secondary, and citations

Citations are in MLA, the format the memo uses, with an access date of Nov. 1, 2026, the download date in the receipts. Dates I confirmed today are from the agency's page or the file itself.

| Source | Used for | Type | Citation |
|---|---|---|---|
| EIA generation | `gen_*`, shares, `fossil_to_renew` | Primary | U.S. Energy Information Administration. "Net Generation by State by Type of Producer by Energy Source (EIA-906, EIA-920, and EIA-923), 1990–2025." *Historical State Data*, released Sept. 2026, www.eia.gov/electricity/data/state/. Accessed 1 Nov. 2026. |
| EIA capacity | `cap_*`, `new_renew_mw` | Primary | U.S. Energy Information Administration. "Existing Nameplate and Net Summer Capacity by Energy Source, Producer Type and State (EIA-860), 1990–2025." *Historical State Data*, released 10 Sept. 2026, www.eia.gov/electricity/data/state/. Accessed 1 Nov. 2026. |
| EIA retail sales | `sales_*`, `price_c_kwh` | Primary | U.S. Energy Information Administration. "Annual Sales to Ultimate Customers (EIA-861), 2010–2025." *Historical State Data*, released 7 Oct. 2026, www.eia.gov/electricity/data/state/. Accessed 1 Nov. 2026. |
| EIA emissions | `co2_*` | Primary (EIA estimates) | U.S. Energy Information Administration. "Estimated Emissions by State (EIA-767, EIA-906, EIA-920, and EIA-923), 1990–2024." *Historical State Data*, final 2024 data released 12 Nov. 2025, www.eia.gov/electricity/data/state/. Accessed 1 Nov. 2026. |
| EIA SEDS | `seds_*` | Primary | U.S. Energy Information Administration. *State Energy Data System (SEDS): 1960–2024 (Complete)*. Released 26 June 2026, www.eia.gov/state/seds/seds-data-complete.php. Accessed 1 Nov. 2026. |
| EIA Forms 860, 860M, 861, 923 | Not in the panel | Primary | U.S. Energy Information Administration. *Form EIA-860, Form EIA-861, and Form EIA-923 Data Files, 2025*, and *Form EIA-860M, September 2026*. www.eia.gov/electricity/data/. Accessed 1 Nov. 2026. |
| BLS QCEW | `dc_jobs`, `tech5415_jobs`, `total_jobs` | Primary | U.S. Bureau of Labor Statistics. *Quarterly Census of Employment and Wages, Annual Averages, 2014–2025* (NAICS 518210, 5415, and all industries). www.bls.gov/cew/. Accessed 1 Nov. 2026. |
| BEA GDP | `gdp_*`, `manuf_share`, `ln_ee` | Primary | U.S. Bureau of Economic Analysis. "SAGDP2: Gross Domestic Product (GDP) by State" and "SAGDP9: Real GDP by State." *Regional Data*, last updated 30 Sept. 2026, apps.bea.gov/regional/downloadzip.htm. Accessed 1 Nov. 2026. |
| BEA population | `population` | **Secondary** for population: BEA's footnote gives "U.S. Census Bureau midyear population estimates" | U.S. Bureau of Economic Analysis. "SAINC1: State Annual Personal Income Summary." *Regional Data*, last updated 30 Sept. 2026, apps.bea.gov/regional/downloadzip.htm. Accessed 1 Nov. 2026. Cite the two Census entries below beside it. |
| Census population | Primary source behind `population`; used here to check it | Primary | U.S. Census Bureau. *State Population Totals: Vintage 2025* (NST-EST2025-ALLDATA) and *State Intercensal Population Estimates, 2010–2020* (SC-EST2020INT-ALLDATA6). www2.census.gov/programs-surveys/popest/datasets/. Accessed 4 Nov. 2026. |
| Census Gazetteer | `land_sqmi`, centroids | Primary | U.S. Census Bureau. *2020 Gazetteer Files: Counties*. www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/. Accessed 1 Nov. 2026. |
| Census adjacency | Border W | Primary | U.S. Census Bureau. *County Adjacency File, 2023*. www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2023.txt. Accessed 1 Nov. 2026. |
| PUDL (FERC Form 1) | `ferc1_*` outputs; not in the panel | **Secondary:** Catalyst Cooperative's processed version of FERC Form 1 and EIA data | Selvans, Zane, et al. *Public Utility Data Liberation Project (PUDL) Data Release*. Version v2026.10.0, Catalyst Cooperative, 2026, Zenodo, doi.org/10.5281/zenodo.23375698. Accessed 1 Nov. 2026. Confirm the version in the raw files before citing; the workbook says "stable release, Oct 14, 2026," which matches this release's notes date. |
| RMI Utility Transition Hub | Not in the panel | **Secondary:** compiled utility data | RMI. *Utility Transition Hub*. utilitytransitionhub.rmi.org/data-download/. Download date unknown; the receipt says only "prior to 2026-11-01." Find the date before citing. |
| Lazard | Reference for the Georgia module | Primary for Lazard's own estimates; private firm, not government | Lazard. *Levelized Cost of Energy+*. July 2026, www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf. Accessed 1 Nov. 2026. |
| Georgia Power IRPs | Georgia case box | Primary filings. The 2025 main document and table of contents are copies hosted by SELC, per `data/data_links.md`; cite the docket | Georgia Power Company. *2025 Integrated Resource Plan*. Docket No. 56002, Georgia Public Service Commission. Also *2023 Integrated Resource Plan Update*. Docket No. 55378. Add the filing dates, which I didn't confirm. |
| Georgia large-load reports | Georgia case box | Primary filings | Georgia Power Company. "Quarterly Large Load Economic Development Report." Docket No. 55378, Georgia Public Service Commission, 15 May 2026 (Q1) and 17 Aug. 2026 (Q2). |
| SEC company facts | `sec_company_financials.csv`; not in the panel | Primary filings data | U.S. Securities and Exchange Commission. *XBRL Company Facts API*. data.sec.gov/api/xbrl/companyfacts/. Access date not recorded. There's no raw copy in `data/raw/`, so this source couldn't be hashed. |

---

## 5. SHA-256 of `data/raw/`

**No raw file with a baseline changed.** I recomputed all 1,664 files (868.9 MB). The per-file list is in `logs/2026-11-04/raw_sha256_manifest.csv`, added by this audit. Its digest is `8e7cfbe1e1b4a7890885e7638c84aab5456bd4d2b53d37c0d8db1c61133bb087`.

**The receipts contain no hashes.** Only the move logs do, so the receipts couldn't be compared. Baselines came from these sources:

| Baseline | Files | Match | Changed | Strength |
|---|---|---|---|---|
| Direct: `phase2_moves.csv` (61) and `phase4_moves.csv` (3) | 64 | 64 | 0 | Strong: logged hash |
| Chain: extracted file matches its member in a logged zip (`SAGDP.zip`, `SAINC.zip`, `gaz_counties.zip`) | 1,588 | 1,588 | 0 | Strong: all three zips match the log |
| Copy only: RMI files match `data/data_download_all_pt1.zip`, whose own hash isn't logged | 12 | 12 | 0 | **Weak:** two copies agree, but no logged hash |
| **Total** | **1,664** | **1,664** | **0** | |

**Other points:**
- **Added since Phase 2:** three files in `data/raw/georgia/`, moved from `data/georgia_psc/` on 2026-11-03 at the team's request. Their hashes match `logs/2026-11-03/phase4_moves.csv`. The move edited raw folder contents, despite the read-only rule, but no existing file changed:
  - `dkt55378_large_load_report_q1_2026_attachment.xlsx`
  - `dkt55378_large_load_report_q2_2026.zip`
  - `irp_2025_public_disclosure.zip`
- **Limit of these baselines:** the logs date from Nov. 1, so they can't detect anything changed before then. As a separate check, the sizes of nine downloaded source files match what the agencies' sites serve today:

| Source file | Live `Last-Modified` |
|---|---|
| `annual_generation_state.xlsx` | Sept. 11, 2026 |
| `existcapacity_annual.xlsx` | Sept. 10, 2026 |
| `HS861_2010-.xlsx` | Oct. 7, 2026 |
| `emission_annual.xlsx` | Sept. 30, 2025 |
| `use_all_btu.csv` | May 26, 2026 |
| `SAGDP.zip`, `SAINC.zip` | Sept. 30, 2026 |
| `gaz_counties.zip` | Jan. 22, 2021 |
| `county_adj.txt` | Sept. 18, 2023 |

- **Stray files:** `data/raw/rmi/` has two macOS metadata files (`._operations_emissions.csv`, `._operations_emissions_by_tech.csv`) that came with the zip. They're harmless.

---

## How the online checks were done
All lookups were read-only. BLS, Census and EIA tables were read into memory, with no agency file saved to the project. EIA's state tables were held briefly in my session's temporary folder during the lookup and then deleted. The only files this audit added are this report and the hash manifest in `logs/2026-11-04/`.

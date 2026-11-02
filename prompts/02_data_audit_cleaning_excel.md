# Phase 2: look at all the data, clean it, prove it's right, then stop before methods

This prompt replaces prompts/02_data_catalog.md and prompts/03_data_cleaning.md. Everything you need is in this file; the old prompts are in prompts/_retired/ for history only.

ECON 499R project (Shunji Lewandowski and Alexander Hendricks, Prof. Fohlin). The project root is the "AI impact on Renewables" folder, already organized in Phase 1.

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (including the divergence register), the newest file in docs/, docs/2026-11-01/context-handoff-from-chat.md, docs/2026-11-01/methods-review.md, data/data_links.md, and the Methods Memo in admin/ (Section 2 outcomes, Section 3 AI measure, the variable table).
- **If any part of this phase already ran:** read its outputs and handoff, tell me what's done, and continue from the first unfinished part. Part C always runs in full.

This phase has three parts and two stops:
- **Part A:** look at every file. Then STOP.
- **Part B:** clean.
- **Part C:** prove the data is right. Then STOP.

Designing the methods starts after this, in prompts/04a_methods_spec.md.

## Hard limits for this phase
- No models, estimation, regressions, winsorizing or "testing" of hypotheses. That is Phase 4.
- Don't download anything without my approval of the specific list.
- Read-only web lookups to check published numbers are fine (Part C).
- Never edit raw files. Never invent, impute or fill data.
- Never delete anything. Unreadable or unneeded files go to data/_to_delete/ with a reason.

---

## PART A: Look at every file. Then STOP and wait for me.

1. **Inventory the whole folder, not just data/.**
   - Walk every subfolder of the project root (notes, notebooks, sources, literature, admin, interviews, decks, data, `_to_delete/`).
   - **Inventory file:** data/FILE_INVENTORY.csv, one row per file that holds data or could. That means csv, xlsx, xls, zip, parquet, json, txt/tsv tables, and PDFs with tables (IRP, large-load reports, dockets). Columns: path, size, sha256, type, what it is, and disposition.
   - **Dispositions:**
     - USED: which variable and which method step
     - REFERENCE: a document we cite, not parsed
     - DUPLICATE: of which file, same sha256
     - OTHER VINTAGE: same dataset, different release; say which is newer
     - NOT NEEDED: why
     - UNREADABLE: why
     - UNKNOWN: ask me
   - **Coverage check:** print the count from `find` and the count of inventory rows, and explain any difference. No file may be left unclassified.
2. **Match files to targets.**
   - Run `python code/python/download_all.py --raw-dir data/raw --list` to get the exact target path each script expects.
   - Match every USED file to its target. Browser downloads often have different names; e.g. "HS861 2010-.xlsx" becomes data/raw/eia/HS861_2010-.xlsx.
   - Show me a table with: current file, matched dataset, target path, and match confidence.
3. **Check readability and the "right product."**
   - Unzip every .zip into a same-name folder beside it, keeping the zip.
   - Open each file. Flag files that are empty, partial downloads, HTML or "Request Rejected" pages, or that won't parse.
   - Check the contents, not the file name, against the product in data_links.md:
     - **QCEW:** must be the annual-averages "by industry" CSV. Check the year and industry_code columns inside the file match the name, and that the file has state rows (area_fips ending in 000), not just counties. Flag quarterly files.
     - **EIA:** must be the state-level historical files with the expected header row and sheet names. Note the latest year in each and whether it's marked preliminary.
     - **BEA:** check the table ID (SAGDP2, SAGDP9, SAINC1) and the units line; SAGDP9 must say chained dollars. Note the release date in the file.
     - **Census:** the 2020 Gazetteer counties file and county_adjacency2023.txt.
     - **Everything else:** rows and columns about what data_links.md implies. Flag anything far smaller, since it may be a partial download.
4. **Check completeness against the methods.**
   - Build a requirements matrix with one row per needed input and these columns: method step, variable(s), source and file, years needed, years we have, status, gap.
   - **Step 1 outcomes and controls:** the EIA state files (generation, capacity, HS861 sales, emissions) through 2025 (emissions end in 2024), plus BEA SAGDP2 (lines 1, 4, 12), SAGDP9 line 1, and SAINC1 line 2 through 2025.
   - **AI measure:** QCEW 518210 and industry 10 for every year 2014-2025, which is 24 files. 2014 is needed for the 2015 lag. Note BLS suppression: AK, ND, SD and WY in 2025.
   - **Step 2:** QCEW 5415 for 2014-2025 (12 files), plus the Census Gazetteer (land area).
   - **Step 3:** the Census Gazetteer (centroids) and county adjacency (border matrix).
   - **Robustness:** EIA SEDS (through 2024), the LBNL RPS/CES targets, and data-center MW (Epoch / Cleanview).
   - **Stretch:**
     - NOAA HDD/CDD (48 states)
     - NSF Table 10 for 2017-2023
     - Census ACS S2801: needs a key; no 2020 1-year release
     - state EPU, monthly: https://policyuncertainty.com/state_epu.html
   - **Georgia:**
     - the 2025 IRP main document
     - the large-load reports from Q1 2024 to the latest quarter
     - the docket documents we cite
     - global cumulative solar PV capacity: https://ourworldindata.org/grapher/solar-pv-cumulative-capacity.csv?v=1&csvType=full&useColumnShortNames=false
     - LBNL Utility-Scale Solar (browser): https://emp.lbl.gov/utility-scale-solar
   - **Dynamics:** QCEW 2012-2013 for 518210 and industry 10, only if we run t-3 lags.
   - **Lookups:** a Census region lookup (state to Northeast/Midwest/South/West).
   - **Finance side:**
     - the PUDL FERC1 tables
     - SEC company facts (script, needs SEC_USER_AGENT; ask me first)
     - Lazard 2026
     - Bloomberg (by hand; licensed, keep out of git)
5. **Answer: do we need more data?** Give two lists, each ordered most important first, then easiest first:
   - **(a) Required but missing, broken or the wrong product:** what it is, which step it blocks, and its link from data_links.md.
   - **(b) Optional additions:** what each one adds, effort, and link. Examples: AI patents (USPTO plus PatentsView) as a second AI measure; EIA-860 battery storage; NSF editions for 2015-2016.

   For each item, say whether download_all.py can fetch it or it needs a browser.
6. **Write the audit and stop.**
   - Write data/DATA_AUDIT.md (the inventory summary, the matrix and both lists) and docs/<date>/phase-2a-data-audit.md (five sections plus "How to resume").
   - Then STOP. I'll approve file moves, tell you which gaps to fill, and add any files I download by hand.

---

## PART B: After my OK. Place, catalog and clean the data. Still no models.

1. **Place the files.**
   - Move and rename the data into data/raw/<source>/ as approved. Log every move in logs/<date>/phase2_moves.csv (old_path, new_path, sha256).
   - Name files that download_all.py doesn't cover `SOURCE_description_years.ext`.
2. **Catalog.**
   - **data/DATA_CATALOG.xlsx, Index sheet,** one row per dataset: plain-English label, path, source and link, what's inside, years, geography, units, size and rows x columns, method step it feeds, status, and quirks (header rows, footnotes, suppressed cells, unit changes, vintage).
   - **One preview tab per tabular dataset** with the first 100 rows, untouched. For very large files, list the sheets and columns only.
   - **data/previews/<label>.md:** the summary plus the full column list.
   - **data/DATA_INDEX.md:** a one-page guide grouped by method step, with a "Missing" section that gives a link for each item.
3. **Clean.**
   - Use a package in code/python/clean/ with one module per source (eia.py, qcew.py, bea.py, census.py, seds.py, pudl.py, sec.py, plus stretch sources). code/python/build_panel.py already works: reuse its logic, split it into these modules, and document each step.
   - The driver is code/python/build_master_panel.py with a required `--date YYYY-MM-DD`. It checks every input before doing any work. Its log goes to logs/<date>/build/.
   - Leave missing values as NA with a reason. Never impute. Don't winsorize or lag here.

   Cleaning rules. These match the working build; log any deviation.

   **EIA**
   - **Net generation (annual_generation_state.xlsx):**
     - The header is on row 2. Keep TYPE OF PRODUCER = "Total Electric Power Industry". Pivot ENERGY SOURCE to columns.
     - Renewable = Hydroelectric Conventional + Wind + Solar Thermal and Photovoltaic + Geothermal + Wood and Wood Derived Fuels + Other Biomass.
     - Fossil = Coal + Natural Gas + Petroleum + Other Gases.
     - renew_share = renewable / Total. Total includes negative pumped storage.
     - Also compute solar_share, wind_share, coal_share, clean_share (renewable plus nuclear) and fossil_to_renew.
     - This is utility-scale generation only.
   - **Capacity (existcapacity_annual.xlsx):** keep "Total Electric Power Industry", nameplate MW. The source is labeled "Hydroelectric" here. new_*_mw is the change from the prior year; keep negative values.
   - **Retail sales (HS861):** three header rows. Use the TOTAL sector block: revenue (thousand $), sales (MWh), customers. price_c_kwh = 100 x revenue / sales. Also keep the commercial block.
   - **Emissions:** keep "Total Electric Power Industry" and "All Sources". It ends in 2024. co2_per_mwh = CO2 / total generation.
   - **SEDS (use_all_btu.csv):** MSN = TETCB, in billion Btu; ends in 2024. Make seds_mmbtu_pc.
   - **net_exporter_2015:** 1 if 2015 in-state generation > 2015 retail sales. It is fixed per state.

   **BLS QCEW (2014-2025)**
   - State rows have area_fips ending in "000". The value column is annual_avg_emplvl.
   - 518210: own_code 5, agglvl 58. 5415: own_code 5, agglvl 56. Industry 10: own_code 0, agglvl 50.
   - disclosure_code "N" means suppressed: leave it blank and add a flag.
   - ai_dc_per1000 = 1000 x dc_jobs / total_jobs. Keep 2014 for the lag.

   **BEA and Census**
   - **BEA:** strip quotes and spaces from GeoFIPS.
     - SAGDP2 line 1 is all-industry GDP, current $M; line 4 is farms; line 12 is manufacturing.
     - SAGDP9 line 1 is real GDP, chained $M.
     - SAINC1 line 2 is population.
   - **Census:**
     - Land area is the sum of the counties' ALAND_SQMI in the 2020 Gazetteer.
     - The centroid is the land-weighted mean of county internal points.
     - Border W comes from county_adjacency2023.txt. Distance W is haversine distance between centroids, then row-standardized inverse distance.
     - Both cover the 50 states, no DC.
   - **Census region:** a lookup for all 51.

   **Derived variables (memo definitions)**
   - ln_ec = ln(sales MWh / population)
   - ln_ee = ln(real GDP $ / sales MWh)
   - ln_gdp_pc
   - manuf_share
   - pop_growth
   - ea_nonfarm_gdp_per_sqmi and ln_ea
   - tech_share
   - hma, from the paper's equation 2 with range-standardized AI and tech_share over 2015-2025
   - energy_equity, the state's share of U.S. GDP / its share of U.S. sales

   **Finance and stretch sources** (only for files that exist)
   - **PUDL FERC1:** prefer reported_value rows, then calculated_value; drop correction rows. Split steam plants into coal or gas by primary_fuel_by_mmbtu.
   - **Stretch tables:** NOAA, NSF, LBNL RPS, ACS, EPU (monthly to annual mean), and OWID solar.
   - **Epoch / Cleanview:** state-year data-center MW only if the source supports it; otherwise a site-level table.
   - **Georgia large-load reports:** a quarterly table with page citations.
4. **Outputs.**
   - **The master file:** data/state_panel_2015_2025.csv, one row per state-year, 51 incl. DC, 2015-2025.
   - **Tables:** data/codebook.csv; the W matrices and centroids; the finance tables; one file per stretch source.
5. **The easy-access Excel workbook:** data/ECON499R_Data_Workbook_<date>.xlsx. Use Arial, frozen header rows, filters on every table, units in headers, and no formula errors (recalculate and check). Tabs:
   - **README:** what the workbook is, the as-of date, how to use each tab, the sources, and what's still missing.
   - **Master Panel:** one row per state-year. Memo variables first, then the rest. Make the core derived columns live formulas from the raw columns beside them, so Alexander can audit each definition.
   - **Georgia:** Georgia's rows next to the U.S. median for the key variables.
   - **Codebook:** variable, definition, unit, source, link, years, non-missing count, and vintage. Mark preliminary values.
   - **Missing Data:** variable x year, with the reason for each gap.
   - **Sources & Receipts:** source, link, raw file(s), vintage, and receipt file.
   - **Validation:** the Part C verdict table.
   - **Financials,** **W Distance,** **W Border,** and one tab per stretch table that exists.
6. **.md receipts, written so they can go on GitHub as-is.** Use relative paths only. No personal emails or local absolute paths, and no licensed data contents.
   - **data/receipts/<source>.md, one per source:**
     - source and link
     - raw file(s), size, sha256, and vintage
     - what we kept and every transformation, in order
     - rows in and out
     - checks and results
     - quirks
     - output file and columns
     - the script and function
   - **data/receipts/README.md:** an index of all receipts plus how to rebuild everything (download_all.py, then build_master_panel.py --date ...), noting which files need a browser.

---

## PART C: Prove the data is right. Then STOP.
Write data/DATA_VALIDATION.md, with detail in logs/<date>/build/validation/. Every check gets PASS, FAIL or NOTE, plus the evidence.

1. **Right definition.** For every memo variable, give one row:
   - the memo's definition, quoted with its page
   - our formula
   - the exact raw series, filter and units
   - whether it matches

   Decide or flag these explicitly:
   - **GDP in ln_ee:** the memo says "State GDP in $" and doesn't say real or nominal. We use real (chained). Say so. Under year FE the choice should matter little; show the correlation of the two versions.
   - **The AI numerator and denominator:** 518210 is private-only (own_code 5); the denominator is all covered jobs (own_code 0), as the memo's "industry code 10" says. Check whether 518210 government rows exist at all. Show the correlation with a private-only denominator.
   - **Fossil:** the memo says "coal, gas, and oil." We add EIA's "Other Gases." Show how much it changes fossil_to_renew.
   - **Renewable:** it excludes nuclear and pumped storage and counts only utility-scale generation; rooftop solar is not in EIA's state generation file. This is a known limitation; note it.
   - **Consumption:** ln_ec uses retail sales (where power is used), not generation (where it's made).
2. **Right numbers.** Cross-check against figures not used in the build.
   - **EIA generation:** for every year, the fuel columns sum to the Total row, and the 50 states + DC sum to the US-Total row.
   - **QCEW:** the state sum of 518210 vs the national (US000) row for each year. Explain the gap: suppressed states. Do the same for industry 10.
   - **BEA:** the states sum to the US row.
   - **Published figures (read-only web lookups):**
     - price_c_kwh for GA, VA, TX, CA and NY in 2015 and 2024, against EIA's published average retail price (State Electricity Profiles or Electric Power Annual)
     - population for the same states against the Census estimates
     - Georgia's 2024 renewable share against EIA's Georgia State Electricity Profile

     Report each with the source link and the difference.
3. **Reproduce.** Compare the new master panel cell by cell with the panel the old build_panel.py makes from the same raw files, with code/reference/expected_values.md, and with code/reference/prelim_means_by_year.csv. Expect zero differences. Explain each one (for example, a newer vintage).
   - **Georgia spot check:** 2025 renew_share 0.1287, solar_share 0.0768, ai_dc_per1000 5.0346; 2015 ai_dc_per1000 2.0106; dc_jobs 8,346 (2015) and 24,620 (2025).
4. **Trace.** Pick 25 random cells (fixed seed) spread across sources and variables. Trace each back to raw file, sheet, row and column. Show: the raw value, each transformation, and the final value.
5. **Plausibility.**
   - **Keys:** (state, year) is unique: 561 rows, 550 without DC. FIPS, postal code and name map correctly for all 51. US and DC rows are excluded wherever they should be.
   - **Ranges:** shares fall in [0, 1]. No negative jobs, GDP, population or sales. Units are as labeled.
   - **Big jumps:** list every year-over-year change above 50% in a model variable, the top 20 at least, each with a reason: a small denominator, a new plant, suppression, or a definition change.
   - **Spotlight states:** VA, TX, GA, WA. Look for anything that looks off.
   - **Missingness:** a table by variable and year, with every gap given a reason.
6. **Vintage.** Give each source's release date and which years are preliminary, especially EIA 2025. Note anything likely to be revised before the paper is due.

**Data verdict table** at the top of DATA_VALIDATION.md, with one row per model variable. Columns:
- right definition (yes/flag)
- numbers check (pass/fail)
- reproduces (yes/diff)
- ready for methods (green/yellow/red)
- note

Any red blocks Phase 4a. Tell me exactly what would fix it.

---

## End of phase
1. **The walkthrough notebook:** notebooks/02_data_and_methods_walkthrough.ipynb. Easy to read, runs top to bottom, no estimation.
   - **Part 1, Data.** One section per source:
     1. what it is and where it came from (link, vintage)
     2. why we need it (which variable, which step)
     3. a look at the raw file
     4. each cleaning step in plain English next to its code
     5. the cleaned result (rows, years, states, missing values)
     6. a link to its receipt

     Then cover the merge.
   - **Part 2, Is the data right?** The Part C checks with their tables, the traced cells, and the verdict table. Add two quick sanity charts, not results: AI per 1,000 and renewable share over time, Georgia vs the U.S. median.
   - **Part 3, Methods preview.** Explained, not run. For each step, give the equation, the columns that feed it, and whether its data is green, yellow or red.
2. **Handoff:** docs/<date>/phase-2-data-audit-and-cleaning.md, with the five sections plus "How to resume". The next prompt is prompts/04a_methods_spec.md.
3. **Updates:** update EXPERIMENTS.md (the Data section) and CLAUDE.md §3-5.
4. **Git commit:** code, notebooks, receipts and docs. Raw data, the workbook and cleaned CSVs stay out of git until Phase 5 decides.
5. **Summary to me:**
   - what's ready
   - the verdict table counts (green, yellow, red)
   - any check that failed
   - what's still missing

   Then STOP. Don't start the methods.

# Phase 2: data audit, then cleaning, an easy Excel workbook, .md receipts and a walkthrough notebook

This prompt replaces prompts/02_data_catalog.md and prompts/03_data_cleaning.md. Use them only as reference: the catalog spec is in 02 §3, and the per-source cleaning rules and checks are in 03 §2 and §4.

ECON 499R project (Shunji Lewandowski and Alexander Hendricks, Prof. Fohlin). The project root is the "AI impact on Renewables" folder, already organized in Phase 1.

Before anything:
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (including the divergence register), the newest file in docs/ (the Phase 1 handoff), docs/2026-11-01/context-handoff-from-chat.md, and data/data_links.md.

## Hard limits for this phase
- No models, estimation, regressions, winsorizing or "testing" of hypotheses. That is Phase 4.
- Don't download anything without my approval of the specific list.
- Never edit raw files. Never invent, impute or fill data.
- Never delete anything. Unreadable files go to data/_to_delete/ with a reason.

---

## PART A: Data audit. Do this first, then STOP and wait for me.

1. **Map what we have.**
   - Run `python code/python/download_all.py --raw-dir data/raw --list` to get the exact target path each script expects.
   - Match every data file in data/ (and any data file Phase 1 left elsewhere) to its target. Browser downloads often have different names; e.g. "HS861 2010-.xlsx" becomes data/raw/eia/HS861_2010-.xlsx.
   - Show me a table with: current file, matched dataset, target path, and match confidence.
2. **Check readability.**
   - Unzip every .zip into a same-name folder beside it, keeping the zip.
   - Open each file just enough to confirm it's real.
   - Flag files that are empty, partial downloads, HTML or "Request Rejected" pages, or that won't parse.
3. **Check completeness against the methods.**
   - Build a requirements matrix with one row per needed input and these columns: method step, variable(s), source and file, years needed, years we have, status, gap.
   - **Step 1 outcomes and controls:** the EIA state files (generation, capacity, HS861 sales) through 2025, plus BEA SAGDP (lines 1, 4, 12; SAGDP9 line 1) and SAINC1 (population) through 2025.
   - **AI measure:** QCEW 518210 and industry 10 for every year 2014-2025, which is 24 files. 2014 is needed for the 2015 lag. Note BLS suppression: AK, ND, SD and WY in 2025.
   - **Step 2:** QCEW 5415 for 2014-2025 (12 files), plus the Census Gazetteer (land area).
   - **Step 3:** the Census Gazetteer (centroids) and county adjacency (border matrix).
   - **Step 4 robustness:** EIA SEDS (through 2024), the LBNL RPS/CES targets, and data-center MW (Epoch / Cleanview).
   - **Stretch:**
     - NOAA HDD/CDD: 48 states x 2 files
     - NSF Table 10 for 2017-2023: note that 2015-2016 would need older editions
     - Census ACS S2801: needs a key; no 2020 1-year release
   - **Georgia case box:**
     - the 2025 IRP main document
     - the large-load reports from Q1 2024 to the latest quarter
     - the docket documents we cite
   - **Finance side:**
     - the PUDL FERC1 tables
     - SEC company facts (script, needs SEC_USER_AGENT)
     - Lazard 2026
     - Bloomberg (by hand; licensed, keep out of git)
4. **Answer: do we need more data?** Give two lists, each ordered most important first, then easiest first:
   - **(a) Required but missing or broken:** what it is, which step it blocks, and its link from data_links.md.
   - **(b) Optional additions that would strengthen the methods:** what each one adds, effort, and link. For example:
     - AI patents (USPTO AI Patent Dataset plus PatentsView) as an alternative AI measure
     - EIA-860 for battery storage capacity
     - NSF editions for 2015-2016
     - later Georgia large-load reports
     - LBNL Utility-Scale Solar for a solar cost projection

   For each item, say whether download_all.py can fetch it or it needs a browser.
5. **Write the audit and stop.**
   - Write data/DATA_AUDIT.md (the matrix plus both lists) and docs/<date>/phase-2a-data-audit.md (five sections plus "How to resume").
   - Then STOP and wait. I'll approve file moves, tell you which gaps to fill, and add any files I download by hand.

---

## PART B: After my OK. Organize, catalog and clean the data. Still no models.

1. **Place the files.**
   - Move and rename the data into data/raw/<source>/ as approved. Log every move in logs/<date>/phase2_moves.csv (old_path, new_path, sha256).
   - Name files that download_all.py doesn't cover `SOURCE_description_years.ext`.
2. **Catalog** (spec in prompts/02_data_catalog.md §3):
   - data/DATA_CATALOG.xlsx: an Index sheet plus a preview tab per dataset (first 100 rows, untouched)
   - data/previews/<label>.md
   - data/DATA_INDEX.md
3. **Clean** (rules in prompts/03_data_cleaning.md §2 and §4).
   - Use a package in code/python/clean/ with one module per source.
   - The driver is code/python/build_master_panel.py with a required `--date YYYY-MM-DD`. It checks inputs before doing any work.
   - **Outputs:** cleaned flat files in data/. The master file is data/state_panel_2015_2025.csv, plus data/codebook.csv, the W matrices, the financial tables and one file per stretch source.
   - **Logs:** logs/<date>/build/, with checks.md.
   - **Expected values:** must match code/reference/expected_values.md. If a file is a newer vintage, explain every difference.
   - **Missing data:** leave it as NA with a reason.
4. **The easy-access Excel workbook:** data/ECON499R_Data_Workbook_<date>.xlsx. Use Arial, frozen header rows, filters on every table, units in headers, and no formula errors (recalculate and check). Tabs:
   - **README:** what the workbook is, the as-of date, how to use each tab, the sources, and what's still missing.
   - **Master Panel:** one row per state-year. Memo variables first (state, year, ln_ec, ln_ee, renew_share, ai_dc_per1000, its lag, tech_share, ea, the 4 controls), then the rest. Make the core derived columns live formulas from the raw columns beside them, so Alexander can audit each definition.
   - **Georgia:** Georgia's rows next to the U.S. median for the key variables.
   - **Codebook:** variable, definition, unit, source, link, years, non-missing count.
   - **Missing Data:** variable x year, with the reason for each gap (suppressed, not released yet, not covered).
   - **Sources & Receipts:** one row per source with its link, raw file(s), vintage, and receipt file name.
   - **Financials:** FERC1 utilities, FERC1 cost by technology, SEC companies (if fetched).
   - **W Distance** and **W Border.**
   - **One tab per stretch table that exists.**
5. **.md receipts, written so they can go on GitHub as-is.** Use relative paths only. No personal emails or local absolute paths, and no licensed data contents.
   - **data/receipts/<source>.md, one per source:**
     - source and link
     - raw file name(s), size, sha256, and download date or vintage
     - what we kept (the filters) and every transformation, in order
     - rows in and rows out
     - checks run and their results
     - known quirks
     - output file and columns
     - the script and function that did it
   - **data/receipts/README.md:** an index of all receipts plus how to rebuild everything (download_all.py, then build_master_panel.py --date ...), noting which files need a browser.
6. **The walkthrough notebook:** notebooks/02_data_and_methods_walkthrough.ipynb. Easy to read, runs top to bottom, no model estimation.
   - **Part 1, Data.** One section per source, each with:
     1. what it is and where it came from (link, vintage)
     2. why we need it (which variable, which method step)
     3. a look at the raw file
     4. each cleaning step in plain English next to its code
     5. the cleaned result (rows, years, states, missing values)
     6. a link to its receipt

     Then cover the merge and the final checks.
   - **Part 2, Methods.** Explained, not run. For each step (H1 two-way FE; H2a and H2b mediation with Sobel; H3 Moran's I, SLX and SDM with direct and indirect impacts; Step 4 robustness; the stretch goals):
     1. the equation
     2. what it tests in plain words
     3. the exact columns that feed it
     4. what result would support the hypothesis
     5. the divergence-register items that apply (tech_share vs HMA, RPS, AI squared, SDM impacts, AI measure)
     6. whether all of its data is ready
   - **Closing table:** every memo variable, its column, its source, its receipt, and its status.
7. **End of phase.**
   - Write docs/<date>/phase-2-data-audit-and-cleaning.md: the five sections plus "How to resume", naming the next prompt as prompts/04_models.md.
   - Update EXPERIMENTS.md (the Data section) and CLAUDE.md §3-5.
   - Git commit code, notebooks, receipts and docs. Raw data, the workbook and cleaned CSVs stay out of git until Phase 5 decides.
   - Give me a summary: what's ready, any check that failed, and what's still missing.

   Then STOP. Don't start models.

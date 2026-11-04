# Phase 4i: upgrade the data workbook into our master data workbook

Start from the newest outputs/ECON499R_Data_Workbook_*.xlsx and the script that builds it. Keep what works:
- Arial
- blue values and black formulas
- live formulas in the Core Panel
- frozen headers and filters on the original tabs
- every data tab

Goal: one workbook that holds all our data and shows where every variable came from and where to find it. It carries every validation result and limitation, and it rebuilds with one command whenever data changes.

## 1. Build script and one source of truth
- Turn the current workbook script into code/python/build_master_workbook.py --date YYYY-MM-DD. It reads only cleaned outputs, receipts and validation files, and never edits data.
- Output: outputs/ECON499R_Master_Data_<date>.xlsx. Move older workbooks to outputs/old/; never delete them.
- Add to CLAUDE.md: after any data change, rerun this script.
- Upgrade the Codebook into data/variable_registry.csv, one row per variable in every tab. Columns:
  - variable, plain-English definition, unit, formula
  - source and publisher, exact file link and landing page, raw file path, sha256, vintage or access date
  - receipt, script and line numbers that build it
  - workbook tab and column letter
  - years and states covered, missing cells with reasons
  - used in (Zhang / Fang / Georgia / finance / not used)
  - primary or secondary source, citation for the paper
  - validation rating with the check behind it
  - limitations
  - status (Ready / Pending / Not available)
- Generate the workbook's Variable Finder tab and data/DATA_DICTIONARY.md (for GitHub) from this registry, so they can't disagree.

## 2. Fix what's broken
- **README:** rewrite it for the current build. Include the as-of date, every tab, how to rebuild, what's pending, and a pointer to the Limitations tab.
- **Sources:**
  - Make every URL a clickable link, and reset the filter to cover all rows.
  - Add columns: publisher, landing page, exact download link, access date, vintage or release date, primary or secondary, citation, license note, raw files with sha256, receipt.
  - Add the missing sources: Georgia PSC dockets and the IRP (cite the PSC docket, and note the SELC copy), Lazard, RMI, the EIA-860/923/861 forms, the Census region lookup, the EIA-860 2017 file, the June 2023 RPS edition, the AI Index editions, SEDS prices and NCSES.
- **Tabs added on Nov 4 (RPS through AI All Ownerships):** add filters and freeze row 1. EPU Annual is frozen at A167 and AI All Ownerships at A123.
- **Prelim Results:** remove it; it stays in the Oct 30 copy in outputs/old/. Add a README line pointing to results/ and the results pack.

## 3. Add what's missing
1. **Variable Finder** (from the registry): every variable, with links to its tab and column, its source URL and its receipt. Color the rating and status cells.
2. **Core Panel:**
   - Add live formulas for the other memo variables: ln_ea, pop_growth, wind_share, coal_share, co2_per_mwh, new_renew_mw, net_exporter_2015 and energy_equity. Add the blue input columns they need.
   - Add the flag columns in_zhang_sample (DC excluded) and in_fang_sample.
3. **Fang Panel:** Fang's variables, including the AI postings with edition and vendor columns.
4. **Validation:**
   - Every check from Phase 2 Part C, the Nov 4 new-data checks, the Nov 4 audit and the Fang Part A checks. Columns: check, what it tested, result, evidence, rating, date.
   - Add a cross-source consistency section:
     - BEA vs Census population
     - EIA retail sales vs SEDS electricity
     - QCEW state sums vs the national row
     - EIA fuel sums vs the total, and state sums vs the US total
     - BEA states vs the US total
     - state codes and years matching across every tab
5. **Limitations:** list them per variable and overall, with how each affects interpretation. Start from the list below plus the README's current caveats.
6. **Missing Data:** variable × year, with the reason for each gap.
7. **Georgia:**
   - Georgia's rows next to the U.S. median
   - the large-load report table, with page citations
   - IRP figures, with document and page
   - Epoch's Georgia sites
8. **Raw Files:** one row per raw file, with path, size, sha256, source, rows × columns, whether it's in the workbook in full or summarized, and receipt.
9. **Changelog:** what changed in each build.

## 4. Size rule
- Every cleaned dataset goes in whole.
- A raw table goes in whole if it's under about 200,000 rows.
- Larger raw tables get a summary tab instead: columns, row count, years, what we kept, and the path. Examples: the EIA-860/923 plant files, raw county-level QCEW files, full PUDL tables.
- Never include licensed Bloomberg data, interview transcript text, keys or personal emails. Point to them only.

## 5. Check the workbook after building
- Recalculate it and confirm there are zero formula errors. Use LibreOffice if it's installed; ask before installing anything.
- Every tab's row count matches its source file.
- 30 random cells (seed 2026) match their source files.
- Every registry variable appears in the Variable Finder and links to a real tab and column.
- Every URL opens (check read-only).
- Report the file size.

Write data/receipts/master_workbook.md and a short handoff in docs/<date>/. Commit the script, registry, dictionary, receipt and docs. The workbook itself stays out of git.

## Known limitations to start from (add to these)
- **AI measure (518210):**
  - It's private data-center jobs per 1,000 workers: a proxy for data-center activity, not for AI use. Jobs don't equal MW.
  - The industry also includes general data processing and hosting.
  - GA ranks above VA.
  - BLS suppressed AK, ND, SD and WY in 2025.
  - Government jobs are excluded: 0.83% overall, 24.6% in NM.
- **AI job postings (Fang):**
  - Postings aren't jobs.
  - The vendor changed (Burning Glass, then Emsi Burning Glass, then Lightcast), and counting changed between editions.
  - Each year comes from a different report; only 2019-2021 come from one edition.
  - Postings are 1.3-3.2 times noisier than data-center jobs.
  - WA shows a method break at 2021-2022.
- **Generation and capacity:**
  - Utility-scale only (1 MW and up), so no rooftop solar.
  - Capacity is nameplate; EIA also publishes summer capacity.
  - EIA moves Gavins Point (132 MW of hydro) between NE and SD.
  - The total includes negative pumped storage.
- **SEDS:** it ends in 2024, and renewable consumption includes non-electric uses (biofuels, wood heat). CO2 also ends in 2024.
- **Price:** average revenue per kWh, all sectors.
- **BEA:**
  - Population comes from Census estimates, and vintages differ by up to about 95,000 people (MA 2017).
  - ln_ea uses nominal GDP.
- **RPS:**
  - This is LBNL's current schedule, not the targets in force.
  - LBNL revised past years.
  - There are 3 conflict rows: NY 2015-2016 and MT 2020.
  - Voluntary goals aren't coded.
- **EPU:** it's newspaper-based, and small states rest on few papers.
- **NSF R&D:** 2017-2023 only, each year from its own edition, with large swings in WY and AK.
- **ACS broadband:** 2015 isn't comparable with later years, and there's no 2020 1-year release.
- **NOAA:** not available.
- **Epoch:** large AI campuses only, about 45% coverage.
- **LBNL solar:** projects over 5 MW only.
- **FERC Form 1:** investor-owned utilities only (Georgia Power yes; EMCs and MEAG no). Solar, wind and storage accounts start in 2021.
- **SEC:**
  - The data are calendar-year frames.
  - NEE, DTE and HASI capex are blank.
  - Georgia Power has no standalone XBRL.
- **Other sources:**
  - PUDL and RMI are secondary sources.
  - Lazard is an industry estimate.
  - The Georgia IRP is the utility's own plan.
  - Kadoa's table is third-party.
- **Interpretation:** the placebo shows reverse timing for renew_share and for the spillover. List this under "affects interpretation," not under data quality.

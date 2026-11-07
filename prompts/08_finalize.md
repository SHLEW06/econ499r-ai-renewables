# Finalize: complete the Fang test, refresh every output, and show me the results

Read first: CLAUDE.md, EXPERIMENTS.md, the newest handoffs in docs/, prompts/04h_fang_test.md, docs/2026-11-04/fixes-before-push.md and data/receipts/README.md.

How to run:
- Run `date`. Show me a one-screen plan with time estimates and wait for my OK. Then run sections 1-6 in order without stopping.
- Keep a run log at docs/<date>/finalize-run-log.md, marking each section done once it's committed. If interrupted, resume from the first section not marked done.
- Commit after each section, one topic per commit.
- Stop and ask me only if: a reproduction gate fails; a data check comes out red; something would need deleting; or something would need a download not listed here.
- Before running each new analysis, write it into EXPERIMENTS.md (Fang test section). Report every result, null or not.
- All earlier rules hold: never edit raw data or invent data; "associated with," not causal language; append-only results with tags; never print the Census key.

## 1. Complete Fang et al. (2025)'s method set
Use both AI measures (postings and data-center jobs). Run Fang's spec (state FE, conventional SEs, logs, 2018-2021, with DC) and our spec (two-way FE, lag, clustered by state, extended sample, no DC) side by side.

1. Splits table (Fang Tables 3-5).
   - Groups: electricity consumption, electricity price, net producer, R&D funding, per capita income, and the four Census regions.
   - For each group, run three versions:
     - Fang-style separate regressions above and below the 51-state mean
     - the same with a median split
     - our interaction test: the group difference with SE and p
   - Pull anything that already ran from fang_results.csv; run only what's missing.
   - Put it all in one table, with a sentence per row on whether it matches Fang's pattern.
2. Negative indicator (Fang Supplement B): fossil-fuel consumption from SEDS as the outcome, in logs and as a share of total energy. If Fang's story holds, the AI sign should be negative.
3. Extreme-weather split (Fang Table 4).
   - Count extreme heat and extreme cold events per state-year from NOAA NCEI's Storm Events Database bulk CSVs (event types such as Excessive Heat, Heat, Extreme Cold/Wind Chill, Cold/Wind Chill).
   - Download by script, and document the event types and counting rule in a receipt.
   - Split high vs low, as Fang did.
4. Exact old SEDS basis.
   - Replace the single-k approximation with a year-by-year rebuild. For wind, solar, hydro and geothermal, convert captured energy back to fossil-fuel equivalence using EIA's fossil-fueled plant heat rate for each year (Monthly Energy Review, Table A6) divided by 3,412 Btu/kWh.
   - Cite the table and the SEDS change notice (eia.gov/state/seds/seds-change).
   - Check the rebuilt totals against any pre-October-2023 SEDS values you can find, and say how close they are.
   - Rerun Fang's Table 2 replication (columns 1-6) on the rebuilt outcome. Compare it with Fang's published coefficients and with the k version.
5. Optional, only if 1-4 are done: an event study.
   - Exposure = each state's 2019 share of U.S. AI postings (single edition).
   - Model: Y = sum over k of beta_k (Exposure x 1[year = k]) + state FE + year FE + controls. Base year 2021; outcome ln(renewable consumption); 2015-2024.
   - Report the joint tests for pre-2022 and post-2022.

## 2. Notebooks
- Update notebooks/04h_fang_test.ipynb; don't create a new one.
  - Add one section per item in section 1. Each section has: what Fang did, what we ran and why, the equation, the table, one chart, and a two-line plain-English reading.
  - Rewrite the summary at the top so the replication story uses the rebuilt SEDS basis.
- If any table it shows changed, update notebooks/04g_results_pack.ipynb too.
- Restart the kernel and run each updated notebook top to bottom, with relative paths only. Confirm there are no errors, then commit the executed notebooks with outputs.

## 3. Results pack
1. Update findings.md, the tables (LaTeX and CSV), number_check.csv, memo-to-paper.md, docs/<date>/methods_section.tex and docs/<date>/project-summary.md with the new Fang results.
   - The Fang paragraph now rests on the rebuilt SEDS basis.
   - Keep the k version only as a check.
2. Rebuild outputs/ECON499R_Results_<date>.pdf.
   - Add the new splits table and the new rows.
   - Use at least 8pt for appendix tables and 10pt for body text; 14-16 pages is fine.
   - Update section 1's validation counts to the current ratings.
   - Wording rules:
     - Fang's Table 2 constants: say the implied mean "is consistent with" the old SEDS basis, not that it proves it.
     - The Q2 2026 large-load report: cite both docket numbers (55378 on the filing, 56002 on the page headers) and the page every time.
3. Number check: every number in the PDF and findings.md must trace to a result tag. Report the count.

## 4. Master workbook (fix links, then rebuild)
1. Internal links: store them as internal links only, with a location and no target. Use the real, quoted sheet name, with no %20. Keep the column-specific targets.
2. Receipt links:
   - Point them to https://github.com/SHLEW06/econ499r-ai-renewables/blob/main/<path>.
   - Add a Receipts tab that holds each receipt's text, and give each Variable Finder row a second, internal link to it.
3. Never let LibreOffice save the final file.
   - Recalculate a copy, and use it only to check formula errors and to get cached values.
   - Write the final file with the cached values and the correct links.
   - Update build_master_workbook.py so every rebuild works this way.
4. Add a link check to the build. It fails if any hyperlink:
   - has a target containing "/Users/", "file:" or "../"
   - has "%" in its location
   - points to a sheet that doesn't exist
   - points outside a sheet's used range
5. Add the new data (storm events, heat rates, rebuilt SEDS), then rerun build_master_workbook.py.
6. Test the result:
   - Copy the workbook to /tmp under a different name and run the link check on the copy.
   - Confirm zero formula errors, matching row counts, and 30 random cells checked.

## 5. Packages
- Rebuild release/results_and_data_<date>/ and its zip. Include the PDF, the workbook, findings.md, the methods draft, memo-corrections.md, the project summary, and the notebooks as HTML.
- Refresh release/github/ and rerun its scans: key, tokens, emails, absolute paths, barred file types, files over 50 MB.
- Commit everything, but don't push.

## 6. Show me the results
In your final message, show:
1. The Fang replication: Fang's Table 2 next to our rebuilt-basis and k versions, columns 1-6.
2. The bridge table (Fang's spec to ours).
3. The splits table, the negative indicator, the extreme-weather split, and the event study if it ran.
4. A 5-line plain-English summary of the whole project's results, covering both the Zhang and Fang tests, the precise nulls and Georgia.
5. What changed since Nov 4, as a short list.
6. The files to send Alexander, with sizes, and the number of traced numbers in the PDF.
7. The link-check counts by type, and confirmation that every notebook ran cleanly.
8. The exact command for me to push: git push from the project folder.

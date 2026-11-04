# Receipt: master data workbook

**File:** `outputs/ECON499R_Master_Data_2026-11-04.xlsx`, 28.1 MB, 63 tabs, 949 registry rows. Stays out of git.

**Rebuild, from the project root:**
```
python3 code/python/build_cross_source_checks.py --date 2026-11-04
python3 code/python/build_raw_file_shapes.py --date 2026-11-04
python3 code/python/build_georgia_tables.py --date 2026-11-04
python3 code/python/build_master_workbook.py --date 2026-11-04
python3 code/python/check_master_workbook.py --date 2026-11-04
```
`check_master_workbook.py` recalculates with LibreOffice and installs the recalculated copy only if the checks pass, so formula values are cached for readers that don't recalculate.

**One source of truth:** `data/variable_registry.csv` generates the Variable Finder tab and `data/DATA_DICTIONARY.md`. Hand-written sources, definitions and limitations are in `code/python/master_workbook_meta.py`. Citations for the sources the audit covered are read from `data/INDEPENDENT_AUDIT_2026-11-04.md` section 4.

**What the script reads:** cleaned outputs, receipts and validation files. It also reads the raw tables that go in whole under the size rule, read-only. It edits no data.

## Checks (`logs/2026-11-04/master_workbook_checks.csv`)
| Check | Result |
|---|---|
| Formula errors after LibreOffice recalculation | 0 |
| Core Panel formulas equal the panel | 19 formula columns x 561 rows, no differences. `net_exporter_2015`: 30 net exporters, 0 rows differ. `in_zhang_sample` 550; `in_fang_sample` 204 |
| Row counts match source | 71 data tabs, no mismatches |
| 30 random cells, seed 2026 | 30 of 30 match, 25 tabs (`logs/2026-11-04/master_workbook_30cells.csv`) |
| Registry to Finder to tab and column | 949 of 949; 948 links, and the 1 row without a tab is Pending |
| Frozen headers, filters, Arial, 13,923 live formulas, blue inputs | Survive recalculation |
| Sources tab | 46 sources, 92 clickable links, filter covers all rows |
| URLs, read-only | 64 unique: all open on Nov 4 |
| Census key or email addresses in any cell | None |

## Cross-source checks (`logs/2026-11-04/cross_source_checks.csv`)
All green. BEA population matches Census in all 561 state-years, gap 0. EIA retail sales match SEDS ESTCB at 3.412 MMBtu/MWh in all 510 state-years, largest gap under 0.01%; SEDS builds this series from EIA's retail data, so this confirms the unit, not an independent measure. QCEW 518210 largest gap 0.22%, all-industry under 0.001%. EIA fuels vs total largest gap 0.0005% (DC 2024). EIA states vs U.S. under 0.001%. BEA states vs U.S. 0.613%, which BEA's footnote attributes to overseas activity. State codes match across 10 tables.

## Decisions to know about
- **Size rule, as applied.** Whole: every cleaned table, plus 27 raw tables. Summarized on Raw Table Summary: county-level QCEW, EIA-860/923 and full PUDL tables (the prompt's examples, even where under 200,000 rows); four RMI tables and the Census intercensal file (over 200,000 rows); and folders of many small files (BEA 1,589 files, NSF, ACS, NCSES, AI Index) whose kept values are whole in a cleaned tab. The all-area BEA tables the panel uses are whole.
- **Validation carries old results with their corrections.** Rows where the Nov 4 audit overturned a Nov 2 note keep the original result and add the correction.
- **P10 result reads "FAIL" in the Nov 2 log.** It's a count of big year-over-year jumps. All 200 were reviewed in C.5, and the Part C verdict has no reds. Rated yellow here.
- **The one red row** is `nsf27300-tab010.xlsx`, the team's wrong NSF table: rated red on Nov 4, not used. It doesn't block anything.
- **Prelim Results removed.** It stays in the copies in `outputs/old/`. README points to `results/`.
- **NOAA.** NCEI timed out when tried on Nov 4. Its link answered the read-only check later the same day. Nothing was downloaded: the team's decision stands.
- **Not rated.** 611 registry rows are raw columns or finance and all-ownership tables with no Part C or Nov 4 rating. They say "not rated" rather than inheriting one.
- **Georgia tables.** `code/python/build_georgia_tables.py` parses Table 2 from the Q2 2026 PDF and stops if a cited figure isn't on its cited page. Attachment totals reconcile with the reports: committed 31 and 32 projects, 12,357 and 15,567 MW, vs the reports' 12,400 and 15,600. The Q2 large-load row prints +6,900 where its rounded levels differ by 7,000. Q1-Q4 2024 reports are Pending.

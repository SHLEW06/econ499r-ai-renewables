# Workbook links fix, 2026-11-04

Every hyperlink in the master workbook now works after the file is moved, renamed or downloaded. No data changed. In `data/variable_registry.csv`, only `script_lines` changed, because the build script's lines moved.

## Cause
LibreOffice saved the final file during the recalculation check. It rewrote all internal links as external links to the file's own path on one Mac, with URL-encoded sheet names. Receipt links were relative paths to `data/receipts/`.

## What changed
| Item | Now |
|---|---|
| Internal links | A location and no target: `'Sheet Name'!A1`. Variable Finder keeps its column-specific targets |
| Receipt links | `https://github.com/SHLEW06/econ499r-ai-renewables/blob/main/data/receipts/<file>` |
| Offline receipts | New Receipts tab with each receipt's text, one row per line, and an index. New Variable Finder column `receipt_in_workbook` |
| Web links | Unchanged |
| Final file | openpyxl's build plus cached values from a LibreOffice-recalculated copy. LibreOffice never saves it (`code/python/workbook_finalize.py`) |
| Link check | `code/python/check_workbook_links.py`. The build won't install a file that fails it |
| Results PDF | Section 1 has the current validation counts. Appendix tables are 8pt, and the report is 14 pages |

Sources rows keep one receipt link, to GitHub. The second, internal link is on Variable Finder only, as asked.

## Link counts
| Type | Links |
|---|---:|
| Internal | 2,933 |
| GitHub receipt | 995 |
| Web | 1,028 |
| Total | 4,956 |

The check also fails the old Nov 4 file (14,706 problems) and each kind of bad link in a small test workbook.

## Validation counts in the PDF
The old sentence, 0 red, 3 yellow and 17 green, is still right for the 20 model variables, so the PDF keeps it and labels it. It now leads with the whole Validation tab: 214 checks, 173 green, 39 yellow, 1 red, 1 not run. Counts are read from `results/2026-11-04/paper/validation_counts.csv`, which the workbook build writes.

## Open items
- **Repo access:** on Nov 4, `SHLEW06` is the repo's only collaborator, so GitHub receipt links return 404 for anyone else until they're added. The Receipts tab works without access.
- **The repo's contents:** GitHub `main` holds the working repo's history, not the clean copy. It includes the interview transcript in `notes/`, and past commits hold the memo and Zhang PDFs. See `release/github/CHECKLIST.md`.
- **Not tested in Excel by script:** the link check reads the file's XML. Clicking the sample links in Excel is the final confirmation.

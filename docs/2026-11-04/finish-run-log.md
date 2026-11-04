# Finish run log (prompts/06_finish.md)

Started 2026-11-04. Resume from the first section not marked done.

| Section | Status | Commit | Notes |
|---|---|---|---|
| Setup | done | see git log | LibreOffice 26.8.2.2 installed by brew as approved. Placeholder email removed from `download_all.py` |
| 1. H3 wording | done | see git log | -0.161, p = 0.035, as approved |
| 2. Fang Part B | done | see git log | Replication does not reproduce on current SEDS; the 2023 SEDS accounting change explains the sign. Not a stop rule: the driver gate passed |
| 3. Stretch goals | done | see git log | IV uninformative (KP F = 2.81). No moderator interaction significant |
| 4. Georgia solar | done | see git log | Paths verified in IEA WEO 2025 Annex A. The IEA PDF is not kept in the project |
| 5. Results pack | done | see git log | All lookups match; `number_check.csv` |
| 6. Master workbook | done | f509104 | 28.1 MB, 61 tabs, all checks pass |
| 7. Project summary | done | 2f2b7ce | 73 numbers match; 3 published figures cited |
| 8. GitHub package | done | 441ee25 | 322 files, 16.5 MB; scans clean; one commit, no remote |
| 9. Results and data package + PDF | done | d2a3684 | PDF 12 pages, 77 numbers match; folder 50.4 MB, zip 37.7 MB |

## Flags from sections 6-9

- **Report and summary numbers:** every number in the text is traced to a tag: `results/2026-11-04/paper/number_check_summary.csv`, `number_check_report.csv`. A published figure is listed with its location.
- **SLX with lead and lag together:** neighbors' past AI is significant for ln_ec (inverse distance and border) and, on border weights, for ln_ee. The SDM versions have CIs that include zero. Stated in the report's H3 section. `findings.md` doesn't mention it; the team should decide whether the paper does.
- **`fig_h1_coefficients.png`:** MW and share outcomes share one axis, so the MW row squashes the others. Left out of the report; the spec curve shows them panel by panel. Replace it before using it in the paper.
- **Notebooks 04a-04c:** they were not executed until this run. They now are, with relative paths; 04b carries the later readings at the top.
- **NOAA:** NCEI answered a read-only link check on Nov 4, after timing out earlier that day. Nothing was downloaded; the team's decision stands unless it changes it.
- **Workbook location in the team package:** `outputs/` inside the folder, so its receipt links keep working.


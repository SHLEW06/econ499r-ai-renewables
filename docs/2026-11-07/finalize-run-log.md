# Finalize run log (prompts/08_finalize.md)

Started 2026-11-07 16:53 EST. Run together with `prompts/09_extend.md` (see `docs/2026-11-07/extend-run-log.md`). Team decision 2026-11-07: run 08 sections 1-2 now; sections 3-5 are folded into 09 section 7 (pass 2).

| Section | Status | Commit | Notes |
|---|---|---|---|
| 1. Fang method set (splits, negative indicator, extreme weather, exact old basis, event study) | **done** | 00c8464, 9a237b7 | Event study (optional 1.5) ran. F27 added after results (deviation, logged) |
| 2. Notebooks (04h, 04g if a table changes) | **done** | 5e99ac5 | 04h executed top to bottom, 21 code cells, 0 errors. 04g unchanged: none of its tables changed |
| 3. Results pack | deferred to 09 section 7 (pass 2) | | |
| 4. Master workbook | deferred to 09 section 7 (pass 2); link fixes already done 11-04 | | |
| 5. Packages | deferred to 09 section 7 (pass 2) | | |
| 6. Show me | with the 09 pass 1 report | | |

## Notes
- Downloads (`logs/2026-11-07/finalize_downloads.csv`): NOAA Storm Events details 2015-2024; EIA SEDS archive (June 2023 release, data through 2021); SEDS change notice; SEDS physical-units file (residential small-scale PV, SOR7P); EIA bulk MER (TOTAL.zip). MER Table A6's own export endpoints returned empty or other tables: `MER_TA6.xlsx` is in fact MER Table 1.1 and `full_data_MER.zip` is EV-charging microdata; both are unused and can be deleted (team decision; not deleted here).
- Old-basis rebuild matches the archived SEDS exactly once the archive's biomass is used (median 0.00%, max 0.19%); with current biomass, median 0.57%.

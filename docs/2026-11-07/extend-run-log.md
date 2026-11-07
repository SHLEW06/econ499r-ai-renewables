# Extend run log (prompts/09_extend.md)

Started 2026-11-07. Plan approved with changes (team, 2026-11-07): two passes. Pass 1: 08 sections 1-2; 09 sections 1-4 with their notebook sections; 09 section 8 items 1-4, 6, 7 and 08 section 6. Pass 2 (on "pass 2"): 09 section 5 and its notebook section, then section 7 once, then the rest of section 8. Disk: stop if under 8 GB free at section 5.

| Section | Status | Commit | Notes |
|---|---|---|---|
| Prereq: 08 sections 1-2 | **done** | 9a237b7, 5e99ac5 | `docs/2026-11-07/finalize-run-log.md` |
| 1. Cross-check against Fang | **done** | e4b57ad | Fang's Table A1 not in literature/; means implied by Table 2 constants used. Placebo industries: distilleries, pet care |
| 2. By type and Georgia | **done** | 7d0f63a | ln geothermal generation not estimable (7 states). Small-scale solar not in the panel |
| 3. AI-impact family | **done** | 209e302 | No q < 0.10 (min 0.44); no lead placebo or restructuring model needed. Battery storage not in the panel. Deviations X1 (Texas), X2 (price controls) |
| 4. National trend drivers | **done (interim)** | 9fd4fbb | Drivers model without wind cost and PTC (CRS, LBNL wind blocked: HTTP 403). NREL unreachable; EIA CF fallback (X4). Full model in pass 2 if the files are provided |
| 5. Better AI measure | **done** | 45b6b6f, bd3ede6 | Infrastructure + talent index, 2018-2023, 43 states; innovation dropped (no inventor locations); add-on run except Queued Up (403) |
| 6. Notebook 09_extend.ipynb | **done** (all sections) | debf237 | Executed top to bottom, 6 code cells, 0 errors |
| 7. Refresh outputs | **done** | 25ceac8, 4b7ed37 | Results pack, findings Extensions, summary, PDF (19 pages: 13 body + 6 appendix), workbook (73 tabs, link check 0 problems), team zip, GitHub copy (scans clean) |
| 8. Show me | **done** | | Final report in the session |

## Pass 2 (started 2026-11-07)
| Item | Status | Commit | Notes |
|---|---|---|---|
| 1 June 2023 SEDS as main old basis (trend, placebos, final spec) | **done** | 5ccf17f | Final spec on the archive limited to 2015-2021 (jobs), 2019-2021 (postings) |
| 2 State-specific trends (H1 core, by-type, bridge, placebos) | **done** | 5ccf17f | Distillery placebo still p = 0.040 with trends |
| 3 Postings-wind row | **done** | 5ccf17f | p = 0.136 with trends; jobs fails the lead test, so exploratory, against expected sign |
| 4 Biomass rows | **done** | 5ccf17f | `p2_biomass_rows.csv` |
| 5 Page check, 15,600 MW | **done** | 1af8ca8 | Both pp. 5 and 8 state it; no citation changed |
| 6 IRP wording | **done** | 5ccf17f | MW by type only where pages quantify it; "mostly gas" dropped |
| 7 Drivers wording | **done**; full model **blocked** | 5ccf17f | CRS R43453, IF10479 and LBNL wind file not in `data/raw/` |
| 8 Section 3 bounds per within-state SD | **done** | 5ccf17f | |
| 9 Relevance test (jobs, postings) | **done** | 5ccf17f | Index versions wait for section 5 |
| 10 Wording | **done** | 36a9a79 | |
| 11 Gap decomposition | **done** | 5ccf17f | |
| 12 Move unused MER files | **done** | 1af8ca8 | |
| 13 New files | **not present** | | Checked `data/raw/crs/`, `data/raw/lbnl/`, `literature/`, ~/Downloads |
| Section 5 | **stopped** (stop rule) | | OEWS state zips: HTTP 403 to scripts. PatentsView tables moved to the USPTO portal; no scriptable URL found (old S3 links: Access Denied). AIPD 2023 and BTOS downloaded. Without OEWS and inventor locations, only QCEW (one source) covers 2015-2023 |
| Sections 6 (section 5 part), 7, 8 | pending | | Waiting on section 5 decision |

## Pass 2, part 2 (after the hand downloads)
| Item | Status | Notes |
|---|---|---|
| A. File downloads | **done** (db4ab9b) | CRS R43453, IF10479, R46865; LBNL wind 2026; OEWS 2015-2024. "Fang Supplement.pdf" was the article (same hash), so the supplement is still missing. Duplicates moved to `data/raw/_to_delete/` |
| B1 full drivers model | **done** (86fa48a) | Section 4 final |
| B2 Table A1 and Supplement B | superseded below | First reported as not run; the supplement arrived later |
| B3 section 5 index | **done** | See section 5 |
| B4 relevance and slope ranks | **done** | |
| B5 IRP page convention and batteries | **done** | 22 cites rechecked; 500 MW is part of 780 MW |
| B6 distillery placebo | **done** | 13 never-suppressed states |
| Add-on A1-A5 | **done** except A4 | Quid covers 2025 only, so grouping; Queued Up 403; X5 land sensitivities post hoc |
| Section 5 stop rule | resolved | OEWS hand download; three components cover 2015-2023 (QCEW) plus research scientists |
| B2 Table A1 and Supplement B (late arrival) | **done** (5484ac3) | `fang supplement.docx` arrived after the first section 7 build; filed to `literature/Fang_Lee_Li_2025_supplement.docx`. A1: EPU about ln 2 below Fang's (doubled index); B1: coal and gas inside our CIs, petroleum not. Outputs, workbook and packages rebuilt |

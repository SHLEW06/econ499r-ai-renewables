# Phase 4g: Results pack
**Date:** 2026-11-04  
**Driver:** `code/python/04g_results_pack.py --date 2026-11-04`  
**Notebook:** `notebooks/04g_results_pack.ipynb`  
**Results:** `results/2026-11-04/paper/`

---

## 1. What was done
19 table groups (CSV and .tex), 9 figures with captions, `findings.md`, `rule_out.csv`, `number_check.csv`, `docs/2026-11-04/memo-to-paper.md` and `docs/2026-11-04/methods_section.tex`.

## 2. Key decisions
Every number in `findings.md` is read from a result file as it's inserted, through `code/python/results_lookup.py`. "What we can rule out" uses the SD of winsorized lagged AI after removing state and year effects (0.5212), as the team specified.

## 3. Results
See `findings.md`.

## 4. What did not change
No new estimation.

## 5. Decisions still open
None for this phase.

## How to resume
Rerun the driver. Next: the master workbook.

# lm_proper.csv header fix (and the same fault in dynamics.csv), 2026-11-09

No result changes. Two committed files have rows whose fields don't line up with their header. The files stay as they are (results are append-only); corrected copies are in `results/2026-11-09/h1/`, and the script that wrote the bad rows is fixed.

## What was wrong

**`results/2026-11-02/h1/lm_proper.csv`.** `code/R/04b_step1_twfe_checks.R` wrote it first: a 16-column header and 8 ctrl5 rows, with no `controls` column. `code/R/04b_step1_twfe_ctrl4.R` then appended 8 ctrl4 rows with 17 fields: `controls` is the second field. Read by the header, every ctrl4 value from `b2` onward sits one column to the right. pandas can't read the file at all ("Expected 16 fields in line 10, saw 17").

**`results/2026-11-02/h1/dynamics.csv`.** Found while testing the fix. The ctrl4 script appended 3 long-difference rows with `lag_k` before `status`, while the header has `status` before `lag_k`. Same field count, so a field-count check misses it. Read by the header, those rows have `status` blank and `lag_k = "ok"`.

The cause in both: the ctrl4 script's `write_append()` called `fwrite(..., append = TRUE)`, which writes the new rows' columns in their own order and never checks the existing header.

A scan of all 248 CSVs under `results/` found no other file with a ragged row, and no other `status` or `lag_k` column holding a value from the wrong column. Two files put notes in `status` on purpose (`h1_extras.csv`, LOSO ranges; `results/2026-11-03/h2/h2_results.csv`, bootstrap counts and a1 values). Those are written that way by `04b_*` and `04c_step2_mediation.R`; nothing is shifted.

## Corrected copies

| File | Change | Check |
|---|---|---|
| `results/2026-11-09/h1/lm_proper.csv` | 17-column header `outcome, controls, b2, ...`. The 8 rows without `controls` get `ctrl5`: `04b_step1_twfe_checks.R` fits them with `ctrl5` (line 56). Every other field is copied as text, unchanged | Equal, byte for byte, to the file a rerun of 04b, checks and ctrl4 with the fixed scripts writes |
| `results/2026-11-09/h1/dynamics.csv` | In the 3 ctrl4 rows, `status` and `lag_k` swapped back (`ok`, blank). Other rows unchanged | Same rerun, byte for byte |

The rerun was in a clean clone with throwaway dates. `h1_core.csv` from that rerun is identical to the committed one.

## Did any reported number come from a misaligned column? No.

| Reader | What it takes | Verdict |
|---|---|---|
| `code/python/04g_results_pack.py` (Table 3a, `lind_mehlum_summary.csv`) | `lm_pass` for the ctrl4 rows only. It already shifted the index by one for those rows, and asserted that every value is TRUE or FALSE | Correct: all 8 FALSE. Now reads the corrected copy. Rerun with the old and new script: identical output, and identical to the committed `results/2026-11-07/paper/` apart from the date |
| Table 3a coefficients (AI, AI squared) | `nonlinearity.csv`, not `lm_proper.csv`; that file is aligned | Unaffected |
| `notebooks/04b_step1_twfe.ipynb`, cell 15 (Lind-Mehlum table, typed by hand) | b2, p(b2), t at min and max for ctrl4 | All 8 rows match the correct columns. Text now points to the corrected copy |
| `EXPERIMENTS.md` section 3 results ("b2 p-values range 0.234-0.864", ln_ec b2 = -0.003, p = 0.364) | ctrl4 | Match |
| `docs/2026-11-02/phase-4b-step1.md` | "all 8 FAIL" | Match; dated handoff left as written |
| `findings.md`, results report (HTML/PDF), project summary | "No curve passes the Lind-Mehlum test" | Match |
| `number_check.csv` (Nov 4, Nov 7) | No Lind-Mehlum or `lm_proper` rows | Not affected |
| `dynamics.csv` readers: `code/R/04e_robustness.R` (long-difference "4b bug" rows), the 04b notebook | Pick rows by tag; use estimate, se, pval, N, CI. Neither uses `status` or `lag_k` | Unaffected; left pointing at the 2026-11-02 file |

**Numbers that change: none.**

## Fixes so this doesn't recur

- `code/R/04b_step1_twfe_ctrl4.R`, `write_append()`: reads the existing header line and writes the new rows in that column order. A column the header has but the rows lack is filled with NA; a column the rows have but the header lacks stops the run with the column's name, rather than shifting fields. Tested: appending to the old 16-column `lm_proper.csv` stops with "new rows have column(s) the header lacks: controls".
- `code/R/04b_step1_twfe_checks.R`: writes `controls = "ctrl5"` as the second column, so the usual run order (04b, checks, ctrl4) produces one consistent `lm_proper.csv`.

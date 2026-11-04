# Receipt: Census state population estimates

**Source:** U.S. Census Bureau, Population Estimates Program. Vintage 2025 state totals and 2010-2020 intercensal estimates.
**Downloaded:** 2026-11-04, by script, at the team's request.
**Use:** check only. `logs/2026-11-04/cross_source_checks.csv` compares BEA population in the panel against these files. Not in the panel and not in any model.

| File | Bytes | SHA-256 | Link |
|---|---:|---|---|
| `NST-EST2025-ALLDATA.csv` | 53,555 | `92188e29cb0a67dcf95afa7d6c47359409782f086478b70ea4128eb70e223ca9` | https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/totals/NST-EST2025-ALLDATA.csv |
| `sc-est2020int-alldata6.csv` | 18,292,193 | `a88c2879490e3283896e953d1aeddc8f9afb95cd90ab40f2910304a2548bd654` | https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/intercensal/state/asrh/sc-est2020int-alldata6.csv |

**What was kept:** `POPESTIMATE2020`-`2025` from Vintage 2025, state rows. `POPESTIMATE2015`-`2019` from the intercensal file, `SEX = 0` and `ORIGIN = 0`, summed over all ages and the six race groups, since that file has no race total.

**Result:** all 561 state-years match the panel exactly (gap 0 people). The panel's BEA population is the current Census series. Older Census vintages differ, by up to about 95,000 people (MA 2017; see `data/DATA_VALIDATION.md` C.6).

**Rating: green** (check source only).

# Receipt: LBNL Utility-Scale Solar, 2026 Edition

**Source:** Seel, Mulvaney Kemp, et al., Lawrence Berkeley National Laboratory, *U.S. Utility-Scale Solar, 2026 Edition*, October 2026.
**Link:** https://eta-publications.lbl.gov/publications/us-utility-scale-solar-2026-edition
**How:** Team browser download; moved from the project root on 2026-11-04.

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/lbnl/Utility Scale Solar 2026 Edition Datafile.xlsx` | 62,885,230 | `d3eccb46ec10c9b71cb77314908ad6ac11ebf83d5eac976492801029903ab341` |

## What was kept
`data/lbnl_utility_solar.csv`: the `Individual_Project_Data` tab, all 48 columns with names in snake_case. Other tabs are charts and summaries, and stay in the raw file.

## Steps
1. Read the tab.
2. Rename columns to snake_case.
3. Drop rows that are entirely empty (none were).

**Rows:** in 2,005, out 2,005.

## Georgia and Southeast
- **Georgia:** 66 projects, 5,249 MW-AC, in service 2013-2025. 37 have a value in a PPA column.
- **Southeast (non-ISO) region:** 414 projects, 24,278 MW-AC: FL 182, NC 69, GA 66, SC 55, TN 21, AL 11, MS 7, KY 3.

## Checks
- **Publisher:** byte-identical to LBNL's copy.
- **Project count:** 1,989 PV rows match LBNL's "1,989 solar projects." The other 16 rows are CSP.
- **Against EIA (panel `cap_solar_mw`, 2025):** GA 0.97, TX 1.04, CA 0.95, FL 1.00, NC 0.60. LBNL covers projects larger than 5 MW-AC, and small projects are a likely reason for NC, but I didn't test that.

## Quirks
- `eia_id`: 3 blank, 2 duplicated, 10 ending in `ret`. Don't use it as a unique key without checking.
- Capacity is the project's current record by in-service year, not a state-year stock.
- 48 states, not 50.

**Rating: green.**

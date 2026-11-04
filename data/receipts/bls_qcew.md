# Receipt: BLS QCEW — NAICS 518210, 5415, 10

## Source

Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW), Annual Averages.
URL pattern: `https://data.bls.gov/cew/data/api/{year}/a/industry/{naics_code}.csv`

## Raw Files

| File pattern | Count | Approx. size each | Downloaded |
|---|---|---|---|
| `data/raw/bls/qcew_{year}_518210.csv` | 12 (2014–2025) | 30–60 KB | 2026-11-01 |
| `data/raw/bls/qcew_{year}_5415.csv` | 12 (2014–2025) | 50–90 KB | 2026-11-01 |
| `data/raw/bls/qcew_{year}_10.csv` | 12 (2014–2025) | 200–400 KB | 2026-11-01 |

36 files total. Script: `download_all.py`.

## NAICS Codes

| Code | Description | Role |
|---|---|---|
| 518210 | Computing Infrastructure Providers, Data Processing, Web Hosting | Data-center / AI compute employment proxy |
| 5415 | Computer Systems Design and Related Services | Broader tech employment |
| 10 | Total, All Industries | State total employment denominator |

## Filters Applied

Each raw file contains county, MSA, state, and national rows. Keep only:

- **518210**: `area_fips` ends in `'000'` AND `own_code = 5` AND `agglvl_code = 58`
- **5415**: `area_fips` ends in `'000'` AND `own_code = 5` AND `agglvl_code = 56`
- **10 (total)**: `area_fips` ends in `'000'` AND `own_code = 0` AND `agglvl_code = 50`

`area_fips` ending in `'000'` selects the statewide row (e.g., `'04000'` = Arizona).

## Government 518210 rows (corrected 2026-11-04)

State-level government rows exist in every file: own_code 1 (federal), 2 (state), 3 (local), agglvl 58. They are left out of the main AI measure by team decision. `build_ai_allown.py` writes `data/ai_allown_518210.csv` for the labeled check and `logs/2026-11-04/gov_518210_shares.csv`. Suppressed government rows show 0 jobs and can't be recovered, so all-ownership counts are lower bounds.

## Key Column

`annual_avg_emplvl` — annual average employment level (full- and part-time jobs, covered by UI).

## Suppression Handling

When `disclosure_code = 'N'`, the cell is suppressed to protect employer confidentiality.
Suppressed cells are set to `NA` before any computation.

**Known quirk:** AK, ND, SD, and WY are suppressed for NAICS 518210 in 2025. These four states
carry `NA` for `dc_jobs` in the 2025 panel row. They are not dropped; the suppression is noted in
the variable metadata.

## Transformations

1. Read all 36 CSVs, parse `area_fips` as string (zero-pad to 5 chars).
2. Map `area_fips` state prefix to USPS abbreviation via a Census FIPS lookup table.
3. Apply filters above; verify exactly 51 rows remain per year-code file (50 states + DC).
4. Replace suppressed cells (`disclosure_code = 'N'`) with `NA`.
5. Merge 518210, 5415, and 10 by state and year.
6. Compute derived columns (see below).

## Rows In / Out

- Input rows per file: varies by year, roughly 4,000–8,000 (all geographies and ownership types).
- After state-level filter: 51 rows per file × 36 files = 1,836 rows total before reshape.
- After merge and pivot to state-year: 561 rows (51 states × 11 years, 2015–2025; 2014 used
  only as lag if needed).

## Output Columns

| Column | Definition |
|---|---|
| `dc_jobs` | `annual_avg_emplvl` from NAICS 518210 |
| `tech5415_jobs` | `annual_avg_emplvl` from NAICS 5415 |
| `total_jobs` | `annual_avg_emplvl` from industry 10 |
| `ai_dc_per1000` | `dc_jobs / total_jobs * 1000` |
| `tech_share` | `tech5415_jobs / total_jobs` |

## Script

`scripts/build_panel.py` (BLS section), called after `download_all.py` fetches the raw CSVs.

# Receipt: BEA State GDP and State Personal Income

## Source

U.S. Bureau of Economic Analysis, Regional Data — Interactive Data Application.
- SAGDP (State Annual GDP): `https://apps.bea.gov/regional/zip/SAGDP.zip`
- SAINC (State Annual Personal Income and Employment): `https://apps.bea.gov/regional/zip/SAINC.zip`

## Raw Files

| File | Contents | Approx. size | Downloaded |
|---|---|---|---|
| `data/raw/bea/SAGDP.zip` | ZIP of ~800 CSVs covering SAGDP series | ~120 MB | 2026-11-01 |
| `data/raw/bea/sagdp/*.csv` | Extracted CSVs, one per table-state combination | — | extracted |
| `data/raw/bea/SAINC.zip` | ZIP of ~787 CSVs covering SAINC series | ~80 MB | 2026-11-01 |
| `data/raw/bea/sainc/*.csv` | Extracted CSVs | — | extracted |

~1,587 CSVs total. Script: `download_all.py`.

## Coverage

- SAGDP: 1997–2025 (nominal and real GDP).
- SAINC: 1929–2025 (population and personal income go back further than GDP).

## Tables Used

| Table | Line | Variable | Units |
|---|---|---|---|
| SAGDP2 | 1 | Nominal GDP | Millions of current USD |
| SAGDP2 | 4 | Farm GDP (nominal) | Millions of current USD |
| SAGDP2 | 12 | Manufacturing GDP (nominal) | Millions of current USD |
| SAGDP9 | 1 | Real GDP (chained 2017 dollars) | Millions of 2017 USD |
| SAINC1 | 2 | Population | Persons |
| SAINC5 | 10 | Earnings, Agriculture | Millions of current USD |
| SAINC5 | 70 | Total earnings | Millions of current USD |

## Filters Applied

- Keep rows where `GeoFIPS` ends in `'000'` (e.g., `'01000'` = Alabama state total).
  This drops county, metro, and multi-state region rows.
- Drop rows where `Description` contains `(D)` (BEA suppressed cell) — set to NA.
- Drop Puerto Rico and other territories; keep 50 states + DC.

## Key Transformations

1. **Reshape:** Each CSV is wide (years as columns). Melt to long format (GeoName, year, value).
2. **Real GDP per capita:** `gdp_real_pc = gdp_real_musd2017 * 1e6 / population`;
   `ln_gdp_pc = log(gdp_real_pc)`.
3. **Manufacturing share:** `manuf_share = gdp_manuf_musd / gdp_nom_musd`.
4. **Population growth:** `pop_growth = (pop_t - pop_{t-1}) / pop_{t-1}`.
5. **Earnings agriculture share:** `ln_ea = log(earnings_ag_musd / total_earnings_musd)` — used
   as an instrument or control for agricultural energy use.
6. **Deflator:** Nominal manufacturing and farm GDP are kept in current USD. When a real series
   is needed, the SAGDP9 implicit price deflator is applied.

## Rows In / Out

- Input: ~1,587 CSVs × ~60 rows each (states + territories + regions × some years per CSV).
- After state filter and melt: approximately 3,000–5,000 rows per table-variable.
- After merge to panel: 561 rows (51 states × 11 years, 2015–2025).

## Known Quirks

- BEA revises historical data annually. The 2026-11-01 download may differ from the
  Oct 30 reference build by small amounts for 2024 and 2025 (advance estimates).
- `GeoFIPS` is stored as a string with leading spaces in some CSVs — strip whitespace before
  filtering.
- DC's SAGDP2 manufacturing line is near-zero; `manuf_share` for DC should be treated as
  unreliable.

## Output Columns

`gdp_nom_musd`, `gdp_real_musd2017`, `gdp_manuf_musd`, `population`, `ln_gdp_pc`,
`manuf_share`, `pop_growth`, `ln_ea`

## Script

`scripts/build_panel.py` (BEA section), after `download_all.py`.

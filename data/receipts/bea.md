# Receipt: BEA State GDP and State Personal Income

## Source

U.S. Bureau of Economic Analysis, Regional Data — Interactive Data Application.
- SAGDP (State Annual GDP): `https://apps.bea.gov/regional/zip/SAGDP.zip`
- SAINC (State Annual Personal Income and Employment): `https://apps.bea.gov/regional/zip/SAINC.zip`

## Raw Files

| File | Contents | Approx. size | Downloaded |
|---|---|---|---|
| `data/raw/bea/SAGDP.zip` | ZIP of ~800 CSVs covering SAGDP series | 10.4 MB | 2026-11-01 |
| `data/raw/bea/sagdp/*.csv` | Extracted CSVs, one per table-state combination | — | extracted |
| `data/raw/bea/SAINC.zip` | ZIP of ~787 CSVs covering SAINC series | 17.6 MB | 2026-11-01 |
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

## Filters Applied

- Keep rows where `GeoFIPS` ends in `'000'` (e.g., `'01000'` = Alabama state total).
  This drops county, metro, and multi-state region rows.
- Non-numeric values become NA through `pd.to_numeric(errors='coerce')`. There's no separate `(D)` step.
- Drop Puerto Rico and other territories; keep 50 states + DC.

## Key Transformations

1. **Reshape:** Each CSV is wide (years as columns). Melt to long format (GeoName, year, value).
2. **Real GDP per capita:** `gdp_real_pc = gdp_real_musd2017 * 1e6 / population`;
   `ln_gdp_pc = log(gdp_real_pc)`.
3. **Manufacturing share:** `manuf_share = gdp_manuf_musd / gdp_nom_musd`.
4. **Population growth:** `pop_growth = (pop_t - pop_{t-1}) / pop_{t-1}`.
5. **Economic density (H2b mediator):** `ea_nonfarm_gdp_per_sqmi = (gdp_nom_musd - gdp_farm_musd) * 1e6 / land_sqmi`;
   `ln_ea = log(ea_nonfarm_gdp_per_sqmi)`. Log nonfarm nominal GDP per square mile (`build_panel.py` lines 164-165).
   SAINC5 isn't used.
6. **Deflator:** none is applied. Nominal manufacturing and farm GDP stay in current USD, and real GDP is read directly from SAGDP9.

**Corrected 2026-11-04:** an earlier version defined `ln_ea` as a log agricultural earnings share from SAINC5. No code ever did that.

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

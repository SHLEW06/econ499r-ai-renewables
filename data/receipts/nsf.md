# Receipt: NSF state R&D (National Patterns Table 10)

**Source:** National Center for Science and Engineering Statistics, *National Patterns of R&D Resources*, Table 10, "U.S. R&D expenditures, by state, performer, and source of funds." Millions of current dollars.
**Link pattern:** https://ncses.nsf.gov/pubs/nsf26313/assets/data-tables/tables/nsf26313-tab010.xlsx
**How:** `download_nsf_tab10.py`, 2026-11-04.

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/nsf/nsf20307-tab010.xlsx` | 19,194 | `3ba1449e34c4cac1a984eb799919806284a34f439bfce7d915665e1f41b1d101` |
| `data/raw/nsf/nsf21325-tab010.xlsx` | 19,315 | `6f3c82cc32f0e4e7eade24db6b3a36b73a3152b7fb444c97f3b4c24b41aa3d38` |
| `data/raw/nsf/nsf22320-tab010.xlsx` | 19,473 | `1ecece3a4a57ad2f31e8567d2bbda3f19e69df371606f57d7d76b591cc5b9b90` |
| `data/raw/nsf/nsf23321-tab010.xlsx` | 19,572 | `b8ed186008b5383c336f3bdc0b65ff195a33f7dccd8d3cef96a0d7a0e632e46e` |
| `data/raw/nsf/nsf24318-tab010.xlsx` | 19,636 | `c851b4cd707500898976a3711f0f75b0e65747afaae7b7d039c917d5ed049cd5` |
| `data/raw/nsf/nsf25326-tab010.xlsx` | 19,483 | `1650577b600f76cb24319129c6afdda8fe07479b7d37f64d73eb7147554ecc29` |
| `data/raw/nsf/nsf26313-tab010.xlsx` | 19,540 | `f974c49a24c960690d1f8c4bb3007bf58867363657825312c956c9d564cef6e3` |
| `data/raw/nsf/nsf27300-tab010.xlsx` | 23,029 | `1d39197718cb22193c70dfd38313c23e5e4a10e0760d23d9f538eb1aa3810695` |

**`nsf27300-tab010.xlsx` is rated red and marked not used.** It came from the team, and is Table 10 of a different publication: 2024 business R&D by industry and company size, with no states. It's kept as you directed.

## What was kept
`data/nsf_state_rd.csv`: 357 rows, 51 areas x 2017-2023: total R&D, performer columns, NSF's GDP, published R&D intensity, edition and `published_not_numeric`.

| Year | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|
| Edition | nsf20307 | nsf21325 | nsf22320 | nsf23321 | nsf24318 | nsf25326 | nsf26313 |

## Steps
1. Check each file's title says "by state" and the right year; stop if not.
2. Map columns by layout, because they shift in 2021: rank and total swap, and a spacer column goes away.
3. Match state names, allowing a trailing footnote letter ("West Virginiaj"). Stop unless there are 51.
4. Non-numeric cells become NA, with the published text kept in `published_not_numeric`.

**Rows:** 62 rows per sheet, including headers, U.S. rows and Puerto Rico; out 51 per year, 357 total.

## Checks
- **Published values:** 2023 NY 48,071, NJ 27,882 and NH 4,631 match NSF's PDF of the table.
- **Totals:** the 51 areas sum to the published States total within 4 ($M) each year (rounding).
- **Intensity:** published intensity equals R&D / NSF GDP within 0.006 points.
- **Non-numeric:** 58 state-years have at least one, all in `rd_nonprofit_musd` or `rd_state_internal_musd` ("*" under $0.5M, "D" suppressed). `rd_total_musd` and intensity have none.

## Caveats
- **No revisions:** each year comes from its own edition. No single NSF table gives a consistent 2017-2023 state series.
- **GDP vintage:** NSF's GDP is 0.91 to 1.04 times the panel's nominal GDP. For the moderator, prefer `rd_total_musd` / panel `gdp_nom_musd`, so one GDP vintage is used throughout.
- **Large swings:** WY 219, 157, 792, 1,169, 238, 252, 237; AK 2018 -74%. These are as published, and likely reflect sparse survey data in small states.
- **Mixed years:** business R&D is calendar year and other performers fiscal year, per NSF.

**Rating: yellow.** NSF's 2024 file: **red**.

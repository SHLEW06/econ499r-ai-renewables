# Receipt: ACS broadband (S2801)

**Source:** U.S. Census Bureau, American Community Survey 1-year estimates, table S2801.
**Link:** https://api.census.gov/data/2024/acs/acs1/subject (same pattern by year)
**How:** `download_acs_broadband.py .env data/raw/acs data/acs_broadband.csv logs/2026-11-04/acs_spot_check.csv`, 2026-11-04.
**Key handling:** read only from `.env`, sent as a request parameter, scrubbed from error text. A search of the outputs, logs and scripts found no copy of it. API responses in `data/raw/acs/` don't contain it.

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/acs/s2801_2015.json` | 3,054 | `c92a6dc3e64372c80b4cb035c42f6f439153ad75ba781f21ab7a42b940685870` |
| `data/raw/acs/s2801_2016.json` | 3,054 | `738e494cece3c3b9d50f4d6ac2e0d775e0bb367ee8c8367f3c126ae179428243` |
| `data/raw/acs/s2801_2017.json` | 3,055 | `b2e680ca43bfc0c31e572c0a79326ddd678b4a80d56f7784506229c93b1056dd` |
| `data/raw/acs/s2801_2018.json` | 3,055 | `2568067102b7ab7a6e59b7d43ca9324872c0ec84cd6310d009d122f1165b17d7` |
| `data/raw/acs/s2801_2019.json` | 3,056 | `21b32516ab509d609580ecdd46d6550d270bdb5f50fd12400375610dc8d9e15b` |
| `data/raw/acs/s2801_2021.json` | 3,061 | `4663f7fea786165109e4ba8715def1ec3ee966c245bdf8f6ed96582fb00ae023` |
| `data/raw/acs/s2801_2022.json` | 3,063 | `0753b74f606a77a67e7ab31cbfc219e6c0be6d832d841829ac33e8d6c22810ec` |
| `data/raw/acs/s2801_2023.json` | 3,064 | `89f9f9563bd5b8a5377b2e73b2797eeb790f8c08700aff8d20c7447b95348121` |
| `data/raw/acs/s2801_2024.json` | 3,064 | `96043315a28d7f3af435d5b058656165894f9dfbcee1dd63f64999263659093e` |
| `data/raw/acs/s2801_variable_codes.csv` | 1,270 | `273711ae3cb51766318558181040b66244a3ecb74d9d40347c4a8c79731c3b0c` |

## Variable by year
| Year | Code | Census label ends with |
|---|---|---|
| 2015 | `S2801_C02_012E` | With broadband subscription |
| 2016-2019, 2021-2024 | `S2801_C02_014E` | Broadband of any type |
| 2020 | none | No 1-year release |

**In 2015, `S2801_C02_014E` means mobile broadband.** The link in `data/data_links.md` would give the wrong series for that year. The script picks the code from the Census label each year.

## What was kept
`data/acs_broadband.csv`: state, year, `broadband_pct`, `broadband_pct_moe`, `broadband_households`, `total_households`, `census_var`, `note`.

## Steps
1. Read each year's S2801 labels from the Census API and pick the code.
2. Pull all states; drop Puerto Rico.
3. Save each response to `data/raw/acs/`.
4. Add 2020 as NA rows with the reason in `note`.

**Rows:** 510 = 51 x 10 (459 with values, 51 NA for 2020).

## Checks
- **Against table B28002:** 9 of 9 cells match to 0.1 (GA, VA, WY in 2015, 2019, 2024), using (with a subscription - dial-up only) / total. See `logs/2026-11-04/acs_spot_check.csv`.
- **Mean by year:** 76.2, 80.8, 82.8, 84.4, 85.8, NA, 89.6, 90.5, 91.6, 92.7.

## Caveats
- **Stretch goal B1 uses 2016-2024, without 2015 and without 2020 (team decision, 2026-11-04).** The 2015 rows stay in the table but aren't used.
- **2015 isn't comparable.** Census revised the computer and internet questions in 2016 and [urges caution comparing across those years](https://www.census.gov/programs-surveys/acs/technical-documentation/user-notes/2017-03.html). The mean rises 4.6 points in 2016, against 2 or less a year after.
- **2020 is missing:** there's no 1-year release.
- **Household subscriptions, not availability.** Small-state estimates carry larger margins of error.

**Rating: yellow.**

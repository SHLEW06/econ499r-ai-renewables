# Receipt: national and state drivers (prompt 09, section 4)

**Status: final, 2026-11-07 (interim version superseded the same day).** Outputs: `data/extend_drivers_national.csv` (2015-2025), `data/extend_drivers_state.csv` (50 states). Script: `python3 -I econ499r_starter/scripts/build_drivers_tables.py data/raw data logs/2026-11-07` (log `logs/2026-11-07/drivers_build.log`). Downloads: `python3 -I econ499r_starter/scripts/download_extend_sources.py data/raw logs/2026-11-07/extend_downloads.csv drivers`, retrieved 2026-11-07. Registered in `EXPERIMENTS.md` section 14.4 (deviations X3, X4).

## Downloaded
| File (`data/raw/`) | URL | Bytes | sha256 |
|---|---|---:|---|
| `crs/PLAW-117publ169.pdf` | https://www.govinfo.gov/content/pkg/PLAW-117publ169/pdf/PLAW-117publ169.pdf | 876,749 | `5bd9bebe719d3d1738e751fe7978ef7bf05167ed8150471f306e010185baed4f` |
| `eia/henry_hub/RNGWHHDa.xls` | https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDa.xls | 34,816 | `7a3c4f947d54358792b11bed055f78659eabe671816ed819fbe373100480805a` |

## In hand, reused
- LBNL Utility-Scale Solar 2026 data file (`lbnl_solar.md`): national solar LCOE = MW-AC-weighted mean of `pv_lcoe_no_tax_credits_2025_mwh` for PV projects by commercial-operation year (83-222 projects a year).
- LBNL current RPS/CES schedule (`lbnl_rps.md`): `target_pct`.
- National AI totals: sums of 50-state private 518210 jobs (panel) and postings (`data/fang_panel.csv`).
- Resource: the prompt's fallback (EIA capacity factors) because NREL is unreachable. Rule (deviation X4): generation / (mean nameplate of y-1 and y x 8,760) in the first year y >= 2015 whose previous year had at least 10 MW. Never qualifies -> 0 (wind: AL, AR, CT, DE, FL, GA, KY, LA, NJ, SC; solar: AK, ND, NH). Ranges: wind 0.18-0.48, solar 0.07-0.33.
- Henry Hub: EIA's `.xls` is read through a temporary LibreOffice conversion to `.xlsx` (xlrd isn't installed); the raw file is untouched.

## Tax credits, by year construction begins (printed page, PDF page in brackets)
| Year | Solar ITC | Source | Wind PTC, share of full | Source |
|---|---|---|---|---|
| 2015 | 30% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 30% for solar beginning construction through 2019 | 100% | CRS R43453 (Sherlock, updated Apr. 29, 2020; data/raw/crs/CRS_R43453_2020-04-29.pdf), p. 2 [PDF p. 5]: full credit for wind beginning construction through 2016 |
| 2016 | 30% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 30% for solar beginning construction through 2019 | 100% | CRS R43453 (Sherlock, updated Apr. 29, 2020; data/raw/crs/CRS_R43453_2020-04-29.pdf), p. 2 [PDF p. 5]: full credit for wind beginning construction through 2016 |
| 2017 | 30% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 30% for solar beginning construction through 2019 | 80% | CRS R43453 (Sherlock, updated Apr. 29, 2020; data/raw/crs/CRS_R43453_2020-04-29.pdf), p. 2 [PDF p. 5]: reduced by 20% for wind beginning construction in 2017 |
| 2018 | 30% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 30% for solar beginning construction through 2019 | 60% | CRS R43453 (Sherlock, updated Apr. 29, 2020; data/raw/crs/CRS_R43453_2020-04-29.pdf), p. 2 [PDF p. 5]: reduced by 40% for 2018 |
| 2019 | 30% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 30% for solar beginning construction through 2019 | 40% | CRS R43453 (Sherlock, updated Apr. 29, 2020; data/raw/crs/CRS_R43453_2020-04-29.pdf), p. 2 [PDF p. 5]: reduced by 60% for 2019 |
| 2020 | 26% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 26% for construction beginning 2020-2022 (pre-IRA); kept by P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), 136 Stat. 1914 [PDF p. 98] for property placed in service before 2022 | 60% | CRS R43453 (Sherlock, updated Apr. 29, 2020; data/raw/crs/CRS_R43453_2020-04-29.pdf), p. 2 [PDF p. 5]: reduced by 40% for 2020 (P.L. 116-94) |
| 2021 | 26% | CRS IF10479 (updated Apr. 23, 2021; data/raw/crs/CRS_IF10479_2021-04-23.pdf), p. 1 [PDF p. 1], Table 1: 26% for construction beginning 2020-2022 (pre-IRA); kept by P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), 136 Stat. 1914 [PDF p. 98] for property placed in service before 2022 | 60% | P.L. 116-260 (data/raw/crs/PLAW-116publ260.pdf), Div. EE, sec. 131(c)(1), 134 Stat. 3052 [PDF p. 1873]: 45(b)(5)(D), the 40% reduction, extended to construction beginning before Jan. 1, 2022 |
| 2022 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf): base 6% (136 Stat. 1914 [PDF p. 98]) x 5 with wage and apprenticeship rules (136 Stat. 1919 [PDF p. 103]); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), sec. 13101(e)(2), 136 Stat. 1906 [PDF p. 90]: the 45(b)(5) phaseout applies only to wind placed in service before Jan. 1, 2022 |
| 2023 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf): base 6% (136 Stat. 1914 [PDF p. 98]) x 5 with wage and apprenticeship rules (136 Stat. 1919 [PDF p. 103]); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), sec. 13101(e)(2), 136 Stat. 1906 [PDF p. 90]: the 45(b)(5) phaseout applies only to wind placed in service before Jan. 1, 2022 |
| 2024 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf): base 6% (136 Stat. 1914 [PDF p. 98]) x 5 with wage and apprenticeship rules (136 Stat. 1919 [PDF p. 103]); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), sec. 13101(e)(2), 136 Stat. 1906 [PDF p. 90]: the 45(b)(5) phaseout applies only to wind placed in service before Jan. 1, 2022 |
| 2025 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf): base 6% (136 Stat. 1914 [PDF p. 98]) x 5 with wage and apprenticeship rules (136 Stat. 1919 [PDF p. 103]); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), sec. 13101(e)(2), 136 Stat. 1906 [PDF p. 90]: the 45(b)(5) phaseout applies only to wind placed in service before Jan. 1, 2022 |

## Wind cost
LBNL Land-Based Wind Energy Technology Data Update 2026, sheet "Wind LCOE Over Time", generation-weighted LCOE by commercial-operation year, 2025 $/MWh (receipt `lbnl_wind.md`): 2015 57.0, 2016 50.8, 2017 47.7, 2018 42.0, 2019 43.3, 2020 44.1, 2021 44.1, 2022 39.8, 2023 47.9, 2024 49.4, 2025 52.1.

## Blocked to scripts on 2026-11-07 (resolved the same day by hand downloads, except NREL)
| Source | URL | What happened | Used for |
|---|---|---|---|
| CRS R43453 (PTC) | https://crsreports.congress.gov/product/pdf/R/R43453 | HTTP 403 to scripted requests | PTC 2015-2021 values with page cites |
| CRS IF10479 (ITC) | https://crsreports.congress.gov/product/pdf/IF/IF10479 | HTTP 403 | Check of the ITC values coded from P.L. 117-169 |
| LBNL Land-Based Wind Market Report data file | https://emp.lbl.gov/wind-technologies-market-report | HTTP 403 | Wind cost series |
| NREL state solar and wind resource | nrel.gov | Host doesn't resolve from this machine's sandbox | Resource; the EIA fallback is used, as the prompt allows |

No workaround was attempted: a retry with a browser user-agent was refused as bot-check circumvention.

**Rating: green** for the national drivers; resource uses the EIA fallback because NREL was unreachable (deviation X4).

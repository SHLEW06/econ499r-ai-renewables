# Receipt: national and state drivers (prompt 09, section 4)

**Status: interim, 2026-11-07.** Outputs: `data/extend_drivers_national.csv` (2015-2025), `data/extend_drivers_state.csv` (50 states). Script: `python3 -I econ499r_starter/scripts/build_drivers_tables.py data/raw data logs/2026-11-07` (log `logs/2026-11-07/drivers_build.log`). Downloads: `python3 -I econ499r_starter/scripts/download_extend_sources.py data/raw logs/2026-11-07/extend_downloads.csv drivers`, retrieved 2026-11-07. Registered in `EXPERIMENTS.md` section 14.4 (deviations X3, X4).

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

## Tax credits, by year construction begins
| Year | Solar ITC | Source | Wind PTC, share of full | Source |
|---|---|---|---|---|
| 2015 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): sec. 13102(d)(1) strikes the prior-law '30 percent' base for solar; the 2020-2021 phase-down applies from 2020 |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2016 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): sec. 13102(d)(1) strikes the prior-law '30 percent' base for solar; the 2020-2021 phase-down applies from 2020 |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2017 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): sec. 13102(d)(1) strikes the prior-law '30 percent' base for solar; the 2020-2021 phase-down applies from 2020 |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2018 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): sec. 13102(d)(1) strikes the prior-law '30 percent' base for solar; the 2020-2021 phase-down applies from 2020 |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2019 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): sec. 13102(d)(1) strikes the prior-law '30 percent' base for solar; the 2020-2021 phase-down applies from 2020 |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2020 | 26% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): new 48(a)(6), construction begins after Dec. 31, 2019 and placed in service before Jan. 1, 2022: 26 percent |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2021 | 26% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914): new 48(a)(6), construction begins after Dec. 31, 2019 and placed in service before Jan. 1, 2022: 26 percent |  | pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07) |
| 2022 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914) base 6 percent x 5 for projects meeting wage and apprenticeship rules, PDF p. 103 (136 Stat. 1919); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 90 (136 Stat. 1906): sec. 13101(e)(2) limits the 45(b)(5) phaseout to wind placed in service before Jan. 1, 2022 |
| 2023 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914) base 6 percent x 5 for projects meeting wage and apprenticeship rules, PDF p. 103 (136 Stat. 1919); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 90 (136 Stat. 1906): sec. 13101(e)(2) limits the 45(b)(5) phaseout to wind placed in service before Jan. 1, 2022 |
| 2024 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914) base 6 percent x 5 for projects meeting wage and apprenticeship rules, PDF p. 103 (136 Stat. 1919); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 90 (136 Stat. 1906): sec. 13101(e)(2) limits the 45(b)(5) phaseout to wind placed in service before Jan. 1, 2022 |
| 2025 | 30% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 98 (136 Stat. 1914) base 6 percent x 5 for projects meeting wage and apprenticeship rules, PDF p. 103 (136 Stat. 1919); placed in service after Dec. 31, 2021 | 100% | P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf), PDF p. 90 (136 Stat. 1906): sec. 13101(e)(2) limits the 45(b)(5) phaseout to wind placed in service before Jan. 1, 2022 |

## Blocked on 2026-11-07 (need a browser download into `data/raw/`)
| Source | URL | What happened | Used for |
|---|---|---|---|
| CRS R43453 (PTC) | https://crsreports.congress.gov/product/pdf/R/R43453 | HTTP 403 to scripted requests | PTC 2015-2021 values with page cites |
| CRS IF10479 (ITC) | https://crsreports.congress.gov/product/pdf/IF/IF10479 | HTTP 403 | Check of the ITC values coded from P.L. 117-169 |
| LBNL Land-Based Wind Market Report data file | https://emp.lbl.gov/wind-technologies-market-report | HTTP 403 | Wind cost series |
| NREL state solar and wind resource | nrel.gov | Host doesn't resolve from this machine's sandbox | Resource; the EIA fallback is used, as the prompt allows |

No workaround was attempted: a retry with a browser user-agent was refused as bot-check circumvention.

**Rating: yellow** (interim; two drivers missing).

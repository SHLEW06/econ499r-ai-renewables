# Receipt: NOAA heating and cooling degree days

**Status: done, 2026-11-04. Used for one check only: `ln_ec` with HDD and CDD (`EXPERIMENTS.md` section 0, item 31). Not in the panel.** NCEI timed out on every host earlier on Nov 4, and the team first decided not to substitute another source. NCEI answered later the same day, and the team asked for the download. No CPC file is used.

**Source:** NOAA National Centers for Environmental Information, Climate at a Glance, statewide time series, January-December totals, 2015-2025. 48 contiguous states; AK and HI have no degree days in these files, and DC isn't a state in them.

- Landing page: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series
- Example (9 = Georgia; swap `hdd` and `cdd`): https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/9/hdd/12/12/2015-2025.csv
- Monthly check files and format: https://www.ncei.noaa.gov/monitoring-content/data/us/climdiv/monthly/current/

**Script:** `python3 econ499r_starter/scripts/download_noaa_degree_days.py data/raw/noaa data/noaa_degree_days.csv`. Output: `state, year, cdd, hdd`, 528 rows, no blanks.

**What the numbers are:** base 65F. NOAA's readme says state degree days use population weights from the 2010 Census, and that these values "may be different from" official degree-day publications.

## Checks
- **Two NCEI routes:** all 528 state-years match exactly on both measures between the state time series and `climdiv-hddcst` and `climdiv-cddcst` summed over 12 months.
- **By eye, 2024:** FL 552 HDD and 4,006 CDD; GA 2,388 and 1,991; ME 6,846 and 359.

**Rating: green.**

## Raw files (`data/raw/noaa/`)
96 state files, `XX_hdd_2015_2025.csv` and `XX_cdd_2015_2025.csv`; hashes are in `data/FILE_INVENTORY.csv`. Plus:

| File | Bytes | sha256 |
|---|---:|---|
| `climdiv-hddcst-v1.0.0-20261006` | 812,028 | `321646a5ab826f827c41797b5eb9e3352547bbb04c5ed6a826caa0a61b39da9b` |
| `climdiv-cddcst-v1.0.0-20261006` | 812,028 | `7b0261158383506d684e4893af619f3ec9c6767760b0fa695f164aaa74228faa` |
| `state-readme.txt` | 18,069 | `b77187cdddfa6ef87c5a5c8eeee2321cbda85e03c0aa6318e547c05236428416` |

## Alternative, rejected
NOAA's Climate Prediction Center has a monthly state degree-day archive. It's a different product, and the team decided not to use it.

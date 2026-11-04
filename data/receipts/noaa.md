# Receipt: NOAA heating and cooling degree days

**Status: NOT DONE (team decision, 2026-11-04). There is no file and no table.**

**Reason:** NCEI could not be reached by script on 2026-11-04, and the team chose not to substitute another source. Degree days are an optional weather control, not part of the memo's core model.

**Source:** NOAA NCEI, Climate at a Glance, statewide time series.
**Attempts on 2026-11-04:** `www.ncei.noaa.gov`, `ftp.ncei.noaa.gov` and `www1.ncdc.noaa.gov` all timed out on connecting, across several tries (the longest waited 180 seconds). Other sites responded normally from the same machine, and `data/raw/noaa/` was not left behind.

## Script
`econ499r_starter/scripts/download_noaa_degree_days.py data/raw/noaa data/noaa_degree_days.csv` stops without writing a table if NCEI can't be reached. **Its parser hasn't run on real NCEI output.** Check the first files by eye on the first run.

## Links to download by hand (48 states; code 9 = Georgia; swap `hdd` and `cdd`)
https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/9/hdd/12/12/2015-2025.csv

## Alternative, rejected
NOAA's Climate Prediction Center has a monthly state degree-day archive (https://ftp.cpc.ncep.noaa.gov/htdocs/products/analysis_monitoring/cdus/degree_days/archives/). It's a different product. The team decided not to substitute it.

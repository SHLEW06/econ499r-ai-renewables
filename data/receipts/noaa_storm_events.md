# Receipt: NOAA Storm Events, extreme heat and cold counts

**Status: done, 2026-11-07. Used for Fang's extreme-weather split (prompt 08, section 1.3; `EXPERIMENTS.md` section 9b, F22).** Output: `data/storm_events_state.csv` (51 states including DC, 2015-2024, 510 rows, zeros where no events). Script: `econ499r_starter/scripts/build_finalize_tables.py`. Downloads: `download_finalize_sources.py`, retrieved 2026-11-07.

**Source:** NOAA National Centers for Environmental Information, Storm Events Database, bulk CSV "details" files. https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/

**Counting rule:** one count per event record (EVENT_ID) with EVENT_TYPE in {Excessive Heat, Heat, Extreme Cold/Wind Chill, Cold/Wind Chill}, by STATE and the year of BEGIN_YEARMONTH. Records are reported by forecast zone, so one heat wave across many zones gives many records. Check: distinct EPISODE_ID. Frost/Freeze, Winter Storm and similar types are left out because Fang names only hot and cold weather occurrences (PDF p. 5). Marine areas, Puerto Rico and other territories are dropped.

**Fang split:** each state's 2018-2021 average count against the mean of the 51 averages (Fang's rule), plus the median. 2018-2021 state means: mean 66.5, median 34.5. 19 states are above the mean, which gives 76 state-years against Fang's 104. FL, HI, NH and RI have no qualifying records in 2018-2021.

| File | Bytes | sha256 |
|---|---:|---|
| StormEvents_details-ftp_v1.0_d2015_c20260323.csv.gz | 10,041,550 | `c4a5a24b8c69ad2b6b867790ce298f5b642a60516c9fce5550a8d2f67cd7bf2e` |
| StormEvents_details-ftp_v1.0_d2016_c20260323.csv.gz | 9,065,715 | `d8e1389897df3557e74ba36820357f6962a7c0ca922595400fe74d883f7a5036` |
| StormEvents_details-ftp_v1.0_d2017_c20260519.csv.gz | 9,340,854 | `bd3ca72b71544222cba8aa2b29eb3f0efe050d3330a0c408e208befb66881750` |
| StormEvents_details-ftp_v1.0_d2018_c20260323.csv.gz | 9,585,982 | `19702480f50cd2a8dacce5e57891feba156afb87b1ea5cbb4eaeda69d2b964a4` |
| StormEvents_details-ftp_v1.0_d2019_c20260323.csv.gz | 11,602,648 | `f5043ecc776818b0feffdf1e0fcbaf63329db0635eab1057c7b8ba00ef332e3b` |
| StormEvents_details-ftp_v1.0_d2020_c20260323.csv.gz | 10,444,606 | `895c56fd46991c4d9a135d67558dc4b447a02a2314efac0ace645135b98f9c9d` |
| StormEvents_details-ftp_v1.0_d2021_c20260323.csv.gz | 10,563,953 | `60c1daf96dbe8eafd48c80df5b70df51a0125ab95d467ee7009a646761d57715` |
| StormEvents_details-ftp_v1.0_d2022_c20260625.csv.gz | 11,817,849 | `7d6b79d0049a6edec96b061738289daddba90be26fc9afe7b0a6fd617f21452e` |
| StormEvents_details-ftp_v1.0_d2023_c20260323.csv.gz | 12,888,092 | `713784bed40d9e5a95b1d6240a654f865f3ef97703713105c7b35437270da134` |
| StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz | 12,693,243 | `2070b83eccab041b36360ab73645b9a249c3eefc5b92b5b3fc0cbba4d9fcc09c` |

**Caveat:** reporting practice differs by NWS office (for example, Florida offices rarely file Heat events), so counts compare reporting as much as weather. **Rating: yellow** (the counting rule is ours; Fang's isn't stated).

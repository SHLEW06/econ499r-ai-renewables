# Receipt: section 5 AI index ("infrastructure + talent") and add-on sources

**Status: done, 2026-11-07.** Script: `python3 -I econ499r_starter/scripts/build_ai_index.py data/raw data logs/2026-11-07` (log `logs/2026-11-07/ai_index_build.log`). Outputs: `data/ai_index_components.csv`, `data/ai_index_state.csv`, `data/ai_index_crossstate.csv`. Registered in `EXPERIMENTS.md` section 14.6 (B3, add-on A1-A5).

## Downloaded by script (retrieved 2026-11-07)
| File (`data/raw/`) | URL | Bytes | sha256 |
|---|---|---:|---|
| `census_btos/State.xlsx` | https://www.census.gov/hfp/btos/downloads/State.xlsx | 4,681,949 | `134b30bb209c7835c9faf7403255da3f2bd425a29ca4b4acfe9185805c07f272` |
| `census_btos/AI_Core_Questions.xlsx` | https://www.census.gov/hfp/btos/downloads/AI%20Core%20Questions.xlsx | 1,109,824 | `e058a098af64427b0cf0c1455435023aeb9a84142a55175d322687e61a3da3ce` |
| `census_btos/AI_Question_Wording_Updates.pdf` | https://www.census.gov/hfp/btos/downloads/AI%20Question%20Wording%20Updates.pdf | 491,343 | `91b018352b693d500258cb649b7c8b1747d5fbfb5f065eeb8969276dd1068c28` |
| `uspto_aipd/oce-aipd-2023.pdf` | https://www.uspto.gov/sites/default/files/documents/oce-aipd-2023.pdf | 1,922,389 | `5681377084dfb7978f9a9b7e2bf672b870380b8002841fe6e3ad9d6190ff0cb9` |
| `uspto_aipd/ai_model_predictions_2023.csv.zip` | https://data.uspto.gov/ui/datasets/products/files/ECOPATAI/2023_r1/ai_model_predictions.csv.zip | 818,035,211 | `38c6182750f33db17fe13ebac72fb064afdcfb47b893f12f113f527bda458d9b` |
| `aiindex/ed2026_fig_4.2.14.csv` | https://drive.google.com/uc?export=download&id=1HLzDyJ61GL50xmjsF2Bq-fyNI5inDJig | 726 | `e1262539628e13523245764d3c65a0968d381d924b2c7e6a2ea4025ae7bbcfaf` |
| `aiindex/ed2026_fig_4.2.15.csv` | https://drive.google.com/uc?export=download&id=1RT5ZLOQFFHBEo9BNi4HRrU7v4vq-H4ZJ | 696 | `e32bca0de63d9cf8c8ad795be0b89de61d2cb423dec26dd541e767aeb9cb7216` |
| `aiindex/ed2026_fig_4.2.16.csv` | https://drive.google.com/uc?export=download&id=1ZswTrGZ3t5ImPaxdo4kGcCyRZnTuo4m3 | 1,758 | `8f991781a56d5084ab0a17499bf38c7c43c588f836a6d76a230ef10a1ec6792f` |

The AIPD file comes from the USPTO Open Data Portal: the product URL returns a signed download link, which the script follows. Hand downloads: OEWS (`bls_oews.md`).

## Components (natural logs; state-years with a missing input are missing, not imputed)
- **Infrastructure** (QCEW NAICS 518210, private, state rows, non-disclosed cells missing; jobs match the panel's `dc_jobs` exactly): jobs per 1,000 workers; establishments per million residents; total 518210 wages per worker in the state.
- **Talent:** AI postings per 1,000 workers (Stanford AI Index, by edition, `ai_index.md`). OEWS computer and information research scientists per 1,000 workers: SOC 15-1111 (2015-2018), 15-1221 (2019-2024), same title. `**` and `#` are missing. Mapping and drops: `logs/2026-11-07/ai_index_oews_mapping.csv`. Software developers and data scientists were dropped because no consistent 2018-2023 series exists (2018 vs 2019-2020 vs 2021+ codes differ in scope), and the rule is no splicing.
- **Innovation: dropped.** USPTO AIPD 2023 (`uspto_aipd/`) is downloaded but **unused**: inventor locations (PatentsView) couldn't be obtained (the old S3 links answer Access Denied, and the new USPTO portal pages are JavaScript-only). Quid investment covers one year only (below).

## Coverage (states with each component; the index needs all five)
|   year |   c_jobs |   c_estab |   c_wage |   c_post |   c_rsci |   all_five |   infra_plus_rsci |
|-------:|---------:|----------:|---------:|---------:|---------:|-----------:|------------------:|
|   2015 |       50 |        50 |       50 |        0 |       33 |          0 |                33 |
|   2016 |       50 |        50 |       50 |        0 |       34 |          0 |                34 |
|   2017 |       50 |        50 |       50 |        0 |       35 |          0 |                35 |
|   2018 |       50 |        50 |       50 |       50 |       39 |         39 |                39 |
|   2019 |       50 |        50 |       50 |       50 |       39 |         39 |                39 |
|   2020 |       50 |        50 |       50 |       50 |       39 |         39 |                39 |
|   2021 |       50 |        50 |       50 |       50 |       37 |         37 |                37 |
|   2022 |       50 |        50 |       50 |       50 |       34 |         34 |                34 |
|   2023 |       50 |        50 |       50 |       50 |       38 |         38 |                38 |
|   2024 |       50 |        50 |       50 |       50 |       34 |         34 |                34 |

OEWS suppresses research scientists in 11-17 states a year, so the main index covers 43 states (226 state-years, 2018-2023).

## Diagnostics
| statistic                                  |      value |
|:-------------------------------------------|-----------:|
| N state-years (main)                       | 226        |
| states (main)                              |  43        |
| Cronbach alpha, 5 components               |   0.731618 |
| Cronbach alpha, infrastructure             |   0.7649   |
| Cronbach alpha, talent                     |   0.337015 |
| PC1 variance explained                     |   0.5375   |
| within-state SD (two-way demeaned) Index A |   0.175789 |
| within-state SD Index B                    |   0.364353 |
| within-state SD infrastructure             |   0.188165 |
| within-state SD talent                     |   0.2402   |
| N state-years (check 2015-2023)            | 328        |
| PC1 variance explained (check)             |   0.547291 |

## Cross-state checks of the 2024 index (scored with the 2018-2023 means, SDs and loadings)
- **Census BTOS:** `AI_Core_Questions.xlsx`, sheet "State Estimates", Q7 ("In the last two weeks, did this business use Artificial Intelligence (AI) in producing goods or services?"), share answering Yes, averaged over the 26 two-week periods of 2024. Asked from September 2023. Census later reworded the question ("Super Intelligence (formerly ... AI)"; `State.xlsx` carries the new wording and is blank for 2024; see `AI_Question_Wording_Updates.pdf`). Multi-state firms are excluded from state estimates.
- **Epoch:** current IT MW, 29 states (context only).
- **Quid 2025 private AI investment** (AI Index 2026, Fig. 4.2.15 data; `aiindex/ed2026_fig_4.2.15.csv`): one year only, so per the add-on it's a grouping and cross-state check, not a regressor or index dimension. Missing (not zero) for AR, OK, SD and WV.

| check                                     |   N_states |   pearson_index_a_2024 |   spearman_index_a_2024 |   spearman_index_b_2024 |
|:------------------------------------------|-----------:|-----------------------:|------------------------:|------------------------:|
| BTOS 2024 average share of firms using AI |         30 |                  0.551 |                   0.525 |                   0.54  |
| Epoch current IT MW                       |         22 |                  0.062 |                  -0.023 |                  -0.01  |
| Quid 2025 private AI investment           |         32 |                  0.232 |                   0.485 |                   0.555 |

## Add-on groupings (cut points fixed in EXPERIMENTS.md before results)
2025 investment: >= $1B (11 states), $100M-$1B (17), < $100M (18), missing (4). Tertiles of 2025 investment per TWh of 2015 retail sales (cuts about $2.45M and $9.08M per TWh). Tertiles of 2015 518210 jobs per TWh (cuts 39.9 and 87.0).

## Not obtained
- **LBNL Queued Up 2026** (https://emp.lbl.gov/queues): HTTP 403 to scripted requests, so add-on A4 (queue outcome) **wasn't run**. It's listed for a hand download.
- **NREL state technical potential:** nrel.gov doesn't resolve from this machine, so land area per TWh of 2015 sales is the "room" moderator (A3), as the add-on allows.

**Rating: yellow** (no innovation dimension; talent rests on two components with alpha 0.34; research-scientist suppression drops 7 states).

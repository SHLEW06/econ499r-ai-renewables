# Receipt: AI job postings by state (Stanford AI Index)

**Source:** Stanford HAI, *AI Index Report*, 2019 and 2021-2026 editions. Underlying data: Burning Glass, then Emsi Burning Glass, then Lightcast.
**Used for:** Fang test only, as Fang's AI measure. It doesn't enter the master panel.
**How:** `econ499r_starter/scripts/download_fang_sources.py`, 2026-11-04. Sheets exported as xlsx; figure CSVs from each edition's public-data folder.

## What was kept
`data/ai_job_postings_state.csv`: 408 rows, 51 areas x 2018-2025.

| Year | Edition | Vendor | Figure | PDF page | Sum of 51 |
|---|---|---|---|---:|---:|
| 2018 | 2019 | Burning Glass | Fig. 4.1.8 shows a scatter; values from its linked sheet | 82 | 189,030 |
| 2019 | 2022 | Emsi Burning Glass | Public-data sheet, tab AI Job Postings by State; not printed in the report |  | 325,702 |
| 2020 | 2022 | Emsi Burning Glass | Public-data sheet, tab AI Job Postings by State; not printed in the report |  | 296,937 |
| 2021 | 2022 | Emsi Burning Glass | Fig. 4.1.6 | 9 | 404,074 |
| 2022 | 2023 | Lightcast | Fig. 4.1.6; share Fig. 4.1.8 (p. 11) | 10 | 795,624 |
| 2023 | 2024 | Lightcast | Fig. 4.2.7; share Fig. 4.2.9 (p. 18) | 17 | 461,225 |
| 2024 | 2025 | Lightcast | Fig. 4.2.8; share Fig. 4.2.10 (p. 17) | 16 | 658,548 |
| 2025 | 2026 | Lightcast | Fig. 4.4.10; share Fig. 4.4.11 (p. 40) | 40 | 994,372 |

| Column | Meaning |
|---|---|
| `postings` | AI job postings |
| `share_pct` | State's share of U.S. AI postings |
| `share_source` | `published` for 2022-2025; `derived: state / sum of 51` for 2018-2021, because those editions publish no such table |
| `ai_share_of_state_postings_pct` | AI's share of that state's own postings, in percent. A different measure |
| `vintage` | Break group: each edition is its own group, and 2019-2021 is the only multi-year group |
| `figure`, `page` | Where the value is. Page is the PDF page. Blank for 2019-2020, which no report prints |

`data/ai_job_postings_overlap_rows.csv` holds the rows not used in the main table: the 2019 edition's Jan-Sep 2019, and the 2021 edition's 2020.

## Which edition supplies each year, and why
- **2018:** only the 2019 edition has it, as a sheet linked from the report. Its chart (Fig. 4.1.8, p. 82) has no numbers.
- **2019:** the 2022 edition. The 2019 edition's 2019 runs only through September: its note reads "data up until September of 2019."
- **2020:** the 2022 edition, to keep 2019-2021 on one vintage. The 2021 edition's values are in the overlap file.
- **2021:** the 2022 edition's map, matched exactly to its sheet.

## Method changes the editions report
- **2021 edition:** "Burning Glass updated the data coverage in 2020 with more job sites; as a result, the numbers in this report should not be directly compared with data in" previous reports.
- **2023 edition:** "In 2022, Lightcast slightly changed their methodology... some of the numbers in this chart do not completely align with those featured in last year's report."
- **2024 edition:** "In 2023, Lightcast slightly changed its methodology... Lightcast also updated its taxonomy of AI-related skills."
- **2026 edition:** "Historical posting counts may differ from previously published versions due to data updates and revisions."

**In the postings extension (2019-2024), almost every year comes from a different edition. So a state's year-to-year change mixes real change with method changes.** Year effects remove shifts that hit all states proportionally. The share-of-national row can't test this: once year effects are in, it equals the postings row by construction (-0.0475 vs -0.0479). Anything uneven stays in as noise, and the edition overlap and share-change tables are the evidence on that. Data-center jobs (BLS, one consistent series) remain the more reliable extension measure.

## Steps
1. Parse each PDF map using word coordinates: each state label is paired with the number just below it, inside that map's part of the page. Stop unless there are 51.
2. Read the sheets. Drop territories to leave 51 areas.
3. Set `share_pct` as published where available, otherwise state / sum of 51.

**Rows:** sheets have 51 to 57 areas per year; PDFs 51. Output 51 per year.

## Checks (`logs/2026-11-04/ai_postings_checks.csv`)
- **51 rows per year:** pass.
- **States sum to the national total:** no edition prints a national count. For 2022-2025, the total implied by published shares is within 0.05% of the sum. For 2018-2021 this can't be tested.
- **PDF vs public CSV:** exact on all 51 states for 2022, 2023, 2024 and 2025. The 2021 map is exact against its sheet. Published shares match within rounding.
- **3 states per year against report text:**
  - 2021, 2022, 2023, 2024: the top three values appear in the report; in each year at least two are printed beside the state's name.
  - 2025: no sentence prints them, so this rests on the exact CSV match.
  - 2020: CA, TX, NY in the 2021 edition's text match that edition's sheet exactly. The 2022 edition's values used here are 0.5-1.5% lower.
  - 2018: the 2019 edition's text gives 2018 plus Jan-Sep 2019 combined: CA over 93,000, NY about 30,000, TX over 24,000. The sheet gives 93,785, 29,889 and 24,215.
  - 2019: no report prints the full-year counts. CA, NY and TX shares are within 0.5 points of Lightcast's published series.

## Edition overlap check
Shares are each state's share of the 51-state total, so levels don't matter. Only these years appear in two editions for all states.

| Year | Edition A | Edition B | Pearson r, shares | Rank correlation | SD of ln(share ratio) | Median state gap |
|---|---|---|---:|---:|---:|---:|
| 2019 | 2019 edition, Jan-Sep | 2022 edition, full year | 0.9978 | 0.9954 | 0.162 | 14.8% |
| 2020 | 2021 edition | 2022 edition | 1.0000 | 0.9996 | 0.012 | 0.7% |
| 2021 | 2022 edition, PDF map | 2022 edition, sheet | 1.0000 | 1.0000 | 0.000 | 0.0% |

**Reading it:** the state pattern is very similar across editions, but high correlations are driven by the ordering of large and small states, so they don't clear within-state noise. For 2019 the median state's share still differs by 14.8% (SD of the log ratio 0.162), part of which is Jan-Sep against the full year. For 2020, with both full years, the median gap is 0.7%, so a one-year revision within Burning Glass is small.

**Four states, every year from 2018 (`logs/2026-11-04/ai_postings_select_states.csv`):** the 2023-2026 editions print a share history for CA, NY, TX and WA. It's the same in all four editions, within rounding. For 2022-2025 it matches this table. For 2018-2021 it's Lightcast's restated history, which differs from the Burning Glass tables used here: CA 2018 is 22.5% against 26.0%; WA 2021 is 3.9% against 4.8%. So **WA's fall from 4.8% to 3.9% in this table at 2021-2022 doesn't exist in Lightcast's own series (3.94 to 3.93).** It's a method change.

## How much state shares move each year (`logs/2026-11-04/ai_postings_share_changes.csv`)
SD across states of the year-to-year change in ln(state share).

| Step | Editions | National change | SD, postings | SD, data-center jobs |
|---|---|---:|---:|---:|
| 2018->2019 | 2019->2022 | +72% | 0.223 | 0.120 |
| 2019->2020 | 2022->2022 (same) | -9% | 0.174 | 0.129 |
| 2020->2021 | 2022->2022 (same) | +36% | 0.217 | 0.096 |
| 2021->2022 | 2022->2023 | +97% | 0.266 | 0.104 |
| 2022->2023 | 2023->2024 | -42% | 0.249 | 0.083 |
| 2023->2024 | 2024->2025 | +43% | 0.200 | 0.062 |
| 2024->2025 | 2025->2026 | +51% | 0.195 | 0.077 |

Postings shares move 1.3 to 3.2 times as much as data-center jobs in every step, **including same-edition steps** (0.174 and 0.217). Steps across editions are somewhat larger on average (0.227 against 0.195). So postings are noisy at the state level for more reasons than edition changes, and small states drive the largest moves.

**Rating: yellow.**

## Raw file hashes
| File | Bytes | SHA-256 | Source |
|---|---:|---|---|
| `ai_index_2019_report.pdf` | 15,725,294 | `d7a6f5fd575415a2aaf9402f68145d2839424809de789d28a416401aef681f99` | https://hai-production.s3.amazonaws.com/files/ai_index_2019_report.pdf |
| `2021-ai-index-report_master.pdf` | 14,236,424 | `9a00d657d883b8dbdb31d497338702722358544abc10ac8804c339c7447b98a5` | https://hai-production.s3.amazonaws.com/files/2021-ai-index-report_mas |
| `2022-ai-index-report_chapter-4.pdf` | 7,470,671 | `7340b0395cc36873ab62f7620d095a1f13cfb8f80d7e259369c7178586a40daa` | https://hai-production.s3.amazonaws.com/files/2022-ai-index-report_cha |
| `hai_ai-index-report-2023_chapter_4.pdf` | 2,459,998 | `0b50b02089d2af4f8d4b9b33a1f47af7fdb96c1f8803b513c08a23ed3e405dce` | https://hai-production.s3.amazonaws.com/files/hai_ai-index-report-2023 |
| `hai_ai-index-report-2024_chapter4.pdf` | 4,165,810 | `5f914854169243fb3313f2bba70c5539a546053690d94f0a439771243c741b4c` | https://hai-production.s3.amazonaws.com/files/hai_ai-index-report-2024 |
| `hai_ai-index-report-2025_chapter4_final.pdf` | 5,303,819 | `e1daf3fc72f58f18dbf9e19872d4c29d18876c30f35af54c8312f1662aeaf0d4` | https://hai-production.s3.amazonaws.com/files/hai_ai-index-report-2025 |
| `ai_index_report_2026_chapter_4_economy.pdf` | 6,450,805 | `6654b484b0c20213ead6ed8388f3145928c2dde9bca86e16a5b7efe9a00d8269` | https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_e |
| `ed2019_ai_postings_by_state.xlsx` | 13,826 | `11fa38fa748f34b9c31e7a5b79cdfe22924f72682302ba439e802116587517b6` | https://docs.google.com/spreadsheets/d/1SAQzv3bUew1pCvW2JtrkYq3ny2Viqj |
| `ed2021_burning_glass.xlsx` | 373,812 | `3bb512eff63879bcb72300ba2e34aad4e3c9e9d86ca8dc30af5847f7125550c3` | https://docs.google.com/spreadsheets/d/1n09zmj_nlzuIiGio8Q8Ja3OPlY_tVj |
| `ed2022_emsi_burning_glass.xlsx` | 56,835 | `f0a2037646c23f43a35134c10da65ba8a688ef7654c3d19ea993266e75b38353` | https://docs.google.com/spreadsheets/d/19UGjvQW-PcnWoHEPe9Wd1Eib5z6S5I |
| `ed2023_fig_4.1.10.csv` | 1,839 | `382d39090f4f5276c7142ec3b61992ed249bd5c43ee5e3d78bed45dd0bcb9253` | https://drive.google.com/uc |
| `ed2023_fig_4.1.6.csv` | 875 | `aa4d5da2ae0e0179c1f95d4c1d74ca9b3df668d5fb82dd6001ad6d5c955045fe` | https://drive.google.com/uc |
| `ed2023_fig_4.1.7.csv` | 1,077 | `74f1bb2ac178977456caf927694da50ba00bcfcb484244f9fa3af179293fca4c` | https://drive.google.com/uc |
| `ed2023_fig_4.1.8.csv` | 1,365 | `6533f4ffd56625173e65a3cd1382654d3b149892dd5d45e5ebc5c422518edcef` | https://drive.google.com/uc |
| `ed2024_fig_4.2.11.csv` | 1,261 | `941af82a319b6a8778640beae55d553ac44c80c474893e3c969700754a56a220` | https://drive.google.com/uc |
| `ed2024_fig_4.2.7.csv` | 514 | `ce236c9835417023221e0aa5bc70863cd9f5da10f945fcef50474e3c3b9f000c` | https://drive.google.com/uc |
| `ed2024_fig_4.2.8.csv` | 569 | `0bcb146d942f1ffa9b2b4f24e9e2713f3450c05f835be2333ac53839d76b1f02` | https://drive.google.com/uc |
| `ed2025_fig_4.2.10.csv` | 554 | `a90210b5fbc2c9250fb5ec4cc66bfabc0687ea35e8a34cdd55f1f655046c4b0b` | https://drive.google.com/uc |
| `ed2025_fig_4.2.12.csv` | 1,344 | `5b8559e6beb1d1e978d703e784219b61b8e5fc83200859124fba6620fdd75164` | https://drive.google.com/uc |
| `ed2025_fig_4.2.8.csv` | 514 | `404d7daa8cb6e0e1bfbabfd1fe651e945b3b9ac4d30d41b7ab471a3be6d246bc` | https://drive.google.com/uc |
| `ed2025_fig_4.2.9.csv` | 564 | `1199959fae303729efb46e210d18f9a76ba3a3fe50dc3ae2e28f5be094b6fbc2` | https://drive.google.com/uc |
| `ed2026_fig_4.4.10.csv` | 463 | `02e77e75c68b04b11473cc58a4031894765d37b0ae96c1d782908fbe8dabd150` | https://drive.google.com/uc |
| `ed2026_fig_4.4.11.csv` | 1,266 | `572651636286a5486ddc3a21c07a7cbb0992ec92c6b613a8b092929a7546d50e` | https://drive.google.com/uc |
| `ed2026_fig_4.4.12.csv` | 1,727 | `1d9d41894b6de7a03098f2a8229e5ab37067083f0d880b24ce2084c457e8afed` | https://drive.google.com/uc |
| `ed2026_fig_4.4.13.csv` | 635 | `08f45d43f03105d18c8eac03b99808efe4fedb006d53f1702f3be3112eaca000` | https://drive.google.com/uc |

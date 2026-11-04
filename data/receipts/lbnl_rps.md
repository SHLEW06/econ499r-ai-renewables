# Receipt: LBNL RPS and CES targets and target achievement

**Source:** Galen Barbose, Lawrence Berkeley National Laboratory, *U.S. State Electricity Resource Standards: 2026 Data Update*, June 2026.
**Link:** https://eta-publications.lbl.gov/publications/us-state-electricity-resource-0 (emp.lbl.gov returns 403 to scripts; this LBNL host works)
**How:** Team browser download; moved from the project root on 2026-11-04 (`logs/2026-11-04/moves.csv`).

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/lbnl/RPS & CES Targets and Demand_June 2026.xlsx` | 201,978 | `46f45337966f6e41871f896410e307d9be39ecf295a2aff97266c3e0c4a08521` |
| `data/raw/lbnl/Historical RPS & CES Target Achievement and Compliance Costs_June 2026.xlsx` | 75,877 | `a440248d200198ce13a4a0af8509d922834cd71293f81dc3855352a6ab9f765c` |

Both files are byte-identical to the copies LBNL serves today.

## Main limit: this is today's schedule, not a record of targets in force
- **Target Achievement has no target levels.** LBNL defines it as "the percentage of the annual RPS or CES target achieved." It can show that an obligation existed in a year, but not its size.
- **Every nonzero `target_pct` therefore comes from the June 2026 schedule.**
- **LBNL revises past years.** Against the June 2023, Aug 2024 and Aug 2025 editions, 60 of the 327 nonzero state-years (13 states) differ by more than 0.05 points from a value printed in an edition of that year or later. Largest: MD 2020, 30.5 then 18.1. 19 program-years moved by more than 2 points (MD, NH, NJ, NY). The files don't say why. See `logs/2026-11-04/rps_vintage_check.csv`.
- **No test before 2023.** I found no editions older than June 2023 on the LBNL host.

## What was kept
`data/lbnl_rps_targets.csv`: 561 rows, 51 areas (50 states + DC), 2015-2025. The keys match the panel exactly.

| Column | Meaning |
|---|---|
| `target_pct` | Larger of `rps_target_pct` and `ces_target_pct`, in percent. Differs from the RPS only in MA and VA, 2021-2025 |
| `rps_target_pct`, `ces_target_pct` | "Total RPS" and "Total CES" rows, times 100 |
| `target_basis` | `todays_schedule_june2026`, or `not_in_lbnl_file_zero` for the 18 states not in the file |
| `ta_status` | `reported`, `no_obligation` ("-"), `no_data`, `not_applicable` ("n/a"), or `state_not_in_file` |
| `ta_achievement_pct` | Share of the target achieved. Not a target |
| `in_force_check` | Target Achievement compared with the schedule (counts below) |
| `revised_vs_older_edition` | 1 if an older edition printed a different value for that year or a later one |

**Voluntary flag:** dropped as you directed. voluntary goals not coded; those states are 0. Neither file has voluntary goals, and LBNL's summary deck says "Targets adopted voluntarily by utilities or corporations, or targets established through executive order" are excluded. A 0 therefore does not mean a state has no goal of any kind.

## Steps
1. `check_rps_vintages.py`: download three older editions to a scratch folder, compare the Total rows, write the log.
2. `build_side_tables_nov4.py`: read the "RPS & CES Targets (%)" sheet and take rows whose label starts with `Total RPS` or `Total CES`.
3. Multiply by 100. States absent from the file get 0.
4. Take `target_pct` as the larger of RPS and CES, not the sum, so that overlapping obligations aren't counted twice. This is my choice; LBNL doesn't define a combined figure.
5. Read the "Target Achievement" Total row for each state-year and classify it.
6. Flag revised cells from the log.

**Rows:** targets sheet, 33 areas with Total rows; output 561 rows (33 x 11 from the file, 18 x 11 set to 0). No NA, no duplicates.

## Coverage check
| `in_force_check` | Rows | Meaning |
|---|---|---|
| `obligation_confirmed` | 294 | Target above 0 and an achievement value reported |
| `not_checkable` | 30 | Target above 0, but "no data" so far. 19 of these are in 2025 |
| `conflict_target_but_no_obligation` | 3 | MT 2020; NY 2015 and 2016 (LBNL's NY figures cover only Tier 1 of the current standard) |
| `zero_consistent` | 24 | Target 0 and "-" |
| `zero_no_policy` | 209 | Target 0 and state not in Target Achievement (18 absent states and NE) |
| `zero_not_checkable` | 1 | TX 2025, "n/a" |

## Series breaks to watch under state fixed effects
- **NY 2018:** falls 11.8 points. LBNL: "RPS targets through 2017 are based on legacy RPS"; 2018-2021 follow a later plan.
- **NH 2020 (-5.0) and MN 2023 (-4.4):** not explained in the notes.
- **CA 2016:** three large IOUs through 2015, all utilities after that.
- **HI 2022:** percent of generation instead of percent of retail sales.
- **IA and TX:** set in MW and translated by LBNL, so the percent moves with sales.
- **Denominator:** percent of *applicable* sales. Many RPSs exclude munis or co-ops, and LBNL warns against comparing nominal percentages across states.
- **Compliance years:** DE, IL, NJ and PA run June to May, and are labeled by end year.

## Checks
- **Publisher:** both files byte-identical to LBNL's copies.
- **Counts:** LBNL's deck says 27 states + DC have mandatory RPSs in April 2026. The 33 areas less KS, MT, TX and AZ (repeals) and NE (CES only) gives 27 + DC.
- **MI (independent):** 10% in 2015, 12.5% in 2019-2020, 15% from 2021, matching [PA 342 as summarized by Michigan](https://www.michigan.gov/mpsc/regulatory/electricity/renewable-energy). The table's 2016-2018 values are 9.9-10.2.
- **AZ (independent):** 15% in 2025 matches the REST rule; 0 from 2026 matches the deck's "Repealed RPS." Secondary sources report a rehearing request on the repeal, and I didn't confirm its current status.
- **KS:** 0 from 2015, matching LBNL's note and [news coverage of the 2015 change to a voluntary goal](https://digital-release.thehill.com/?p=242353).

**Rating: yellow.** See `data/DATA_VALIDATION.md`.

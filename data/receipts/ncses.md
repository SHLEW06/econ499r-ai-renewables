# Receipt: Bachelor's degrees per 1,000 age 18-24 (NCSES)

**Source:** National Center for Science and Engineering Statistics, *State Indicators*, "Bachelor's Degrees Conferred per 1,000 Individuals 18-24 Years Old." Underlying: NCES IPEDS Completions and Census Population Estimates. Last updated July 14, 2026.
**Link:** https://ncses.nsf.gov/indicators/states/indicator/bachelors-degrees-per-1000-18-24-year-olds
**How:** by script from the JSON API the site itself uses (`/indicators/states/api/v2/`), 2026-11-04.

## What was kept
`data/ncses_bachelors_state.csv`: state, year, `edu_bach_per1000`, `degrees`, `pop_18_24`. 510 rows, 51 areas x 2015-2024. The source runs 2000-2024.

## Steps
Keep FIPS regions for 50 states + DC (drop `00` national and `72` Puerto Rico), 2015 onward.

## Checks
- **Internal:** the indicator equals 1,000 x degrees / population exactly.
- **Flags, 2015-2024:** none marked not available, suppressed or rounded to zero.

**Rating: green.**

## Raw file hashes
| File | Bytes | SHA-256 | Source |
|---|---:|---|---|
| `bachelors-degrees-per-1000-18-24-year-olds.json` | 453,177 | `5cfef311550d50cfea6b2086d50cadb656638dcee2c702622572dafa829cb4dc` | https://ncses.nsf.gov/indicators/states/api/v2/indicators/bachelors-de |
| `degconferred-bach.json` | 436,171 | `eaafdc8a5f29f335b4259318db77630a3a93122b239ebef0acd6b9574f0568f4` | https://ncses.nsf.gov/indicators/states/api/v2/dataseries/degconferred |
| `population18-24.json` | 437,697 | `115eb0f05cf352a86a81f0091e0fcb949e8c873168895dc6ff343f71d09d0f72` | https://ncses.nsf.gov/indicators/states/api/v2/dataseries/population18 |

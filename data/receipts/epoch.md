# Receipt: Epoch AI data centers

**Source:** Epoch AI, "AI data centers," https://epoch.ai/data/ai-data-centers . Page and CSV: "Updated Nov. 1, 2026." CC BY license; cite Epoch.
**How:** Team browser download; moved from `data_centers/` on 2026-11-04.

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/epoch/data_centers.csv` | 72,026 | `cc66e9295c6ec2bada6a1928fda19da59a600b0ce14b8df40caaab7a9efbafed` |
| `data/raw/epoch/data_center_timelines.csv` | 195,555 | `b0b74fdf6b4d24737565c4c7aa339f808bd044eb5584346f72c4a9378f723a46` |
| `data/raw/epoch/data_center_chip_quantities.csv` | 90,505 | `3ca7576669c3bc9492d25ba8ff78c0a63636b8380d2167e77ef872108d59deab` |
| `data/raw/epoch/data_center_cooling_towers.csv` | 85,832 | `c9ce622e1eaf15cc70bf2445a66f17c9c2be19a3638a96c421dc7e31c3a2db66` |
| `data/raw/epoch/data_center_chillers.csv` | 34,665 | `9711dcfdac0b0de82a1808717e106ea28e213c2a845b42a691ad3cd63caeb704` |
| `data/raw/epoch/chip_types.csv` | 7,311 | `56040986a0d4b9ebb39845ee39385bfcb67c06a75c19f438241019a35a3cea00` |
| `data/raw/epoch/README.md` | 573 | `56894747f3e4e2733a52345eee5f5d81301f7c2682c1d6967f3c96dfcf4c9f61` |

## Use: context and the Georgia box only. Not a model variable.
Epoch covers the largest AI sites only, mostly operational from 2024, and estimates its coverage at 45% of global AI compute (90% CI 30-78%). It says an IT power estimate is within a factor of 1.4 about 80% of the time.

## What was kept
`data/epoch_ai_campuses_by_state.csv`: state, sites, sites operating, current IT MW, planned IT MW, planned facility MW.

- **Current IT MW:** `Current power (MW)`. This column is IT power: Colossus 2 shows 946, as on Epoch's page, where facility power is higher.
- **Planned:** the highest value in each site's timeline, then summed by state. Timeline dates run to 2030-01-01.

## Steps
1. Keep `Country` = United States.
2. Take state from the address (67 sites).
3. For 9 sites with no state in the address, take it from the site's name or location: Google Mesa AZ; Google Storey County NV; Stargate Michigan MI; Stargate Milam TX; Stargate New Mexico NM; Stargate Wisconsin WI; Anthropic Barber Lake TX; AWS New Albany OH; Stream Phoenix AZ.
4. Google Kansas City East could be MO or KS, so it's listed as `UNRESOLVED` rather than guessed.
5. Join each site's highest timeline values and sum by state.

**Rows:** in 96 sites and 575 timeline rows; 77 US sites; out 29 rows (28 states + `UNRESOLVED`).

## Georgia
| Site | Current IT MW | Planned IT MW | Planned facility MW |
|---|---:|---:|---:|
| Microsoft Fairwater Atlanta (Fayetteville) | 636 | 636 | 859 |
| CoreWeave Dalton 1 & 2 | 28 | 28 | 40 |
| xAI QTS Atlanta | 17 | 17 | 24 |
| **Total** | **681** | **681** | **923** |

No Georgia site shows growth beyond current levels. That reflects Epoch's site list, not Georgia's demand; the large-load filings are the source for that.

## Checks
- **Publisher:** `data_centers.csv` is byte-identical to Epoch's download link. I didn't compare the other files this way.
- **Page counts:** TX 14, OH 7, VA 7, NE 4, IA 4 all match the table's site counts.
- **Page values:** Colossus 2 at 946 MW and Fairwater Atlanta at 636 MW match.

**Rating: green, for context use only.**

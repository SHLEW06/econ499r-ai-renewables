# Receipt: Census 2020 County Gazetteer and 2023 County Adjacency

## Sources

- **2020 County Gazetteer:** U.S. Census Bureau
  `https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip`
- **2023 County Adjacency File:** U.S. Census Bureau
  `https://www2.census.gov/geo/docs/reference/county_adjacency.txt`

## Raw Files

| File | Description | Approx. size | Downloaded |
|---|---|---|---|
| `data/raw/census/gaz_counties.zip` | ZIP of 2020 county Gazetteer | ~500 KB | 2026-11-01 |
| `data/raw/census/2020_Gaz_counties_national.txt` | Extracted Gazetteer, tab-delimited | ~500 KB | extracted |
| `data/raw/census/county_adj.txt` | 2023 county adjacency list | ~1 MB | 2026-11-01 |

Script: `download_all.py`.

## Gazetteer: Key Columns Used

| Column | Meaning |
|---|---|
| `USPS` | State abbreviation |
| `GEOID` | 5-digit county FIPS |
| `ALAND_SQMI` | Land area in square miles |
| `INTPTLAT` | Internal point latitude |
| `INTPTLONG` | Internal point longitude |

## Gazetteer Transformations

1. Group counties by `USPS` (state abbreviation).
2. Sum `ALAND_SQMI` across all counties in a state → `land_sqmi`.
3. Compute land-area-weighted centroid for each state:
   - `centroid_lat = sum(ALAND_SQMI * INTPTLAT) / sum(ALAND_SQMI)`
   - `centroid_lon = sum(ALAND_SQMI * INTPTLONG) / sum(ALAND_SQMI)`
4. Keep 50 states (drop DC, PR, territories).
5. Write `data/out/state_centroids_land.csv` (50 rows × 3 cols: state, lat, lon, land_sqmi).

**Note:** These are land-area-weighted centroids, not population-weighted. The DATA_INDEX
description says "population-weighted" — treat this as an approximation; land-area weighting
is used because county population data is not merged in this step.

## Distance Matrix Transformations

1. For each pair of states (i, j), compute great-circle distance in miles using the
   Haversine formula applied to centroids.
2. Set diagonal to 0.
3. Write `data/out/W_distance_miles.csv` (50 × 50 symmetric matrix).
4. Compute `W_ij = 1 / d_ij` for i ≠ j, set diagonal to 0.
5. Row-standardize: divide each row by its row sum.
6. Write `data/out/W_inverse_distance_rowstd.csv` (50 × 50).

## Adjacency File Transformations

Format: pipe-delimited; alternating county-name and GEOID pairs listing each county
and all its neighbors.

1. Parse GEOID → 2-digit state FIPS prefix.
2. Map state FIPS to state abbreviation via lookup table.
3. For each county pair (i, j) in different states, record `(state_i, state_j)` as adjacent.
4. Build symmetric 50 × 50 binary matrix: `W_border[i,j] = 1` if any county in state i
   is adjacent to any county in state j.
5. Set diagonal to 0.
6. Write `data/out/W_border_binary.csv` (50 × 50).

## Known Quirks

- **AK and HI have no contiguous neighbors.** Their rows and columns in `W_border_binary.csv`
  are all zeros. Spatial lag models must handle these isolated units (drop or treat separately).
- The adjacency file lists county-to-county adjacency including water boundaries in some
  cases. This may cause a small number of coastal state pairs to show as adjacent even where
  land continuity is ambiguous (e.g., RI–NY via water). Review manually if needed.
- DC is excluded from the 50 × 50 matrices but is present in `state_panel_2015_2025.csv`.
  Any spatial regression that uses W must handle DC separately or drop it.

## Output Files

| File | Rows | Description |
|---|---|---|
| `data/out/state_centroids_land.csv` | 50 | State, centroid lat/lon, land area (sq mi) |
| `data/out/W_distance_miles.csv` | 50 × 50 | Pairwise great-circle distances (miles) |
| `data/out/W_inverse_distance_rowstd.csv` | 50 × 50 | Row-standardized inverse-distance W |
| `data/out/W_border_binary.csv` | 50 × 50 | Binary contiguity (shared county border) |

## Script

`scripts/build_panel.py` (Census/spatial section), after `download_all.py`.

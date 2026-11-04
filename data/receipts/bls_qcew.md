# Receipt: BLS QCEW — NAICS 518210, 5415, 10

## Source

Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW), Annual Averages.
URL pattern: `https://data.bls.gov/cew/data/api/{year}/a/industry/{naics_code}.csv`

## Raw Files

| File pattern | Count | Approx. size each | Downloaded |
|---|---|---|---|
| `data/raw/bls/qcew_{year}_518210.csv` | 12 (2014–2025) | 30–60 KB | 2026-11-01 |
| `data/raw/bls/qcew_{year}_5415.csv` | 12 (2014–2025) | 50–90 KB | 2026-11-01 |
| `data/raw/bls/qcew_{year}_10.csv` | 12 (2014–2025) | 200–400 KB | 2026-11-01 |

36 files total. Script: `download_all.py`.

## NAICS Codes

| Code | Description | Role |
|---|---|---|
| 518210 | Computing Infrastructure Providers, Data Processing, Web Hosting | Data-center / AI compute employment proxy |
| 5415 | Computer Systems Design and Related Services | Broader tech employment |
| 10 | Total, All Industries | State total employment denominator |

## Filters Applied

Each raw file contains county, MSA, state, and national rows. Keep only:

- **518210**: `area_fips` ends in `'000'` AND `own_code = 5` AND `agglvl_code = 58`
- **5415**: `area_fips` ends in `'000'` AND `own_code = 5` AND `agglvl_code = 56`
- **10 (total)**: `area_fips` ends in `'000'` AND `own_code = 0` AND `agglvl_code = 50`

`area_fips` ending in `'000'` selects the statewide row (e.g., `'04000'` = Arizona).

## Government 518210 rows (corrected 2026-11-04)

State-level government rows exist in every file: own_code 1 (federal), 2 (state), 3 (local), agglvl 58. They are left out of the main AI measure by team decision. `build_ai_allown.py` writes `data/ai_allown_518210.csv` for the labeled check and `logs/2026-11-04/gov_518210_shares.csv`. Suppressed government rows show 0 jobs and can't be recovered, so all-ownership counts are lower bounds.

## Key Column

`annual_avg_emplvl` — annual average employment level (full- and part-time jobs, covered by UI).

## Suppression Handling

When `disclosure_code = 'N'`, the cell is suppressed to protect employer confidentiality.
Suppressed cells are set to `NA` before any computation.

**Known quirk:** AK, ND, SD, and WY are suppressed for NAICS 518210 in 2025. These four states
carry `NA` for `dc_jobs` in the 2025 panel row. They are not dropped; the suppression is noted in
the variable metadata.

## Transformations

1. Read all 36 CSVs, parse `area_fips` as string (zero-pad to 5 chars).
2. Map `area_fips` state prefix to USPS abbreviation via a Census FIPS lookup table.
3. Apply filters above and keep the 51 state FIPS codes. The code doesn't assert a row count; own-code 5 files have 53 state-level rows before the FIPS filter drops PR and VI.
4. Replace suppressed cells (`disclosure_code = 'N'`) with `NA`.
5. Merge 518210, 5415, and 10 by state and year.
6. Compute derived columns (see below).

## Rows In / Out

- Input rows per file: varies by year, roughly 4,000–8,000 (all geographies and ownership types).
- After state-level filter: 51 rows per file × 36 files = 1,836 rows total before reshape.
- After merge and pivot to state-year: 561 rows (51 states × 11 years, 2015–2025; 2014 used
  only as lag if needed).

## Output Columns

| Column | Definition |
|---|---|
| `dc_jobs` | `annual_avg_emplvl` from NAICS 518210 |
| `tech5415_jobs` | `annual_avg_emplvl` from NAICS 5415 |
| `total_jobs` | `annual_avg_emplvl` from industry 10 |
| `ai_dc_per1000` | `dc_jobs / total_jobs * 1000` |
| `tech_share` | `tech5415_jobs / total_jobs` |

## Script

`scripts/build_panel.py` (BLS section), called after `download_all.py` fetches the raw CSVs.

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 36 files.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/bls/qcew_2014_10.csv` | 3,503,742 | `3b0793bc5a047804899d6b6c06e9efd88491845fd4193632fdfc420df6578e13` |
| `data/raw/bls/qcew_2014_518210.csv` | 264,711 | `bb0a47833a2b470ad5b52bb909323b9ded4573fd403ff9b1b5da83bdbabb7be3` |
| `data/raw/bls/qcew_2014_5415.csv` | 540,057 | `82fcb0c4489abe04f646c346b382bb4438cfbcf7545026ee9d3dd8c5d0ab81fe` |
| `data/raw/bls/qcew_2015_10.csv` | 3,512,521 | `af6a953d8fb7178baedea35985d5afadebb70953e13bca26fc95ea05d0db30af` |
| `data/raw/bls/qcew_2015_518210.csv` | 268,570 | `a20d5859d002518b28805eecb56f0f4c5bcd5f2d392d828a9ca61d110d430f18` |
| `data/raw/bls/qcew_2015_5415.csv` | 545,827 | `1862b83b791b43318524f844fd006520faed5bc428fd90f4e628dd212455723e` |
| `data/raw/bls/qcew_2016_10.csv` | 3,518,923 | `6ce9a8d3b392410e270153b2875f26d72e2c04d91e961d941afed8d5ce97ab09` |
| `data/raw/bls/qcew_2016_518210.csv` | 269,939 | `b6fc7483dba4ab22bdca944e0e160e3d9b6b21b8220824499bbc0d272c2be699` |
| `data/raw/bls/qcew_2016_5415.csv` | 551,094 | `320c24bf225e6f66d802492e1e4cc0ba0370966d2cb810db6a30139de01ce929` |
| `data/raw/bls/qcew_2017_10.csv` | 3,505,449 | `7a5c847dc154d544683583e44d32c51228ebeec7970029359c9133c3af65f23c` |
| `data/raw/bls/qcew_2017_518210.csv` | 276,142 | `b7e3f2887afe40e78d16529eca60288ad8defb36dfe1f9e4c9a2fdbc25edca06` |
| `data/raw/bls/qcew_2017_5415.csv` | 551,984 | `271ec731731e93a38eadf040143eb52731880518b6d247ad461a6a7fa47118e3` |
| `data/raw/bls/qcew_2018_10.csv` | 3,503,453 | `9c91e968679426f9bd0cc30050c44aee0145bea0a598a8b019fc07bc39e86fe6` |
| `data/raw/bls/qcew_2018_518210.csv` | 279,626 | `9a6a24a0327b4432194997c7280ea001cd671d4c03578ec464d31cb35cecfc2f` |
| `data/raw/bls/qcew_2018_5415.csv` | 557,319 | `20b14477e5258b9daeacccda49cd5104fa91e10e55deb762f57a14e9ea1d0e35` |
| `data/raw/bls/qcew_2019_10.csv` | 3,498,506 | `2d65b5f60a5c5665fdac38af08bdb85c2c652c87781eb28fbfd9f78891621c7e` |
| `data/raw/bls/qcew_2019_518210.csv` | 287,004 | `eb043932a91762354e0546de2c3e76da3444c7d08424ed0dab7cd00ad59a2b25` |
| `data/raw/bls/qcew_2019_5415.csv` | 563,494 | `07ada88bea227ca75d16fdfcee8077164ce5b8e1b7111313ff3d5b102773b7b0` |
| `data/raw/bls/qcew_2020_10.csv` | 3,546,346 | `d76b6499fba0f4c6527133900d240b85674bd7ffc1ec96463275c043ddd0c80c` |
| `data/raw/bls/qcew_2020_518210.csv` | 303,070 | `f32645eb32f651a469fef233a91f543d19f2be0a25390a3f8891c0a2377cb4fb` |
| `data/raw/bls/qcew_2020_5415.csv` | 573,090 | `1aa695e055517784ef3d7760e9a8be465e1076fb8d252cb21207e43fad321c8a` |
| `data/raw/bls/qcew_2021_10.csv` | 3,512,154 | `331d81786235e57217ef1498efc64d5e3abf39f1cbca1cf841ea10533920db51` |
| `data/raw/bls/qcew_2021_518210.csv` | 322,170 | `b5d21a5e44143584ea7c82c054ef3cc498697c46e911a006327cb69fd40054e6` |
| `data/raw/bls/qcew_2021_5415.csv` | 586,845 | `714c9a333a8735776e497f9e27d7c43031d8d2c377c3426073cbffc5d994d0cc` |
| `data/raw/bls/qcew_2022_10.csv` | 3,543,500 | `9a95487df1dd1ded3f2dc712b5d19747e2aacfc30102869cd3a0b985501e739a` |
| `data/raw/bls/qcew_2022_518210.csv` | 347,177 | `2f6d14f2d405bfd23ab6ff3413f8e3876fe3d474b1c8fb8ae98aa085dd133dce` |
| `data/raw/bls/qcew_2022_5415.csv` | 617,781 | `67cd3618befac635b83dd601153ed7cf8c700a9ae0a77dc6123593cffacd1479` |
| `data/raw/bls/qcew_2023_10.csv` | 3,561,704 | `0115a20a201b821d29f731340976aad8fc8dac16cb6a0c13df0f7f52afe108b1` |
| `data/raw/bls/qcew_2023_518210.csv` | 361,958 | `628f9d688e1e7faebd5382dbe7f37b4fe83743271046a0624bc42018ca7fd1af` |
| `data/raw/bls/qcew_2023_5415.csv` | 635,601 | `d350a976609e0d5a9f4a7c64c4d888eadacabc2ae2ea135cca1079ff0a17b475` |
| `data/raw/bls/qcew_2024_10.csv` | 3,562,701 | `e73da8f6b2b415180b1910351327faa51183589021357535fd880f8761e12a12` |
| `data/raw/bls/qcew_2024_518210.csv` | 355,053 | `847b0e11e778dff55be07665b35e3d21fc06109a8dc982761cf366928ff5fb1e` |
| `data/raw/bls/qcew_2024_5415.csv` | 629,032 | `831a0af464b373378ebbd6e973256407353c31544cfeea93cfd82bf90217f5b0` |
| `data/raw/bls/qcew_2025_10.csv` | 3,273,494 | `5a5f89142aae74beea5b526f2e5591c7775c846968a14251b12b2c68f32071c2` |
| `data/raw/bls/qcew_2025_518210.csv` | 299,257 | `c0d43a0b277179bf8a2b6fb41a5aaaecc749fbec8173903473d754fe8bd0a082` |
| `data/raw/bls/qcew_2025_5415.csv` | 559,735 | `f5304280483346c4762dd900d7aea80c848b952f2572579de84420f3bd7567b4` |

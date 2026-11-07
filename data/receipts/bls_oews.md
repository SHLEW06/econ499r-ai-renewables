# Receipt: BLS Occupational Employment and Wage Statistics (OEWS), state files, May 2015 to May 2024

**Status: filed 2026-11-07.** Downloaded by hand by the team (bls.gov refused scripted requests). Zips are kept as downloaded, not unzipped.

| Original filename | New path | Source URL | Downloaded (file modified time) | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| `oesm15st.zip` | `data/raw/bls/oews/oesm15st.zip` | https://www.bls.gov/oes/special-requests/oesm15st.zip | 2026-11-07 18:03 | 6,128,285 | `76fe0cb8a10397c79f19c4b197e8a9e6acc82d9fb9ef005f1521ef5112298f25` |
| `oesm16st.zip` | `data/raw/bls/oews/oesm16st.zip` | https://www.bls.gov/oes/special-requests/oesm16st.zip | 2026-11-07 18:03 | 6,118,466 | `a53bd9c45786b5f7a8e253a71b3e71ba5a76768ac265de5cf52d351b050e27c5` |
| `oesm17st.zip` | `data/raw/bls/oews/oesm17st.zip` | https://www.bls.gov/oes/special-requests/oesm17st.zip | 2026-11-07 18:03 | 6,024,998 | `4ac7aab4272b93e2cc4105a649f0225bbf18f5434a216273a14101b977f116ee` |
| `oesm18st.zip` | `data/raw/bls/oews/oesm18st.zip` | https://www.bls.gov/oes/special-requests/oesm18st.zip | 2026-11-07 18:03 | 6,013,818 | `b5b0e2b8825149eaae85dc3a741f4e1d8d33dd73232ba80785f9d5c0c2f0b2da` |
| `oesm19st.zip` | `data/raw/bls/oews/oesm19st.zip` | https://www.bls.gov/oes/special-requests/oesm19st.zip | 2026-11-07 18:03 | 6,795,106 | `d121e196beb40053241c02a1f264b459958cf35096e07940c866e68eea971388` |
| `oesm20st.zip` | `data/raw/bls/oews/oesm20st.zip` | https://www.bls.gov/oes/special-requests/oesm20st.zip | 2026-11-07 18:03 | 7,026,272 | `fc2d2cd6684f6b1f342a69631efb8d6c8ef375c495c17ccba78e7b05c48ae5dc` |
| `oesm21st.zip` | `data/raw/bls/oews/oesm21st.zip` | https://www.bls.gov/oes/special-requests/oesm21st.zip | 2026-11-07 18:03 | 7,525,249 | `a4397cb1524512c21ca900dcc25d6a21d2b6342031efb746494ffd7ffc6c6941` |
| `oesm22st.zip` | `data/raw/bls/oews/oesm22st.zip` | https://www.bls.gov/oes/special-requests/oesm22st.zip | 2026-11-07 18:03 | 7,424,445 | `5d1fdf7bd2d011f092df86995e389f83bc958211145b0080f6582e319a8508eb` |
| `oesm23st.zip` | `data/raw/bls/oews/oesm23st.zip` | https://www.bls.gov/oes/special-requests/oesm23st.zip | 2026-11-07 18:03 | 7,445,440 | `e76daf090fc4ea8bd2061839dcc151b7fbee7007d9f602cfd1645a2261e9d887` |
| `oesm24st.zip` | `data/raw/bls/oews/oesm24st.zip` | https://www.bls.gov/oes/special-requests/oesm24st.zip | 2026-11-07 18:03 | 7,617,815 | `5b66eb673f120c10fd17824d4d1e8bcf2fba0e6b39122b66404ce42cad5fb816` |

**Identified by content:** every zip passes `unzip -t`. Each holds `oesmYYst/state_MYYYY_dl.xlsx`; 2015-2018 also hold `field_descriptions.xlsx`. `oesm22st.zip` also contains an Excel lock file, `~$state_M2022_dl.xlsx` (it came that way), which the build ignores.

**Used for:** the talent dimension of the section 5 index; mapping and suppression rules in `ai_index.md` (section 5).

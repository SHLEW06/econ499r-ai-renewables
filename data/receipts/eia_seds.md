# Receipt: EIA State Energy Data System (SEDS)

**Source:** U.S. Energy Information Administration, State Energy Data System  
**Link:** https://www.eia.gov/state/seds/sep_use/total/csv/use_all_btu.csv  
**How:** Script (`download_all.py` → `raw/eia/seds/use_all_btu.csv`)  
**Downloaded:** 2026-11-01  
**File:** `data/raw/eia/seds/use_all_btu.csv` (4.3 MB)

## What we kept

Series TETCB only: total energy consumption, all fuels, all sectors, billion Btu. States in panel (50 + DC). Years 2010–2024 (SEDS ends 2024; 2025 not yet published).

## Transformations

1. Filter MSN == 'TETCB' and State in STATES.
2. Melt year columns to long format; filter to model range.
3. Derived: seds_mmbtu_pc = seds_total_energy_bbtu * 1000 / population.

## Known quirks

Ends 2024. Covers all energy end uses, not just electricity — it is the paper-matching check variable, not the primary EC outcome. 51 NA cells in the panel for 2025.

## Output columns

seds_total_energy_bbtu, seds_mmbtu_pc in data/out/state_panel_2015_2025.csv

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 1 file.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/eia/seds/use_all_btu.csv` | 4,277,144 | `cbf0e26022e90303d355856ce750eaeedcb1cc6642c01c8b21f46d0284a9cedc` |

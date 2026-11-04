# Receipt: Lazard LCOE+ 2026

**Source:** Lazard, *Levelized Cost of Energy Analysis Plus 2026*, July 13, 2026  
**Link:** https://www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf  
**How:** Script (`download_all.py` → `raw/costs/Lazard_LCOEplus_2026.pdf`)  
**Downloaded:** 2026-11-01 (originally placed in `literature/`, moved to `data/raw/costs/` in Phase 2B)  
**File:** `data/raw/costs/Lazard_LCOEplus_2026.pdf`

## What we kept

PDF reference document — not parsed by a script. Consulted manually for:
- New-build LCOE ranges by technology (solar, wind, gas, nuclear)
- Learning-curve context for the Georgia solar cost projection module (stretch goal)

## Known quirks

- PDF only; no machine-readable data file.
- "Plus" edition includes storage, transmission, and integration costs not in the base LCOE analysis.
- Figures are for new capacity only; FERC Form 1 data covers book value of existing utility plants.

## Output

Used as a citation and cost benchmark in the Georgia case box and methods writeup. No CSV output.

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 1 file.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/costs/Lazard_LCOEplus_2026.pdf` | 1,181,395 | `a541d1ecd2e837fb779a6370c76336d899216fc4439e2a8b7b93cb1d046f25b5` |

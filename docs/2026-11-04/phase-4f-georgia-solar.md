# Phase 4f: Georgia solar learning curve
**Date:** 2026-11-04  
**Driver:** `code/python/04f_georgia_solar.py --date 2026-11-04`  
**Notebook:** `notebooks/04f_georgia_solar.ipynb`  
**Results:** `results/2026-11-04/georgia_solar/`

---

## 1. What was done
Base cost from LBNL project data, IEA scenario capacity paths, a 12-trajectory fan, and a learning-rate check.

## 2. Key decisions
- Base: Georgia, COD 2023-2025, capacity-weighted LCOE without tax credits: $63.81/MWh.
- Paths: IEA WEO 2025 Current Policies, Stated Policies and Net Zero, with growth ratios applied to IRENA's series.

## 3. Results
At the main 24% learning rate on the central path, about $37/MWh in 2035 (range across the 12 trajectories: $14.51 to $50.40). These aren't forecasts of ours.

## 4. What did not change
No AI variable and no change to the panel or either test.

## 5. Decisions still open
None. LCOE has risen since 2022, so say that wherever the fan appears.

## How to resume
1. `results/2026-11-04/georgia_solar/RECEIPT.md`
2. `notebooks/04f_georgia_solar.ipynb`

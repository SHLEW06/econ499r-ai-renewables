# Phase 4c: Step 2 — Mediation (H2a, H2b)
**Date:** 2026-11-03  
**Driver:** `code/R/04c_step2_mediation.R --date 2026-11-03`  
**Notebook:** `notebooks/04c_step2_mediation.ipynb`

---

## 1. What changed

- Created `code/R/04c_step2_mediation.R` — runs all three mediators × three outcomes (9 mediation analyses), computes Sobel z + cluster bootstrap (999 reps, seed=42), writes results to `results/2026-11-03/h2/`.
- Results: `results/2026-11-03/h2/h2_results.csv` (63 rows), `ln_ea_redundancy.csv`, `RECEIPT.md`.
- Tables: `results/2026-11-03/tables/h2_{tech_share,hma,ln_ea}.csv + .tex`, `PROVENANCE.md`.
- Figures: `results/2026-11-03/figures/h2_path_{tech_share_c,hma,ln_ea}.pdf/.png` (3 path diagrams).
- Notebook: `notebooks/04c_step2_mediation.ipynb` (Python kernel reading CSVs).
- **Tag correction:** EXPERIMENTS.md §6/§7 originally said "ctrl5" for mediation tags. Corrected to ctrl4 — same as H1 baseline. Logged in §0 divergence register.

---

## 2. Why (key decisions)

**Controls = ctrl4 throughout.** The prompt says "use the same controls as Step 1." Step 1 baseline is ctrl4. Using ctrl5 (which includes tech_share) in the mediation equations would be circular when M=tech_share and inconsistent with H1 for the other mediators.

**tech_share mean-centered.** Grand mean (0.01272) subtracted before entering the first-stage regression. This makes the intercept interpretable (expected M at average AI level) and is standard for continuous mediators. No substantive difference from raw since the mean is absorbed by the FE intercept anyway.

**Bootstrap = pairs cluster bootstrap.** Resample states (not observations) with replacement, assign unique cluster IDs to repeated states, refit equations (a) and (c). This is the correct approach for panel data with clustered errors. 999 reps, seed=42.

**ln_ea redundancy check.** Within-state `cor(ln_ea, ln_gdp_pc) = 0.943` — confirms the EXPERIMENTS.md §0 item 9 caveat. ln_gdp_pc absorbs nearly all within-state variation in economic density (since land_sqmi is constant). Result: AI does not predict ln_ea after state FE + ctrl4 (b1 = -0.003, p=0.296).

---

## 3. Results

### Full mediation results table

| Mediator | Outcome | b1 (AI→M) | p(b1) | e1 (M→Y) | p(e1) | Indirect | Sobel p | Boot 95% CI | Share med. | Channel? |
|---|---|---|---|---|---|---|---|---|---|---|
| tech_share_c | ln_ec | −0.000157 | 0.454 | −3.872 | 0.285 | 0.000608 | 0.536 | [−0.0020, 0.0032] | −0.388 | **No** |
| tech_share_c | ln_ee | −0.000157 | 0.454 | 6.006 | 0.145 | −0.000943 | 0.501 | [−0.0044, 0.0025] | −0.427 | **No** |
| tech_share_c | renew_share | −0.000157 | 0.454 | −1.179 | 0.816 | 0.000185 | 0.823 | [−0.0019, 0.0044] | −0.018 | **No** |
| hma | ln_ec | +0.041637 | <0.001* | −0.001 | 0.991 | −0.000059 | 0.991 | [−0.0104, 0.0124] | +0.038 | **No** |
| hma | ln_ee | +0.041637 | <0.001* | +0.124 | 0.524 | +0.005184 | 0.522 | [−0.0104, 0.0219] | +2.350 | **No** |
| hma | renew_share | +0.041637 | <0.001* | −0.135 | 0.412 | −0.005613 | 0.409 | [−0.0217, 0.0066] | +0.554 | **No** |
| ln_ea | ln_ec | −0.003362 | 0.296 | −0.333 | 0.018 | +0.001120 | 0.332 | [−0.0008, 0.0051] | −0.716 | **No** |
| ln_ea | ln_ee | −0.003362 | 0.296 | +0.403 | 0.006 | −0.001355 | 0.322 | [−0.0057, 0.0010] | −0.615 | **No** |
| ln_ea | renew_share | −0.003362 | 0.296 | −0.254 | 0.240 | +0.000855 | 0.430 | [−0.0009, 0.0050] | −0.084 | **No** |

*hma b1>0 is mechanical (HMA = AI × tech_share by construction).

**ln_ea redundancy:** within-state cor(ln_ea, ln_gdp_pc) = **0.943**; cor(ln_ea, pop_growth) = 0.002.

### Summary
- **No channel holds for any mediator or outcome.** The paper's rule (b1, c1, and e1 all significant) fails in every cell.
- **tech_share (main H2a):** First stage fails (b1 p=0.454). AI does not predict tech worker share within states after FE.
- **hma (memo):** First stage mechanically passes (b1 p<0.001) but downstream (c1, e1) all non-significant. The memo channel is not supported.
- **ln_ea (H2b):** First stage fails (b1 p=0.296). ln_gdp_pc already absorbs the AI→EA path (r=0.943 within state). Downstream is significant for ln_ec and ln_ee but the broken first stage blocks the channel.

---

## 4. What did not change

- Panel: `data/out/state_panel_2015_2025.csv` unchanged.
- H1 results unchanged; a1 loaded from `results/2026-11-02/h1/h1_core.csv`.
- load_panel.R unchanged.
- Tag grammar: ctrl4 tags now consistent with H1 (corrected from ctrl5 in EXPERIMENTS.md §6/§7).

---

## 5. Decisions still open

| Item | Options | Deadline |
|---|---|---|
| LBNL RPS control | Download LBNL spreadsheet; add to §9 robustness | Before 04e (Nov 17) |
| t-2/t-3 distributed lags | Obtain QCEW 2012–2013 | Before 04e |
| SE choice for paper | CL vs DK — decide which is "primary" | Before draft (Nov 24) |

---

## How to resume

Read in this order:
1. `CLAUDE.md` (project state, conventions)
2. `EXPERIMENTS.md` §0, §6–§8 (divergence register, H2a, H2b, H3 specs)
3. This file
4. `notebooks/04c_step2_mediation.ipynb` (all results)
5. `results/2026-11-03/h2/RECEIPT.md`

Then run: `prompts/04d_step3_spatial.md`

Key result files:
- `results/2026-11-03/h2/h2_results.csv` — all 63 rows (equations + indirect effect rows)
- `results/2026-11-03/h2/ln_ea_redundancy.csv` — within-state correlations
- `results/2026-11-03/tables/h2_*.csv + .tex` — per-mediator summary tables
- `results/2026-11-03/figures/h2_path_*.pdf/.png` — path diagrams

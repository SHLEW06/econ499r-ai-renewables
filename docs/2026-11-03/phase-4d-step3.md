# Phase 4d: Step 3 — Spatial Analysis (H3)
**Date:** 2026-11-03  
**Driver:** `code/R/04d_step3_spatial.R --date 2026-11-03`  
**Notebook:** `notebooks/04d_step3_spatial.ipynb`

---

## 1. What was done

- Created `code/R/04d_step3_spatial.R` — Moran's I, LM pre-tests, SLX (clustered SEs), SDM (SDPDmod), splm cross-check, maps and figures.
- Three W matrices: invdist-50 (main), invdist-48, border-48. All row-standardized; ordering asserted before each spatial operation.
- SDM run with LYtrans=TRUE (main, bias-corrected) and LYtrans=FALSE (for splm comparison).
- Results: `results/2026-11-03/h3/` (6 CSVs + RECEIPT.md).
- Tables/figures in `results/2026-11-03/tables/` and `results/2026-11-03/figures/`.
- Notebook: `notebooks/04d_step3_spatial.ipynb`.

---

## 2. Key decisions

**SDPDmod vs splm for SDM:** SDPDmod::SDPDm with `model="sdm"` adds W·X automatically and `impactsSDPDm()` gives correct direct/indirect/total decomposition. splm with hand-made W·X columns used only as a cross-check; impacts not taken from splm (W·AI is a fixed regressor outside splm's impact machinery).

**LYtrans=TRUE convergence failure:** SDPDmod gave ρ>1 for ln_ec (ρ≈4.8) and ln_ee (ρ≈6.1) with invdist W. Valid interval is (−4.74, 1) for invdist-50 (eigenvalue range [−0.211, 1]). renew_share converges correctly (ρ=0.776). LYtrans=FALSE used as primary for ln_ec and ln_ee. This is a numerical issue in SDPDmod when combining LYtrans=TRUE + twoways + static for log-scale outcomes.

**SLX as clustered-SE companion:** Only model with clustered SEs. Total = b1+θ1 with delta-method SE from clustered vcov. Reports the SDM indirect channel in a framework economists can audit directly.

**State ordering:** SDPDm sorts panel alphabetically; W reordered to alphabetical state order inside `run_sdm_fit()`. SLX and Moran's I use the original W row order (non-alphabetical). An `assert_order()` guard fires before every spatial multiplication.

**Impact check:** Analytical (b1+θ1)/(1−ρ) vs simulated `impactsSDPDm` total. For near-zero ρ (ln_ee, LYtrans=FALSE), simulation SE=0.5 swamps the signal — analytical formula (−0.003) is more reliable than sim total (0.022). Flagged when |diff| > 0.01.

---

## 3. Results

### Moran's I — renew_share (invdist-50)

| Year | I | p |
|---|---|---|
| 2015 | 0.094 | 0.001 |
| 2016 | 0.111 | 0.002 |
| 2017 | 0.120 | 0.001 |
| 2018 | 0.116 | 0.001 |
| 2019 | 0.109 | 0.001 |
| 2020 | 0.115 | 0.002 |
| 2021 | 0.121 | 0.001 |
| 2022 | 0.133 | 0.001 |
| 2023 | 0.134 | 0.001 |
| 2024 | 0.148 | 0.001 |
| 2025 | 0.157 | 0.001 |

Renewable share is significantly spatially clustered in every year. AI lag1 is also positively clustered. Residual Moran's I is small after TWFE.

### SLX (renew_share, clustered SEs)

| W | b1 | p(b1) | θ1 | p(θ1) | Total | p(total) |
|---|---|---|---|---|---|---|
| invdist-50 | −0.0136 | 0.014 | −0.0551 | 0.117 | −0.0686 | 0.068 |
| invdist-48 | −0.0136 | 0.014 | −0.0562 | 0.121 | −0.0698 | 0.071 |
| border-48  | −0.0135 | 0.025 | −0.0299 | 0.108 | −0.0434 | 0.057 |

ln_ec and ln_ee: all null.

### SDM — renew_share (main H3 result)

| LYtrans | ρ | valid | direct | p | indirect | p | total | p |
|---|---|---|---|---|---|---|---|---|
| TRUE  | 0.776 | ✓ | −0.017 | 0.001 | −0.252 | 0.063 | −0.269 | 0.054 |
| FALSE | 0.617 | ✓ | −0.015 | <0.001 | −0.165 | 0.038 | −0.181 | 0.029 |

### SDM — ln_ec and ln_ee (invdist-50)

| Outcome | LYtrans | ρ | valid | direct | p | total | p |
|---|---|---|---|---|---|---|---|
| ln_ec | TRUE | 4.79 | ✗ | — | — | — | — |
| ln_ec | FALSE | 0.137 | ✓ | −0.002 | 0.878 | 0.040 | 0.945 |
| ln_ee | TRUE | 6.09 | ✗ | — | — | — | — |
| ln_ee | FALSE | −0.018 | ✓ | 0.004 | 0.678 | 0.022 | 0.965 |

### splm cross-check (invdist-50, LYtrans=FALSE basis)

| Outcome | ρ SDPDm | ρ splm | b1 SDPDm | b1 splm | θ1 SDPDm | θ1 splm |
|---|---|---|---|---|---|---|
| ln_ec | 0.137 | 0.137 | −0.00266 | −0.00266 | 0.01577 | 0.01577 |
| ln_ee | −0.018 | −0.019 | 0.00366 | 0.00366 | −0.00640 | −0.00641 |
| renew_share | 0.617 | 0.622 | −0.01284 | −0.01283 | −0.05491 | −0.05491 |

b1 and θ1 match to 5 decimal places. ρ differs slightly (different ML approximations). Cross-check passes.

---

## 4. What did not change

- Panel and H1/H2 results unchanged.
- W matrices unchanged (data/out/).

---

## 5. Decisions still open

| Item | Options | Deadline |
|---|---|---|
| LBNL RPS/CES control | Download spreadsheet; add to 4e robustness | Before 4e (Nov 17) |
| t-2/t-3 lags | Obtain QCEW 2012–2013 | Before 4e (Nov 17) |
| SE choice for paper | CL vs DK; primary SE for H1 | Before draft (Nov 24) |
| SDPDm LYtrans=TRUE for log outcomes | Investigate alternative SDM package (R2sdmx?) | Optional |

---

## How to resume

Read in this order:
1. `CLAUDE.md` (project state)
2. `EXPERIMENTS.md` §0, §8–§9 (H3 spec, divergence register)
3. This file
4. `notebooks/04d_step3_spatial.ipynb`
5. `results/2026-11-03/h3/RECEIPT.md`

Then run: `prompts/04e_robustness.md`

Key result files:
- `results/2026-11-03/h3/h3_moran.csv` — Moran I all vars/years/W
- `results/2026-11-03/h3/h3_slx.csv` — SLX clustered SEs
- `results/2026-11-03/h3/h3_sdm_core.csv` — SDM ρ/b1/θ1
- `results/2026-11-03/h3/h3_sdm_impacts.csv` — direct/indirect/total
- `results/2026-11-03/h3/h3_splm_check.csv` — cross-check

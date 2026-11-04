# Phase 4d: Step 3 — Spatial Analysis (H3)
**Date:** 2026-11-03  
**Driver:** `code/R/04d_step3_spatial.R --date 2026-11-03`  
**Notebook:** `notebooks/04d_step3_spatial.ipynb`

---

## 1. What was done

- Created `code/R/04d_step3_spatial.R` — Moran's I, LM pre-tests, SLX (clustered SEs), SDM (SDPDmod), splm cross-check, maps and figures.
- Three W matrices: invdist-50 (main), invdist-48, border-48. All row-standardized; ordering asserted before each spatial operation.
- SDM run with LYtrans=TRUE and LYtrans=FALSE. **Revised 2026-11-03:** LYtrans=FALSE is the main spec for all three outcomes; see section 3b.
- Results: `results/2026-11-03/h3/` (6 CSVs + RECEIPT.md).
- Tables/figures in `results/2026-11-03/tables/` and `results/2026-11-03/figures/`.
- Notebook: `notebooks/04d_step3_spatial.ipynb`.

---

## 2. Key decisions

**SDPDmod vs splm for SDM:** SDPDmod::SDPDm with `model="sdm"` adds W·X automatically and `impactsSDPDm()` gives correct direct/indirect/total decomposition. splm with hand-made W·X columns used only as a cross-check; impacts not taken from splm (W·AI is a fixed regressor outside splm's impact machinery).

**LYtrans=TRUE out of range:** SDPDmod gave ρ>1 for ln_ec (ρ≈4.8) and ln_ee (ρ≈6.1) with invdist W. The valid interval is (−4.74, 1) for invdist-50 (eigenvalue range [−0.211, 1]). This is not a convergence failure: SDPDm applies a one-step bias formula after fitting, ρ + T·Var(ρ)/(1−ρ) approximately, and it overshoots because ρ is so imprecise for these outcomes (SE about 0.6–0.75).

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

Renewable share is significantly spatially clustered in every year. AI lag1 is also positively clustered. After two-way FE and AI(t-1), renew_share residuals still cluster: I = 0.02–0.11, with p < 0.05 in 10 of 11 years (2020: p = 0.055). Two-way FE does not absorb the spatial pattern, so clustered-by-state SEs may be too small. 4e check A8 (Conley SEs) tests this.

### SLX (renew_share, clustered SEs)

| W | b1 | p(b1) | θ1 | p(θ1) | Total | p(total) |
|---|---|---|---|---|---|---|
| invdist-50 | −0.0136 | 0.014 | −0.0551 | 0.117 | −0.0686 | 0.068 |
| invdist-48 | −0.0136 | 0.014 | −0.0562 | 0.121 | −0.0698 | 0.071 |
| border-48  | −0.0135 | 0.025 | −0.0299 | 0.108 | −0.0434 | 0.057 |

ln_ec and ln_ee: all null.

### SDM — renew_share (original 4d runs; impacts are means of draws)

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

## 3b. Revised main spec (added 2026-11-03)

Driver: `code/R/04d2_sdm_mainspec.R --date 2026-11-03`. Results: `results/2026-11-03/h3_mainspec/`. Rule: `EXPERIMENTS.md` §0 items 15–16.

**Rule outcome:** LYtrans=TRUE with demn=TRUE gives ρ = 0.814 (ln_ec), 0.610 (ln_ee), 1.406 (renew_share). renew_share is outside (−4.74, 1), so **LYtrans=FALSE is the main spec for all three**, with renew_share LYtrans=TRUE (demn=FALSE) kept as a labeled check.

**Main spec (invdist-50). Point estimates are plug-in values; p and CIs use 2,000 draws.**

| Outcome | ρ | b1 | θ1 | Direct (p) | Indirect (p) | Indirect 95% CI | Total (p) |
|---|---|---|---|---|---|---|---|
| ln_ec | 0.137 | −0.0027 | 0.0158 | −0.0026 (0.760) | 0.0178 (0.963) | −0.147, 0.226 | 0.0152 (0.969) |
| ln_ee | −0.018 | 0.0037 | −0.0064 | 0.0037 (0.916) | −0.0064 (0.997) | −0.229, 0.153 | −0.0027 (0.999) |
| renew_share | 0.617 | −0.0128 | −0.0549 | −0.0155 (<0.001) | −0.1613 (0.035) | −0.344, −0.035 | −0.1768 (0.026) |

For ln_ec and ln_ee, 7–10% of ρ draws fall out of range and inflate the draw SE, so read the CIs rather than the p-values.

**H3 verdict (main spec: SDM, LYtrans=FALSE, inverse-distance W, 50 states):** borderline: the renew_share spillover is negative (indirect −0.161) with p = 0.035 in the main spec, and p between about 0.03 and 0.09 across the other SDM versions and border W; in the SLX, θ1 has p about 0.11–0.12 and the total has p about 0.06–0.07. No spillover for ln_ec or ln_ee in the main spec.

**Other renew_share indirect effects:** LYtrans=TRUE on invdist-50 −0.244 (p = 0.058); LYtrans=FALSE on invdist-48 −0.159 (p = 0.037); LYtrans=FALSE on border-48 −0.045 (p = 0.087); LYtrans=TRUE on border-48 −0.032 (p = 0.033). LYtrans=TRUE with demn=TRUE fails the rule, so its rows are not counted.

**W·AI variation after state and year FE:** within-state SD 0.086 on invdist-50 (11.5% of variance left) vs 0.248 on border-48 (17.1% left). Per one-within-state-SD change in neighbors' AI, the main-spec indirect effect is −1.4 percentage points on invdist-50 and −1.1 on border-48. These are associations.

---

## 4. What did not change

- Panel and H1/H2 results unchanged.
- W matrices unchanged (data/out/).

---

## 5. Decisions still open

| Item | Options | Deadline |
|---|---|---|
| LBNL RPS/CES control | Download spreadsheet; add to 4e robustness | Before 4e (Nov 17) |
| t-2/t-3 lags | **Closed 2026-11-03:** full-sample t-3 lags not run; see `EXPERIMENTS.md` §0 item 14 | — |
| SE choice for paper | CL vs DK; primary SE for H1 | Before draft (Nov 24) |

---

## How to resume

Read in this order:
1. `CLAUDE.md` (project state)
2. `EXPERIMENTS.md` §0, §8–§9 (H3 spec, divergence register)
3. This file
4. `notebooks/04d_step3_spatial.ipynb`
5. `results/2026-11-03/h3/RECEIPT.md`

Then run: `prompts/04e_robustness_stretch.md`

Key result files:
- `results/2026-11-03/h3/h3_moran.csv` — Moran I all vars/years/W
- `results/2026-11-03/h3/h3_slx.csv` — SLX clustered SEs
- `results/2026-11-03/h3/h3_sdm_core.csv` — SDM ρ/b1/θ1
- `results/2026-11-03/h3/h3_sdm_impacts.csv` — direct/indirect/total
- `results/2026-11-03/h3/h3_splm_check.csv` — cross-check

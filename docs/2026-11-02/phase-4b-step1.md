# Phase 4b: Step 1 — Two-Way Fixed Effects
**Date:** 2026-11-02  
**Driver:** `code/R/04b_step1_twfe.R --date 2026-11-02`  
**Notebook:** `notebooks/04b_step1_twfe.ipynb`

---

## 1. What changed

- Created `code/R/04b_step1_twfe.R` — runs all 9 H1 experiments and writes outputs to `results/2026-11-02/h1/`, `results/2026-11-02/tables/`, `results/2026-11-02/figures/`.
- All five reproduce-gate coefficients match `econ499r_starter/reference/prelim_step1_slx.csv` exactly (diff = 0.00000 for all).
- Created `results/2026-11-02/h1/RECEIPT.md` documenting inputs, hashes, tags, N, and warnings.
- Created `notebooks/04b_step1_twfe.ipynb` (ir kernel) with one section per experiment.

---

## 2. Why (key decisions)

**Reproduce gate:** Uses a fresh panel read with prelim.py's exact winsorization spec (same 5 variables, no additional winsorization). load_panel.R's spec (more variables winsorized) is for the main analysis only, not for comparing against the Python reference.

**Heterogeneity moderators:** Defined from 2015 values frozen at baseline (`net_exporter_2015`, `high_price_2015`) so they cannot respond to the treatment variable AI. Merged from `dt[year == 2015, .]` rather than using the time-varying columns from load_panel.R. fixest drops the time-invariant main effects as collinear with state FE — this is expected and the interaction term is still identified.

**Dynamics:** QCEW 2012–2013 absent; t-2 and t-3 distributed lags were omitted. Only t-1 baseline and long-difference (ΔY 2015→2025 on ΔAI 2014→2024) run. Long-difference N = 46 (AK, ND, SD, WY dropped — suppressed 2025 AI counts).

**DK SEs smaller than clustered:** Driscoll-Kraay SEs are ~4× smaller than state-clustered for renew_share and ln_ee. This is interpretable: after year FE removes common time shocks, cross-sectional correlation is low, so DK does not inflate the SE. Report both; baseline = clustered (more conservative).

---

## 3. Decisions still open

| Item | Options | Deadline |
|---|---|---|
| LBNL RPS control (EXP-003) | Browser-download the LBNL spreadsheet; add RPS indicator to §9 robustness run | Before 04e (Nov 17) |
| t-2/t-3 distributed lags | Obtain QCEW 2012–2013 data | Before 04b re-run or 04e |
| EPU-S moderation stretch | Download Baker-Davis-Levy 2022 EPU-S panel | Stretch only |
| Report SE choice | Decide whether DK or clustered is "primary" for the final paper | Before paper draft (Nov 24) |

---

## 4. What did not change

- Equation: `Y = α₁·AI(t-1) + β·X + μᵢ + λₜ` unchanged from EXPERIMENTS.md §1.
- Tag grammar unchanged; all tags follow §12.
- load_panel.R unchanged; all main-analysis models call it.
- W matrices and spatial setup unchanged (used in 04d).
- Panel: `data/out/state_panel_2015_2025.csv` (561×80) unchanged.

---

## 5. Follow-ups for Alexander

- The only unambiguous significant result is **new_renew_mw** (b = +74.5 MW, p = 0.022, CL). This is the headline number for H1.
- **renew_share** is borderline under clustered SEs (p = 0.103) and significant under DK (p = 0.001) — but the sign is **negative** (peril direction, not blessing).
- The clearest H1 pattern is **heterogeneity**: high-electricity-price states show a significantly more positive AI–renewable share association (γ₁ = +0.032, p = 0.004). Worth emphasizing in the discussion.
- The **NAICS 518210 caveat** applies everywhere: the AI variable measures all data processing and hosting, not AI compute specifically. Georgia's high rank (2nd nationally in 2025) likely reflects cloud hosting, not AI training.

---

## How to resume

Read in this order:
1. `CLAUDE.md` (project state, conventions)
2. `EXPERIMENTS.md` §0–§5 (divergence register + H1/extras/nonlin/het/dyn specs)
3. This file
4. `notebooks/04b_step1_twfe.ipynb` (all results and readings)
5. `results/2026-11-02/h1/RECEIPT.md` (what ran, tags, N, warnings)

Then run: `prompts/04c_step2_mediation.md`

Key result files:
- `results/2026-11-02/h1/h1_core.csv` — H1 core (ln_ec, ln_ee, renew_share; ctrl4 and ctrl5)
- `results/2026-11-02/h1/h1_extras.csv` — solar, wind, new_renew_mw, fossil_to_renew, coal_share, co2_per_mwh_t
- `results/2026-11-02/h1/se_check.csv` — CL vs DK for core three outcomes
- `results/2026-11-02/h1/nonlinearity.csv` — quadratic models (all outcomes)
- `results/2026-11-02/h1/turning_points.csv` — turning point estimates with delta-method CI
- `results/2026-11-02/h1/heterogeneity.csv` — interaction terms (net_exporter, high_price, south)
- `results/2026-11-02/h1/dynamics.csv` — t-1 baseline + long difference
- `results/2026-11-02/h1/georgia_descriptive.csv` — Georgia AI and outcome paths vs US median

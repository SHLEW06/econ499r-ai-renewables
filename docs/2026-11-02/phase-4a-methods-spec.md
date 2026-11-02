# Phase 4a handoff — Methods spec and R environment (2026-11-02)

**Phase:** 4a  
**Status:** Complete  
**Next prompt:** `prompts/04b_step1_twfe.md`

---

## 1. What changed

**New files:**
- `EXPERIMENTS.md` — fully rewritten with §0 divergence register (all 11 items from methods-review.md §4), §1–§11 experiment blocks (equations, columns, support rules, output paths, method tags), §12 tag grammar, §13 analysis calendar
- `code/R/load_panel.R` — single panel loader called by every Phase 4 experiment; guarantees identical sample, winsorization, and W-matrix order
- `docs/2026-11-02/memo-corrections.md` — 11 copy-paste-ready prose fixes + 11 non-prose design decisions for Alexander
- `notebooks/04a_methods_spec.ipynb` — experiment-block equations, environment check, smoke-check tables
- `docs/2026-11-02/phase-4a-methods-spec.md` — this file

**Modified:**
- `CLAUDE.md` §2, §4, §5 — updated folder layout (code/R/, results/), R conventions, project state
- `EXPERIMENTS.md` — full rewrite (was a placeholder divergence register)

**R environment (installed 2026-11-02):**
- R 4.6.2 at `/opt/homebrew/bin/R`
- Packages: fixest 0.14.2, modelsummary 2.6.0, spdep 1.4-2, splm 1.6-5, SDPDmod 0.0.8, spatialreg 1.4-3, boot 1.3-32, data.table 1.18.6.1, dplyr 1.2.1, ggplot2 4.0.3, sf 1.1-3, IRkernel 1.3.2, renv 1.3.1
- IRkernel registered for Jupyter (`ir` kernel)

---

## 2. Why (decisions made)

**EXPERIMENTS.md structure:** Rewritten from the placeholder to match methods-review.md §5 block-for-block. The divergence register (§0) preserves all 11 agreed design changes with status. Tag grammar ensures result files are unambiguously tied to a spec.

**load_panel.R single-loader:** All experiments must produce comparable results. A shared loader that winsorizes identically and builds the same derived columns (coal_share, net_exporter, high_price, south, ai_sq_lag1, lag2, lag3, lead1, centered interaction terms) prevents accidental variation across scripts.

**W matrices:** Both `W_border_binary.csv` and `W_inverse_distance_rowstd.csv` load and row-standardise in the loader. Row-standardisation confirmed (sum of each row = 1 for rows with any neighbors). AK and HI are in the border W with zero rows — they have no contiguous neighbors; this is handled by the `contig48 == 1` filter used in H3.

**IRkernel:** Works. R code can be written directly in `.ipynb` notebooks. No Python fallback needed.

---

## 3. Decisions still open

| Item | Decision needed | Who |
|---|---|---|
| QCEW 2012–2013 | Download for t−3 lags (§5 dynamics)? Takes ~15 min via download_all.py | Shunji |
| RPS control (EXP-003) | LBNL file still needs browser download before 4e robustness | Alexander |
| EPU-S data (EXP-010) | Baker-Davis-Levy state indexes; stretch only | Alexander |
| Broadband / R&D data | Needed for stretch moderation; not blocking | Alexander |
| QCEW 2012–2013 for dynamics | Only needed for t−3 lag | Shunji |

---

## 4. What did NOT change

- Panel `data/out/state_panel_2015_2025.csv` (561×80) — not touched
- All raw data under `data/raw/` — not touched
- W matrix CSVs — not touched (loaded read-only)
- `data/DATA_VALIDATION.md` — not touched
- Smoke check N = 550 — confirmed correct

---

## 5. Follow-ups

- [ ] Alexander: review `docs/2026-11-02/memo-corrections.md` — 11 prose fixes + 11 non-prose design changes
- [ ] Before 4b: confirm `code/R/` is where experiment scripts will live; each script takes `--date YYYY-MM-DD`
- [ ] Before 4e: download LBNL RPS file (EXP-003 unblocked)
- [ ] Optional: download QCEW 2012–2013 if dynamics t−3 lags are needed

---

## How to resume

**Files to read first:**
1. `CLAUDE.md` (§4 conventions, §5 project state)
2. `EXPERIMENTS.md` (full spec; §0 divergence register; §12 tag grammar)
3. `code/R/load_panel.R` (understand what load_panel() returns before writing experiment scripts)
4. `data/DATA_VALIDATION.md` (carry the yellow-variable notes into any models that use co2_per_mwh_t or seds_mmbtu_pc)

**Next prompt:** `prompts/04b_step1_twfe.md`  
**Target date:** 2026-11-08  
**R binary:** `/opt/homebrew/bin/Rscript`  
**Working directory:** project root (`AI impact on Renewables/`)

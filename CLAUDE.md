# CLAUDE.md — Project Conventions for AI Impact on Renewables

## §1 Project Overview

Course: ECON 499R, Emory University, Fall 2026
Team: Shunji Lewandowski (modeling) and Alexander Hendricks (data/finance)
Advisor: Prof. Fohlin
Research question: Testing Zhang et al. (2026) "Blessing or Peril?" on 50 U.S. states, 2015–2025.

Deadlines:
- Steps 1–3 complete: Nov 17
- Draft: Nov 24
- Turn-in: Dec 1

---

## §2 Folder Layout

```
data/raw/<source>/          Raw files — never edit, treat as read-only
data/out/                   Panel build outputs:
                              state_panel_2015_2025.csv
                              W_border_binary.csv, W_inverse_distance_rowstd.csv
                              state_centroids_land.csv
data/                       DATA_AUDIT.md, DATA_INDEX.md, DATA_CATALOG.xlsx
data/receipts/              One .md per source documenting provenance
econ499r_starter/scripts/   Download and build scripts:
                              build_panel.py, ferc_fin.py, sec_fin.py,
                              build_xlsx.py, prelim.py, download_all.py
outputs/                    ECON499R_Data_Workbook_<date>.xlsx
notes/                      Context handoffs, Grijalva transcript, methods memo
literature/                 PDFs
code/R/                     R analysis scripts:
                              load_panel.R (single panel loader, call from all experiments)
docs/<YYYY-MM-DD>/          Dated handoffs per phase
logs/<YYYY-MM-DD>/          Move logs, build logs
results/<YYYY-MM-DD>/       Model outputs (append-only; each row has method tag + status)
notebooks/                  Jupyter notebooks (one per phase)
archive/                    Saved Claude chats
```

---

## §3 Rebuilding the Panel

```bash
python3 econ499r_starter/scripts/build_panel.py data/raw data/out
```

Run from project root. Takes ~30 seconds.
Dependencies: pandas, numpy, openpyxl, pyarrow.

---

## §4 Key Conventions

- **data/raw/ is read-only.** Never edit any file under data/raw/.
- **No invented data.** If a value is missing, leave it as NA and add a reason in the codebook.
- **Deviations from the Methods Memo** must be logged in EXPERIMENTS.md first with a reason, before running.
- **Script argument convention:** positional args only.
  - `build_panel.py <raw_dir> <out_dir>`
  - `ferc_fin.py <pudl_dir> <out_dir>`
- **Dated handoffs** go in `docs/YYYY-MM-DD/`.
- **Move logs** go in `logs/YYYY-MM-DD/phase2_moves.csv` with columns: old_path, new_path, sha256.
- **Models are Phase 4.** Use R 4.6.2 (installed at `/opt/homebrew/bin/R`). Packages: fixest, modelsummary, spdep, splm/SDPDmod, spatialreg, boot, data.table, ggplot2, sf, IRkernel, renv. Single loader: `code/R/load_panel.R`.
- **Results** go in `results/<YYYY-MM-DD>/<experiment>/`. Append-only. Every row carries a parseable method tag and status (ok / FAILED).
- **R drivers** take a required `--date YYYY-MM-DD` argument and fail-fast-check inputs.
- **Use "associated with,"** not "causes," unless the design supports causation.
- **IRkernel status:** to be confirmed (see Phase 4a smoke check). Fallback: Python notebooks that read R result CSVs.

---

## §5 Project state (as of 2026-11-03)

**Phase 4d complete.** H3 spatial analysis: Moran's I, SLX, SDM (SDPDmod), splm cross-check. renew_share shows significant spatial dependence; its spillover is negative and borderline (main spec p = 0.035).

- Phase 2A (audit): done — `data/DATA_AUDIT.md`, `docs/2026-11-01/phase-2a-data-audit.md`
- Phase 2B (build): done — `data/out/state_panel_2015_2025.csv` (561×80), workbook, receipts
- Phase 2C (validate): done — `data/DATA_VALIDATION.md`, `logs/2026-11-02/build/validation/`
- Phase 4a (spec + env): done — `EXPERIMENTS.md`, `code/R/load_panel.R`, `docs/2026-11-02/phase-4a-methods-spec.md`
- Phase 4b (TWFE): done — `code/R/04b_step1_twfe.R`, `notebooks/04b_step1_twfe.ipynb`, `results/2026-11-02/h1/`, `docs/2026-11-02/phase-4b-step1.md`
- Phase 4c (mediation): done — `code/R/04c_step2_mediation.R`, `notebooks/04c_step2_mediation.ipynb`, `results/2026-11-03/h2/`, `docs/2026-11-03/phase-4c-step2.md`
- Phase 4d (spatial): done — `code/R/04d_step3_spatial.R`, `notebooks/04d_step3_spatial.ipynb`, `results/2026-11-03/h3/`, `docs/2026-11-03/phase-4d-step3.md`

**Validation verdict:** 0 red, 3 yellow (co2_per_mwh_t, seds_mmbtu_pc, hma — 2025 gaps only), 17 green.

**R environment:** R 4.6.2 at `/opt/homebrew/bin/R`. All required packages installed (incl. SDPDmod, splm, spdep, sf, maps). See `code/R/load_panel.R`.

**H1 headline results (2026-11-02, ctrl4 baseline = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth):**
- new_renew_mw: **+70.8 MW per unit AI, p = 0.033** (CL) — positive in raw MW, driven by large-grid states; not robust to scaling (per-capacity p=0.616; per-capita p=0.212); LOSO [+54, +87]
- renew_share: −0.0101, p = 0.100 (CL) / p = 0.001 (DK) — negative sign (peril direction); DK sensitivity only (T=11)
- ln_ec, ln_ee: insignificant under CL (p=0.795, p=0.707); ln_ee borderline under DK (p=0.036, sensitivity only)
- Heterogeneity: AI × high_price on renew_share γ₁ = +0.032, p = 0.003 — negative in low-price states (−0.027, p<0.001), null in high-price states (+0.005, p=0.54); exploratory, 1 of 9 tests
- **ctrl4 is the H1 baseline.** ctrl5 (+ tech_share) retained as one sensitivity row only.

**H2 mediation results (2026-11-03, ctrl4, CL — negative for all):**
- tech_share (H2a main): first stage b1 = −0.000157, p = 0.454 — channel fails
- hma (H2a memo): b1 mechanically positive; downstream all non-significant — not supported
- ln_ea (H2b): first stage b1 = −0.003, p = 0.296 — ln_gdp_pc absorbs AI→EA (within-state r=0.943); channel fails
- All 9 Sobel p-values: 0.322–0.991; all 9 bootstrap CIs span zero
- share_mediated not meaningful: a1 not significantly different from zero for primary outcomes

**H3 spatial results (2026-11-03, main spec = SDM, LYtrans=FALSE, invdist-50; `results/2026-11-03/h3_mainspec/`; plug-in impacts):**
- Moran's I renew_share: I=0.094–0.157, p≤0.002 all years — significant positive clustering, rising over time
- Residual Moran's I after two-way FE: I=0.02–0.11, p<0.05 in 10 of 11 years — clustered-by-state SEs may be too small
- SLX renew_share: b1=−0.014(p=0.014), θ1=−0.055(p=0.117), total=−0.069(p=0.068)
- SDM renew_share: ρ=0.617, direct=−0.0155(p<0.001), indirect=−0.1613(p=0.035), total=−0.1768(p=0.026)
- SDM renew_share check (LYtrans=TRUE, demn=FALSE): ρ=0.776, indirect=−0.244(p=0.058), total=−0.261(p=0.049)
- SDM ln_ec/ln_ee: indirect CIs span zero. LYtrans=TRUE gives ρ>1 because its one-step bias formula overshoots
- Main-spec rule: LYtrans=TRUE with demn=TRUE gives ρ=1.406 for renew_share, so LYtrans=FALSE is main for all three (`EXPERIMENTS.md` §0 item 15)
- W·AI within-state SD after FE: 0.086 (invdist-50) vs 0.248 (border-48). Indirect per one SD: −1.4 vs −1.1 percentage points
- splm cross-check: b1 and θ1 match SDPDm LYtrans=FALSE to 5 d.p. — passes
- **H3 verdict (main spec: SDM, LYtrans=FALSE, invdist-50):** borderline: the renew_share spillover is negative (indirect −0.161) with p = 0.035 in the main spec, and p between about 0.03 and 0.09 across the other SDM versions and border W; in the SLX, θ1 has p about 0.11–0.12 and the total has p about 0.06–0.07. No spillover for ln_ec or ln_ee in the main spec.

**Next step:** Phase 4e — robustness, then stretch goals (`prompts/04e_robustness_stretch.md`). Target 2026-11-17. RPS control runs if `data/lbnl_rps_targets.csv` exists. Full-sample t-3 lags are dropped; see `EXPERIMENTS.md` §0 item 14.

---

## §6 Known Issues and Measurement Caveats

- **NAICS 518210 scope:** counts all data processing and hosting, not AI data centers specifically. Georgia ranks 2nd (above Virginia), which is suspicious and likely reflects colocation/cloud hosting, not AI compute.
- **Within-state AI variation is small:** SD of ai_dc_per1000 is approximately 0.57 per 1,000 workers. Coefficient estimates will be imprecise.
- **CO2 and SEDS data end in 2024:** year 2025 produces 51 NA rows in the panel (one per state).
- **Suppressed 518210 counts (2025):** AK, ND, SD, WY have suppressed BLS data — 4 NA rows for dc_jobs and ai_dc_per1000.
- **Border W matrix (W_border_binary.csv)** excludes AK and HI — neither has contiguous neighbors in the 48-state graph.
- **ln_ee and ln_gdp_pc use real (chained 2017) GDP.** The memo says "State GDP in $" without specifying. Real preferred; corr(real, nominal) = 0.98 under two-way FE.
- **Renewable share is utility-scale only.** Rooftop solar appears in retail sales but not in EIA state generation file.
- **Phase 5 (GitHub): clean the history before pushing.** `econ499r_starter/reference/Methods_Memo.pdf` and `Zhang_et_al_2026.pdf` were untracked on 2026-11-03 but are still in past commits.

---

## §7 Data Still Needed

See DATA_AUDIT.md for full details.

| Item | Method | Needed for |
|------|--------|------------|
| LBNL RPS/CES spreadsheet | Browser download | Step 4 RPS control (EXP-003) |
| Q1–Q4 2024 large-load reports (Docket 55378) | Browser, FERC | Georgia case box |
| NOAA HDD/CDD | Script | Climate control (optional) |
| NSF R&D by state | Script | Tech intensity control (optional) |
| Epoch data center counts | Script | Alternative AI measure (optional) |
| SEC company facts | sec_fin.py + SEC_USER_AGENT env var | Finance channel (optional) |

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
outputs/                    ECON499R_Master_Data_<date>.xlsx (older workbooks in outputs/old/)
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
- **No invented data.** If a value is missing, leave it as NA and add a reason in the registry.
- **After any data change, rerun `code/python/build_master_workbook.py --date YYYY-MM-DD`** and its companion scripts; commands are in `data/receipts/master_workbook.md`.
- **LibreOffice never saves the final workbook.** It recalculates a copy only; the build adds that copy's cached values and fails on a bad link (`code/python/workbook_finalize.py`, `code/python/check_workbook_links.py`).
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

## §5 Project state (as of 2026-11-04)

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
- **Earlier H3 verdict, before the spillover placebo; replaced by the readings below (main spec: SDM, LYtrans=FALSE, invdist-50):** borderline: the renew_share spillover is negative (indirect −0.161) with p = 0.035 in the main spec, and p between about 0.03 and 0.09 across the other SDM versions and border W; in the SLX, θ1 has p about 0.11–0.12 and the total has p about 0.06–0.07. No spillover for ln_ec or ln_ee in the main spec.

**Phase 4e robustness done (2026-11-04):** gate, A1-A8, P1, P2, RPS control, all-ownership AI, Gavins Point row and spillover placebo (`code/R/04e_robustness.R`, `code/R/04e2_spillover_placebo.R`, `results/2026-11-04/`, `notebooks/04e_robustness_stretch.ipynb`, `docs/2026-11-04/phase-4e-robustness-stretch.md`).

**Readings (team, 2026-11-04; these override the H1 and H3 wording above):**
- **renew_share:** next year's AI predicts this year's share (p = 0.006), and with both in one model the lag is about zero. Describe the negative association as reflecting where and when data-center jobs grow (reverse timing or selection), not AI lowering the renewable share.
- **new_renew_mw:** positive in raw MW, not robust to scaling, and its lead is also positive. With both in one model, neither is significant. Same caution.
- **H3:** On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate (-0.161, p = 0.035) can't be separated from this reverse timing. H3 is not supported.
- **RPS control and all-ownership AI:** they change no result. Holding Gavins Point in NE doesn't either.

**Fang test done (2026-11-04):** `code/R/04h_fang_test.R`, `results/2026-11-04/fang/`, `notebooks/04h_fang_test.ipynb`. Fang's +0.053 doesn't reproduce on current SEDS (-0.019, p = 0.317). EIA's Oct 2023 change to how SEDS counts wind, solar, hydro and geothermal (https://www.eia.gov/state/seds/seds-change/index.php) explains the sign (approx. old basis: +0.022 to +0.034; k = 2.3-2.9 is our approximation), not the full size. Final spec: postings -0.048 (p = 0.109), data-center jobs -0.057 (p = 0.208). Data-center jobs are the more reliable extension measure.

**Stretch and Georgia (2026-11-04):** shift-share IV uninformative (KP F = 2.81); no broadband or R&D interaction significant; Hansen not run (`results/2026-11-04/stretch/`). Georgia solar at 24% on IEA Stated Policies: $37.06/MWh in 2035, range $14.51-$50.40; not forecasts of ours (`results/2026-11-04/georgia_solar/`).

**Data corrections (2026-11-04):** `dc_wages_usd` is blank where suppressed (only change in the panel; SDM and other results stand). D23, receipts and C.6 corrected. See `data/receipts/README.md`.

**Finish run complete (2026-11-04; `docs/2026-11-04/finish-run-log.md`):** results pack, master workbook (`outputs/ECON499R_Master_Data_2026-11-04.xlsx`, Variable Finder from `data/variable_registry.csv`), project summary, results report (`outputs/ECON499R_Results_2026-11-04.pdf`), clean GitHub copy (`release/github/`; not pushed; see `CHECKLIST.md`) and team package (`release/results_and_data_2026-11-04.zip`). The Hansen threshold is dropped (`EXPERIMENTS.md` §0 item 30). Full-sample t-3 lags are dropped (`EXPERIMENTS.md` §0 item 14).

**Fixes before push (2026-11-04; `docs/2026-11-04/fixes-before-push.md`):** exploratory SLX note in findings; new `fig_h1_coefficients.png`; citations for Georgia commitments (Q2 2026 report, PDF p. 8), EIA's SEDS notice and IEA WEO tables; net-producer definitions (`code/R/04h2_fang_net_producer.R`); NOAA weather check on ln_ec (AI -0.0021, p = 0.711).

**Workbook links fix (2026-11-04; `docs/2026-11-04/workbook-links-fix.md`):** internal links are now true internal links, receipt links go to the private GitHub repo, and a Receipts tab covers offline use. No data changed. The repo's only collaborator is SHLEW06, so others need access for GitHub links.

**Next step:** team review for Nov 17; download the Q1-Q4 2024 large-load reports by browser; draft by Nov 24.

---

## §6 Known Issues and Measurement Caveats

- **NAICS 518210 scope:** counts all data processing and hosting, not AI data centers specifically. Georgia ranks 2nd (above Virginia), which is suspicious and likely reflects colocation/cloud hosting, not AI compute.
- **AI measure is private only:** "private data-center jobs per 1,000 workers." Government 518210 rows exist (largest shares: NM 24.6%, MN 10.3%, PA 9.4%, OH 6.0%) and are left out by team decision; `EXPERIMENTS.md` §0 item 24.
- **Within-state AI variation is small:** SD of ai_dc_per1000 is approximately 0.57 per 1,000 workers. Coefficient estimates will be imprecise.
- **CO2 and SEDS data end in 2024:** year 2025 produces 51 NA rows in the panel (one per state).
- **Suppressed 518210 counts (2025):** AK, ND, SD, WY have suppressed BLS data — 4 NA rows for dc_jobs and ai_dc_per1000.
- **Border W matrix (W_border_binary.csv)** excludes AK and HI — neither has contiguous neighbors in the 48-state graph.
- **ln_ee and ln_gdp_pc use real (chained 2017) GDP.** The memo says "State GDP in $" without specifying. Real preferred; corr(real, nominal) = 0.98 under two-way FE.
- **`new_renew_mw` has one known artifact:** Gavins Point (132.3 MW hydro) moves between NE and SD in EIA's file, giving false changes in 2016 and 2018. The panel keeps EIA's data as published (team decision); a labeled row holding it in NE changes nothing (71.0 vs 70.8 MW). The NE and NM 2017 blank-fuel rows are natural gas and don't affect it.
- **Renewable share is utility-scale only.** Rooftop solar appears in retail sales but not in EIA state generation file.
- **Phase 5 (GitHub): clean the history before pushing.** `econ499r_starter/reference/Methods_Memo.pdf` and `Zhang_et_al_2026.pdf` were untracked on 2026-11-03 but are still in past commits.

---

## §7 Data Status

See `data/DATA_VALIDATION.md` ("New data, Nov 4") and `data/receipts/README.md`.

| Item | Status | Used for |
|------|--------|------------|
| LBNL RPS/CES (label: "LBNL current RPS/CES schedule") | **Done** — `data/lbnl_rps_targets.csv` | Step 4 RPS control |
| NSF R&D by state (National Patterns Table 10, 2017-2023) | **Done** — `data/nsf_state_rd.csv` | Stretch moderator |
| Epoch data centers | **Done** — `data/epoch_ai_campuses_by_state.csv`. Context and Georgia box only, not a model variable | Georgia box |
| ACS broadband (S2801) | **Done** — `data/acs_broadband.csv`. B1 uses 2016-2024, without 2015 and 2020 | Stretch moderator |
| State EPU | **Done** — `data/epu_state_annual.csv` | Stretch moderator |
| OWID/IRENA solar, LBNL Utility-Scale Solar | **Done** | Phase 4f |
| Fang test data (AI Index postings, SEDS renewables, TETCD, NCSES) | **Done** — `data/fang_panel.csv`; `data/receipts/ai_index.md` | Fang test |
| NOAA HDD/CDD | **Done** — `data/noaa_degree_days.csv`, 48 states. Not in the panel; one check only (`code/R/04e4_weather_check.R`) | Weather check on ln_ec |
| Q1-Q4 2024 large-load reports (Docket 55378) | **Pending** — PSC document list returns 404 to scripts; browser download needed | Georgia case box |
| SEC company facts | Optional — sec_fin.py + SEC_USER_AGENT env var | Finance channel |

# EXPERIMENTS.md — Spec and Divergence Register

Phase 4 spec for ECON 499R: AI Impact on Renewables.  
Derived from methods-review.md §5. Every deviation from the Methods Memo is registered in §0 before being implemented. Never run a deviation without logging it here first.

---

## §0 Divergence Register

All 11 items from methods-review.md §4. Items 1–11 correspond to the numbered list there.

| # | What the Memo says | What we run | Why | Status |
|---|---|---|---|---|
| 1 | Report theta (W·AI coefficient) as the spillover for H3 | Report direct, indirect, and total impacts via LeSage/Pace (2009) decomposition using `spatialreg::impacts()` | theta alone is not the spillover when rho ≠ 0; the partial derivative matrix is the correct estimand | **Adopted** |
| 2 | H2a mediator = HMA (coupling index built from AI × tech_share) | Main: M = tech_share. Keep HMA as memo version, label its first-stage as uninformative | HMA is a function of AI, so regressing HMA on AI is positive by construction; tech_share tests H2a without the mechanical correlation | **Adopted** |
| 3 | No quadratic AI term; linear specification throughout | Add AI² as the main nonlinearity test (Melguizo et al. 2026); keep Hansen threshold as stretch only | Kuznets-type nonlinearity is theoretically plausible; turning point −b1/(2·b2) with delta-method SE and Lind-Mehlum test | **Adopted** |
| 4 | Electricity price included as control in core model | Run Step 1 with and without price control; report both columns side-by-side | Data-center demand can raise prices, so price may absorb part of the AI effect (bad control problem) | **Adopted** |
| 5 | Heterogeneity by subgroup (Fang: separate regressions) | Heterogeneity by interaction inside the two-way FE model: AI × net_exporter, AI × high_price, AI × south | Interaction-in-one-model is valid; separate regressions inflate type-I error and cannot test whether the difference is significant | **Adopted** |
| 6 | Core outcomes: ln_ec, ln_ee, renew_share only | Add solar_share, wind_share, new_renew_mw, co2_per_mwh_t (through 2024), coal_share as falsification | Solar largest in Fang; coal falsification check from Melguizo; all data already in panel | **Adopted** |
| 7 | No dynamics specification | Distributed lags AI t−1, t−2, t−3 and their sum; 2015-to-2025 long difference. Needs QCEW 2012–2013 for full t−3 | Short-run null / long-run positive is theoretically motivated (Zhao et al. 2024) | **Adopted in part; full-sample t−3 dropped (item 14)** |
| 8 | No comment on efficiency vs consumption sign expectation | Add one paragraph in §H1 core and in the results handoff explaining why both can hold or why efficiency may fall where AI grows | Wording only, no new code; prevents a misread of "efficiency increases" when data centers sit in the numerator of the ratio | **Adopted (wording)** |
| 9 | H2b reports ln_ea mediation straightforwardly | Keep as memo version but include a caveat: EA is nearly redundant under state FE because land area is constant | Within-state EA variation = nonfarm GDP variation, which ln_gdp_pc and pop_growth already capture | **Adopted (caveat note)** |
| 10 | No state EPU moderator | AI × EPU-S (Baker-Davis-Levy 2022) as a stretch moderator; mean-center before interacting | Fang et al. 2025 use EPU-S; confirms generalizability of AI-renewable link across political-economy conditions | **Stretch — data ready (`data/epu_state_annual.csv`)** |
| 11 | Georgia solar learning curve not in memo | Add Georgia solar cost projection to 2035 (Bolinger 2022 method); LR = 24% central; fan of 12/19/24/45% × 3 capacity paths | Answers "future of renewables" for Georgia case box; learning curves are correlations, not causal | **Adopted (Phase 4f)** |
| 12 | Core H1 model: 4 controls (ln_gdp_pc, manuf_share, price_c_kwh, pop_growth) | Add tech_share as 5th control (ctrl5) was considered but **rejected**: tech_share is the H2a mediator (Baron-Kenny M). Controlling for it in H1 removes the AI→tech_share→outcome pathway and a₁ no longer captures the total effect (bad control problem). Actual first-stage: tech_share on lagged AI b=−0.0165, p=0.43 — the claimed positive correlation does not hold. ctrl4 is the H1 baseline. ctrl5 retained as one labeled sensitivity row only. | **Rejected** |
| 13 | H2a/H2b method tags used ctrl5 | Tags corrected to ctrl4 in 04c_step2_mediation.R and EXPERIMENTS.md §6/§7. ctrl4 = H1 baseline; using ctrl5 in mediation would be circular when M=tech_share and inconsistent across mediators. | **Adopted (Phase 4c, 2026-11-03)** |
| 14 | Item 7 plans distributed lags t−1 to t−3 on the full sample | Full-sample t-3 lags not run (would need QCEW 2012-2013). The 4b long difference and 2017-2025 distributed lags cover short vs long run. | Team decision 2026-11-03: the extra QCEW years are not worth the cost, because 2017-2025 lags are possible with the existing 2014-2025 data | **Adopted 2026-11-03. 4b ran only t-1 and the long difference (`results/2026-11-02/h1/dynamics.csv`); the 2017-2025 distributed lags are approved for 4e as check P1, reporting the sum of the three lags with its SE.** |
| 15 | H3 tested with an SDM; no estimator named. 4d used LYtrans=TRUE as main on renew_share and LYtrans=FALSE as fallback for ln_ec, ln_ee | One estimator for all three outcomes. (a) Try SDPDm LYtrans=TRUE, demn=TRUE on invdist-50; if ρ is inside (−4.74, 1) for all three outcomes, that is the main spec. (b) Otherwise LYtrans=FALSE is the main spec for all three, with renew_share LYtrans=TRUE kept as a labeled check | A verdict should not mix estimators across outcomes | **Adopted 2026-11-03. Outcome: (b); ρ = 1.406 for renew_share under (a)** |
| 16 | Not specified | Impact point estimates are plug-in values at the estimated ρ, b1, θ1. Simulation draws are used only for SEs and CIs | `impactsSDPDm` reports means of draws; impacts are nonlinear in ρ, so the mean differs from the plug-in value (renew_share main total: −0.269 vs −0.261) | **Adopted 2026-11-03** |
| 17 | Not specified | A8: Conley SEs from state centroids at 500 and 1,000 km on the core outcomes and new_renew_mw. Labeled a check | Residual Moran's I is significant in 10 of 11 years after two-way FE, so clustered-by-state SEs may be too small | **Adopted 2026-11-03 (check only)** |
| 18 | "RPS" control, form unspecified | Target percent by state-year. States with no mandatory RPS/CES = 0. Voluntary goals = 0 with a flag column. Use the target in force each year under the law at that time if the file allows it; if it only has today's schedules, say so in the receipt and notebook | Dropping non-mandate states would lose them from the regression; later laws raised many targets, so current schedules overstate past targets | **Superseded 2026-11-04 by item 21** |
| 19 | Long difference (item 7) | P2: rerun with ΔAI 2014→2024, N = 50. 4b's rows stay in place, labeled as the version with the bug | Both 4b scripts labeled ΔAI 2014→2024 but used the 2025 value, which dropped AK, ND, SD, WY (N = 46). They also labeled classical SEs as HC0 | **Adopted 2026-11-03** |
| 21 | "RPS" control, form unspecified (replaces item 18's coding rules) | Main: `target_pct`, the larger of the RPS and CES targets each year, from LBNL's June 2026 file. Label: **"LBNL current RPS/CES schedule."** States with no entry = 0. Voluntary goals not coded; those states are 0. Checks: `rps_target_pct` (RPS only); the June 2023 edition's values, all of 2015-2025 and separately 2015-2023; main version without NY. Flag the 3 obligation conflicts (MT 2020; NY 2015, 2016) in the notebook | LBNL's Target Achievement file has no target levels, and LBNL revises past years between editions, so the file can't show what earlier law required. The larger-of rule avoids double counting. NY's series breaks in 2018 | **Adopted 2026-11-04 (team decision)** |
| 22 | Moderators, stretch goal B1: broadband, "years available" | Use S2801 for 2016-2024, without 2015 and without 2020 | Census changed the internet question in 2016; there's no 2020 1-year release | **Adopted 2026-11-04 (team decision)** |
| 23 | Not in memo; `CLAUDE.md` listed degree days as an optional control | NOAA degree days not done, and no substitute | NCEI unreachable on 2026-11-04; CPC is a different product | **Superseded 2026-11-04 by item 31** |
| 24 | Memo p. 4: AI is employment in NAICS 518210; ownership not stated | Main: private rows only (own_code 5), over all covered jobs. Name: **"private data-center jobs per 1,000 workers."** Check: private + published government jobs (own_code 1, 2, 3), one labeled 4e row | Government rows exist in every year, contrary to the original D23, so private-only is a choice. Keeps the main measure on commercial hosting. It also avoids a coverage break: published government rows jump from 5 in 2021 to 16 in 2022 as suppressed rows fall from 25 to 13 | **Adopted 2026-11-04 (team decision)** |
| 25 | Memo pp. 9, 11: population from Census county data 2020-2025 and BEA 1969-2024; "population growth (Census)" | BEA SAINC1 line 2 for every year | One series with no splice. BEA's footnote gives Census midyear estimates as its source; all 3 cells the audit sampled match the newest Census series exactly | **Documented 2026-11-04** |
| 26 | Memo p. 11: Census 2010 state area file (Georgia 57,513 sq mi) | Sum of 2020 Gazetteer county land areas (Georgia 57,716.96 sq mi, +0.35%) | Same file supplies the centroids. Land area doesn't change over time, so state FE absorb the difference in `ln_ea` | **Documented 2026-11-04** |
| 27 | Memo p. 11: Census TIGER state boundary file for spatial weights | Centroids: land-weighted average of 2020 Gazetteer county points. Border W: 2023 county adjacency file | Built from files already downloaded. Effect on W against TIGER centroids not measured | **Documented 2026-11-04** |
| 28 | H3 tested only on W·AI(t−1) | Spillover placebo, invdist-50 (main) and border-48 (check), SLX (clustered) and SDM (LYtrans=FALSE main spec), all core outcomes. Versions: (a) AI(t−1), W·AI(t−1) on the same sample; (b) AI(t+1), W·AI(t+1); (c) AI(t−1), W·AI(t+1); (d) AI(t−1), W·AI(t−1), W·AI(t+1); (e) version (d) plus own AI(t+1). 2015-2023, N = 450 (432 on border-48) | The own-AI placebo fails for renew_share, and the spillover uses the same timing. W·AI(t+1) in 2024 would need 2025 AI for AK, ND, SD and WY, which BLS suppresses, and inverse-distance W gives every state weight on them, so 2024 is dropped to keep the panel balanced | **Adopted 2026-11-04 (team decision)** |
| 29 | Not specified | One labeled new_renew_mw row with Gavins Point (132.3 MW hydro) held in NE in every year. The panel keeps EIA's data as published | EIA's state file counts the plant in SD in 2016-2017, giving false changes in NE and SD in 2016 and 2018 | **Adopted 2026-11-04 (team decision)** |
| 30 | Hansen threshold as a stretch goal | Dropped. Stretch order: the Fang test, then shift-share IV, then broadband and R&D moderation | The placebo makes reverse timing the main question, which the IV addresses. The AI² model in 4b already covers nonlinearity | **Adopted 2026-11-04 (team decision)** |
| 31 | Not in memo; item 23 left degree days out because NCEI was unreachable | One labeled check: `ln_ec` on AI(t-1), ctrl4, two-way FE, clustered by state, plus annual HDD and CDD (thousands of degree days), 48 contiguous states, 2015-2025. Beside it: the same 48 states without weather, so a change can be read apart from dropping AK and HI. `code/R/04e4_weather_check.R` | NCEI answered on 2026-11-04 and the team asked for one check, reported whatever it shows. Replaces item 23's "not done". Source is nClimDiv's statewide files (`climdiv-hddcst`, `climdiv-cddcst`), not the CPC files item 23 rejected. Not added to the panel or to the baseline | **Adopted 2026-11-04 (team decision, logged before running)** |

---

### Winsorization clarification (Phase 4b, 2026-11-02)

§1 specifies winsorize "outcomes (ln_ec, ln_ee, renew_share) and AI." load_panel.R extends this to all extras outcomes: solar_share, wind_share, new_renew_mw, co2_per_mwh_t, fossil_to_renew, seds_mmbtu_pc. This is an application of the same 1/99 pooled policy to the additional outcomes in §2 — consistent with the spirit of §1. **Adopted (extension).**

### Data-section confirmations (from Phase 2C, 2026-11-02)

These are confirmed choices embedded in the panel, not model deviations.

| Decision | Choice | Evidence |
|---|---|---|
| GDP in ln_ee and ln_gdp_pc | Real chained-2017 (BEA SAGDP9) | corr(real, nominal) = 0.976 under two-way FE; real removes inflation |
| AI numerator | Private 518210 only (own_code=5, agglvl=58): "private data-center jobs per 1,000 workers" | Team choice (§0 item 24). **Corrected 2026-11-04:** government rows do exist at state level |
| Fossil includes Other Gases | Yes | 0.34% of fossil; matches EIA source structure |
| Renewable = utility-scale only | Yes | Rooftop not in EIA state generation file |
| NE and NM 2017 blank-fuel capacity | Not reassigned | Natural gas per EIA-860 2017 (Rokeby 2-3; Hobbs CHW-T), so not renewable. `data/receipts/eia_state.md` |
| Gavins Point in `new_renew_mw` | Left as EIA publishes it (team decision; §0 item 29) | 132.3 MW hydro moves between NE and SD: false changes in 2016 and 2018. Holding it in NE changes nothing (71.0 vs 70.8 MW) |
| Validation verdict | 0 red, 3 yellow, 17 green | Full detail: data/DATA_VALIDATION.md |

---

## §1 H1 Core

**Question:** Is AI data-center concentration associated with state-level electricity consumption, energy efficiency, and renewable share?

**Equation:**
$$Y_{it} = \alpha_1 \, \text{AI}_{i,t-1} + \beta X_{it} + \mu_i + \lambda_t + \varepsilon_{it}$$

| Term | Column(s) |
|---|---|
| $Y_{it}$ | ln_ec, ln_ee, renew_share (separate regressions) |
| $\text{AI}_{i,t-1}$ | ai_dc_per1000_lag1 |
| $X_{it}$ | ln_gdp_pc, manuf_share, price_c_kwh, pop_growth (ctrl4 — baseline) |
| $\mu_i$ | state FE |
| $\lambda_t$ | year FE |

**Sample:** 50 states (DC dropped via is_dc==0), 2015–2025; N = 550 for lagged sample.  
**Fixed effects:** two-way (state + year).  
**SEs:** clustered by state (baseline); Driscoll-Kraay SEs reported alongside.  
**Winsorizing:** outcomes (ln_ec, ln_ee, renew_share) and AI at 1st/99th percentile over pooled 2015–2025 sample.  
**Price control variant:** run with and without price_c_kwh; report two columns.  
**Support rule:** $\hat{\alpha}_1 > 0$ for renew_share (AI raises renewable share). For ln_ec, sign could go either way; for ln_ee, explain that efficiency can rise or fall depending on whether GDP growth outpaces the load increase from data centers.  
**Output path:** `results/<date>/h1_core/`  
**Method tags:** `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4 = baseline); ctrl5 retained as one labeled sensitivity row.  
**Status:** Memo (adapted) — **COMPLETE 2026-11-02**

**Results (2026-11-02, ctrl4, CL — baseline):**

| Outcome | b | SE | p (CL) | p (DK) | N | Verdict |
|---|---|---|---|---|---|---|
| ln_ec | −0.0016 | 0.0060 | 0.795 | 0.246 | 550 | Does not support H1 |
| ln_ee | +0.0022 | 0.0058 | 0.707 | **0.036** | 550 | Does not support under CL; supports under DK (sensitivity only, T=11) |
| renew_share | −0.0101 | 0.0061 | 0.100 | **0.001** | 550 | Negative (peril direction); borderline CL, significant DK (sensitivity only) |

DK results are sensitivity checks only — with T=11, Bartlett lag ≈ 2, too short to fully capture serial correlation.

---

## §2 H1 Extras

**Question:** Does the AI association extend to solar and wind separately, new renewable capacity additions, CO2 intensity, and coal share (falsification)?

Same equation as §1 with additional outcomes.

| Outcome | Column | Support rule | Coverage |
|---|---|---|---|
| solar_share | solar_share | $\hat{\alpha}_1 > 0$ | 2015–2025 |
| wind_share | wind_share | $\hat{\alpha}_1 > 0$ | 2015–2025 |
| new_renew_mw | new_renew_mw | $\hat{\alpha}_1 > 0$ | 2015–2025 |
| co2_per_mwh_t | co2_per_mwh_t | $\hat{\alpha}_1 < 0$ | 2015–2024 (51 NAs in 2025) |
| coal_share | gen_coal_mwh / gen_total_mwh | Null expected (falsification) | 2015–2025 |

**SEs:** clustered by state + Driscoll-Kraay.  
**Output path:** `results/<date>/h1_extras/`  
**Method tags:** `h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4 = baseline).  
**Status:** Added — **COMPLETE 2026-11-02**

**Results (2026-11-02, ctrl4, CL — baseline):**

| Outcome | b | SE | p | Verdict |
|---|---|---|---|---|
| new_renew_mw | **+70.8 MW** | 32.3 | **0.033** | **Supports H1 — only unambiguous significant result** |
| solar_share | −0.0001 | 0.0030 | 0.984 | Null |
| wind_share | −0.0084 | 0.0067 | 0.213 | Null |
| fossil_to_renew | +0.997 | 0.619 | 0.114 | Wrong sign; does not support H1 |
| coal_share | +0.0020 | 0.0075 | 0.793 | Null — falsification passes |
| co2_per_mwh_t | +0.0025 | 0.0061 | 0.689 | Null |

---

## §3 Nonlinearity

**Question:** Is the AI–renewable share relationship non-monotonic (inverted-U or U-shape)?

**Equation:**
$$Y_{it} = \alpha_1 \, \text{AI}_{i,t-1} + \alpha_2 \, \text{AI}_{i,t-1}^2 + \beta X_{it} + \mu_i + \lambda_t + \varepsilon_{it}$$

| Term | Column |
|---|---|
| $\text{AI}^2_{i,t-1}$ | ai_dc_per1000_lag1² (computed in load_panel.R as ai_sq_lag1) |

**Outcomes:** ln_ec, ln_ee, renew_share.  
**Turning point:** $-\hat{\alpha}_1 / (2\hat{\alpha}_2)$ with delta-method SE. Report whether it falls inside the observed within-state range of ai_dc_per1000_lag1.  
**Lind-Mehlum test:** for an interior extremum.  
**Sample, FE, SEs:** same as §1.  
**Output path:** `results/<date>/nonlin/`  
**Method tags:** `nonlin_twfe_ai518210sq_lag1_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4 = baseline).  
**Status:** Added (replaces Hansen as main nonlinearity test) — **COMPLETE 2026-11-02**

**Results (2026-11-02, ctrl4, proper LM test):** Proper delta-method LM test (slope b₁+2b₂·AI must be one-sided significant at both min and max of AI, SE includes cov(b₁,b₂), threshold |t|>1.645) run for all 8 outcomes: **all 8 FAIL**. b₂ p-values range 0.234–0.864. Example: ln_ec b₂=−0.003 (p=0.364), t at min=+0.84, t at max=−0.91 — neither clears 1.645. **No statistically significant evidence of nonlinearity for any outcome.** Results in `lm_proper.csv` (ctrl4 rows).

---

## §4 Heterogeneity

**Question:** Does the AI association differ by net electricity export status, electricity price level, or Census region (South)?

**Equation:**
$$Y_{it} = \alpha_1 \, \text{AI}_{i,t-1} + \gamma_1 (\text{AI}_{i,t-1} \times D_i) + \alpha_2 D_i + \beta X_{it} + \mu_i + \lambda_t + \varepsilon_{it}$$

| Moderator | Column | Definition |
|---|---|---|
| net_exporter | net_exporter (derived: gen_total_mwh > sales_mwh) | in-state generation exceeds retail sales that year |
| high_price | high_price (derived: price_c_kwh > national median by year) | above-median retail price that year |
| south | south (derived: Census South lookup) | AL, AR, DC, DE, FL, GA, KY, LA, MD, MS, NC, OK, SC, TN, TX, VA, WV |

**Note:** Mean-center AI and $D_i$ before interacting (done in load_panel.R).  
**Outcomes:** renew_share, ln_ec, ln_ee.  
**Output path:** `results/<date>/het/`  
**Method tags:** `het_twfe_ai518210_lag1_<mod>_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4 = baseline).  
**Status:** Added (from Fang et al. 2025, done better) — **COMPLETE 2026-11-02**

**Results (2026-11-02, ctrl4, renew_share):** AI × high_price_2015: γ₁ = +0.032, p = **0.003** — significant. High-price states show more positive AI–renewable association. AI × net_exporter_2015: γ₁ = −0.019, p = 0.091 — borderline. AI × south: γ₁ ≈ 0, p = 0.992 — null. Exploratory: 9 tests total (3 moderators × 3 outcomes); AI×high_price survives Bonferroni (0.05/9 = 0.0056). Sign was not pre-specified.

---

## §5 Dynamics

**Question:** Do AI data centers have different short-run vs. long-run associations with renewable energy outcomes?

**Equation (distributed lags):**
$$Y_{it} = \sum_{k=1}^{K} \alpha_k \, \text{AI}_{i,t-k} + \beta X_{it} + \mu_i + \lambda_t + \varepsilon_{it}$$

| Lag | Column | Needs |
|---|---|---|
| t−1 | ai_dc_per1000_lag1 | Already in panel |
| t−2 | ai_dc_per1000_lag2 | 2013 QCEW |
| t−3 | ai_dc_per1000_lag3 | 2012 QCEW |

**Sum:** $\sum_{k=1}^{3} \hat{\alpha}_k$ = medium-run cumulative association.  
**Long difference:** $\Delta Y_{i,2025-2015}$ on $\Delta \text{AI}_{i,2025-2015}$ with controls.  
**Sample:** 50 states; t−2 sample = 2017–2025; t−3 sample = 2018–2025.  
**Note:** Skip t−3 if 2012 QCEW not available.  
**Output path:** `results/<date>/dyn/`  
**Method tags:** `dyn_twfe_ai518210_lag<k>_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4 = baseline). Long-diff controls: dAI + dlngdp + dprice + dmanuf + dpop (no dtech — tech_share is mediator, omitted per ctrl4 spec).  
**Status:** Added — **PARTIAL COMPLETE 2026-11-02** (t-1 only + long difference; full-sample t-3 dropped per §0 item 14; 2017-2025 distributed lags run in 4e as P1)

**Bug in the results below (found 2026-11-03):** the code uses the 2025 AI value, so ΔAI is really 2014→2025, not 2014→2024 as labeled. That is why N = 46. The SEs labeled HC0 are classical. Corrected rerun: 4e check P2 (§0 item 19).

**Results (2026-11-02, ctrl4; version with the bug):** Long-difference results all insignificant (N = 46; AK, ND, SD, WY dropped). renew_share: b=−0.017, p=0.163. ln_ec: b=−0.009, p=0.342. ln_ee: b=+0.008, p=0.406. ΔAI (2014→2024) has no detectable association with ΔY (2015→2025). Consistent with small within-state AI variation (SD ≈ 0.57).

---

## §6 H2a — Mediation: Tech Workers

**Question:** Does AI data-center activity predict renewable outcomes through the technology-worker share (main) or HMA (memo)?

**Equations (Baron-Kenny three-step):**
$$Y_{it} = c_1 \, \text{AI}_{i,t-1} + \beta X + \mu_i + \lambda_t \tag{total effect}$$
$$M_{it} = a_1 \, \text{AI}_{i,t-1} + \beta X + \mu_i + \lambda_t \tag{first stage}$$
$$Y_{it} = c'_1 \, \text{AI}_{i,t-1} + b_1 M_{it} + \beta X + \mu_i + \lambda_t \tag{direct effect}$$

**Mediators:**

| Version | M column | Note |
|---|---|---|
| Main | tech_share | NAICS 5415 / total covered employment |
| Memo | hma | Built as AI × tech_share; first stage is mechanically positive — uninformative as falsification |

**Indirect effect:** $\hat{b}_1 \hat{e}_1$ with Sobel test + cluster bootstrap (999 reps, seed=42) for 95% CI.  
**Outcomes:** ln_ec, ln_ee, renew_share.  
**Support rule:** $\hat{b}_1 \hat{e}_1 > 0$ for renew_share (AI → more tech workers → more renewables).  
**Output path:** `results/2026-11-03/h2/`  
**Method tags:** `h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4; corrected from ctrl5 per §0 item 13)  
**Status:** Memo + change — **COMPLETE 2026-11-03**

**Results (2026-11-03, ctrl4, CL):**

| Mediator | Outcome | b1 (AI→M) | p(b1) | e1 (M→Y) | p(e1) | Indirect | Sobel p | Boot 95% CI | Channel? |
|---|---|---|---|---|---|---|---|---|---|
| tech_share_c | ln_ec | −0.000157 | 0.454 | −3.872 | 0.285 | +0.000608 | 0.536 | [−0.0020, +0.0032] | **No** |
| tech_share_c | ln_ee | −0.000157 | 0.454 | +6.006 | 0.145 | −0.000943 | 0.501 | [−0.0044, +0.0025] | **No** |
| tech_share_c | renew_share | −0.000157 | 0.454 | −1.179 | 0.816 | +0.000185 | 0.823 | [−0.0019, +0.0044] | **No** |
| hma | ln_ec | +0.042 | <0.001* | −0.001 | 0.991 | −0.000059 | 0.991 | [−0.0104, +0.0124] | **No** |
| hma | ln_ee | +0.042 | <0.001* | +0.124 | 0.524 | +0.005184 | 0.522 | [−0.0104, +0.0219] | **No** |
| hma | renew_share | +0.042 | <0.001* | −0.135 | 0.412 | −0.005613 | 0.409 | [−0.0217, +0.0066] | **No** |

*hma b1>0 is mechanical (HMA = AI × tech_share). First stage uninformative.  
tech_share mean-centered (grand mean = 0.01272 subtracted).  
**No H2a channel holds.** tech_share first stage fails (p=0.454). HMA downstream fails despite mechanical b1.

---

## §7 H2b — Mediation: Economic Density

**Question:** Does AI predict renewable outcomes through higher economic density (nonfarm GDP per square mile)?

Same three-step structure as §6 with M = ln_ea.

**Caveat (§0 item 9):** ln_ea is nearly redundant under state FE because land_sqmi is constant within states; within-state variation in EA is entirely driven by nonfarm GDP growth, which ln_gdp_pc and pop_growth already capture. **Confirmed 2026-11-03: within-state cor(ln_ea, ln_gdp_pc) = 0.943.**  
**Output path:** `results/2026-11-03/h2/`  
**Method tags:** `h2b_med_ai518210_lag1_M-lnea_ctrl4_w9901_cl-state_<outcome>_50s2015_2025` (ctrl4; corrected from ctrl5 per §0 item 13)  
**Status:** Memo (with redundancy caveat) — **COMPLETE 2026-11-03**

**Results (2026-11-03, ctrl4, CL):** b1 = −0.003362, p = 0.296 for all outcomes (single first-stage equation). Channel fails at first stage for all three outcomes. ln_gdp_pc absorbs AI→EA pathway (r=0.943 within state). Downstream (eq-b, eq-c) significant for ln_ec and ln_ee but irrelevant given broken first stage.

| Outcome | b1 (AI→ln_ea) | p(b1) | e1 (ln_ea→Y) | p(e1) | Indirect | Sobel p | Boot 95% CI | Channel? |
|---|---|---|---|---|---|---|---|---|
| ln_ec | −0.003362 | 0.296 | −0.333 | 0.018 | +0.001120 | 0.332 | [−0.0008, +0.0051] | **No** |
| ln_ee | −0.003362 | 0.296 | +0.403 | 0.006 | −0.001355 | 0.322 | [−0.0058, +0.0010] | **No** |
| renew_share | −0.003362 | 0.296 | −0.254 | 0.240 | +0.000855 | 0.430 | [−0.0009, +0.0050] | **No** |

---

## §8 H3 — Spatial

**Question:** Does AI concentration in one state spill over to neighboring states' renewable energy outcomes?

**Step 1 — Moran's I by year:**  
Compute Moran's I for renew_share residuals (after removing state+year FE) using both W matrices. Run for each year 2015–2025.

**Step 2 — SLX (baseline):**
$$Y_{it} = \alpha_1 \, \text{AI}_{i,t-1} + \theta_1 (W \cdot \text{AI}_{t-1})_i + \beta X + \mu_i + \lambda_t + \varepsilon_{it}$$

SLX has no $\rho$ term; $\hat{\theta}_1$ is the spillover directly.

**Step 3 — SDM (main):**
$$Y_{it} = \rho (W \cdot Y_t)_i + \alpha_1 \, \text{AI}_{i,t-1} + \theta_1 (W \cdot \text{AI}_{t-1})_i + \beta X + \mu_i + \lambda_t + \varepsilon_{it}$$

Report direct, indirect (spillover), and total effects with simulated SEs via `spatialreg::impacts()`.

| W matrix | File |
|---|---|
| Border (binary contiguity) | data/out/W_border_binary.csv |
| Inverse-distance (row-std) | data/out/W_inverse_distance_rowstd.csv |

**H3 support rule:** Indirect effect < 0 for renew_share (siphoning); > 0 for ln_ec; < 0 for ln_ee.  
**Main W:** invdist-50 (all 50 states). Border-48 and invdist-48 are checks.  
**Output path:** `results/2026-11-03/h3/`  
**Method tags:** h3_moran/slx/sdm with W_version and LYtrans columns  
**Status:** Memo + change (impacts decomposition per §0 item 1) — **COMPLETE 2026-11-03**

**Results (invdist-50, all outcomes):**

**Moran's I — renew_share:** I=0.094–0.157, p≤0.002 all years 2015–2025. Significant positive spatial clustering, rising over time.

**SLX (renew_share, clustered SEs):**
- b1=−0.014 (p=0.014), θ1=−0.055 (p=0.117), total=−0.069 (p=0.068)
- ln_ec, ln_ee: all null

**SDM (renew_share):**
- LYtrans=TRUE (valid, ρ=0.776): direct=−0.017(p=0.001), indirect=−0.252(p=0.063), total=−0.269(p=0.054)
- LYtrans=FALSE (ρ=0.617): direct=−0.015(p<0.001), indirect=−0.165(p=0.038), total=−0.181(p=0.029)

**ρ out of range:** LYtrans=TRUE gave ρ>1 for ln_ec and ln_ee with invdist W. This is the one-step bias formula overshooting, not a convergence failure.

**splm cross-check:** b1 and θ1 match to 5 d.p.; ρ differs slightly (ML approximation). Cross-check passes.

**Revised main spec (2026-11-03, §0 items 15–16):** LYtrans=FALSE for all three outcomes, because LYtrans=TRUE with demn=TRUE gives ρ = 1.406 for renew_share. Plug-in impacts on invdist-50: renew_share ρ=0.617, direct=−0.0155 (p<0.001), indirect=−0.1613 (p=0.035), total=−0.1768 (p=0.026). Results: `results/2026-11-03/h3_mainspec/`. The results listed above are the original 4d runs, and their impacts are means of draws.

**H3 reading (team, 2026-11-04; replaces the verdict below):** On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate (-0.161, p = 0.035) can't be separated from this reverse timing. H3 is not supported.

**Earlier H3 verdict, 2026-11-03, before the spillover placebo (main spec: SDM, LYtrans=FALSE, inverse-distance W, 50 states):** borderline: the renew_share spillover is negative (indirect −0.161) with p = 0.035 in the main spec, and p between about 0.03 and 0.09 across the other SDM versions and border W; in the SLX, θ1 has p about 0.11–0.12 and the total has p about 0.06–0.07. No spillover for ln_ec or ln_ee in the main spec.

---

## §9 Robustness

Follows `prompts/04e_robustness_stretch.md`. Core outcomes = ln_ec, ln_ee, renew_share. Controls = ctrl4 throughout. Clustered-by-state SEs are the basis for every conclusion.

| Check | Model | Outcome(s) | Expected | Note |
|---|---|---|---|---|
| fossil_to_renew | §1 model, swap Y | fossil_to_renew | $\hat{\alpha}_1 < 0$ supports H1 | N = 550 |
| SEDS energy per person | §1 model, swap Y | seds_mmbtu_pc | Ambiguous | 2015–2024; N = 500 |
| Data-center MW | §1 model, swap AI | all core | — | Only if Phase 2 built a state-year series; otherwise a "not run" row with the reason |
| Drop 2020 | §1, year ≠ 2020 | all core | Stable | COVID outlier check; N = 500 |
| Drop AK, HI | §1, contig48==1 | all core | Stable | Energy-isolated states; N = 528 |
| Drop VA | §1, state ≠ 'VA' | all core | Stable | Outlier state; N = 539 |
| Border W | §8 SLX only, border-48 | all core | Stable | N = 528. The border-W SDM is not rerun; cite `results/2026-11-03/h3/h3_sdm_impacts.csv` |
| RPS control: LBNL current RPS/CES schedule | Add `target_pct` | all core, new_renew_mw | Shrinks $\hat{\alpha}_1$ | Main RPS version (§0 item 21); N = 550 |
| RPS check: RPS only | Add `rps_target_pct` | all core, new_renew_mw | — | Labeled check; N = 550 |
| RPS check: June 2023 edition | Add `target_pct_ed2023`, 2015-2025; and on 2015-2023 beside the main version on the same years | all core, new_renew_mw | — | Labeled check; N = 550 and N = 450 |
| RPS check: without NY | Main version, state ≠ 'NY' | all core, new_renew_mw | — | NY's series breaks in 2018; N = 539 |
| AI with all ownerships (added 2026-11-04) | §1 with AI numerator = private + published government 518210 jobs | all core, new_renew_mw | Stable | Labeled check (§0 item 24); N = 550 |
| Next-year-AI placebo | Replace AI(t−1) with AI(t+1) | all core | Null | Falsification; 2015–2024, N = 496 (AK, ND, SD, WY lose 2024) |
| Placebo diagnostics (added 2026-11-03) | Same placebo with the lead not winsorized; and AI(t+1) and AI(t−1) in one model | all core, new_renew_mw | — | Run because the placebo is significant for renew_share and new_renew_mw. Labeled diagnostics; N = 496 |
| Gavins Point held in NE (added 2026-11-04) | §1 with new_renew_mw adjusted for NE and SD in 2016 and 2018 | new_renew_mw | — | Labeled check (§0 item 29); N = 550 |
| Spillover placebo (added 2026-11-04) | §8 SLX and SDM with W·AI(t+1) | all core | θ and indirect effect about 0 | Labeled falsification (§0 item 28); `results/<date>/h3_placebo/` |
| Spec curve: new_renew_mw | §1 model, swap Y | new_renew_mw, raw and per 1,000 MW of 2015 capacity | — | Only positive raw-MW result; not robust to scaling in 4b |
| Driscoll-Kraay SEs | Re-run §1 | all core | Often smaller with T = 11 | Labeled sensitivity only; never the basis for a conclusion |
| A8: Conley SEs | Re-run §1; `fixest` Conley from state centroids, 500 and 1,000 km | all core, new_renew_mw | — | Labeled check (§0 item 17) |
| P1: Distributed lags | AI t−1, t−2, t−3 and their sum with delta-method SE; lags built from ai_dc_per1000_lag1 so 2014 is usable | all core, new_renew_mw | — | 2017–2025; N = 450. t−1 alone on the same sample shown beside it (§0 item 14) |
| P2: Corrected long difference | ΔY 2015→2025 on ΔAI 2014→2024 + Δcontrols; heteroskedasticity-robust SEs | all core | — | N = 50 (§0 item 19) |

### Readings (team, 2026-11-04)

- **renew_share:** next year's AI predicts this year's share, and with both in one model the lag is about zero. Describe the negative association as reflecting where and when data-center jobs grow (reverse timing or selection), not AI lowering the renewable share.
- **new_renew_mw:** positive in raw MW, not robust to scaling, and its lead is also positive. With both in one model, neither is significant. Same caution.
- **H3:** On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate (-0.161, p = 0.035) can't be separated from this reverse timing. H3 is not supported. (`results/2026-11-04/h3_placebo/`)
- **RPS control and all-ownership AI:** they change no result.

**Output path:** `results/<date>/robustness/`  
**Method tags:** `rob_<spec>_ai518210_<lag>_ctrl4_w9901_cl-state_<outcome>_<sample>`  
**Status:** Memo + added

---

## §9b Fang Test

Follows `prompts/04h_fang_test.md`. Tests Fang, Lee & Li (2025), *Renewable Energy* 246, 122969, on Fang's variables, alongside the Zhang test (4b-4e). Output: `results/<date>/fang/`, tags prefixed `fang_`. **Status: done 2026-11-04.** Results: `results/2026-11-04/fang/`. Handoff: `docs/2026-11-04/phase-4h-fang-test.md`.

**Model (Fang eq. 2, all variables in logs, state FE):**
$$\ln ET_{it} = \beta_0 + \beta_1 \ln AI_{it} + \beta_2 \ln EPU_{it} + \sum_k \beta_k \ln CV_{kit} + \alpha_i + \varepsilon_{it}$$

**Columns (`data/fang_panel.csv`):** ET `re_bbtu`; AI `ai_postings` (Fang) and `dc_jobs` (ours), with `ai_dc_per1000` as a check; EPU `epu_composite`; EP `ep_tetcd`; GDP `gdp_real_musd2017`; POP `population`; EDU `edu_bach_per1000`.

**Fang's Table 2 AI coefficients, columns 1-6:** 0.0428, 0.0452, 0.0396, 0.0548, 0.0561, 0.0531. N = 204.

### Readings (2026-11-04)
All are associations. Data-center jobs (BLS, one consistent series) are the more reliable extension measure.
- **Replication doesn't reproduce on current SEDS.** Column 6 is -0.0188 (p = 0.317) against Fang's +0.0531. EIA changed how SEDS counts wind, solar, hydro and geothermal in Oct 2023 (https://www.eia.gov/state/seds/seds-change/index.php). k = 2.3-2.9 is our approximation of the old accounting. On an approximate rebuild of the old basis (k = 2.6), column 2 is +0.0342 (p = 0.025; Fang +0.0452) and column 6 is +0.0216 (p = 0.287). So the accounting change explains the sign, but the rebuild is smaller than Fang's and column 6 isn't significant.
- **Bridge:** on current SEDS, adding year FE moves postings to -0.1095 (p = 0.004). With the lag, clustering and longer sample, neither measure is significant: postings -0.0479 (p = 0.109), data-center jobs -0.0567 (p = 0.208).
- **EPU moderation:** in Fang's spec AI x EPU is positive for all three EPU measures (state: 0.0193, p = 0.002; Fang 0.0160). Under two-way FE, none is significant.
- **Placebo:** no failure, but it's weak evidence, because AI(t-1) isn't significant either and lead and lag correlate at about 0.71-0.72.
- **Robustness:** only postings with ctrl4 is significant (-0.0616, p = 0.034). The RPS control changes no result.
- **Heterogeneity:** exploratory, with no multiplicity correction. Fang's subgroup pattern doesn't reproduce.

### Reading the two AI measures
**In the postings extension (2019-2024), almost every year comes from a different edition. So a state's year-to-year change mixes real change with method changes.** Year effects remove shifts that hit all states proportionally. The share-of-national row can't test this: once year effects are in, it equals the postings row by construction (-0.0475 vs -0.0479). Anything uneven stays in as noise, and the edition overlap and share-change tables are the evidence on that. Data-center jobs (BLS, one consistent series) remain the more reliable extension measure.

### Expected samples
| Step | Measure | N |
|---|---|---|
| Replication, 2018-2021, with DC | ln(postings) | 204 |
| Same-vintage sample, 2019-2021, no lag (added) | ln(postings) | 153 |
| Lag AI, 2019-2021 | ln(postings) | 153 |
| Extension with lag, 2019-2024, with DC / no DC | ln(postings) | 306 / 300 |
| Extension with lag, 2015-2024, with DC / no DC | ln(data-center jobs) | 510 / 500 |

### Divergence list (Fang test)
| # | What Fang does | What we run | Why | Status |
|---|---|---|---|---|
| F1 | Real GDP in chained 2012 dollars | Chained 2017 (BEA's current series) | The 2012-dollar series is no longer current. Logs absorb the base-year level but not chain revisions | **Adopted** |
| F2 | AI Index postings 2018-2021; source year by year not stated | 2018 from the 2019 edition; 2019-2021 from the 2022 edition. Same-vintage 2019-2021 row beside it (N = 153) | Only route to N = 204. The 2019 edition's 2019 stops in September, and Burning Glass expanded coverage in 2020 | **Adopted (team, 2026-11-04)** |
| F3 | SE type not stated | Conventional SEs first, as the likely match; clustered by state in the bridge | The paper says only "standard errors" | **Adopted** |
| F4 | Extreme-weather split | Not run | Fang's split counts extreme hot and cold weather occurrences per year (PDF p. 5). Degree-day totals aren't that count, so the Nov 4 degree-day download doesn't change this | **Not run** |
| F5 | Data as of the paper | Current vintages of SEDS, BEA, NCSES and EPU | Exact matches aren't possible; compare sign, size and significance | **Noted** |
| F6 | Splits at "the mean across the 51 states," period not stated | Each state's 2018-2021 average against the mean of those averages | Keeps each state in one group | **Adopted** |
| F7 | Wind N = 164 | Nonzero wind state-years are 165 | One state-year differs in current SEDS | **Noted** |
| F8 | State FE only | Bridge: add year FE, lag AI, cluster, extend, drop DC, one at a time. Our test uses two-way FE, lag and clustering | Shows which step changes the answer | **Adopted (prompt)** |
| F9 | ln(AI postings) only | Also ln(data-center jobs), with per-1,000 as a check | Our count, from one consistent series | **Adopted (prompt)** |
| F10 | No lag step on the same sample | Added bridge row: 2019-2021 without a lag, before the lag row | There's no 2017 postings data, so the lag also drops 2018; this separates the two | **Adopted (team, 2026-11-04)** |
| F11 | Levels of postings only | Added row after the sample extension: ln(state share of national postings) | Planned as a test of whether year effects absorb edition shifts. **Corrected 2026-11-04:** with year FE it equals the postings row by construction, so it confirms the algebra and isn't a test | **Adopted (team, 2026-11-04); not a test** |
| F12 | Separate subgroup regressions | Fang's splits for comparability; interactions in one model as our test | Same as §0 item 5 | **Adopted (prompt)** |
| F13 | No placebo | AI(t+1), and both in one model | Same concern as the Zhang test | **Adopted (prompt)** |
| F14 | Splits "at the mean" | Mean split as written, plus a labeled median split | Fang's group sizes (104/100, 108/96, 100/104, 96/108 state-years) look like median splits. A mean split gives 80, 56, 48 and 76 in the high group | **Adopted 2026-11-04** |
| F15 | Net producer: production above consumption, 76 state-years | Annual average generation above retail sales: 120 state-years | Fang's rule is electricity production above consumption from EIA (PDF p. 4); the series isn't stated. EIA generation includes plants' sales outside the state. Other definitions: F19 | **Noted** |
| F17 | Fang's source year by year isn't stated | Labeled replication variant: each year as first published (2018 and Jan-Sep 2019 from the 2019 edition; 2020 from the 2021 edition; 2021 from the 2022 edition) | Added because the main replication doesn't reproduce Fang's sign; tests whether vintage choice explains it | **Adopted 2026-11-04 (diagnostic)** |
| F18 | SEDS renewables as published through about 2021: fossil fuel equivalency for wind, solar, hydro and geothermal | Current SEDS: captured-energy approach at 3,412 Btu/kWh, adopted Oct 2023. Labeled sensitivity rebuilds `re_bbtu` as biomass + k x (wind + solar + hydro + geothermal), k = 2.3, 2.6, 2.9. It's approximate: k is one number across years and states, and geothermal and solar direct use are treated like electricity | EIA's notice: https://www.eia.gov/state/seds/seds-change/index.php. The change shrinks those fuels against biomass. Fang names no SEDS release and was received Dec 2024, but says EIA's data ended in 2021 (PDF p. 3), and its Table 2 constants imply a mean log outcome of about 11.79, which fits the old basis, not the current one (11.44): `results/2026-11-04/fang/seds_basis_level_check.csv`. Tests whether the vintage of the outcome explains the failed replication | **Adopted 2026-11-04 (diagnostic)** |
| F19 | Net producer, Fang's rule on electricity from EIA (PDF p. 4); N = 76 and 128 (Table 3) | Same split in Fang's spec on two other definitions, on each state's 2018-2021 average: SEDS total energy production above consumption, and SEDS net interstate electricity flow below zero. `code/R/04h2_fang_net_producer.R` | Our main rule gives 120, not 76. Total energy gives 40, closer by count though not Fang's stated concept (electricity). Interstate flow gives 104, the closest electricity rule tried. None reaches 76 | **Adopted 2026-11-04 (team request, logged before running)** |
| F16 | Main postings series for the extension | Stays the stitched series, by edition. "Lightcast's own series" (`fig_4.4.12`) covers only CA, NY, TX and WA, so it can't be the main measure | `prompts/06_finish.md` section 2 | **Adopted 2026-11-04** |

### Finalize (prompt 08, section 1), pre-registered 2026-11-07 before running
Driver: `code/R/04h3_fang_finalize.R --date 2026-11-07`. Output: `results/2026-11-07/fang/`, tags `fang8_...`. Data: `data/seds_old_basis.csv` and `data/storm_events_state.csv` (`econ499r_starter/scripts/build_finalize_tables.py`; receipts `seds_old_basis.md`, `noaa_storm_events.md`). Both AI measures (ln postings, ln data-center jobs) everywhere. **Fang's spec:** state FE, conventional SEs, logs, 2018-2021, 51 including DC, controls ln EPU, EP, GDP, POP, EDU. **Our spec:** two-way FE, AI(t-1), clustered by state, 50 states without DC, postings 2019-2024 and jobs 2015-2024, same Fang controls (as in the 11-04 bridge).

| # | Analysis | Outcome | Expected sign if Fang's story holds | Notes |
|---|---|---|---|---|
| F20 | Splits table (Fang Tables 3-5): electricity consumption, electricity price, net producer, R&D, per capita income, four Census regions, plus extreme weather (F22) | ln RE (current SEDS) | Fang: positive in L_EleC, H_ElePri, Net_EleC, L_Tech, H_Income, H_ExtrW, West, Midwest | Per group: separate regressions above/below the 51-state mean, the same with a median split, and the interaction (difference, SE, p), in Fang's spec and ours. Rows that ran on 11-04 are copied from `results/2026-11-04/fang/fang_results.csv`; new rows: our-spec separate regressions and the extreme-weather group. Net producer and regions are binary or categorical, so mean/median don't apply |
| F21 | Negative indicator (Fang Supplement B) | ln fossil-fuel consumption (SEDS FFTCB); fossil share of total energy, FFTCB / TETCB, in levels | Negative | Both specs |
| F22 | Extreme-weather split (Fang Table 4, cols 5-6) | ln RE | Positive in H_ExtrW, null in L_ExtrW | Count = NOAA Storm Events records with event type Excessive Heat, Heat, Extreme Cold/Wind Chill or Cold/Wind Chill, per state-year. Group = each state's 2018-2021 average count against the 51-state mean (Fang's rule), plus median. Check: distinct episodes in place of records |
| F23 | Exact old SEDS basis, year by year | ln RE rebuilt | Fang's Table 2: +0.043 to +0.056 | **Rule (replaces the single k of F18 as the main old-basis series):** convert only the electricity parts of wind, solar, hydro and geothermal with k_t = HR_t / 3.412, where HR_t is EIA's fossil-fueled plant heat rate; leave geothermal direct use and residential solar thermal unconverted. Component-by-component comparison with the June 2023 SEDS release showed exactly this pattern, so 08's wording "convert wind, solar, hydro and geothermal" is applied to their electricity only. The all-components version is kept as a check. HR_t from EIA's bulk MER series (wind fossil-fuel equivalent / wind captured x 3.412), which equals the archived SEDS FFETK 2015-2021 to 0.001; MER Table A6 itself couldn't be pulled by script. Also reported: Table 2 on the archived June 2023 SEDS values as published (2018-2021 only) |
| F24 | Table 2 replication, columns 1-6 | ln RE rebuilt; ln RE archived | as above | Four versions side by side: Fang | current | k = 2.6 | rebuilt; archived as a fifth column |
| F25 | Our final spec on the rebuilt basis | ln RE rebuilt | none expected | Two-way FE, lag, clustered, no DC |
| F26 | Event study (optional, 08 1.5) | ln RE, current SEDS; rebuilt as a check | Fang: post-2022 positive; pre-2022 flat | Exposure = state's 2019 share of U.S. postings from the 2022 edition only. Y = sum_k beta_k (Exposure x 1[year = k]) + state FE + year FE + ctrl4; base year 2021; 2015-2024; 50 states without DC; clustered by state. Joint Wald tests: pre (2015-2020) and post (2022-2024) |

| F27 | **Deviation, added 2026-11-07 after seeing F24:** the F20/F22 splits (Fang's spec only: separate regressions and the interaction difference) rerun on the archived June 2023 SEDS outcome, 2018-2021 | ln RE archived | As F20 | Added because Table 2 reproduces on the archived basis (Fang's numbers inside our 95% CIs in all six columns) but not on current SEDS, so the subgroup comparison is only fair on the archived basis. Labeled as added after results; the pre-registered current-basis rows stay the main F20 rows |

All F20-F27 rows are exploratory and reported in full; no multiplicity correction (as F12).

### Edition overlap (`data/receipts/ai_index.md`)
| Year | Edition A | Edition B | Pearson r, shares | Rank correlation | SD of ln(share ratio) | Median state gap |
|---|---|---|---:|---:|---:|---:|
| 2019 | 2019 edition, Jan-Sep | 2022 edition, full year | 0.9978 | 0.9954 | 0.162 | 14.8% |
| 2020 | 2021 edition | 2022 edition | 1.0000 | 0.9996 | 0.012 | 0.7% |
| 2021 | 2022 edition, PDF map | 2022 edition, sheet | 1.0000 | 1.0000 | 0.000 | 0.0% |

**Reading it:** the state pattern is very similar across editions, but high correlations are driven by the ordering of large and small states, so they don't clear within-state noise. For 2019 the median state's share still differs by 14.8% (SD of the log ratio 0.162), part of which is Jan-Sep against the full year. For 2020, with both full years, the median gap is 0.7%, so a one-year revision within Burning Glass is small.

---

## §10 Stretch (drop if behind on Nov 17 deadline)

| Goal | Equation | Key parameter | Effort | Status |
|---|---|---|---|---|
| Moderation: broadband × AI | AI × broadband + broadband main effect, centered; AI slope at p25, p75 | interaction coefficient | Medium | 2016-2024, no 2020 (§0 item 22); N = 400 |
| Moderation: R&D share × AI | AI × rd_share + rd_share main effect, centered; AI slope at p25, p75. rd_share = R&D / panel nominal GDP | interaction coefficient | Medium | 2017-2023; N = 350 |
| Moderation: EPU-S × AI | Run in the Fang test (§9b), composite, national and state | interaction coefficient | — | Not repeated in the Zhang spec (`prompts/06_finish.md` section 3 lists broadband and R&D only) |
| Shift-share IV | $Z_{it}$ = state 2015 share of national 518210 jobs × national jobs in $t-1$ excluding state $i$, indexed to 2015 ($\times$ 1,000). `feols(Y ~ ctrl4 | state + year | ai_lag1 ~ Z)`, clustered. First stage, reduced form, KP F, KP rank test. F < 10 means uninformative | IV 2nd-stage $\hat{\alpha}_1$ | Medium | Lag aligned to AI(t−1); the 2015 base falls inside the sample, so a 2014-base version is a check. N = 550 |
| Hansen threshold | energy_equity as threshold variable | threshold value | — | **Dropped 2026-11-04** (§0 item 30) |

**Readings (2026-11-04):** IV uninformative: KP F = 2.81 (below 10), KP rank LM p = 0.081. No AI x broadband or AI x R&D interaction is significant. Hansen threshold not run.

**Output path:** `results/<date>/stretch/`  
**Status:** Memo + added

---

## §11 Georgia Solar Module

**Question:** At what cost will utility-scale solar reach grid parity in Georgia by 2035?

**Learning-curve model (Bolinger et al. 2022):**
$$C_t = C_{\text{base}} \left(\frac{X_t}{X_{\text{base}}}\right)^b, \quad b = \frac{\ln(1-\text{LR})}{\ln 2}$$

| Parameter | Value |
|---|---|
| LR (central) | 24% → b ≈ −0.396 |
| LR fan | 12%, 19%, 24%, 45% |
| $X_t$ | Global cumulative PV capacity (IRENA/OWID) |
| $C_{\text{base}}$ | Georgia utility-scale solar LCOE in base year |

**Capacity paths (2026-11-04):** IEA *World Energy Outlook 2025*, Annex A: Current Policies 8,067 GW, Stated Policies 8,855 GW, Net Zero 12,499 GW in 2035, from 2,164 GW in 2024. IEA's growth ratios are applied to IRENA's series; years between are log-linear.  
**Base:** Georgia COD 2023-2025, capacity-weighted LCOE without tax credits, $63.81/MWh, 17 projects.  
**Readings (2026-11-04):** at 24% on the central path, $37.06/MWh in 2035; range $14.51-$50.40 across 12 trajectories. Not forecasts of ours. LCOE rose from $49.0 in 2022 to $61.0 in 2025, so the curve's assumption isn't visible in recent data.  
**Output:** fan chart: 4 learning rates × 3 capacity paths (low/central/high) = 12 trajectories.  
**Note:** Learning curves are correlations, not causal. Georgia has no state-specific learning rate.  
**Output path:** `results/<date>/georgia/`  
**Method tags:** `ga_solar_lc_lr<LR>_cap-<path>_2025_2035`  
**Status:** Added (Phase 4f)

---

## §12 Tag Grammar

Full tag: `<block>_<model>_<ai-var>_<lag>_<controls>_<winsor>_<se>_<outcome>_<sample>`

| Field | Allowed values | Example |
|---|---|---|
| block | h1, h1x, nonlin, het, dyn, h2a, h2b, h3, rob, stretch, ga, fang | h1 |
| model | twfe, slx, sdm, med, lc | twfe |
| ai-var | ai518210 (private), ai518210sq, ai518210allown (private + published government; check only) | ai518210 |
| lag | lag1, lag2, lag3, lag1to3sum, longdiff, lead1, lead1lag1 | lag1 |
| controls | ctrl4 (ln_gdp_pc + manuf_share + price_c_kwh + pop_growth; baseline), ctrl5 (ctrl4 + tech_share; one sensitivity row only) | ctrl4 |
| winsor | w9901 (1/99 pooled), nowins | w9901 |
| se | cl-state (clustered by state), dk (Driscoll-Kraay), conley500, conley1000, hc1, ml (asymptotic ML) | cl-state |
| outcome | ln_ec, ln_ee, renew_share, solar_share, wind_share, fossil_to_renew, co2_per_mwh_t, coal_share, new_renew_mw, seds_mmbtu_pc | renew_share |
| sample | 50s2015_2025, 48s2015_2025, 50s2015_2024, 50s2015_2025no2020, 49s2015_2025noVA, 49s2015_2025noNY, 50s2017_2025, 50s2015_2023 | 50s2015_2025 |

**Rule:** Never reuse a tag whose meaning has changed. Change the spec → create a new tag.

---

## §13 Analysis Calendar

| Phase | Target date | Hours | Notes |
|---|---|---|---|
| 4a — spec + env | 2026-11-02 | 3 h | Today |
| 4b — TWFE | 2026-11-08 | 3 h | H1 core, extras, nonlin, het, dyn |
| 4c — mediation | 2026-11-11 | 3 h | H2a + H2b |
| 4d — spatial | 2026-11-14 | 4 h | Moran, SLX, SDM, impacts |
| 4e — robustness (+stretch) | 2026-11-17 | 4 h | **Steps 1–3 deadline**; stretch only if core done |
| 4f — Georgia solar | 2026-11-18 | 2 h | Stretch — drop if behind |
| 4g — results pack | 2026-11-21 | 3 h | Tables, figures, findings.md |
| Draft | 2026-11-24 | — | Hard deadline |
| Turn-in | 2026-12-01 | — | Hard deadline |

---

## §14 Extensions, Nov 2026

Follows `prompts/09_extend.md`; run log `docs/2026-11-07/extend-run-log.md`. Output: `results/2026-11-07/extend/`, tags `ext_...`. Each block is written here before its models run.

### Shared rules for this section
- **Main spec:** 50 states (no DC), two-way FE (state, year), AI(t-1), ctrl4, SEs clustered by state, outcomes and AI winsorized 1/99 (pooled), via `code/R/load_panel.R`.
- **Two AI measures in every main-spec model:** (a) private data-center jobs per 1,000 workers (`ai_dc_per1000`, NAICS 518210); (b) AI job postings per 1,000 workers (`ai_postings` / `total_jobs` x 1,000, from `data/fang_panel.csv`). Postings exist 2018-2025, so their lag covers 2019-2025. The edition caveats in section 9b apply. Using postings per 1,000 workers rather than in logs keeps both measures on the same scale as the Zhang test.
- **Families and BH q-values:** (i) by type (section 2), (ii) AI-impact outcomes (section 3), (iii) AI index (section 5). Within a family, BH q-values run over all its main-spec AI(t-1) rows, both measures pooled.
- **A finding requires** q < 0.10, plus a lead placebo that is "clearly smaller": AI(t+1) in place of AI(t-1) on the same sample, with |lead| < 0.5 x |lag| and lead p >= 0.10. Lead placebos run for every row with p < 0.10 (section 2) or q < 0.10 (section 3).
- **Winsorizing new outcomes:** each new outcome is winsorized 1/99, pooled over its available state-years, the same way `load_panel.R` treats the existing outcomes.

### §14.1 Cross-check against Fang (no year FE), pre-registered 2026-11-07
| # | Item | Spec | Expected | Notes |
|---|---|---|---|---|
| E1 | Descriptive statistics | — | — | Fang's Table A1 is in Supplementary Material A, which isn't in `literature/` as of 2026-11-07. Fallback, as the prompt allows: **means implied by Table 2's constants.** With Stata-style FE constants (constant = mean(Y) - sum of b x mean(X)), columns 1-6 give six equations in seven unknown means. We fix one, the mean of ln AI postings, at our value (same AI Index source), then solve the rest column by column. Compared with our means on the three bases (only ET differs). The gap is in our SD units; flag > 0.25 SD. Unit-shift candidates: ln 1,000 = 6.908; chained 2012 vs 2017 dollars (ln of the GDP price index ratio, about 0.07) |
| E2 | Table 2, columns 1-6, with controls | Fang | — | Reuses the F24 rows (`results/2026-11-07/fang/`): Fang published, current, k = 2.6, rebuilt, plus archived. Fang inside our 95% CI marked |
| E3 | Linear trend | Fang col. 6 + (year - 2018), current and rebuilt, both AI measures | If Fang's positive comes from shared trends, the trend absorbs it | |
| E4 | Trend placebo | ln(industry employment) in place of ln AI. Fang col. 6 (state FE, conventional SEs, 2018-2021, with DC) and our main spec (lag, two-way FE, ctrl4, clustered, 50 states, 2015-2024, ln employment winsorized), outcome ln RE current and rebuilt | Fang's spec: positive for any variable that trends up with renewables; ours: null | **Candidates (chosen before any data):** 621610 home health care; 624120 services for the elderly and disabled; 621511 medical laboratories; 812910 pet care (except veterinary); 541940 veterinary services; 621493 freestanding ambulatory surgical centers; 561612 security guards; 621420 outpatient mental health centers; 812199 other personal care; 621340 offices of physical, occupational and speech therapists; 541613 marketing consulting; 312140 distilleries. **Excluded on purpose:** transportation and warehousing (fuel use, and biofuels sit inside SEDS renewables), utilities, mining, tech and information industries (AI-related), and retail (NAICS 2022 recoded it, breaking 2022-2024). **Selection rule:** national private employment (QCEW US000, own_code 5, annual average), log growth 2018-2021. Keep the two closest to AI postings' 0.760 (sum of 51, 2018 to 2021). Only national growth is looked at before the choice |

**E4 choice (2026-11-07, from national growth only; no regression run yet; `logs/2026-11-07/placebo_industry_selection.csv`):** 312140 distilleries (log growth 2018-2021 = 0.315) and 812910 pet care, except veterinary (0.139). No candidate came close to postings' 0.760, so these are the two closest by the rule, not matches. The other ten grew between -0.033 and 0.122.

### §14.2 By renewable type, pre-registered 2026-11-07 (family "bytype")
Main spec, both AI measures, BH q-values over all 38 rows (19 outcomes x 2 measures); lead placebo for every row with p < 0.10. Data: `data/extend_outcomes.csv` (`econ499r_starter/scripts/build_extend_tables.py`, same EIA files and filters as `build_panel.py`: Total Electric Power Industry, nameplate capacity). In-state, 2015-2025 (SEDS 2015-2024).

| Outcomes | Measures | Expected sign | Why |
|---|---|---|---|
| Wind, utility-scale solar | Share of in-state generation (levels, zeros kept); ln generation (zeros dropped, N reported); MW added per 1,000 MW of 2015 total capacity (net change in nameplate) | Share: negative. ln generation and additions: positive | Data-center load raises total generation, mostly from gas, so shares fall even when wind and solar grow. Corporate procurement by data-center operators would raise wind and solar generation and additions (Fang's story) |
| Hydro, geothermal, biomass (wood + other biomass) | Same three | Zero | Resource-fixed or declining; no channel from AI |
| Small-scale solar | — | — | **Not in the panel** (EIA's state generation file is utility-scale); skipped as the prompt allows |
| SEDS wood and waste (WWTCB); biofuels (BFTCB: fuel ethanol, biodiesel, renewable diesel, other, losses and co-products) | ln consumption, current basis | Wood/waste: zero. Biofuels: zero | Biofuels follow transport fuel demand |
| SEDS renewables without all biomass (RETCB - BMTCB); without biofuels only (RETCB - BFTCB) | ln consumption, current basis | Without biomass: positive; without biofuels: zero or positive | Tests whether the negative total (bridge, 11-04) is transport fuel rather than power |

Reference row, outside the family: ln RETCB (current) in the main spec.

**Georgia (section 2.4):** implied change = coefficient x Georgia's change in AI(t-1): jobs, 2015 to 2025 (AI 2014 to 2024); postings, 2019 to 2025 (AI 2018 to 2024), the window postings allow. 95% CI from the coefficient's CI. Placed next to Georgia's actual change in the outcome over the same window (SEDS ends 2024). "At most" uses the end of the 95% CI farthest from zero. Not a forecast.

### §14.3 What AI has been associated with, pre-registered 2026-11-07 (family "impact")
Main spec, both AI measures, BH q-values over all 30 rows (15 outcomes x 2 measures); lead placebo for every row with q < 0.10; for outcomes that pass, one model with AI x restructured.

| Outcome | Expected sign | Why |
|---|---|---|
| ln sales per person: commercial | Positive | Much data-center load is billed as commercial |
| ln sales per person: industrial | Zero or positive | Some data centers take industrial tariffs |
| ln sales per person: residential | Zero | No direct channel |
| Retail price, commercial, cents/kWh | Positive | Load growth raises capacity costs |
| Retail price, industrial | Positive | Same |
| Retail price, residential | Positive | Costs shifted across classes |
| Gas share of in-state generation | Positive | New load met mostly by gas |
| Coal share | Zero or positive | Delayed retirements (e.g. Georgia's 2025 IRP) |
| Nuclear share | Negative | Fixed output, larger denominator |
| MW added per 1,000 MW of 2015 capacity: gas | Positive | Capacity for new load |
| MW added: solar | Positive | Procurement |
| MW added: wind | Positive | Procurement |
| Battery storage additions | — | **Not in the panel** (EIA's state capacity file has no storage category); skipped as the prompt allows |
| Net imports, (retail sales - in-state generation) / retail sales | Positive | Load grows faster than in-state generation |
| ln power-sector CO2 (`co2_power_t`) | Positive | More fossil generation |
| Power-sector CO2 per MWh (`co2_per_mwh_t`) | Positive | Gas and coal on the margin |

Note: MW added for solar and wind also appear in the "bytype" family. They are counted in both families, as the prompt lists them in both.

**Restructured market (registered before computing any state's value):** from EIA-861 (`data/raw/eia/HS861_2010-.xlsx`, already downloaded), the share of each state's 2015 total retail sales (MWh) sold by Energy-Only Providers (retail power marketers). **Restructured if the share is >= 10%.** Flag every state within 5 points of the cutoff (5-15%). The list of states on each side goes in `data/extend_restructured.csv` and the notebook. Source: EIA Form 861 annual data, sheets "Total Electric Industry" and "Energy Only Providers".

**Deviation X1 (logged 2026-11-07, after building the classification and before any section 3 model ran):** the pre-registered rule (EIA-861 Energy-Only Providers' share of 2015 retail sales >= 10%) classifies **Texas as regulated (0%)**. EIA's summary sheets don't report Texas's competitive retailers separately: they are bundled-service sellers with ownership "Retail Power Marketer". EIA-861's 2025 detail file (`data/raw/eia_forms/f8612025.zip`, `Sales_Ult_Cust_2025.xlsx`, already downloaded) puts 63.6% of Texas retail sales with retail power marketers. **Main classification:** the pre-registered 2015 rule with Texas set to restructured. 15 restructured states in the 50-state sample: CA, CT, DE, IL, MA, MD, ME, MT, NH, NJ, NY, OH, PA, RI, TX (DC also qualifies but is out of the sample). Near the cutoff (5-15%): CA 11.0, MI 9.1, NV 6.4. **Labeled check:** the share of 2025 sales by Retail Power Marketers >= 10% (bundled and energy-only rows). It moves CA (4.8%) and MT (0.9%) to regulated and keeps TX restructured. If an outcome passes, the AI x restructured model is reported under both.

**Deviation X2 (logged 2026-11-07, before any section 3 model ran):** ctrl4 includes the average retail price (`price_c_kwh`). With a sector's retail price as the outcome, that control would absorb most of the variation, because the average is a sales-weighted mix of the sector prices. **For the three price outcomes only, the controls are ctrl4 without `price_c_kwh`** (ln GDP per capita, manufacturing share, population growth). Tag model `twfe-ctrl3`. Every other outcome keeps ctrl4.

### §14.4 Why renewables grew nationally, pre-registered 2026-11-07
**Outcomes:** renewable share (`renew_share`), ln wind generation, ln solar generation (zeros dropped), winsorized as in section 14.2. Both AI measures.

**E4.1 Year effects:** the main two-way model with year dummies (base 2015) in place of absorbed year FE, AI(t-1) (jobs), ctrl4, clustered by state, 2015-2025. Year coefficients with 95% CIs, charted.

**E4.2 National drivers, 2015-2025** (`data/extend_drivers.csv`; receipts `drivers_sources.md`):
- **Solar cost:** LBNL Utility-Scale Solar (in hand). Capacity-weighted (MW-AC) mean of `pv_lcoe_no_tax_credits_2025_mwh` for PV projects by commercial-operation year.
- **Wind cost:** LBNL Land-Based Wind Market Report data file. **Blocked:** emp.lbl.gov returns HTTP 403 to scripted requests (2026-11-07), so it needs a browser download. Lazard (in hand) is a check only.
- **Solar ITC by year:** 30% before 2020, 26% for 2020-2021, 30% from 2022 (6% base x 5 with the wage and apprenticeship rules). Coded from P.L. 117-169 (govinfo), with PDF pages, and to be checked against CRS IF10479.
- **Wind PTC, share of full credit by construction-start year:** 2022+ = 100% (P.L. 117-169 section 13101(e)(2), PDF p. 90). The 2017-2021 phase-down values need CRS R43453. **Blocked:** crsreports.congress.gov returns HTTP 403 to scripted requests, so R43453 and IF10479 need a browser download.
- **Gas price:** Henry Hub spot, annual average (EIA RNGWHHDa).
- **State mandates:** LBNL current RPS/CES schedule, `target_pct` (in hand).
- **National AI totals:** sum of 50-state private 518210 jobs and of postings (in hand).
- **Resource:** NREL state tables can't be reached (nrel.gov doesn't resolve from this machine's sandbox), so the prompt's fallback applies. Wind (solar) resource = the state's wind (solar) capacity factor in 2015, generation / (nameplate MW x 8,760). A state with under 10 MW in 2015 uses the first later year with at least 10 MW; a state that never reaches 10 MW gets 0, with a flag.
- **2015 gas share** of in-state generation.

**E4.3 Drivers model:** Y_st = mu_s + b1 RPS_st + b2 (solarCF_s x solarLCOE_t) + b3 (windCF_s x windLCOE_t) + b4 (solarCF_s x ITC_t) + b5 (windCF_s x PTC_t) + b6 (gasshare2015_s x HH_t) + national main effects of solarLCOE, windLCOE, ITC, PTC, HH + a AI_s,t-1 + ctrl4. State FE, no year FE, clustered by state.
- **Deviation X3 (interim, logged before running):** until the CRS PDFs and the LBNL wind file arrive, the model runs **without b3, b5 and the windLCOE and PTC main effects**, labeled `drivers-interim`. The full model runs in pass 2 if the files are provided.
- **Reported:** (a) the fitted national driver path, the mean over states of the driver terms by year, normalized to 2015 = 0, against the year effects: correlation and R-squared (corr^2); (b) the AI coefficient in three models: state FE only (ctrl4, no year FE), the drivers model, and two-way FE.
- **Expected:** with state FE only, AI is positive for all three outcomes (it trends up with renewables). With drivers, it moves toward zero. Two-way FE as in sections 14.2 and 4b.

**Deviation X4 (logged 2026-11-07, after building the resource measures and before any section 4 model ran):** the registered fallback (capacity factor in 2015, or the first year with at least 10 MW) gave implausible values where a state's first plants came online mid-year (wind 0.003 in NC; solar 0.001 to 0.06 in WY, MN, AR and others), because a full year's capacity is divided into a partial year's generation. **Revised rule:** CF = generation_y / (mean of nameplate in y-1 and y x 8,760), in the first year y >= 2015 whose previous year already had at least 10 MW (2014 nameplate from `existcapacity_annual.xlsx`, same filter as the panel). A state that never qualifies gets 0, with a flag.

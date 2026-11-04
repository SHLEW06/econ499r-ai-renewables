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
| 23 | Not in memo; `CLAUDE.md` listed degree days as an optional control | NOAA degree days not done, and no substitute | NCEI unreachable on 2026-11-04; CPC is a different product | **Adopted 2026-11-04 (team decision)** |
| 24 | Memo p. 4: AI is employment in NAICS 518210; ownership not stated | Main: private rows only (own_code 5), over all covered jobs. Name: **"private data-center jobs per 1,000 workers."** Check: private + published government jobs (own_code 1, 2, 3), one labeled 4e row | Government rows exist in every year, contrary to the original D23, so private-only is a choice. Keeps the main measure on commercial hosting. It also avoids a coverage break: published government rows jump from 5 in 2021 to 16 in 2022 as suppressed rows fall from 25 to 13 | **Adopted 2026-11-04 (team decision)** |
| 25 | Memo pp. 9, 11: population from Census county data 2020-2025 and BEA 1969-2024; "population growth (Census)" | BEA SAINC1 line 2 for every year | One series with no splice. BEA's footnote gives Census midyear estimates as its source; all 3 cells the audit sampled match the newest Census series exactly | **Documented 2026-11-04** |
| 26 | Memo p. 11: Census 2010 state area file (Georgia 57,513 sq mi) | Sum of 2020 Gazetteer county land areas (Georgia 57,716.96 sq mi, +0.35%) | Same file supplies the centroids. Land area doesn't change over time, so state FE absorb the difference in `ln_ea` | **Documented 2026-11-04** |
| 27 | Memo p. 11: Census TIGER state boundary file for spatial weights | Centroids: land-weighted average of 2020 Gazetteer county points. Border W: 2023 county adjacency file | Built from files already downloaded. Effect on W against TIGER centroids not measured | **Documented 2026-11-04** |

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
| Gavins Point in `new_renew_mw` | Left as EIA publishes it; **open question** | 132.3 MW hydro moves between NE and SD: false changes in 2016 and 2018 |
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

**H3 verdict (main spec: SDM, LYtrans=FALSE, inverse-distance W, 50 states):** borderline: the renew_share spillover is negative (indirect −0.161) with p = 0.035 in the main spec, and p between about 0.03 and 0.09 across the other SDM versions and border W; in the SLX, θ1 has p about 0.11–0.12 and the total has p about 0.06–0.07. No spillover for ln_ec or ln_ee in the main spec.

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
| Spec curve: new_renew_mw | §1 model, swap Y | new_renew_mw, raw and per 1,000 MW of 2015 capacity | — | Only positive raw-MW result; not robust to scaling in 4b |
| Driscoll-Kraay SEs | Re-run §1 | all core | Often smaller with T = 11 | Labeled sensitivity only; never the basis for a conclusion |
| A8: Conley SEs | Re-run §1; `fixest` Conley from state centroids, 500 and 1,000 km | all core, new_renew_mw | — | Labeled check (§0 item 17) |
| P1: Distributed lags | AI t−1, t−2, t−3 and their sum with delta-method SE; lags built from ai_dc_per1000_lag1 so 2014 is usable | all core, new_renew_mw | — | 2017–2025; N = 450. t−1 alone on the same sample shown beside it (§0 item 14) |
| P2: Corrected long difference | ΔY 2015→2025 on ΔAI 2014→2024 + Δcontrols; heteroskedasticity-robust SEs | all core | — | N = 50 (§0 item 19) |

**Output path:** `results/<date>/robustness/`  
**Method tags:** `rob_<spec>_ai518210_<lag>_ctrl4_w9901_cl-state_<outcome>_<sample>`  
**Status:** Memo + added

---

## §10 Stretch (drop if behind on Nov 17 deadline)

| Goal | Equation | Key parameter | Effort | Status |
|---|---|---|---|---|
| Moderation: broadband × AI | AI × broadband_rate + broadband_rate main effect | interaction coefficient | Medium | Data ready; 2016-2024, no 2020 (§0 item 22) |
| Moderation: R&D share × AI | AI × rd_share + rd_share main effect | interaction coefficient | Medium | Data ready; 2017-2023 |
| Moderation: EPU-S × AI | AI × epu_s; mean-center first | interaction coefficient | Medium | Data ready |
| Shift-share IV | First stage: $\hat{AI}$ = national growth × base share; KP-F | IV 2nd-stage $\hat{\alpha}_1$ | Medium — weak instrument risk | Under review |
| Hansen threshold | energy_equity as threshold variable | threshold value | Medium | Under review |

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
| block | h1, h1x, nonlin, het, dyn, h2a, h2b, h3, rob, stretch, ga | h1 |
| model | twfe, slx, sdm, med, lc | twfe |
| ai-var | ai518210 (private), ai518210sq, ai518210allown (private + published government; check only) | ai518210 |
| lag | lag1, lag2, lag3, lag1to3sum, longdiff, lead1 | lag1 |
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

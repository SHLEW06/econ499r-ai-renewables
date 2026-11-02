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
| 7 | No dynamics specification | Distributed lags AI t−1, t−2, t−3 and their sum; 2015-to-2025 long difference. Needs QCEW 2012–2013 for full t−3 | Short-run null / long-run positive is theoretically motivated (Zhao et al. 2024) | **Adopted (medium effort; 2012–2013 QCEW needed for t−3)** |
| 8 | No comment on efficiency vs consumption sign expectation | Add one paragraph in §H1 core and in the results handoff explaining why both can hold or why efficiency may fall where AI grows | Wording only, no new code; prevents a misread of "efficiency increases" when data centers sit in the numerator of the ratio | **Adopted (wording)** |
| 9 | H2b reports ln_ea mediation straightforwardly | Keep as memo version but include a caveat: EA is nearly redundant under state FE because land area is constant | Within-state EA variation = nonfarm GDP variation, which ln_gdp_pc and pop_growth already capture | **Adopted (caveat note)** |
| 10 | No state EPU moderator | AI × EPU-S (Baker-Davis-Levy 2022) as a stretch moderator; mean-center before interacting | Fang et al. 2025 use EPU-S; confirms generalizability of AI-renewable link across political-economy conditions | **Stretch — blocked until EPU-S data downloaded** |
| 11 | Georgia solar learning curve not in memo | Add Georgia solar cost projection to 2035 (Bolinger 2022 method); LR = 24% central; fan of 12/19/24/45% × 3 capacity paths | Answers "future of renewables" for Georgia case box; learning curves are correlations, not causal | **Adopted (Phase 4f)** |

---

### Data-section confirmations (from Phase 2C, 2026-11-02)

These are confirmed choices embedded in the panel, not model deviations.

| Decision | Choice | Evidence |
|---|---|---|
| GDP in ln_ee and ln_gdp_pc | Real chained-2017 (BEA SAGDP9) | corr(real, nominal) = 0.976 under two-way FE; real removes inflation |
| AI numerator | Private 518210 only (own_code=5, agglvl=58) | No government 518210 rows exist at state level |
| Fossil includes Other Gases | Yes | 0.34% of fossil; matches EIA source structure |
| Renewable = utility-scale only | Yes | Rooftop not in EIA state generation file |
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
| $X_{it}$ | ln_gdp_pc, price_c_kwh, tech_share, manuf_share, pop_growth |
| $\mu_i$ | state FE |
| $\lambda_t$ | year FE |

**Sample:** 50 states (DC dropped via is_dc==0), 2015–2025; N = 550 for lagged sample.  
**Fixed effects:** two-way (state + year).  
**SEs:** clustered by state (baseline); Driscoll-Kraay SEs reported alongside.  
**Winsorizing:** outcomes (ln_ec, ln_ee, renew_share) and AI at 1st/99th percentile over pooled 2015–2025 sample.  
**Price control variant:** run with and without price_c_kwh; report two columns.  
**Support rule:** $\hat{\alpha}_1 > 0$ for renew_share (AI raises renewable share). For ln_ec, sign could go either way; for ln_ee, explain that efficiency can rise or fall depending on whether GDP growth outpaces the load increase from data centers.  
**Output path:** `results/<date>/h1_core/`  
**Method tags:** `h1_twfe_ai518210_lag1_ctrl5_w9901_cl-state_<outcome>_50s2015_2025`  
**Status:** Memo (adapted)

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
**Method tags:** `h1x_twfe_ai518210_lag1_ctrl5_w9901_cl-state_<outcome>_50s2015_2025`  
**Status:** Added

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
**Method tags:** `nonlin_twfe_ai518210sq_lag1_ctrl5_w9901_cl-state_<outcome>_50s2015_2025`  
**Status:** Added (replaces Hansen as main nonlinearity test)

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
**Method tags:** `het_twfe_ai518210_lag1_<mod>_ctrl5_w9901_cl-state_<outcome>_50s2015_2025`  
**Status:** Added (from Fang et al. 2025, done better)

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
**Method tags:** `dyn_twfe_ai518210_lag<k>_ctrl5_w9901_cl-state_<outcome>_50s2015_2025`  
**Status:** Added

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

**Indirect effect:** $\hat{a}_1 \hat{b}_1$ with Sobel test + cluster bootstrap (1,000 reps) for 95% CI.  
**Outcomes:** renew_share (primary); ln_ec, ln_ee (secondary).  
**Support rule:** $\hat{a}_1 \hat{b}_1 > 0$ for renew_share (AI → more tech workers → more renewables).  
**Output path:** `results/<date>/h2a/`  
**Method tags:** `h2a_med_ai518210_lag1_M-techshare_ctrl5_cl-state_<outcome>_50s2015_2025`  
**Status:** Memo + change

---

## §7 H2b — Mediation: Economic Density

**Question:** Does AI predict renewable outcomes through higher economic density (nonfarm GDP per square mile)?

Same three-step structure as §6 with M = ln_ea.

**Caveat (§0 item 9):** ln_ea is nearly redundant under state FE because land_sqmi is constant within states; within-state variation in EA is entirely driven by nonfarm GDP growth, which ln_gdp_pc and pop_growth already capture. Report as the memo version; note this caveat.  
**Output path:** `results/<date>/h2b/`  
**Method tags:** `h2b_med_ai518210_lag1_M-lnea_ctrl5_cl-state_<outcome>_50s2015_2025`  
**Status:** Memo (with redundancy caveat)

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
**AK/HI:** excluded (contig48 == 1); N ≈ 539 with lag.  
**Output path:** `results/<date>/h3/`  
**Method tags:** `h3_sdm_ai518210_lag1_W-border_ctrl5_cl-state_<outcome>_48s2015_2025`  
**Status:** Memo + change (impacts decomposition per §0 item 1)

---

## §9 Robustness

| Check | Model | Outcome(s) | Expected | Note |
|---|---|---|---|---|
| fossil_to_renew | §1 model, swap Y | fossil_to_renew | $\hat{\alpha}_1 < 0$ | More AI → lower fossil/renew |
| SEDS energy per person | §1 model, swap Y | seds_mmbtu_pc | Ambiguous | Through 2024 only |
| Drop 2020 | §1, year ≠ 2020 | renew_share | Stable | COVID outlier check |
| Drop AK, HI | §1, contig48==1 | renew_share | Stable | Energy-isolated states |
| Drop VA | §1, state ≠ 'VA' | renew_share | Stable | Outlier tech-worker state |
| Border W only | §8 SDM, border W | renew_share | Stable | W sensitivity |
| RPS control | Add RPS indicator | renew_share | Shrinks $\hat{\alpha}_1$ | **Blocked** — LBNL file needed (EXP-003) |
| Next-year-AI placebo | Replace AI(t−1) with AI(t+1) | renew_share | Null | Falsification |
| Driscoll-Kraay SEs | Re-run §1 | all core | Wider SEs expected | Cross-sectional correlation |

**Output path:** `results/<date>/rob/`  
**Method tags:** `rob_<spec>_ai518210_<lag>_ctrl5_w9901_cl-state_<outcome>_<sample>`  
**Status:** Memo + added

---

## §10 Stretch (drop if behind on Nov 17 deadline)

| Goal | Equation | Key parameter | Effort | Status |
|---|---|---|---|---|
| Moderation: broadband × AI | AI × broadband_rate + broadband_rate main effect | interaction coefficient | Medium — need broadband data | Blocked |
| Moderation: R&D share × AI | AI × rd_share + rd_share main effect | interaction coefficient | Medium — need R&D data | Blocked |
| Moderation: EPU-S × AI | AI × epu_s; mean-center first | interaction coefficient | Medium — need EPU-S data | Blocked (EXP-010) |
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
| ai-var | ai518210, ai518210sq | ai518210 |
| lag | lag1, lag2, lag3, longdiff, lead1 | lag1 |
| controls | ctrl5 (ln_gdp_pc + price + tech_share + manuf_share + pop_growth), ctrl4 (no price) | ctrl5 |
| winsor | w9901 (1/99 pooled), nowins | w9901 |
| se | cl-state (clustered by state), dk (Driscoll-Kraay) | cl-state |
| outcome | ln_ec, ln_ee, renew_share, solar_share, wind_share, fossil_to_renew, co2_per_mwh_t, coal_share, new_renew_mw, seds_mmbtu_pc | renew_share |
| sample | 50s2015_2025, 48s2015_2025, 50s2015_2024 | 50s2015_2025 |

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

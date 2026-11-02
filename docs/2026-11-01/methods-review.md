# Methods review: the Oct 22 Methods Memo against our main papers (Nov 1, 2026)

**Bottom line:**
- **Citations:** The memo is mostly right. We checked all 36 claims it attributes to Zhang et al. (2026) against the paper. Every one was found, and most are correct. Six are misstated: a wrong test name, a wrong equation number, "clustered" vs. "robust" standard errors, a missing moderator term, a quote that is the paper citing another study, and an unstated logging choice. Section 3 fixes each with before/after text.
- **Design:** five changes are needed. Two are corrections: report spatial direct and indirect effects instead of theta alone, and use the tech-worker share instead of HMA as the H2a mediator. Three are added checks: an AI-squared nonlinearity test, results with and without the electricity-price control, and heterogeneity by interaction instead of split samples.
- **Main papers:** four main papers and one supporting paper (Section 1).

This review was checked against the PDFs on Nov 1, 2026. The supplementary appendices of Zhang et al., Fang et al. and Bolinger et al. were not available, so their appendix tables were not checked.

## 1. Our main papers and what each is for

| Paper | Role | What we take from it |
| --- | --- | --- |
| Zhang, Ji, Dou & Hao (2026), *Applied Economics* 58(32), 6495-6513 (China, 261 cities, 2006-2019, N = 3,654) | **The spec we transpose** (not in this upload; we already have it) | H1-H3, the three outcomes, two-way FE (eq 4), mediation (eqs 5-7), moderation (eq 8), threshold (eq 9), Moran's I (eq 10), SDM (eq 11) |
| Fang, Lee & Li (2025), *Renewable Energy* 246, 122969 (U.S., 51 states, 2018-2021, N = 204) | **Closest U.S. precedent** | Heterogeneity by net electricity exporter vs importer, high vs low electricity price, and Census region (the South was not significant); outcomes by renewable type (solar effect largest); state economic policy uncertainty (EPU-S) as a moderator |
| Melguizo, Katz & Jung (2026), *Energy Policy* 208, 114883 (23 countries, 2019-2023) | **Nonlinearity** | AI + AI² ("Kuznets") with a turning point. They find curvature for the renewable share and CO2, not for energy use or efficiency. Adds a CO2 outcome and a coal-share falsification check |
| Bolinger, Wiser & O'Shaughnessy (2022), *iScience* 25, 104378 (U.S. wind and solar, plant-level LCOE) | **Georgia "future of renewables" module** | Learning-curve projection of solar cost to 2035: learning rate 24% for solar, 15% for wind (normalized LCOE, global cumulative capacity) |
| Zhao, Wang, Stan & Mirza (2024), *Energy Economics* 134, 107584 (China, monthly national series, 93 obs.) | **Supporting literature, not a methods paper** | AI effects on the renewable share can be negative in the short and medium run and positive in the long run. This is a reason a null or negative one-year-lag result is plausible. Its wavelet quantile-on-quantile method needs one long time series, so it can't be used on an 11-year state panel |

What the other papers do worse than us (don't copy):
- **Fang et al.:**
  - state FE only, no year FE
  - SE type not stated
  - no lag and no endogeneity strategy
  - a four-year panel
  - "significant in one group, not the other" treated as a real difference
- **Melguizo et al.:**
  - robust (not clustered) SEs
  - turning points far outside the data (around $570-580 against a mean of $53)
  - the AI² coefficient printed to one significant figure
  - weak instruments
- **Zhao et al.:**
  - no standard errors for its main estimates
  - no stationarity tests
  - a lagged dependent variable (would cause Nickell bias in our FE panel)

## 2. What the memo gets right
- **The paper's facts:** sample and N; H1-H3; the three outcomes and how the paper builds each; winsorizing at 1/99; the robot shift-share (eq 1); the HMA formula (eq 2); the EA, broadband and TAC definitions; two-way FE (eq 4); mediation (eqs 5-7) with Sobel; Moran's I (eq 10); the SDM (eq 11); Table 2 and Table 12 results; the Works Cited entry.
- **Our deliberate departures are disclosed:** a direct AI measure instead of the shift-share, the one-year lag, electricity-based outcomes, U.S. controls.
- **The panel is 550 state-years with the lag:** we added 2014 QCEW, so 2015 has a lagged AI value. No observations are lost.

## 3. Prose fixes to the memo (copy-paste ready)
These change wording only. Items 4 and 11 are table cells in the memo, so their line breaks will differ when you paste.

1. **Section 4, IV test name**
   - Before: "with the KP-LM (Kleibergen-Paap Lagrange Multiplier) test the paper reports to show the helper is strong enough (p. 6504)."
   - After: "with the Kleibergen-Paap tests the paper reports: KP-LM for under-identification and KP-F for instrument strength (Table 3, pp. 6504-6505)."
2. **Section 4, role of the IV**
   - Before: "The paper fixed this with an instrumental variable (a helper variable that moves AI but cannot move the outcome except through AI), using U.S. robot use as the helper for China (p. 6504, Table 3)."
   - After: "The paper checked this, as a robustness test, with an instrumental variable (a helper variable that moves AI but cannot move the outcome except through AI), using U.S. robot use as the helper for China (p. 6504, Table 3)."
3. **Section 2, logs**
   - Before: "Second, we take the natural log (a math transform that turns big-versus-small gaps into percentage gaps) of consumption and efficiency, which is how the paper's consumption numbers look in its Table 1 (p. 6503)."
   - After: "Second, we take the natural log (a math transform that turns big-versus-small gaps into percentage gaps) of consumption and efficiency. The paper does not say whether it logs its outcomes. Its Table 1 (p. 6503) suggests consumption is logged and efficiency is not, so logging efficiency is our choice."
4. **Section 2, fossil-to-renewable ratio row**
   - Before: "Fossil-to-renewable ratio: MWh from coal, gas, and oil divided by renewable MWh; lower means cleaner, same direction as the paper"
   - After: "Fossil-to-renewable ratio: MWh from coal, gas, and oil divided by renewable MWh; lower means cleaner. This is the same direction as the paper's coal-to-clean ratio (p. 6499), which counts coal only. H1 is supported if a1 is negative."
5. **Step 1 framing**
   - Before: "A panel (the same 50 states watched every year) regression with state and year fixed effects, copied from the paper's equation 4 (Zhang et al. 2026, p. 6502)."
   - After: "A panel (the same 50 states watched every year) regression with state and year fixed effects, adapted from the paper's equation 4 (Zhang et al. 2026, p. 6502). We lag AI one year and use U.S. controls. The paper's controls are ln GDP, government size, an industrial-structure index, transport and finance."
6. **Step 3, what counts as support**
   - Before: "Theta-1 is the neighbor effect of AI. H3 (siphoning) is supported if theta-1 has the harmful sign: positive for consumption, negative for efficiency, negative for renewable share."
   - After: "Because the neighbors' outcomes (rho) feed effects back and forth, theta-1 alone is not the spillover. We report the direct, indirect (spillover) and total effects of AI (LeSage and Pace 2009). H3 (siphoning) is supported if the indirect effect has the harmful sign: positive for consumption, negative for efficiency, negative for renewable share. The paper's Table 12 reports only the W*AI coefficient (p. 6509)."
7. **Step 3, SLX fallback**
   - Before: "It tests the same theta-1."
   - After: "Because the SLX has no rho term, its theta-1 is the spillover itself. It is a different parameter from the SDM's theta-1."
8. **Step 4, robustness SEs**
   - Before: "and re-run with clustered standard errors."
   - After: "and re-run with Driscoll-Kraay standard errors, which allow shocks shared across states. Our baseline already clusters by state. The paper's Appendix B uses robust standard errors (p. 6505)."
9. **Stretch, moderation**
   - Before: "add interaction terms (AI multiplied by broadband subscription rate, and AI multiplied by research spending share), as in the paper's equation 8 (p. 6503)."
   - After: "add each moderator and its interaction with AI (AI x broadband subscription rate; AI x research spending share), as in the paper's equation 8 (p. 6503), which includes the moderator's own main effect. We leave out the paper's third moderator, labour-intensive factor endowment."
10. **Stretch, threshold**
    - Before: "Hansen (1999) threshold model with energy equity, the ratio of a state's GDP share to its electricity share, as in the paper's equation 3 (p. 6502)."
    - After: "Hansen (1999) threshold model (the paper's equation 9, p. 6503) with energy equity as the threshold variable: a state's share of U.S. GDP divided by its share of U.S. electricity use. The paper's equation 3 (p. 6502) uses total energy."
11. **Section 10, the data-centre quote**
    - Before: "The paper's own review warns that AI \"drives energy consumption through data centre scale effects\" (p. 6497)."
    - After: "The paper's literature review, citing Zou, Yang and Feng (2023), notes that AI \"drives energy consumption through data centre scale effects\" (p. 6497)."

## 4. Changes that are more than prose (look these over with Alexander)
Ordered most important first.

1. **H3: report spatial impacts.** Use the SDM direct, indirect and total effects with simulated SEs. H3 support is judged by the indirect effect.
   - Why: theta alone is not the spillover when rho is not zero.
   - Effort: low (spatialreg or splm `impacts()`).
2. **H2a: use the tech-worker share (NAICS 5415) as the mediator.**
   - Why: HMA is built from AI, so AI predicts HMA by construction. The memo's own H2a wording ("share of tech workers") describes this variable anyway.
   - Keep HMA as the memo version, and label its first step as uninformative.
   - Effort: low.
3. **Nonlinearity: AI + AI² (Melguizo) as the main nonlinearity test.** Keep Hansen as a stretch goal.
   - Report the turning point -b1/(2·b2) with a delta-method SE, and whether it lies inside the observed range of within-state AI.
   - Add a Lind-Mehlum test.
   - Effort: low.
4. **Electricity-price control may be a bad control.** Data-center demand can raise prices, so the control can absorb part of the effect. Run Step 1 with and without it; report both. Effort: low.
5. **Heterogeneity by interaction (from Fang, done better).** Use AI x (net electricity exporter), AI x (above-median price) and AI x (South) inside the two-way FE model, instead of separate subgroup regressions.
   - Net exporter = in-state generation above retail sales, from EIA files we already have.
   - Effort: low.
6. **Extra outcomes.**
   - solar and wind shares separately (Fang found solar largest)
   - CO2 per MWh (EIA, through 2024)
   - coal share as a falsification check (Melguizo)

   Effort: low; the data is already in the panel.
7. **Short run vs long run (from Zhao, done in a panel).**
   - Distributed lags of AI (t-1 to t-3) and their sum, or a 2015-to-2025 long-difference regression. Don't use a lagged dependent variable.
   - Needs QCEW 2012-2013 for full t-3 lags.
   - Effort: medium.
8. **Efficiency vs consumption expectation.** The memo expects AI to raise electricity use per person but also raise GDP per MWh. Data-center load sits in the denominator of efficiency, so explain why both can hold. Otherwise expect efficiency to fall where data centers grow. This is wording plus interpretation, no new code.
9. **Economic density (H2b) is nearly redundant under state FE.** Land area never changes, so within a state EA moves only with nonfarm GDP, which ln GDP per person and population growth already track. Keep it as the memo version and report it, but say so.
10. **State policy uncertainty moderator (from Fang, stretch).** AI x EPU-S, using the Baker-Davis-Levy monthly state indexes averaged to years.
    - Mean-center before interacting.
    - Effort: medium (new data; confirm it covers 2025).
11. **Georgia solar cost module (Bolinger).**
    - Project Georgia utility-scale solar cost to 2035 with C_t = C_base × (X_t / X_base)^b, where b = ln(1 - LR)/ln 2 (LR = 24% gives b ≈ -0.396).
    - X is global cumulative PV capacity.
    - Show a fan of learning rates (12%, 19%, 24%, 45%) crossed with low, central and high global capacity paths.
    - It answers "the future of renewables," not "does AI improve renewables." Learning curves are correlations, and Georgia does not have its own learning rate.
    - Effort: medium.

## 5. Final method specification (what the implementation prompts build)

| Block | Model | Status |
| --- | --- | --- |
| H1 core | Y = a1·AI(t-1) + controls + state FE + year FE; SEs clustered by state; 50 states, 2015-2025; outcomes and AI winsorized 1/99. Y = ln_ec, ln_ee, renew_share | Memo |
| H1 extras | solar_share, wind_share, new_renew_mw, co2_per_mwh, coal share; with and without price; Driscoll-Kraay SEs | Added |
| Nonlinearity | AI + AI², turning point with delta-method SE, Lind-Mehlum | Added (replaces Hansen as main) |
| Heterogeneity | AI x net exporter, AI x high price, AI x South | Added (from Fang) |
| Dynamics | distributed lags t-1..t-3; long difference | Added (from Zhao) |
| H2a | mediation, M = hma (memo) and M = tech_share (main), Sobel plus bootstrap | Memo + change |
| H2b | mediation, M = ln_ea, with the redundancy caveat | Memo |
| H3 | Moran's I by year (inverse distance and border W); SLX; SDM with two-way FE; direct, indirect and total impacts | Memo + change |
| Robustness | fossil_to_renew (expect a1 < 0); SEDS energy per person; drop 2020, AK/HI, VA; border W; RPS control if LBNL file present; next-year-AI placebo | Memo + added |
| Stretch | moderation (broadband, R&D, EPU-S) with main effects; shift-share IV with KP-F; Hansen threshold (eq 9) | Memo + added |
| Georgia | case box from the IRP, dockets and interview; solar learning-curve projection to 2035 | Memo + added |

## 6. Data still needed for this specification
- **Already in the panel:** all core variables, solar and wind shares, CO2 (through 2024), fossil generation by fuel (coal share), sales and generation (net-exporter flag), Census regions (add as a lookup).
- **New:**
  - Baker-Davis-Levy state EPU, monthly: https://policyuncertainty.com/state_epu.html
  - Global cumulative solar PV capacity (IRENA via Our World in Data, 2000-2025): https://ourworldindata.org/grapher/solar-pv-cumulative-capacity.csv?v=1&csvType=full&useColumnShortNames=false
  - LBNL Utility-Scale Solar project data (browser): https://emp.lbl.gov/utility-scale-solar
  - QCEW 2012-2013 for 518210 and industry 10 (download_all.py pattern), only if we run t-3 lags
  - The LBNL RPS file (already listed)

## Sources checked
- Zhang, S., Ji, R., Dou, W., Hao, Y. (2026). *Applied Economics* 58(32), 6495-6513. doi:10.1080/00036846.2025.2521038
- Fang, Y., Lee, C.-C., Li, X. (2025). *Renewable Energy* 246, 122969. doi:10.1016/j.renene.2025.122969
- Melguizo, A., Katz, R., Jung, J. (2026). *Energy Policy* 208, 114883. doi:10.1016/j.enpol.2025.114883
- Bolinger, M., Wiser, R., O'Shaughnessy, E. (2022). *iScience* 25, 104378. doi:10.1016/j.isci.2022.104378
- Zhao, Q., Wang, L., Stan, S.-E., Mirza, N. (2024). *Energy Economics* 134, 107584. doi:10.1016/j.eneco.2024.107584
- Baker, S. R., Davis, S. J., Levy, J. A. (2022). State-level economic policy uncertainty. *Journal of Monetary Economics* 132, 81-99.
- LeSage, J., Pace, R. K. (2009). *Introduction to Spatial Econometrics*. CRC Press.

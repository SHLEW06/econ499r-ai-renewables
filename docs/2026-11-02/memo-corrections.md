# Memo corrections — for Alexander (2026-11-02)

From methods-review.md §3 (prose fixes) and §4 (non-prose changes).  
All prose fixes are copy-paste ready. Section and page references are to the Oct 22 Methods Memo.

---

## Prose fixes (wording only)

**1. Section 4, IV test name**

Before:
> "with the KP-LM (Kleibergen-Paap Lagrange Multiplier) test the paper reports to show the helper is strong enough (p. 6504)."

After:
> "with the Kleibergen-Paap tests the paper reports: KP-LM for under-identification and KP-F for instrument strength (Table 3, pp. 6504-6505)."

---

**2. Section 4, role of the IV**

Before:
> "The paper fixed this with an instrumental variable (a helper variable that moves AI but cannot move the outcome except through AI), using U.S. robot use as the helper for China (p. 6504, Table 3)."

After:
> "The paper checked this, as a robustness test, with an instrumental variable (a helper variable that moves AI but cannot move the outcome except through AI), using U.S. robot use as the helper for China (p. 6504, Table 3)."

---

**3. Section 2, logs**

Before:
> "Second, we take the natural log (a math transform that turns big-versus-small gaps into percentage gaps) of consumption and efficiency, which is how the paper's consumption numbers look in its Table 1 (p. 6503)."

After:
> "Second, we take the natural log (a math transform that turns big-versus-small gaps into percentage gaps) of consumption and efficiency. The paper does not say whether it logs its outcomes. Its Table 1 (p. 6503) suggests consumption is logged and efficiency is not, so logging efficiency is our choice."

---

**4. Section 2, fossil-to-renewable ratio row**

Before:
> "Fossil-to-renewable ratio: MWh from coal, gas, and oil divided by renewable MWh; lower means cleaner, same direction as the paper"

After:
> "Fossil-to-renewable ratio: MWh from coal, gas, and oil divided by renewable MWh; lower means cleaner. This is the same direction as the paper's coal-to-clean ratio (p. 6499), which counts coal only. H1 is supported if a1 is negative."

---

**5. Step 1 framing**

Before:
> "A panel (the same 50 states watched every year) regression with state and year fixed effects, copied from the paper's equation 4 (Zhang et al. 2026, p. 6502)."

After:
> "A panel (the same 50 states watched every year) regression with state and year fixed effects, adapted from the paper's equation 4 (Zhang et al. 2026, p. 6502). We lag AI one year and use U.S. controls. The paper's controls are ln GDP, government size, an industrial-structure index, transport and finance."

---

**6. Step 3, what counts as support**

Before:
> "Theta-1 is the neighbor effect of AI. H3 (siphoning) is supported if theta-1 has the harmful sign: positive for consumption, negative for efficiency, negative for renewable share."

After:
> "Because the neighbors' outcomes (rho) feed effects back and forth, theta-1 alone is not the spillover. We report the direct, indirect (spillover) and total effects of AI (LeSage and Pace 2009). H3 (siphoning) is supported if the indirect effect has the harmful sign: positive for consumption, negative for efficiency, negative for renewable share. The paper's Table 12 reports only the W*AI coefficient (p. 6509)."

---

**7. Step 3, SLX fallback**

Before:
> "It tests the same theta-1."

After:
> "Because the SLX has no rho term, its theta-1 is the spillover itself. It is a different parameter from the SDM's theta-1."

---

**8. Step 4, robustness SEs**

Before:
> "and re-run with clustered standard errors."

After:
> "and re-run with Driscoll-Kraay standard errors, which allow shocks shared across states. Our baseline already clusters by state. The paper's Appendix B uses robust standard errors (p. 6505)."

---

**9. Stretch, moderation**

Before:
> "add interaction terms (AI multiplied by broadband subscription rate, and AI multiplied by research spending share), as in the paper's equation 8 (p. 6503)."

After:
> "add each moderator and its interaction with AI (AI x broadband subscription rate; AI x research spending share), as in the paper's equation 8 (p. 6503), which includes the moderator's own main effect. We leave out the paper's third moderator, labour-intensive factor endowment."

---

**10. Stretch, threshold**

Before:
> "Hansen (1999) threshold model with energy equity, the ratio of a state's GDP share to its electricity share, as in the paper's equation 3 (p. 6502)."

After:
> "Hansen (1999) threshold model (the paper's equation 9, p. 6503) with energy equity as the threshold variable: a state's share of U.S. GDP divided by its share of U.S. electricity use. The paper's equation 3 (p. 6502) uses total energy."

---

**11. Section 10, the data-centre quote**

Before:
> "The paper's own review warns that AI 'drives energy consumption through data centre scale effects' (p. 6497)."

After:
> "The paper's literature review, citing Zou, Yang and Feng (2023), notes that AI 'drives energy consumption through data centre scale effects' (p. 6497)."

---

## Data-source differences (added 2026-11-04)

The memo names different sources from the ones we built with. Registered in EXPERIMENTS.md §0 items 24-27.

**12. Section on data, population row (p. 9) and control row (p. 11)**

Before:
> "Census county population 2020 to 2025 and BEA population 1969 to 2024" and "population growth (Census)"

After:
> "BEA state population (table SAINC1, line 2) for all years. BEA's source is the U.S. Census Bureau's midyear population estimates."

**13. Economic agglomeration row (p. 11)**

Before:
> "Census 2010 state area file (Georgia: 57,513 square miles)"

After:
> "Land area from the Census 2020 county Gazetteer, summed to states (Georgia: 57,717 square miles). Land area is constant over time, so state fixed effects absorb the difference."

**14. Spatial weights row (p. 11)**

Before:
> "Census TIGER state boundary file"

After:
> "State centroids from the Census 2020 county Gazetteer (the land-weighted average of county points). The border matrix uses the Census 2023 county adjacency file."

**15. AI measure (p. 4 step 1, and the AI row on p. 10)**

Before:
> "Take annual average employment in NAICS ... code 518210" and "Data-center jobs per 1,000 workers"

After:
> "Take annual average private employment in NAICS ... code 518210" and "Private data-center jobs per 1,000 workers." A robustness row adds published government jobs.

---

## Non-prose changes (design decisions — review with Alexander)

These are changes to what we actually estimate. Full detail in EXPERIMENTS.md §0.

1. **H3:** Report direct, indirect, and total spatial impacts instead of theta alone. (Correct econometric practice; theta ≠ spillover when rho ≠ 0.)
2. **H2a:** Use tech_share as main mediator; run HMA as the memo version but label its first-stage as mechanically positive.
3. **Nonlinearity:** Add AI² as the main nonlinearity test; report turning point with delta-method SE and Lind-Mehlum test. Keep Hansen threshold as stretch only.
4. **Price control:** Run Step 1 with and without price_c_kwh; report both columns. (Price may be a bad control if AI demand raises prices.)
5. **Heterogeneity:** Use interactions inside two-way FE rather than split-sample regressions. (Better statistical practice; Fang-style.)
6. **Extra outcomes:** solar_share, wind_share, new_renew_mw, co2_per_mwh_t, coal_share (falsification) added to Step 1.
7. **Dynamics:** Distributed lags t−1 to t−3 + long difference. Needs QCEW 2012–2013 for t−3.
8. **Efficiency interpretation:** Add an explicit note explaining why ln_ee can rise even when data centers add load (requires GDP to grow faster than load — not guaranteed).
9. **H2b caveat:** ln_ea is near-redundant under state FE (land area is constant). Report as memo; add caveat.
10. **EPU-S moderator (stretch):** AI × state policy uncertainty index; needs data download.
11. **Georgia solar module:** Learning-curve cost projection to 2035 using Bolinger (2022) method.

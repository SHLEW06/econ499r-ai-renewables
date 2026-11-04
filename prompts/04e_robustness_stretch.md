# Phase 4e: Step 4 robustness, then stretch goals

ECON 499R project. The project root is "AI impact on Renewables". The stretch-goal cutoff is Nov 17, 2026.

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (robustness and stretch sections and §0), the newest handoff in docs/, and docs/2026-11-01/methods-review.md.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md.
- Plan first and wait for my OK. In the plan, say how long each piece will take, so I can cut stretch items if we're short on time.

**Settled in 4b-4d. Apply these everywhere in this phase:**
- **Controls:** X = ctrl4: ln_gdp_pc, manuf_share, price_c_kwh, pop_growth. tech_share is never a control, because it is the H2a mediator.
- **Standard errors:** clustered by state is the baseline for every conclusion. Driscoll-Kraay is a labeled sensitivity check only; with T = 11 its SEs tend to be too small (fixest's own docs suggest about 20 or more periods).
- **Spatial weights:** the main W is row-standardized inverse distance, all 50 states. The border W and inverse distance without AK and HI are checks.
- **Interactions:** report the AI slope at each moderator value, using linear combinations with clustered SEs, not only the interaction coefficient.
- **Mediation:** never report "share mediated" when the total effect is not different from zero.
- **Tools:** R fixest for every regression here. Python is fine for tables and charts that read the result CSVs.

## A. Robustness (do all of these)
Rerun the Step 1 core models (ln_ec, ln_ee, renew_share) with these changes:
1. **Swap the outcome:**
   - fossil_to_renew (a1 < 0 supports H1)
   - seds_mmbtu_pc, all-fuel energy per person, 2015-2024: this matches the paper's broader consumption measure
2. **Swap the cause:** data-center MW. Run it only if Phase 2 built a state-year series; otherwise record it as "not available" with the reason.
3. **Change the sample:** drop 2020; drop AK and HI; drop VA.
4. **Swap W:** the border W in the SLX (the SDM version was done in 4d).
5. **RPS control (added):** use the LBNL RPS/CES target as a percent by state-year, if data/lbnl_rps_targets.csv exists. If not, record it as missing.
6. **Placebo (added):** next-year AI, AI(t+1), in place of AI(t-1). A significant placebo means a pre-trend or reverse causality.
   - The placebo sample is 2015-2024, because there is no 2026 AI.
   - AK, ND, SD and WY have suppressed 2025 AI, so they also lose 2024. Expect N = 496; confirm it and say so.
7. **Spec curve also covers new_renew_mw.** Include it raw and per 1,000 MW of 2015 capacity, since it is the only positive raw-MW result and it isn't robust to scaling (4b).

## B. Stretch goals (only after A is done; check the time first)
**Order set 2026-11-04:** the Fang test first, then B2 (shift-share IV), then broadband and R&D moderation. B3 (Hansen threshold) is dropped. Broadband uses 2016-2024, without 2015 and 2020. See EXPERIMENTS.md section 0 items 22 and 30.

1. **Moderation, following the paper's equation 8 (p. 6503), with each moderator's main effect:**
   - AI x broadband share (ACS S2801; years available only, and no 2020)
   - AI x R&D share of GDP (NSF Table 10, 2017-2023 only; restrict the sample and say so)
   - AI x state economic policy uncertainty (EPU-S), Baker-Davis-Levy, averaged to years. This follows Fang et al. (2025) and was the only EPU version that moderated there.

   - Mean-center the moderators.
   - Report the AI slope at the 25th and 75th percentiles of each moderator, using linear combinations with clustered SEs.
2. **Shift-share instrument:**
   - Z = each state's 2015 share of national 518210 jobs x national 518210 growth, excluding the state's own jobs (leave-one-out).
   - Run 2SLS with two-way FE in fixest: `feols(Y ~ ctrl4 | state + year | ai_lag1 ~ Z, cluster = ~state)`.
   - Report the first stage and the reduced form.
   - Report the first-stage F robust to clustering; with one instrument this is the KP F, for strength. Report the KP rank test for under-identification. Check ?fitstat for the names.
   - If the first-stage F is below 10, say the instrument is weak and treat the IV estimate as uninformative.
3. **Hansen threshold (the paper's eq 9, p. 6503).**
   - The threshold variable is energy equity (GDP share / electricity share).
   - Run it only if a maintained R implementation of the Hansen (1999) panel threshold exists (for example pdR::ptm). Name the package, confirm which fixed effects it removes, and bootstrap the threshold test.
   - Otherwise, report that the AI² model in 4b covers nonlinearity. All 8 Lind-Mehlum tests failed there.

## Outputs
- **Results:** results/<date>/robustness/ and results/<date>/stretch/. Every row has tags and status. Record a "not run" row with the reason for anything skipped.
- **Tables:** one summary table across all robustness specs for the AI coefficient on each core outcome, like a specification curve. Write CSV and .tex, with PROVENANCE.md.

## End of phase
1. **Notebook:** notebooks/04e_robustness_stretch.ipynb. Explain what each check guards against in plain words. Include a specification-curve chart, the IV first stage, and the moderation plots.
2. **Receipt:** results/<date>/robustness/RECEIPT.md, plus the same for stretch/.
3. **Handoff:** docs/<date>/phase-4e-robustness-stretch.md, with the five sections plus "How to resume". The next prompt is prompts/04f_georgia_solar_learning_curve.md.
4. **Updates:** update EXPERIMENTS.md and CLAUDE.md §4-5, then git commit.
5. **Summary:** a short summary, then STOP.

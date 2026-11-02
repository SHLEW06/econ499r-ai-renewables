# Phase 4b: Step 1 (H1), two-way fixed effects and its checks

ECON 499R project. The project root is "AI impact on Renewables".

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (H1 sections and §0 divergence register), the newest handoff in docs/, and docs/2026-11-01/methods-review.md.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md.
- Plan first and wait for my OK.

## Experiments
Every model goes through code/R/load_panel.R. Defaults: state and year FE, SEs clustered by state, 50 states, 2015-2025, outcomes and AI winsorized 1/99.

1. **Reproduce the first pass.**
   - Run Y = a1·AI(t-1) + ln_gdp_pc + manuf_share + price_c_kwh + pop_growth + FE.
   - Y = ln_ec, ln_ee, renew_share, solar_share, new_renew_mw.
   - The result must match code/reference/prelim_step1_slx.csv within rounding. If it doesn't, stop and explain why before going on.
2. **H1 core table (memo).** Run ln_ec, ln_ee and renew_share, each with and without controls. Report the coefficient on lagged AI, SE, p, N and within-R2.
3. **H1 extras (added).**
   - Run the same model on solar_share, wind_share, new_renew_mw, co2_per_mwh (2015-2024) and coal share.
   - Run fossil_to_renew; for it, a1 < 0 supports H1.
4. **Price control check (added).** Run the core models without price_c_kwh, because data-center demand can move prices. Report both versions side by side.
5. **SE check (added).** Run Driscoll-Kraay SEs (fixest `vcov = "DK"`) next to the clustered SEs.
6. **Nonlinearity (added, from Melguizo et al. 2026).** Y = b1·AI(t-1) + b2·AI(t-1)² + controls + FE, on each core and extra outcome.
   - Turning point: AI* = -b1/(2·b2), with a delta-method SE from the clustered covariance (including cov(b1, b2)).
   - Report whether AI* and its 95% CI lie inside the observed range of lagged AI, and inside the range states actually move through within their own data.
   - Report the share of state-years past AI*.
   - Run a Lind-Mehlum style test: the slope b1 + 2·b2·AI should be significant with opposite signs at the min and max of AI.
   - Print b2 with enough digits to be useful.
7. **Heterogeneity (added, a better version of Fang et al. 2025).** Inside the two-way FE model, add each interaction and its own main effect where it isn't absorbed by FE:
   - AI(t-1) x net_exporter (in-state generation above retail sales; define it from the 2015 value so it can't respond to AI)
   - AI(t-1) x high_price (above the 2015 median)
   - AI(t-1) x South (Census region)

   Report each interaction coefficient. This is the direct test of whether groups differ.
8. **Dynamics (added, a panel version of Zhao et al. 2024's short vs long run).**
   - Distributed lags AI(t-1), AI(t-2), AI(t-3) and their summed effect with an SE. Run it only if QCEW 2012-2013 exist; otherwise use 2017-2025 and say so.
   - Long difference: ΔY(2015→2025) on ΔAI(2014→2024) plus Δcontrols, with robust SEs.
   - Do NOT add a lagged dependent variable (Nickell bias with T = 11).
9. **Georgia check (descriptive only).** Show Georgia's AI path and outcome paths next to the U.S. median, and Georgia's contribution to the residuals. No Georgia-only regression.

## Outputs
- **Results:** results/<date>/h1/, one CSV per outcome. Every row has the tag, status, estimate, SE, p, CI, N, within-R2, vcov type, sample and controls. Add turning-point rows and interaction rows.
- **Tables:** results/<date>/tables/h1_*.csv and .tex (modelsummary), built by a script from the result rows, with PROVENANCE.md.
- **Figures:** results/<date>/figures/: a coefficient plot across outcomes and specs; for any outcome with significant curvature, a marginal-effect curve of AI with the data range shaded.

## End of phase
1. **notebooks/04b_step1_twfe.ipynb.** One section per experiment, each with:
   - the equation
   - what it tests in one plain sentence
   - the main table
   - one chart
   - a two-line reading ("supports / doesn't support H1 for X because ...")

   Flag the NAICS 518210 caveat: Georgia ranks 2nd, above Virginia.
2. **results/<date>/h1/RECEIPT.md.** List what ran, the input file hashes, the tags, N per model, warnings, and failures.
3. **Handoff:** docs/<date>/phase-4b-step1.md, with the five sections plus "How to resume". The next prompt is prompts/04c_step2_mediation.md.
4. **Updates:** update EXPERIMENTS.md and CLAUDE.md §4-5, then git commit.
5. **Summary:** the headline per outcome, then STOP.

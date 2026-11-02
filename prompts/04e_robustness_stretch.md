# Phase 4e: Step 4 robustness, then stretch goals

ECON 499R project. The project root is "AI impact on Renewables". The stretch-goal cutoff is Nov 17, 2026.

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (robustness and stretch sections and §0), the newest handoff in docs/, and docs/2026-11-01/methods-review.md.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md.
- Plan first and wait for my OK. In the plan, say how long each piece will take, so I can cut stretch items if we're short on time.

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

## B. Stretch goals (only after A is done; check the time first)
1. **Moderation, following the paper's equation 8 (p. 6503), with each moderator's main effect:**
   - AI x broadband share (ACS S2801; years available only, and no 2020)
   - AI x R&D share of GDP (NSF Table 10, 2017-2023 only; restrict the sample and say so)
   - AI x state economic policy uncertainty (EPU-S), Baker-Davis-Levy, averaged to years. This follows Fang et al. (2025) and was the only EPU version that moderated there.

   Mean-center the moderators.
2. **Shift-share instrument:**
   - Z = each state's 2015 share of national 518210 jobs x national 518210 growth, excluding the state's own jobs (leave-one-out).
   - Run 2SLS with two-way FE: report the first stage, the KP-F (strength) and the KP-LM (under-identification).
   - Also report the reduced form.
3. **Hansen threshold (the paper's eq 9, p. 6503).**
   - The threshold variable is energy equity (GDP share / electricity share).
   - Run it only if a maintained R implementation of panel thresholds with FE exists. Name the package, and bootstrap the threshold test.
   - Otherwise, report that the AI² model in 4b covers nonlinearity.

## Outputs
- **Results:** results/<date>/robustness/ and results/<date>/stretch/. Every row has tags and status. Record a "not run" row with the reason for anything skipped.
- **Tables:** one summary table across all robustness specs for the AI coefficient on each core outcome, like a specification curve. Write CSV and .tex, with PROVENANCE.md.

## End of phase
1. **Notebook:** notebooks/04e_robustness_stretch.ipynb. Explain what each check guards against in plain words. Include a specification-curve chart, the IV first stage, and the moderation plots.
2. **Receipt:** results/<date>/robustness/RECEIPT.md, plus the same for stretch/.
3. **Handoff:** docs/<date>/phase-4e-robustness-stretch.md, with the five sections plus "How to resume". The next prompt is prompts/04f_georgia_solar_learning_curve.md.
4. **Updates:** update EXPERIMENTS.md and CLAUDE.md §4-5, then git commit.
5. **Summary:** a short summary, then STOP.

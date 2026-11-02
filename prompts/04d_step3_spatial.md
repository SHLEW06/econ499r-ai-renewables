# Phase 4d: Step 3 (H3), neighbors and spillovers

ECON 499R project. The project root is "AI impact on Renewables".

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (H3 sections and §0), the newest handoff in docs/, and docs/2026-11-01/methods-review.md.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md.
- Plan first and wait for my OK.

## Experiments (Zhang et al. 2026, equations 10-11, p. 6508)
1. **Moran's I** for each outcome (ln_ec, ln_ee, renew_share) and for lagged AI, every year 2015-2025.
   - Use 999 permutations and a fixed seed.
   - Run it with W = row-standardized inverse distance (data/W_inverse_distance_rowstd.csv) and with W = shared border (row-standardize it for the test).
   - AK and HI have no border neighbors, so for the border W either drop them or use zero-policy, and say which. Also run the inverse-distance version without AK and HI.
   - Report I, the expected I, z, and the permutation p.
2. **Model choice tests (added; the paper's Table 11 uses LM tests).** Run LM lag, LM error and their robust versions on the two-way FE Step 1 residuals, if your package supports panels. Report them, but keep the memo's SDM as the main model regardless.
3. **SLX (memo fallback; its theta is the spillover).** Step 1 plus W·AI(t-1), with clustered SEs. Theta is read directly as the neighbor effect.
4. **SDM with state and year FE (memo).**
   - The model: Y = rho·W·Y + b1·AI(t-1) + b2·X + theta1·W·AI(t-1) + theta2·W·X + FE.
   - Use splm or SDPDmod and justify the choice (two-way FE, Lee-Yu bias correction if available).
   - The panel must be balanced. The lagged core sample is 50 x 11 with no gaps; confirm it before estimating.
   - Report rho, b1, theta1, and the **direct, indirect (spillover) and total impacts** of AI with simulated SEs.
   - **H3 rule:** it is judged by the indirect effect's sign. Harmful means positive for ln_ec, negative for ln_ee, negative for renew_share. Theta1 alone is not the spillover, because rho feeds effects back through W.
5. **Checks.** Rerun the SDM with the border W, and without AK and HI.

## Outputs
- **Results:** results/<date>/h3/, covering Moran rows, LM rows, SLX rows, SDM coefficient rows and impact rows. Every row has tags and status.
- **Tables:** results/<date>/tables/h3_*.csv and .tex, with PROVENANCE.md.
- **Figures:**
  - maps of each outcome, 2015 beside 2025, like the paper's Figures 2-4
  - Moran's I by year
  - an impacts bar chart, direct vs indirect, with CIs

## End of phase
1. **Notebook:** notebooks/04d_step3_spatial.ipynb. It should explain these in plain words, with a picture of W:
   - what "neighbors" means here
   - what Moran's I says
   - why the SDM needs impacts

   Then add one section per experiment with a two-line reading.
2. **Receipt:** results/<date>/h3/RECEIPT.md.
3. **Handoff:** docs/<date>/phase-4d-step3.md, with the five sections plus "How to resume". The next prompt is prompts/04e_robustness_stretch.md.
4. **Updates:** update EXPERIMENTS.md and CLAUDE.md §4-5, then git commit.
5. **Summary:** a short summary, then STOP.

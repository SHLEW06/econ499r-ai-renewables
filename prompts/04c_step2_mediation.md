# Phase 4c: Step 2 (H2a, H2b), mediation

ECON 499R project. The project root is "AI impact on Renewables".

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (H2 sections and §0), the newest handoff in docs/, and docs/2026-11-01/methods-review.md.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md.
- Plan first and wait for my OK.

## Experiments (Zhang et al. 2026, equations 5-7, pp. 6502-6503)
Use the same FE, SEs, sample and winsorizing as Step 1. Each run goes through code/R/load_panel.R.

**The three regressions**, for each mediator M and each core outcome Y (ln_ec, ln_ee, renew_share):
- (a) M = b1·AI(t-1) + X + FE
- (b) Y = c1·M + X + FE
- (c) Y = e1·M + e2·AI(t-1) + X + FE

The paper's rule: the channel holds if b1 is significant and c1 and e1 are significant.

**Indirect effect b1 × e1, reported three ways:**
- with the Sobel z: z = b1·e1 / sqrt(e1²·SE_b1² + b1²·SE_e1²)
- with a cluster (by state) bootstrap CI: 999 or more reps, fixed seed
- with the share mediated, b1·e1 / a1, where a1 comes from Step 1

**Mediators:**
1. **M = tech_share (main H2a, Changed).** The NAICS 5415 share, mean-centered or in percentage points. Say which.
2. **M = hma (memo version).** Run it exactly as the memo says. Label in the table and notebook that b1 > 0 is mechanical, because hma is built from AI, so a positive b1 tells us nothing.
3. **M = ln_ea (H2b, memo).** Add the caveat that under state FE, density moves only with nonfarm GDP, which ln_gdp_pc and pop_growth already track. So also report the correlation of within-state ln_ea with those controls.

## Outputs
- **Results:** results/<date>/h2/. One row per regression, plus indirect-effect rows (Sobel and bootstrap). Every row has tags and status.
- **Tables:** results/<date>/tables/h2_*.csv and .tex, with PROVENANCE.md.
- **Figure:** a path diagram per mediator, AI → M → Y, with the coefficients.

## End of phase
1. **Notebook:** notebooks/04c_step2_mediation.ipynb. Explain the four-step idea in plain words with a small diagram. Then give one section per mediator: the equations, the tables, the indirect effect with its CI, and a two-line reading. Include the hma caveat and the ea caveat.
2. **Receipt:** results/<date>/h2/RECEIPT.md.
3. **Handoff:** docs/<date>/phase-4c-step2.md, with the five sections plus "How to resume". The next prompt is prompts/04d_step3_spatial.md.
4. **Updates:** update EXPERIMENTS.md and CLAUDE.md §4-5, then git commit.
5. **Summary:** a short summary, then STOP.

# Phase 4a: lock the method spec and set up the R modeling environment (no results yet)

ECON 499R project (Shunji Lewandowski and Alexander Hendricks, Prof. Fohlin). The project root is the "AI impact on Renewables" folder. Core results are due Nov 17, 2026; the draft is due Nov 24.

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md, the newest handoff in docs/, docs/2026-11-01/methods-review.md, the Methods Memo in admin/, data/receipts/README.md and data/DATA_VALIDATION.md.
- **Data gate:** if any variable in the DATA_VALIDATION.md verdict table is red, stop and tell me. Don't design around bad data. Carry the yellow notes into EXPERIMENTS.md.

**Rules for every 4x phase:**
1. Plan first and wait for my OK.
2. Models run in R. Each driver takes a required `--date YYYY-MM-DD` and fail-fast-checks its inputs.
3. Results go to results/<date>/<experiment>/. These files are append-only. Every row carries a parseable method tag and status (ok / FAILED).
4. The memo version and any added or changed version are separate tags. Neither silently replaces the other.
5. Never edit data/. Never fill in or impute data.
6. Use "associated with," not "causes," unless the design supports causation.

## Part A: the spec (writing only)
1. **Rewrite EXPERIMENTS.md** from methods-review.md §5. Make one subsection per experiment block: H1 core, H1 extras, nonlinearity, heterogeneity, dynamics, H2a, H2b, H3, robustness, stretch, Georgia solar module. Each subsection gives:
   - the question in one line
   - the equation in LaTeX
   - the exact data columns for each term
   - the sample (50 states, DC dropped, 2015-2025, N expected)
   - fixed effects and SE type
   - winsorizing
   - the result that counts as support, with the sign for each outcome. Spell out that renew_share, solar_share and wind_share need a1 > 0, while fossil_to_renew and co2_per_mwh need a1 < 0.
   - output paths
   - method tags
   - whether it is Memo, Changed or Added
2. **Divergence register (EXPERIMENTS.md §0).** List every place the plan differs from the memo, each with: what the memo says, what we run, why, and status. Include all 11 items in methods-review.md §4.
3. **Tag grammar.** Example: `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_<outcome>_<sample>`. Document every field. Never reuse a tag whose meaning changed.
4. **docs/<date>/memo-corrections.md.** Copy the 11 before/after prose fixes from methods-review.md §3 for Alexander, plus the list of non-prose changes.
5. **Analysis calendar.** Phases 4b to 4g with target dates, ending by Nov 17. Give hour estimates per phase. Note which pieces are stretch work and can be dropped.

## Part B: environment and the single loader
1. **R packages:** set up renv or record versions. Needed:
   - fixest (two-way FE, clustered and Driscoll-Kraay SEs)
   - modelsummary
   - spdep
   - splm or SDPDmod (panel SDM with two-way FE and impacts), with spatialreg if needed
   - boot
   - data.table or dplyr
   - ggplot2
   - sf (or tigris) for maps

   Check whether IRkernel works so notebooks can run R. If it doesn't, tell me and propose the fallback: Python notebooks that read the R result CSVs.
2. **code/R/load_panel.R:** one function that every experiment calls. It:
   - reads data/state_panel_2015_2025.csv
   - drops DC
   - builds lags (AI t-1, plus t-2 and t-3 when the data allow)
   - builds the extra variables: coal share, net-exporter flag, high-price flag, South flag, AI squared
   - mean-centers interaction terms
   - winsorizes outcomes and AI at 1/99 over the pooled 2015-2025 sample
   - returns the analysis table and a log of what it did

   Document what it guarantees is identical across experiments. Also load the W matrices and check their state order against the panel.
3. **Smoke check, no estimation:** print N by year, missingness for every model variable, and the ranges of AI and the outcomes. Confirm N = 550 for the lagged core sample. (The 2025 suppressed AI cells don't matter because Step 1 uses the 2024 lag.)

## End of phase
1. **Notebook:** notebooks/04a_methods_spec.ipynb, short. For each experiment block: the equation, what it tests in plain English, the columns it uses, and the support rule. Then the smoke-check tables.
2. **Handoff:** docs/<date>/phase-4a-methods-spec.md. Use the five sections plus "How to resume". The next prompt is prompts/04b_step1_twfe.md.
3. **Updates:** update CLAUDE.md §3-5, then git commit.
4. **Summary to me:** a short summary, and STOP.

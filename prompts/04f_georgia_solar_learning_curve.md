# Phase 4f: Georgia "future of renewables" module, a solar cost learning curve to 2035

ECON 499R project. The project root is "AI impact on Renewables".

**Before anything:**
- Run `date`.
- Read prompts/00_START_HERE.md, CLAUDE.md, EXPERIMENTS.md (Georgia section), the newest handoff in docs/, and docs/2026-11-01/methods-review.md §4 item 11.
- Read the Bolinger, Wiser & O'Shaughnessy (2022) PDF in literature/ (iScience 25, 104378): equations 2-7 on p. 20-21, and the projection method on p. 8-10 and 21.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md. This module can use R or Python; choose one and say why.
- Plan first and wait for my OK.

## What this module is (and is not)
- **It answers** "what could utility-scale solar cost in Georgia by 2035?"
- **It does not answer** "does AI improve renewables." There is no AI variable in it. Learning curves are correlations: the paper itself says "the direction of causality is not clear" (p. 12).
- **Learning is driven by global deployment.** Georgia does not have its own learning rate. Holding Georgia's cost gap to the U.S. average constant is our assumption, and we say so.

## Method
1. **Base cost.**
   - Use Georgia or Southeast utility-scale PV from LBNL Utility-Scale Solar (data/raw/lbnl/..., project-level, through 2024).
   - Use LBNL's LCOE if it is available by region. Otherwise compute LCOE with the paper's equation 1 inputs (CapEx, capacity factor, OpEx, design life, WACC) and document every input and its source.
   - Do NOT use PPA prices as the base, because they include tax credits.
   - If Georgia has too few projects, use the Southeast and say so.
2. **Learning driver:** global cumulative solar PV capacity, 2000-2025 (data/raw/..., IRENA via Our World in Data).
3. **Future global capacity paths, 2026-2035.**
   - Low, central and high scenarios, each tied to a cited published projection.
   - Ask me which sources to use before building them. Don't invent growth rates.
4. **Projection.**
   - C_t = C_base × (X_t / X_base)^b, with b = ln(1 - LR)/ln 2.
   - Main LR = 24% (normalized solar LCOE, full period), which gives b ≈ -0.396.
   - Fan of LR = 12%, 19% (CapEx), 24% and 45% (the 2014-2020 epoch), crossed with the 3 capacity paths.
   - Optional: the paper's equations 5-7 forecast intervals, if we re-estimate.
5. **Check.** Re-estimate the paper's equation 2 on the U.S. national LBNL series, 2007-2024, against global cumulative capacity. Compare it with 24%, and explain any gap (for example, post-2020 supply-chain cost increases, p. 9 and 12).

## Outputs
- **results/<date>/georgia_solar/:**
  - the projection table for 2025-2035, by LR x scenario
  - the base-cost table with inputs
  - the re-estimated learning rate
- **Fan chart.** Compare it with the paper's projected 47% solar LCOE decline from 2020 to 2035 (p. 10).
- **Plain-English paragraph** for the Georgia case box. Name the IRP context: the 2025 IRP plans up to 4,000 MW of new renewables by 2035.

## End of phase
1. **notebooks/04f_georgia_solar.ipynb:**
   - what a learning curve is, with a doubling example
   - the data
   - the base cost
   - the projection fan
   - what we can and cannot claim
2. **Receipt:** results/<date>/georgia_solar/RECEIPT.md.
3. **Handoff:** docs/<date>/phase-4f-georgia-solar.md, with the five sections plus "How to resume". The next prompt is prompts/04g_results_pack.md.
4. **Updates:** update EXPERIMENTS.md and CLAUDE.md §4-5, then git commit.
5. **Summary:** a short summary, then STOP.

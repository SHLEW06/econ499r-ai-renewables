# Phase 4h: the Fang et al. (2025) test, alongside the Zhang test

Context: the team's latest methods plan follows Fang, Lee & Li (2025), Renewable Energy 246, 122969 (the PDF is in literature/). We keep the Zhang test (4b-4e) and add this one, using the same panel, receipts and conventions.
- Follow the rules for every 4x phase in prompts/04a_methods_spec.md, except that this test uses Fang's variables and controls. That's the point; our ctrl4 is only a check.
- Plan first and wait for my OK.

## Part A: data. Build it, check it, then STOP.
1. SEDS outcomes from use_all_btu.csv (in hand), billion Btu, 2015-2024:
   - total renewable energy consumption (RETCB)
   - by type: wind WYTCB, solar SOTCB, geothermal GETCB, hydro HYTCB, biomass BMTCB
   Confirm each MSN code against EIA's SEDS code list first.
2. Energy price: the SEDS total energy average price (TETCD, $/MMBtu). Download the SEDS prices CSV by script.
3. Education: the NCSES state indicator "bachelor's degrees conferred per 1,000 individuals 18-24 years old." Download it by script if NCSES allows; otherwise give me the link. Note which years exist.
4. Real GDP and population from BEA (in hand). EPU national, state and composite (in hand), as annual means.
5. AI job postings by state (Fang's AI measure), from the Stanford AI Index:
   - Each report's Chapter 4 (Economy) gives the number and share of AI job postings by U.S. state for one year: 2022 report → 2021, 2023 → 2022, 2024 → 2023, 2025 → 2024, 2026 → 2025. Check whether earlier reports (2019-2021) have state data for 2018-2020.
   - Try the chapter PDFs first (hai-production.s3.amazonaws.com or hai.stanford.edu). Extract the state tables with pdftotext, and record the figure and page for every year.
   - If the PDFs don't parse cleanly, give me the "Access the public data" Google Drive link from each chapter and I'll download the folders by browser.
   - Checks: 51 rows per year; the states sum to the national total in the same report; 3 states per year spot-checked against the report text.
   - Record the vendor per year (Emsi Burning Glass or Lightcast) and any note that counting changed between editions.
   - Save data/ai_job_postings_state.csv (state, year, postings, share_pct, edition, figure, page) with a receipt.
6. Fang's split variables:
   - electricity consumption, electricity price, net producer (in hand)
   - R&D (NSF, in hand, 2017-2023)
   - per capita income (BEA SAINC, in hand)
   - Census region
   - Extreme weather isn't available (NOAA is down); record it as not run.
7. Save each as a side table, plus data/fang_panel.csv (50 states + DC, 2015-2025). Write a receipt per source and add DATA_VALIDATION.md ratings. Then STOP and show me the coverage table (variable × years) and the AI postings checks.

## Part B: models (after my OK)
All variables in logs, as in Fang. Run two AI measures side by side: ln(AI job postings), Fang's measure, and ln(data-center jobs), our count. Our per-1,000 measure is a check.
1. Replication: Fang's eq. 2 on 2018-2021 with DC (N = 204 if the postings cover those years), state FE only. Start with AI and EPU, then add EP, GDP, POP and EDU one at a time (their Table 2, columns 1-6). Compare with their AI coefficients (0.0428 to 0.0561).
2. Bridge table, one change at a time: Fang's spec → add year FE → lag AI one year → cluster SEs by state → extend the sample (2015-2024, or the years the postings cover) → drop DC. This shows which step changes the answer.
3. Moderation (Fang's eq. 3): AI × EPU for composite, national and state EPU, centered. Report the AI slope at the 25th and 75th percentiles of EPU. Run it under both Fang's spec and our two-way FE spec.
4. By type: wind, solar, geothermal, biomass and hydro as outcomes. Drop zero-consumption state-years as Fang did, and report N.
5. Heterogeneity: Fang's above/below-mean splits (electricity consumption, price, net producer, R&D, income) and the four regions, for comparability. Then the same groups as interactions in one model, which is our actual test.
6. Placebo: AI(t+1) in place of AI(t-1), and both in one model.
7. Robustness: renewable share of total energy (RETCB / TETCB) as the outcome; drop 2020; add the RPS control; use our ctrl4 control set.

Outputs:
- results/<date>/fang/, with tags prefixed fang_
- tables, plus a chart of the AI coefficient across the bridge steps
- notebooks/04h_fang_test.ipynb: what Fang did, what we replicate, what changes and why, in plain English
- a receipt and a handoff
- an EXPERIMENTS.md section "Fang test" with its own divergence list
Commit and STOP.

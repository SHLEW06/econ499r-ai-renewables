# Extend: data cross-check, AI by renewable type and Georgia, what AI affected, what drove the national trend, and a better AI measure

Read first: CLAUDE.md, EXPERIMENTS.md, prompts/08_finalize.md and its run log (docs/*/finalize-run-log.md), the newest handoffs in docs/, data/receipts/README.md, the current fang_results.csv, and Fang, Lee & Li (2025) in the papers folder.

## Before you start
- If 08 §1 (Fang's methods, including the year-by-year SEDS rebuild) isn't marked done in its run log, finish 08 §1-2 first, because this prompt needs the rebuilt basis. If 08 §3-5 aren't done, skip them: §7 here rebuilds the results pack, workbook and packages once for both prompts.
- Run `date`. Show me a one-screen plan with time estimates and the download list, and wait for my OK.
- Then run §1-§8 in order without stopping, except under the stop rules. If I say "core only", run §1-3, then §6-8.
- Keep a run log at docs/<date>/extend-run-log.md, marking each section done once it's committed. If interrupted, resume from the first section not done.
- Commit after each section, one topic per commit. Don't push.

## Rules (all earlier rules still hold)
- **Pre-register.** Before running any new model, add it to EXPERIMENTS.md under a new section "Extensions, Nov 2026", with:
  - the outcome, AI measure and spec
  - the expected sign and why
  - which test family it belongs to

  Don't add or drop outcomes after seeing results. If you must, log it as a deviation.
- **Multiple testing.**
  - Report every estimate.
  - Within each family (by type; AI-impact outcomes; AI index), add Benjamini-Hochberg q-values next to the p-values.
  - Call something a finding only if q < 0.10 and its lead (AI at t+1 in place of t-1) is clearly smaller.
- **Main spec unless stated otherwise:** 50 states, two-way FE (state and year), AI(t-1), ctrl4, SEs clustered by state, winsorized 1/99. Run both AI measures: the 518210 jobs share and AI postings.
- **Data:** never edit raw data, invent values or impute. Where coverage is short, shorten the sample and say so.
- **Downloads:** by script only, from the public sources listed here, with one receipt per source (URL, date, file hash, what was kept). No Emory-licensed databases.
- **Wording:** "associated with," never causal language.
- **Census key:** never print it.
- **Stop and ask me only if:**
  - a reproduction gate fails
  - a data check comes out red
  - something would need deleting
  - a download outside this list is needed
  - §5 can't get at least three index components covering 2015-2023

## 1. Cross-check our data against Fang (no year FE) [easy; data in hand]
1. **Descriptive statistics.**
   - Copy Fang's descriptive-statistics table (mean, SD, min, max and N for each variable) into results/<date>/extend/fang_table1_published.csv, with the page number. If the paper has no such table, say so and use the means implied by Table 2's constants instead.
   - Compute the same statistics on our Fang panel three ways: current SEDS, k = 2.6, and the rebuilt basis from 08.
   - For each variable, show ours, theirs, and the difference in SD units. Flag any difference over 0.25 SD.
   - If a gap is a constant shift that matches a unit change (for example ln 1,000 = 6.91), say so.
2. **Coefficients.**
   - Make one table for Fang's Table 2, columns 1-6, state FE only, with four versions side by side: Fang published | current | k = 2.6 | rebuilt.
   - Include the control coefficients (EPU, EP, GDP, POP, EDU).
   - Mark whether Fang's number falls inside our 95% CI.
3. **Trend tests.** Use Fang's spec (column 6, state FE, no year FE), on both the current and the rebuilt basis.
   a. Add a linear year trend. Report the AI coefficient with and without it.
   b. Run a placebo with an unrelated trending variable:
      - Before looking at any results, pick two QCEW industries that have nothing to do with energy and grew nationally about as fast as AI postings did in 2018-2021. Write the choice and the reason in EXPERIMENTS.md.
      - Put ln employment in each industry in place of ln AI.
      - Report the coefficient and p in Fang's spec and in ours.
4. **Verdict:** one paragraph. Does our data match Fang's? Which variables match, which don't, and why?

## 2. Which renewable did AI move, and what it means for Georgia [easy-medium; data in hand]
1. **Outcomes by type, 2015-2025, in-state**, from the EIA-923 and EIA-860 data already in the panel.
   - Types: wind, utility-scale solar, small-scale solar (if in the panel), hydro, geothermal, biomass.
   - For each type, three measures:
     - share of in-state generation (in levels, which keeps zeros)
     - ln generation (zeros dropped; report N)
     - MW added per 1,000 MW of 2015 total capacity
2. **SEDS consumption by type.**
   - Split biomass into wood and waste vs biofuels (fuel ethanol, biodiesel).
   - Add total renewables excluding all biomass, and excluding biofuels only.
   - This tests whether the negative total is transport fuel rather than power.
3. Run the main spec for each, with both AI measures and BH q-values across this family. Add the lead placebo for anything with p < 0.10.
4. **Georgia.**
   a. **Profile, 2015-2025:**
      - Georgia's AI measures: level, change, and rank among states
      - its generation mix and capacity additions by type
      - large-load commitments (Q2 2026 report, p. 8; dockets 55378 and 56002)
   b. **What our estimates imply for Georgia:**
      - For each type, multiply the coefficient by Georgia's actual change in AI(t-1) from 2015 to 2025, with a 95% CI, and put it next to Georgia's actual change in that outcome.
      - Write one sentence for each: at most, how much of Georgia's change the AI association could account for.
   c. **Chart:** across states, the 2015-2025 change in AI against the change in solar share and in renewable share, with Georgia labeled.
   d. **Georgia Power's plans:**
      - From the Georgia PSC documents already in the project, summarize what Georgia Power's latest IRP plans for coal, gas, solar and storage, and how it ties those plans to large-load growth.
      - Cite the docket and page for every claim.
      - If the documents aren't there, say so; don't download them.

## 3. What has AI been associated with? [medium; data in hand]
Pre-register this family first, with expected signs:
- electricity sales per person, in logs, for the commercial, industrial and residential sectors (much data-center load is billed as commercial)
- retail price by sector (cents/kWh)
- generation shares: gas, coal, nuclear
- capacity added per 1,000 MW of 2015 capacity: gas, solar, wind, and battery storage (if in the panel)
- net imports: (retail sales - in-state generation) / retail sales
- power-sector CO2: total (ln) and per MWh

How to run it:
- Use the main spec with both AI measures and BH q-values across the family.
- Run the lead placebo for anything with q < 0.10.
- For outcomes that pass, run one extra model with AI x restructured market (regulated vs restructured), and document the source of that classification.

## 4. Why did renewables grow nationally? [medium; small downloads]
1. **Year effects.** From the main two-way model, extract the year effects for renewable share, ln wind generation and ln solar generation. Chart them with 95% CIs.
2. **National drivers, 2015-2025**, each with a receipt:
   - **Federal tax credits:**
     - the wind PTC phase-down by construction-start year and the solar ITC rate by year
     - coded from CRS reports R43453 (PTC) and IF10479 (ITC) and from the Inflation Reduction Act (P.L. 117-169)
     - cite the page for each year's value
   - **Costs:** LBNL utility-scale solar data (have), the LBNL Land-Based Wind Market Report data file (download), and Lazard (have) as a check
   - **Gas price:** Henry Hub natural gas price (EIA)
   - **State mandates:** state RPS/CES requirements (LBNL, have)
   - **National AI totals** (have)
3. **Drivers model.** Drop the year FE and replace them with measured drivers that vary by state:
   Y_st = mu_s + b1 RPS_st + b2 (solar resource_s x solar cost_t) + b3 (wind resource_s x wind cost_t) + b4 (solar resource_s x ITC_t) + b5 (wind resource_s x PTC_t) + b6 (2015 gas share_s x gas price_t) + national main effects of those drivers + a AI_s,t-1 + ctrl4
   - **Resource data:** NREL state-level solar and wind resource. If you can't find a public NREL state table within 30 minutes, use each state's 2015 wind and solar capacity factors from EIA-923/860 instead, and say so.
   - **Report:**
     a. how much of the year-effect path the drivers reproduce: the correlation and R-squared between the fitted national average and the year effects
     b. the AI coefficient in three models: state FE only, the drivers model, and two-way FE

     If AI goes to about zero once the drivers are in, that answers "isn't the national trend AI?"
4. **Write-up:** one paragraph on what drove the national trend, with citations.

## 5. A better AI measure [hardest; new downloads]
1. **Components**, by state-year, per capita or per 1,000 workers, in logs:
   - **Infrastructure:**
     - QCEW 518210 employment, establishments and wages (have)
     - Epoch AI data-center data by state (have; note its coverage)
   - **Talent:**
     - AI job postings (have)
     - BLS OEWS state employment in three occupations: computer and information research scientists (15-1221), data scientists (15-2051) and software developers (15-1252). Document any SOC code changes across years.
   - **Innovation:**
     - AI patents by inventor state, from the USPTO AI Patent Dataset (AIPD 2023: patents and pre-grant publications through 2023)
     - join to PatentsView inventor locations, count by filing year, and split each patent fractionally across its inventors
     - document the AIPD threshold you use
   - **Validation only, not in the index:**
     - the Census BTOS share of businesses using AI, by state, from Sept 2023
     - note the question change, and that multi-state firms are left out of state estimates
2. **Exclusion rule:** no electricity, energy or emissions variable may enter the index. Those are outcomes.
3. **Build:**
   - Index A: z-score each component, average within each dimension, then average the dimensions.
   - Index B: the first principal component. Report the loadings and the variance explained.
   - Sub-indices for infrastructure, talent and innovation.
   - Use only years where every component exists (expect 2015-2023). No imputation. Include a coverage table.
   - Diagnostics:
     - correlations among the components
     - Cronbach's alpha
     - within-state SD
     - correlation of the 2024 index with the BTOS 2024 average
4. **Use:**
   - Rerun three sets of outcomes with Index A, Index B and each sub-index:
     - H1 core (ln_ec, ln_ee, renew_share)
     - the by-type outcomes from §2
     - the §3 family
   - Report effects per within-state SD, with BH q-values within this family.
5. **Measurement-error check:**
   - Instrument postings with 518210 jobs, and the reverse (2SLS, same FE).
   - Report the first-stage F. If F < 10, call the check uninformative.

## 6. Notebook
- Create notebooks/09_extend.ipynb with one section per part above. Each section has: the question, what we ran, the equation, a table, one chart, and a two-line plain-English reading.
- Use relative paths only.
- Restart the kernel, run top to bottom, and commit the executed notebook.

## 7. Refresh outputs
Do 08 §3-5 once, now covering both 08 and this prompt:
- findings.md, with a new section "Extensions"
- the tables, number_check (every number traced), methods_section.tex and project-summary.md
- the results PDF, following the rules in 08 §3
- the master workbook: new data, Variable Finder rows, receipts and the link check. Never let LibreOffice save the final file.
- the team zip and release/github, with their scans

Commit; don't push.

## 8. Show me
1. **§1:** the descriptive-statistics comparison (flagged rows only), the Table 2 comparison, the trend and placebo results, and the verdict.
2. **§2:** the by-type table with q-values, Georgia's implied vs actual changes, and the IRP summary.
3. **§3:** the AI-impact table with q-values, and which outcomes pass the lead placebo.
4. **§4:** the share of the year-effect path the drivers explain, and the AI coefficient in the three models.
5. **§5:**
   - coverage, loadings, alpha and the BTOS correlation
   - the H1 results with the index
6. A 6-line plain-English summary of what's new.
7. Any deviations from the pre-registration.
8. **Housekeeping:**
   - the files changed and the count of traced numbers
   - the link-check counts and confirmation that the notebooks ran cleanly
   - the push command

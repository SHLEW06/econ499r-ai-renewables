You're helping me (Shunji Lewandowski, modeling side) with an ECON 499R research project at Emory (Prof. Caroline Fohlin). My partner is Alexander Hendricks (data and finance side). We are testing Zhang, Ji, Dou and Hao (2026), "Blessing or Peril? The Impact of Artificial Intelligence on the Energy Transition: Evidence from China" (Applied Economics 58(32)), on the 50 U.S. states, 2015 to 2025. Core results are due Nov 17, 2026; the draft is due Nov 24.

## What's in this folder
- reference/Methods_Memo.pdf: our submitted methods (Oct 22). This is the spec. Read it fully first.
- reference/Zhang_et_al_2026.pdf: the paper we transpose (equations 4 to 11).
- reference/expected_values.md and reference/*.csv: numbers from a first pass, to check the rebuild against.
- data_links.md: every data source with direct links, marked Script or Browser.
- download_all.py: downloads everything scriptable into raw/.
- scripts/: Python that already works. build_panel.py builds the state-year panel. ferc_fin.py and sec_fin.py build the utility and company financials. prelim.py runs a first-pass Step 1, SLX and Moran's I.
- R/econ499r_step1_to_3.R: a first R port of Steps 1 to 3. It has not been run yet.

## How I want you to work
1. Read the memo, the paper's methods section, and this folder. Then write a short plan and wait for my OK before writing modeling code.
2. Set the repo up with my project-conventions skill if you have it: dated docs/YYYY-MM-DD/ change logs, results/ and logs/ split by date, and a CLAUDE.md. Use git. Never edit anything in raw/.
3. Use R for the models, as the memo says: fixest for panels, spdep for Moran's I, and spatialreg or splm for the spatial Durbin model. Use renv or note package versions. Python is fine for the data build.
4. Follow the memo's specification exactly. When you think something should change, keep the memo version and add the alternative as an extra column or spec. Log every deviation in docs/ with the reason.
5. Never invent or fill in data. If a source fails or needs a browser (the LBNL RPS file, Georgia PSC filings), stop and tell me what to download and where to put it.

## Tasks, in order
A. Data. Run `python download_all.py`, then `python scripts/build_panel.py raw out`. Check the output against reference/expected_values.md: 561 rows (550 without DC), the Georgia values, and the four suppressed 2025 cells (AK, ND, SD, WY). Write a data-check log.

B. Step 1 (H1), memo equation: Y_st = a0 + a1 AI_s,t-1 + a2 X_st + mu_s + tau_t + e_st.
- Y is ln_ec, ln_ee and renew_share. Also run solar_share and new_renew_mw as extra outcomes.
- X is ln_gdp_pc, manuf_share, price_c_kwh and pop_growth. Use state and year fixed effects and cluster SEs by state.
- Use the 50 states only (drop DC). Winsorize outcomes and AI at the 1st and 99th percentiles.
- First reproduce reference/prelim_step1_slx.csv in R (within rounding), then make clean tables.

C. Step 2 (H2a, H2b): the memo's mediation equations 5 to 7, plus the Sobel z.
- Run it with M = hma (the memo version) and with M = tech_share. hma is built from AI itself, so b1 is positive by construction. Report both and explain this in the log.
- Run the same steps with M = ln_ea for H2b.

D. Step 3 (H3).
- Compute Moran's I by year for each outcome with the inverse-distance W and with the border W. Alaska and Hawaii have no border neighbors, so run it with and without them.
- Run SLX: add W times lagged AI to Step 1.
- Run the SDM with two-way fixed effects. Report direct, indirect and total impacts, not just theta, because theta alone is not the spillover.

E. Step 4: the memo's robustness list.
- Swap the outcome (fossil_to_renew, seds_mmbtu_pc).
- Change the sample: drop 2020; drop AK and HI; drop VA.
- Swap W.
- Add two extra specs: an RPS control (once I supply the LBNL file) and AI squared.

F. Outputs.
- Regression tables as CSV and LaTeX (etable or modelsummary).
- Maps of each outcome, 2015 beside 2025, like the paper's Figures 2 to 4, plus a table of means by year.
- results/summary.md: what each result means for H1 to H3 in plain language, for Alexander.

G. Only after A to F are done: the memo's stretch goals.
- Moderation: AI x broadband and AI x R&D. The download script fetches the NOAA and NSF files; broadband needs a CENSUS_KEY.
- A shift-share instrument with the Kleibergen-Paap test.
- The Hansen threshold model on energy equity.

Known issue to keep in view: NAICS 518210 counts all data processing and hosting jobs, not only AI data centers. Georgia ranks 2nd in 2025, above Virginia. Flag anything in the results that looks driven by that.

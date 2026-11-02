# ECON 499R context handoff (as of Sun Nov 1, 2026)

Read this first. It covers the project's scope and history, the methods, the data built so far, first results, the Grijalva interview, open decisions, and where every file lives.

## 1. Who, what, when
- **Course:** ECON 499R research seminar, Emory, Prof. Caroline Fohlin (ATL Economics), Fall 2026.
- **Team:**
  - Shunji Lewandowski: modeling side. Use this name on all assignment materials.
  - Alexander Hendricks: data and finance side. He builds and checks every variable in a spreadsheet before it goes into R.
- **Where the work lives:** Google Drive, plus the "ECON 499R" folder on Shunji's laptop. Literature PDFs are in ECON 499R/NEW TOPIC/SOURCES, named in APA style with (PR) peer-reviewed or (w) working-paper prefixes.
- **Research question (approved by Prof. Fohlin Oct 17, broadened Oct 19):** Does AI improve renewable energy, and what does the future of renewables look like (growth, efficiency)? It must include a Georgia component.
- **Topic history:**
  - Georgia Power residential rates and data centers, then
  - whether data-center demand raises the value of gas vs. renewable power plants (dropped: plant sale prices aren't public), then
  - the current question.
- **Deadlines:**

  | Date | Milestone |
  | --- | --- |
  | Fri Oct 23 | Methods Memo due (dated Oct 22, submitted) |
  | Fri Oct 30 | Methods presentation (done) |
  | Tue Nov 17 | Cutoff for stretch goals; Steps 1 to 3 must be done |
  | Tue Nov 24 | Final draft, last work day |
  | Tue Dec 1 | Turn-in |

- **Course pace:** about 6 hours a week each. Each person keeps a separate hours tracker; Shunji's is ECON499R_Hours_Tracker_Lewandowski.xlsx.

## 2. The method (Methods Memo, Oct 22, by Alexander)
- **Design:** a U.S. test of Zhang, Ji, Dou and Hao (2026), "Blessing or Peril? The Impact of Artificial Intelligence on the Energy Transition: Evidence from China," Applied Economics 58(32), 6495-6513. That paper covers 261 Chinese cities, 2006-2019, and uses robot density as its AI proxy.
- **Our sample:** 50 states, 2015-2025, which gives 550 state-years.

### Variables

| Role | Variable | Definition |
| --- | --- | --- |
| Outcome | EC | ln(MWh sold per person) |
| Outcome | EE | ln(real GDP per MWh sold) |
| Outcome | ES | Renewable share of in-state generation |
| Outcome (extra) | New renewable MW | Change in renewable capacity from the prior year |
| Paper-matching check | Fossil-to-renewable ratio | Fossil MWh / renewable MWh |
| Cause (AI) | AI_st | 1,000 x NAICS 518210 jobs / all jobs (BLS QCEW), lagged one year |
| Controls | X | ln GDP per person, manufacturing share of GDP, average electricity price (revenue/sales), population growth |

- **Estimation:** state and year fixed effects, SEs clustered by state, variables winsorized at the 1st and 99th percentiles.

### Steps
1. **H1, two-way fixed effects:** Y_st = a0 + a1 AI_s,t-1 + a2 X_st + mu_s + tau_t + e_st.
   - Supported if a1 is below 0 for EC, above 0 for EE, and above 0 for ES.
2. **H2a and H2b, mediation:** paper equations 5 to 7 plus a Sobel test.
   - H2a mediator: human-machine alignment (HMA), the paper's coupling index of AI and the NAICS 5415 tech-worker share.
   - H2b mediator: economic agglomeration (EA), nonfarm GDP per square mile.
3. **H3, spillovers to neighbors:**
   - Moran's I to check whether neighboring states have similar outcomes.
   - Spatial Durbin Model with an inverse-distance matrix W (the border matrix as a check). SLX is the fallback.
   - Supported if neighbors' AI has the harmful sign ("siphoning").
4. **Robustness:**
   - Swap the outcome (fossil-to-renewable ratio).
   - Swap the cause (data-center MW).
   - Change the sample: drop 2020; drop AK and HI; drop VA.
- **Stretch goals:**
  - Moderation: AI x broadband, AI x R&D share.
  - Hansen threshold model on energy equity (GDP share / electricity share).
  - Shift-share instrument (national 518210 growth x each state's 2015 share) with the Kleibergen-Paap test.
- **Software:** R with fixest, spdep and spatialreg (Stata is the alternative). Shunji runs the models.
- **What the memo expects:** consumption flips sign versus China (data centers use electricity). Efficiency, the channels and spillovers match. The energy mix is positive in market states and weak in regulated Georgia.

### Changes recommended but NOT yet adopted (decide with Alexander)
From Claude's Oct 25 paper review and the Oct 30 guide.

- **Use the tech-worker share directly instead of HMA.** HMA is built from AI, so regressing it on AI is positive by construction.
- **Report SDM direct and indirect impacts,** not theta alone.
- **Move the RPS (renewable mandate) control into the core model.**
- **Use AI squared instead of the Hansen threshold model.**
- **Possibly switch the main AI measure to AI patents per capita by inventor state** (USPTO AI Patent Dataset plus PatentsView) or the AI job-postings share. Keep data-center jobs as an "AI load" variable.
- **Other additions from Oct 25:**
  - solar and wind outcomes;
  - a next-year-AI placebo test;
  - region-by-year effects;
  - an AI x South interaction;
  - citing Fang, Lee and Li (2025, Renewable Energy 246, 122969; the closest U.S. state-level precedent), Melguizo et al. (2026) and Bolinger et al. (2022);
  - a Bolinger learning-curve module projecting Georgia solar cost to 2035 (LBNL Utility-Scale Solar data).

The current Claude Code prompt (CLAUDE_CODE_PROMPT.md) keeps the memo spec and adds these as extra columns: tech_share, RPS, AI squared, SDM impacts.

## 3. Data built so far (Oct 30; rebuilt identically from fresh downloads Nov 1)

### The state panel
- **File:** state_panel_2015_2025.csv, 561 rows x 80 columns (50 states + DC, 2015-2025).
- **Sources:**
  - EIA state files: generation, capacity, sales/revenue/price, emissions
  - EIA SEDS
  - BLS QCEW for 518210, 5415 and all industries, 2014-2025 (2014 is only there for the lag)
  - BEA SAGDP and SAINC
  - Census Gazetteer (land area, centroids)
  - Census county adjacency (border matrix)
- **Gaps:**
  - 518210 is suppressed for AK, ND, SD and WY in 2025 (left blank).
  - CO2 data and SEDS end in 2024.
  - EIA state generation is utility-scale only: no rooftop solar.
- **Workbook:** ECON499R_Data_Workbook_Lewandowski_Hendricks.xlsx. Tabs:
  - Core Panel (derived columns are live formulas)
  - Full Panel and Codebook
  - Prelim Results
  - FERC1 Utilities, FERC1 Cost by Tech and FERC1 Plants (FERC Form 1 via Catalyst Cooperative PUDL, 2015-2025)
  - SEC Companies (58 SEC filers: utilities, renewables developers, clean-tech, power producers, coal/gas/oil)
  - inverse-distance and border weight matrices
  - Sources
- **Download links:** every link is in data_links.md and the "Download links" tab of the guide doc. download_all.py fetches everything scriptable.
- **Needs a browser:**
  - the LBNL RPS/CES spreadsheet (June 2026)
  - Georgia PSC filings after the Q1 2026 large-load report
  - Cleanview full export, USPTO AI patents and PatentsView
  - Bloomberg stock prices (Goizueta Business Library; licenses forbid scripts)
- **Needs a free key:** Census ACS broadband (S2801).

### Key facts from the data
- **Georgia renewable share:** 6.1% (2015) to 12.9% (2025). Solar went from 0.1% to 7.7%.
- **Georgia's 2025 generation mix:** gas 38.6%, nuclear 35.2% (Vogtle 3 and 4), coal 13.7%, solar 7.7%, wood/biomass 3.1%, hydro 1.9%.
- **Georgia NAICS 518210 jobs:** 8,346 (2015) to 24,620 (2025), which is 5.03 per 1,000 workers and 2nd of 50 states. Washington is 1st at 6.48; Missouri 4.98; Virginia 4.86. Georgia ranking above Virginia suggests 518210 also counts general data processing, not only AI data centers. This is the biggest measurement caveat.
- **Within-state movement in AI is small** (SD 0.57 per 1,000), so statistical power is limited.

## 4. First results (Python pyfixest, Oct 30)
These are not yet re-run in R. N = 550; state and year fixed effects; state-clustered SEs.

| Outcome | a1 (own lagged AI) | p |
| --- | --- | --- |
| ln EC | -0.0016 | 0.79 |
| ln EE | 0.0022 | 0.71 |
| Renewable share | -0.0101 | 0.10 |
| Solar share | -0.0001 | 0.98 |
| New renewable GW | 0.076 | 0.07 |

- **SLX neighbor terms:** none significant at 5%.
- **Moran's I:** outcomes cluster. The renewable share rose from 0.09 (2015) to 0.16 (2025); EC and EE sit at 0.18 to 0.20; all p <= 0.002. The AI measure itself does not cluster.
- **Step 2b:** AI does not move the tech-worker share (p = 0.43).
- **Plain reading:** there is no within-state link between data-center jobs and energy use or efficiency yet. The renewable share leans slightly negative. A spatial model is justified.

## 5. Interview: Prof. Santiago Grijalva, Georgia Tech ECE (Oct 28, 2026, 27:47)
Grijalva is Georgia Power Distinguished Professor and directs the ACES Lab. The interviewers noted he spent seven years at PowerWorld. The transcript is Grijalva_interview_transcript_2026-10-28.txt, a machine transcript with names corrected.

### How Georgia's power system works
- Georgia is vertically integrated: Georgia Power (Southern Company) owns generation, transmission (69 kV and up) and distribution (down to 12.7 kV), and manages customers.
- Deregulated states instead run competitive day-ahead and spot markets. Texas also has retail choice.
- Georgia's rates are below the U.S. average, its transmission is strong, and it has built nuclear.
- He said Georgia has "not been very progressive" on renewables, but renewables are growing. He put solar at "more than about 15%," mostly utility-scale rather than rooftop. EIA shows 7.7% of 2025 generation, so his figure may be capacity or include other sources. Use the EIA number.
- Georgia has mandates for solar and energy storage. Its diversified mix and reliability attract data centers and manufacturing.

### Data access
- Use EIA for generation, prices, plant incremental costs and revenues.
- The Georgia PSC hosts the Integrated Resource Plan (IRP): about 800 pages, a 10-15 year plan, public, redone about every three years.
- Grid models (lines, topology, parameters) are confidential critical-infrastructure data. Getting them takes months of legal review; he said FERC fines run about $1 million per day for losing such data. He gives students synthetic data. Don't request utility grid data.

### Valuing plants and finances
- Use EIA cost and revenue data, balance sheets of public utilities like Southern Company, and IRP and rate-case economics.

### Solar and storage
- Solar is variable and non-dispatchable.
- Without storage, a solar-connected transmission line is used only about 20 to 25% of the time. Co-located storage firms solar output.
- Flexible demand: Georgia Tech buys on a Georgia Power real-time price, updated about every 15 minutes, and shifts load.
- Microgrids (hospitals, data centers, Georgia Tech) are both software and infrastructure.

### Modeling advice
- PowerWorld has a free demo and MATPOWER has synthetic cases, but both need grid data.
- He suggested "resource-only" modeling instead: resource costs, generation mix, prices and rates. That fits our solar cost projection idea.

### AI
- "Smart grid" is a 15-year-old term. He expects AI to improve forecasting and operations a great deal and make algorithms faster.
- The risks he named are cybersecurity, hallucinations and precision. This is a good quote for the mechanism slide.

### Note
The memo's five standard interview questions were mostly not asked. Say so in the report.

## 6. Georgia case box material
- **Dockets:**
  - 56002: 2025 IRP, filed Jan 31, 2025, approved Jul 15, 2025
  - 56003: DSM plan
  - 55378: 2023 IRP Update; home of the quarterly Large Load Economic Development Reports
  - 56298 and 56310: about 10,000 MW of gas, batteries and some solar certified Dec 19, 2025
  - 57171: RTP revenue credit and allocation methodology; hearing Nov 12, 2026
  - 57243: investigation into the legality of an electric service arrangement; earlier notes call it a petition against VoltaGrid; hearing Dec 9, 2026
  - Others: 56765 (fuel cost recovery), 56368 (2032-33 all-source RFP), 56139 (2025 storage RFP), 57154 (CARES 2025 renewable PPAs)
- **2025 IRP highlights:**
  - about 8,500 MW of load growth over six years
  - up to 4,000 MW of new renewables by 2035 (1,100 MW first)
  - more than 1,500 MW of batteries
  - 1,000+ miles of transmission
  - base rates frozen through 2028
- **Q1 2026 Large Load report (May 15, 2026):**
  - total pipeline 76,200 MW, of which 73,100 MW is large load
  - near-term (winter 2028/29) large load 23,600 MW
  - commitments 12,400 MW
- **Events:**

  | Date | Event |
  | --- | --- |
  | Nov 5, 1 pm ET | Southern Company Q3 earnings webcast |
  | Nov 12, 9:35 am | PSC hearing, Docket 57171, 244 Washington St SW |
  | Nov 18 | ATL CleanTech Connect (Georgia Tech) |
  | Dec 2 | TAG Data Center Summit, Truist Park |
  | Dec 9, 10 am | PSC hearing, Docket 57243 |

## 7. Contacts and interviews
- **Done:** Santiago Grijalva (Oct 28).
- **Kristin Phillips** (Emory Anthropology; Sloan-funded study of data-center energy in the South): earlier notes conflict. One says she was already interviewed; another says an email was drafted. Confirm, and check the "AI REVIEW + Phillips Interview" folder.
- **Yu Ding** (Georgia Tech ISyE): unavailable, per earlier notes.
- **Drafted or listed, status unknown:** Laura Taylor (GT EPIcenter), Daniel Molzahn (GT ECE, backup), Matthew Oliver, Gaurav Doshi, Mindy Goldstein, Cyrus Bhedwar, Daniel Matisoff, Joachim Seel, Robert O'Reilly, Dev Millstein, Tony Harding, Eugenie Dugoua. Also organizations: SELC Georgia, Walton EMC, Oglethorpe Power / Green Power EMC, CEBA, GIPL, Drawdown Georgia, Silicon Ranch, Google Douglas County.
- **Before using interview material:** confirm with Prof. Fohlin whether interviews need consent forms. The memo still lists generic interviewees; update it to the actual names.

## 8. Open items, in order
1. Organize the research folder and catalog every dataset (separate Claude Code prompt).
2. Re-run Steps 1 to 3 in R and match the Python numbers (CLAUDE_CODE_PROMPT.md).
3. Decide with Alexander: keep 518210 as the main AI measure or switch to AI patents; which recommended changes to adopt.
4. Get the LBNL RPS file and add the RPS control. Pull the Q2 and Q3 2026 large-load reports.
5. Run Step 4 robustness, then stretch goals if time allows before Nov 17.
6. Write up the Georgia case box from the IRP, the dockets and the interview.
7. Housekeeping:
   - Replace the Weeks 1-5 placeholder hours in the tracker (81.0 estimated through Week 8; Alexander's shows 48.0).
   - Confirm the titles of Sun, Li and Wang (2025), Sustainable Development 34(3), doi 10.1002/sd.70547, and Xu, Chen, Yang and Shao (2025), World Development 195, 107126.
8. Correction to remember: Alvarez et al. (NBER WP 35194, revised Sept 2026) find positive electricity-price effects that emerge later. Not "no clear effect."

## 9. Files and links
- **Guide doc** (Oct 30; data, methods, interview, first results, Download links tab): https://claude.ai/artifact/JfRKdHdCNpiRjgsmQinMXL
- **Paper review and methods plan** (Oct 25): https://claude.ai/artifact/Cr88DbWeUkFPNKP3mkcJ3K
- **Sources and methods doc** (Oct 19, 52 sources, 44 peer-reviewed): https://claude.ai/code/artifact/e22c8f9d-b52d-463d-a063-11df085dff73
- **Check-in brief** (Oct 20): https://claude.ai/code/artifact/db58034c-f85e-43a2-b48f-2b577ae3402b
- **Lab notebook:** https://claude.ai/code/artifact/d51076cd-8439-42e9-9482-24f83cb0b4b2
- **Local files:**
  - ECON499R_Data_Workbook_Lewandowski_Hendricks.xlsx
  - ECON499R_csv_for_R.zip
  - econ499r_starter.zip (scripts, R, download_all.py, data_links.md, the memo, the Zhang paper, check values, this handoff)
  - Grijalva_interview_transcript_2026-10-28.txt
  - ECON499R_Hours_Tracker_Lewandowski.xlsx

## 10. How Shunji likes to work
- Verify every number against the primary source; don't guess.
- Separate what authors or sources say from your own assessment.
- Cite pages, tables or links.
- Follow the memo's spec; flag and log any deviation instead of changing it silently.
- Plain-English summaries for Alexander.
- Never invent or fill in data.

# Artificial Intelligence and Renewable Energy in U.S. States, 2015–2025

**ECON 499R · Emory University · Fall 2026**
Shunji Lewandowski (modeling) and Alexander Hendricks (data and finance) · Advisor: Prof. Fohlin

> All results in this repository are **associations**. Nothing here shows that AI causes a change in energy use or renewable energy.

---

## Contents

1. [Overview](#overview)
2. [Main findings](#main-findings)
3. [Methods: the Fang test](#methods-the-fang-test)
4. [Methods: the Zhang test](#methods-the-zhang-test)
5. [Data](#data)
6. [Repository layout](#repository-layout)
7. [Getting started](#getting-started)
8. [Reproducing the results](#reproducing-the-results)
9. [Documentation](#documentation)

---

## Overview

Fang, Lee and Li (2025, *Renewable Energy* 246, 122969) report that U.S. states with more AI job postings consumed more renewable energy in 2018–2021. This project asks whether that finding holds:

- **on the data Fang used**, and on the same data after the U.S. Energy Information Administration (EIA) changed how its State Energy Data System (SEDS) counts renewable energy in October 2023;
- **under a standard panel design**, with year effects, a one-year lag, clustered standard errors and a longer sample;
- **with a second AI measure**: private data-center jobs per 1,000 workers from the Bureau of Labor Statistics (BLS), a single consistent series, alongside Fang's postings.

We also test Zhang et al. (2026), "Blessing or Peril?", on the same state panel. A plain-English walkthrough of the whole project, with every number traced to a result file, is in [`outputs/ECON499R_Explained_2026-11-09.pdf`](outputs/ECON499R_Explained_2026-11-09.pdf).

## Main findings

**Fang's positive association depends on the data version and on leaving out year effects.**

| Specification (Fang's Table 2, column 6, unless noted) | AI coefficient | p-value |
|---|---:|---:|
| Fang et al. (2025), published | 0.0531 | < 0.01 |
| Our replication, SEDS as published in June 2023 (Fang's version) | 0.0348 | 0.057 |
| Our replication, current SEDS (after EIA's October 2023 change) | −0.0188 | 0.317 |
| June 2023 SEDS, adding a linear year trend | −0.0419 | 0.121 |
| Our design, AI postings (year effects, lag, clustered SEs, 2019–2024) | −0.0479 | 0.109 |
| Our design, data-center jobs (2015–2024) | −0.0567 | 0.208 |

1. **Fang's data match ours on the version Fang used.** Our AI postings, energy price, population and education series reproduce Fang's Table A1 to within 0.01 standard deviations. Renewable consumption matches only on the June 2023 SEDS release.
2. **EIA's accounting change explains most of the gap.** It accounts for 61% of the difference between current and June 2023 SEDS in column 6; EIA's later data revisions account for the rest.
3. **The association isn't specific to AI.** In Fang's model, pet-care employment, an industry unrelated to energy, is significantly associated with renewables (0.298, p = 0.003), while AI postings lose significance once a trend is included.
4. **It doesn't survive a standard design.** With year effects, a lag, clustering and a longer sample, neither AI measure is significant.
5. **Fang's moderation, subgroup and robustness results depend on the same choices.** The EPU (Economic Policy Uncertainty index) interaction is positive in Fang's model (p = 0.002) but not under two-way fixed effects (p = 0.163). Half of Fang's eight subgroup claims (Supplement Table A3) reproduce on June 2023 SEDS (low consumption, high income, low R&D, Midwest); the electricity-price, net-importer, extreme-weather and West claims don't. Fang's Supplement B1 (columns 1–2) and B2 coefficients fall inside our confidence intervals on June 2023 SEDS and outside them on current SEDS.

**The Zhang test.** Data-center jobs aren't associated with electricity use or efficiency. A negative association with the renewable share fails a timing test: next year's AI predicts this year's share. Mediation and spatial-spillover hypotheses aren't supported.

Full results: [`results/2026-11-07/paper/findings.md`](results/2026-11-07/paper/findings.md).

## Methods: the Fang test

All Fang-test models use 50 states plus the District of Columbia, 2018–2021 (N = 204), unless noted.

**1. Replication.** Fang's specification regresses log renewable energy consumption on log AI job postings, log state EPU and controls (energy price, GDP, population, education), with **state fixed effects only** and conventional standard errors.

**2. Four versions of the outcome.** We run the replication on each version of SEDS renewable consumption:

| Version | Description |
|---|---|
| June 2023 SEDS | The archived release Fang used, before EIA's accounting change |
| Current SEDS | Today's release, which counts wind, solar, hydro and geothermal at 3,412 Btu/kWh ([EIA notice](https://www.eia.gov/state/seds/seds-change/index.php)) |
| Rebuilt | Our year-by-year rebuild of the old method on current data (`data/receipts/seds_old_basis.md`) |
| k = 2.6 | A rough rescaling, kept only as a check |

**3. Data check.** Our descriptive statistics against Fang's supplementary Table A1, variable by variable.

**4. Bridge to a standard design.** We change one element at a time: add year effects, restrict to the lag sample, lag AI one year, cluster by state, extend the sample, drop the District of Columbia.

**5. Trend and placebo tests.** We add a linear year trend, and we replace AI with employment in two industries unrelated to energy (pet care; distilleries) from BLS QCEW (Quarterly Census of Employment and Wages).

**6. Moderation, subgroups and supplement.** The AI × EPU interaction in both designs; Fang's subgroup splits (Tables 3–5 and A3) with Fang's net-producer definition and alternatives; Fang's Supplement Tables B1 and B2 (other AI and outcome measures, fossil-fuel indicators, winsorizing, added controls) on both SEDS versions.

Every deviation from Fang's design and from our Methods Memo was registered in [`EXPERIMENTS.md`](EXPERIMENTS.md) before running (sections 9 and 14). **Pending:** a rerun with GDP in chained 2012 dollars, which needs a browser download from the Bureau of Economic Analysis (BEA) archive.

## Methods: the Zhang test

Two-way fixed effects (state and year), last year's data-center jobs per 1,000 workers, four controls, standard errors clustered by state, 50 states, 2015–2025 (N = 550).

| Hypothesis | Model | Result |
|---|---|---|
| H1: AI and electricity use, efficiency, renewables | Two-way fixed effects; lead (placebo) test | No association that passes the timing test |
| H2: a channel through tech jobs or density | Mediation, Sobel tests, cluster bootstrap | No channel |
| H3: spillovers to neighboring states | Spatial Durbin model, inverse-distance and border weights | Not supported after the timing test |

Robustness checks, an instrumental-variable check, nonlinearity tests and extensions are described in [`EXPERIMENTS.md`](EXPERIMENTS.md) and the explained notebook.

## Data

| Source | Used for |
|---|---|
| Stanford AI Index (job postings by state) | Fang's AI measure |
| BLS QCEW, NAICS 518210 (data processing and hosting) | Our AI measure; placebo industries |
| EIA SEDS (current and June 2023 archive) | Renewable consumption, the Fang outcome |
| EIA electricity data (generation, capacity, sales, prices) | Zhang outcomes and controls |
| BEA (GDP, income, population) | Controls |
| Baker, Davis and Levy (state EPU) | Fang's moderator |
| Lawrence Berkeley National Laboratory, NOAA, Census Bureau, NCSES | Controls and checks |
| Georgia Public Service Commission filings | Georgia case study |

Every variable, with its source, coverage, validation rating and limitations, is in [`data/variable_registry.csv`](data/variable_registry.csv) and [`data/DATA_DICTIONARY.md`](data/DATA_DICTIONARY.md). Provenance by source is in [`data/receipts/`](data/receipts/).

## Repository layout

```
code/R/            Model drivers (one per analysis; each takes --date)
code/python/       Data checks, tables, reports, the explained notebook builder
econ499r_starter/  Download and panel-build scripts
data/              Registry, dictionary, receipts, manifest (raw data come separately)
results/<date>/    Model output, append-only; every row has a method tag and status
outputs/           Reports, master workbooks, the explained notebook (HTML, PDF)
notebooks/         One notebook per phase, plus ECON499R_explained.ipynb
docs/<date>/       Handoffs and methods notes
EXPERIMENTS.md     Pre-registered specifications and every deviation
```

## Getting started

The repository holds code, documentation and results. The data the code needs come separately as a zip.

**1. Clone.** The repository is private; ask Shunji (GitHub `SHLEW06`) for access.

```bash
git clone https://github.com/SHLEW06/econ499r-ai-renewables.git
cd econ499r-ai-renewables
```

**2. Add the data.** Download `data_bundle_2026-11-09.zip` (about 460 MB) from the team's Google Drive folder and unzip it in the repository root.

```bash
unzip ~/Downloads/data_bundle_2026-11-09.zip -d .
```

**3. Check the data.** The script compares every file with [`data/MANIFEST.csv`](data/MANIFEST.csv) (path, size, SHA-256) and should end with `RESULT: PASS`.

```bash
python3 -I code/python/verify_data.py
```

**4. Census key (optional).** Needed only to re-download the American Community Survey broadband table. Copy `.env.example` to `.env` and add your own free key from https://api.census.gov/data/key_signup.html. Never commit `.env`.

**5. Install packages.** Python 3.13 and R 4.6.2.

```bash
python3 -m pip install -r requirements.txt
Rscript code/R/packages.R          # add "exact" to install the pinned versions
```

Files left out of the bundle (journal articles, licensed data, private material) and how to obtain each are listed in [`docs/DATA_ACCESS.md`](docs/DATA_ACCESS.md).

## Reproducing the results

Each driver takes `--date` and writes to `results/<date>/`, appending to files already there. **Use a new date**, not one already in `results/`.

**Fang test**

```bash
D=$(date +%F)
Rscript code/R/04h_fang_test.R --date $D             # replication, bridge, moderation, subgroups
Rscript code/R/04h2_fang_net_producer.R --date $D    # net-producer definitions
Rscript code/R/04h3_fang_finalize.R --date $D        # Table 2 on each SEDS version, splits, event study
Rscript code/R/09a_fang_crosscheck.R --date $D       # trend test and placebo industries (needs 04h3, same date)
Rscript code/R/09h_fang_supplement.R --date $D       # Table A1 and Supplement B1 fossil-fuel indicators
Rscript code/R/09i_fang_supplement_b.R --date $D     # Supplement B1 columns 1-2 and B2
```

**Zhang test**

```bash
python3 -I econ499r_starter/scripts/build_panel.py data/raw data/out   # rebuild the panel (about 30 s)
Rscript code/R/04b_step1_twfe.R --date $D            # H1
Rscript code/R/04c_step2_mediation.R --date $D       # H2
Rscript code/R/04d_step3_spatial.R --date $D         # H3
```

**Explained notebook and reports**

```bash
python3 code/python/build_explained_notebook.py $D   # notebook, HTML, PDF and number check
```

The full run order, including side tables and the master workbook, is in [`data/receipts/README.md`](data/receipts/README.md). The data bundle is rebuilt with `python3 -I code/python/build_data_bundle.py <date>`.

## Documentation

| Document | Contents |
|---|---|
| [`outputs/ECON499R_Explained_2026-11-09.pdf`](outputs/ECON499R_Explained_2026-11-09.pdf) | Plain-English walkthrough of every model and result |
| [`results/2026-11-07/paper/findings.md`](results/2026-11-07/paper/findings.md) | Findings with every number logged in `number_check.csv` |
| [`EXPERIMENTS.md`](EXPERIMENTS.md) | Pre-registered specifications and deviations |
| [`data/DATA_VALIDATION.md`](data/DATA_VALIDATION.md) | Data validation ratings |
| [`docs/DATA_ACCESS.md`](docs/DATA_ACCESS.md) | Files not in the data bundle and how to obtain them |
| [`CLAUDE.md`](CLAUDE.md) | Project conventions |

**References.** Fang, Y., Lee, C.-C., and Li, X. (2025). Assessing the impact of artificial intelligence on the transition to renewable energy? Analysis of U.S. states under policy uncertainty. *Renewable Energy* 246, 122969. https://doi.org/10.1016/j.renene.2025.122969 · Zhang, S., Ji, R., Dou, W., and Hao, Y. (2026). Blessing or peril? The impact of artificial intelligence on the energy transition: evidence from China. *Applied Economics* 58(32), 6495–6513. https://doi.org/10.1080/00036846.2025.2521038

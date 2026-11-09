# AI and renewable energy across U.S. states, 2015-2025

ECON 499R, Emory University, Fall 2026. Shunji Lewandowski and Alexander Hendricks; advisor Prof. Fohlin. We test Zhang et al. (2026), "Blessing or Peril?", on 50 U.S. states, 2015-2025. All results are associations.

Project conventions: [`CLAUDE.md`](CLAUDE.md). Registered deviations from the Methods Memo: [`EXPERIMENTS.md`](EXPERIMENTS.md). Data provenance: [`data/receipts/README.md`](data/receipts/README.md).

## Getting started (collaborators)

The repo holds code, documentation and results. The data it needs (`data/raw/`, `data/out/` and the side tables in `data/`) are gitignored and come separately, as a zip.

### 1. Clone

```bash
git clone https://github.com/SHLEW06/econ499r-ai-renewables.git
cd econ499r-ai-renewables
```

The repo is private: ask Shunji (GitHub `SHLEW06`) for access. Run every command below from the repo root.

### 2. Add the data

Download `data_bundle_<date>.zip` from the team's Google Drive folder (ask Shunji for the link). Unzip it **in the repo root**: its paths start with `data/`, so the files land in `data/raw/`, `data/out/` and `data/`.

```bash
unzip ~/Downloads/data_bundle_2026-11-09.zip -d .
```

The bundle is about 460 MB zipped and 1 GB unzipped. It holds the raw files the scripts read, not every file we downloaded: see [Downloaded but unused](#downloaded-but-unused).

### 3. Check the data

```bash
python3 -I code/python/verify_data.py
```

It checks every file against [`data/MANIFEST.csv`](data/MANIFEST.csv) (path, size, SHA-256) and lists any file that's missing or doesn't match. It should end with `RESULT: PASS`. A `HASH` line under `data/raw/` means a damaged or different download; get the bundle again.

### 4. Census key

Copy `.env.example` to `.env` and paste in your own free key from https://api.census.gov/data/key_signup.html:

```bash
cp .env.example .env     # then edit: CENSUS_KEY=your_key
```

`.env` is gitignored: never commit it, and don't share your key. You need it only to download the ACS broadband table again (`download_acs_broadband.py`); the bundle already has that table, so the panel and models run without it.

### 5. Install packages

Python 3.13 and R 4.6.2 (the versions behind the results):

```bash
python3 -m pip install -r requirements.txt
Rscript code/R/packages.R          # installs missing R packages, then compares versions with the pins
Rscript code/R/packages.R exact    # optional: installs the exact pinned versions
```

### 6. Rebuild the panel and run the main results

```bash
# Panel, W matrices and centroids from data/raw/ into data/out/ (about 30 seconds)
python3 -I econ499r_starter/scripts/build_panel.py data/raw data/out
python3 -I code/python/verify_data.py        # the rebuilt data/out/ should still pass
```

The main results are three R drivers, one per hypothesis. Each takes `--date` and writes to `results/<date>/`, appending to files already there. **Use today's date, not a date already in `results/`,** so your run doesn't add rows to the committed results.

```bash
D=$(date +%F)
Rscript code/R/04b_step1_twfe.R --date $D        # H1 core spec: two-way FE, ctrl4 -> results/$D/h1/h1_core.csv
Rscript code/R/04b_step1_twfe_ctrl4.R --date $D  # H1 extras with ctrl4, incl. new_renew_mw (run after the line above)
Rscript code/R/04c_step2_mediation.R --date $D   # H2 mediation
Rscript code/R/04d_step3_spatial.R --date $D     # H3 spatial; main spec SDM: code/R/04d2_sdm_mainspec.R
```

Compare yours with the committed run, e.g. `results/2026-11-02/h1/h1_core.csv`: the `ctrl4` rows are the baseline. Robustness, the Fang test and the Nov 7 extensions follow the same pattern; the full run order, side tables and workbook steps are in [`data/receipts/README.md`](data/receipts/README.md) and [`data/receipts/master_workbook.md`](data/receipts/master_workbook.md). Some drivers read earlier dated folders, so check the paths at the top of a driver before changing dates.

### Files that aren't in the bundle, and how to get them

| File | Why it's left out | How to get it |
|---|---|---|
| `.env` | Holds a personal API key | Make your own, step 4 |
| `literature/AI_Impact_China.pdf` | Journal article | Zhang, Ji, Dou and Hao (2026), *Applied Economics* 58(32), https://doi.org/10.1080/00036846.2025.2521038, via Emory Libraries |
| `literature/Assessing_AI_Impact_on_Renewable_Energy_Transition.pdf` | Journal article | Fang, Lee and Li (2025), *Renewable Energy* 246, 122969, https://doi.org/10.1016/j.renene.2025.122969, via Emory Libraries |
| `literature/Fang_Lee_Li_2025_supplement.docx` | Publisher supplement | Same DOI, "Supplementary data" (Appendix A), via Emory Libraries; see [`data/receipts/fang_supplement.md`](data/receipts/fang_supplement.md) |
| `literature/Can_AI_Grow_Green.pdf` | Journal article | Melguizo, Katz and Jung (2026), *Energy Policy* 208, 114883, https://doi.org/10.1016/j.enpol.2025.114883, via Emory Libraries |
| `literature/Can_AI_Help_Accelerate_Transition_to_RE.pdf` | Journal article | Zhao, Wang, Stan and Mirza (2024), *Energy Economics* 134, 107584, https://doi.org/10.1016/j.eneco.2024.107584, via Emory Libraries |
| `literature/Transferable_Energy_Storage_Bidder.pdf` | Journal article | Baker, Zheng and Xu (2024), *IEEE Trans. Power Systems* 39(2), https://doi.org/10.1109/TPWRS.2023.3280841, via Emory Libraries (IEEE Xplore) |
| `literature/Wind_Power_Forecasting_Grid_Integration.pdf` | Journal article | Mahoney et al. (2012), *IEEE Trans. Sustainable Energy* 3(4), https://doi.org/10.1109/TSTE.2012.2201758, via Emory Libraries (IEEE Xplore) |
| `literature/Deep_Learning_Materials_Discovery.pdf` | Journal article | Merchant et al. (2023), *Nature*, https://doi.org/10.1038/s41586-023-06735-9 (open access) |
| `literature/Cost_Benefit_Wind_Farm_Monitoring_Strategy.pdf` | Journal article | Turnbull and Carroll (2021), *Energies* 14, 4922, https://doi.org/10.3390/en14164922 (open access) |
| `literature/Levelized_Costs_Learning_Analysis_Wind_Solar.pdf` | Journal article | Bolinger, Wiser and O'Shaughnessy (2022), *iScience* 25, 104378, https://doi.org/10.1016/j.isci.2022.104378 (open access) |
| `literature/Offshore_Wind_Forecasting_Value_NY_Grid.pdf` | Journal article | Bin Walid et al. (2026), *IEEE Access*, https://doi.org/10.1109/ACCESS.2026.3737067 (open access) |
| `literature/Lazard_LCOE_Plus.pdf` | Industry report kept with the literature | Free from Lazard: https://www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf (same file as `data/raw/costs/Lazard_LCOEplus_2026.pdf`, listed under Downloaded but unused) |
| `notes/Methods_Memo_*.pdf` | Course document | Ask the team |
| `notes/Grijalva_interview_transcript_*.txt` | Interview material, private | Not distributed; no script reads it |
| Bloomberg data (`data/raw/bloomberg/`) | Emory-licensed | No script reads it. If needed, Bloomberg terminals through Emory Libraries; don't share exports |
| SEC cache (`data/raw/sec/cache/`) | Built with a personal contact string | Optional. Set `SEC_USER_AGENT` to your own "Name email" and run `econ499r_starter/scripts/sec_fin.py`; the bundle already has its output, `data/out/sec_company_financials.csv` |
| `_to_delete/` folders | Duplicates and mistaken downloads | Not needed |
| `data/bea/`, `data/bls/`, `data/census/`, `data/eia/`, `data/ferc/`, `data/data_download_all_pt1.zip` | Phase 1 copies of `data/raw/` | Not needed; no script reads them |
| `outputs/`, `release/` | Built by script | `code/python/build_master_workbook.py` and companions, see [`data/receipts/master_workbook.md`](data/receipts/master_workbook.md) |

The full list of what was left out is in `logs/<date>/data_bundle_exclusions.csv`.

### Downloaded but unused

We downloaded these raw files, but no script reads them, so they aren't in the bundle (1,631 files, 1.13 GB). They stay on the team's disk, and every file is listed with its size and source in [`data/raw_unused.csv`](data/raw_unused.csv). You need none of them to rebuild the panel or run the models. Some were read by hand, as the note says; get those from the source if you want to check that step. How the list was made: [`docs/2026-11-09/data-bundle-unused-raw.md`](docs/2026-11-09/data-bundle-unused-raw.md).

| Files | Count | MB | Source | Note |
|---|---:|---:|---|---|
| `uspto_aipd/ai_model_predictions_2023.csv.zip` | 1 | 818.0 | https://data.uspto.gov/ui/datasets/products/files/ECOPATAI/2023_r1/ai_model_predictions.csv.zip | AI Patent Dataset 2023; downloaded for the AI index add-on, not used |
| `uspto_aipd/oce-aipd-2023.pdf` | 1 | 1.9 | https://www.uspto.gov/sites/default/files/documents/oce-aipd-2023.pdf | Its documentation |
| `georgia/irp_2025_public_disclosure.zip` | 1 | 103.7 | https://psc.ga.gov/search/facts-docket/?docketId=56002 | 2025 IRP technical appendices; browser download; reference only |
| `georgia/2023_IRP_Update_Main_Document.pdf` | 1 | 1.3 | https://georgiapower.com/content/dam/georgia-power/pdfs/company-pdfs/2023-irp-update-main-document.pdf | Read by hand for the Georgia box |
| `georgia/2025_IRP_TOC.pdf` | 1 | 0.2 | https://www.selc.org/wp-content/uploads/2025/02/2025-IRP-TOC.pdf | Reference |
| `bea/SAGDP.zip`, `bea/SAINC.zip` | 2 | 28.0 | https://apps.bea.gov/regional/zip/SAGDP.zip, https://apps.bea.gov/regional/zip/SAINC.zip | The zips as downloaded; the three extracted files the scripts read (SAGDP2, SAGDP9, SAINC1, all areas) are in the bundle |
| `bea/sagdp/*` other than SAGDP2 and SAGDP9 all-areas | 568 | 27.1 | https://apps.bea.gov/regional/zip/SAGDP.zip | Per-state files, other tables, footnotes, definitions |
| `bea/sainc/*` other than SAINC1 all-areas | 1,016 | 44.1 | https://apps.bea.gov/regional/zip/SAINC.zip | Same |
| `eia_forms/eia8602017.zip` | 1 | 16.2 | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602017.zip | Read by hand once, to identify the NE and NM 2017 blank-fuel rows |
| `eia_forms/eia8602025.zip` | 1 | 23.6 | https://www.eia.gov/electricity/data/eia860/xls/eia8602025.zip | Reference |
| `eia_forms/f923_2025.zip` | 1 | 23.3 | https://www.eia.gov/electricity/data/eia923/xls/f923_2025.zip | Reference |
| `eia_forms/september_generator2026.xlsx` | 1 | 14.0 | https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx | Reference |
| `bls/placebo/qcew_{2018,2021}_<naics>.csv`, 10 NAICS not chosen | 20 | 7.8 | `https://data.bls.gov/cew/data/api/<year>/a/industry/<naics>.csv` | Read by hand to pick the two placebo industries ([`qcew_placebo.md`](data/receipts/qcew_placebo.md)); the two chosen, 312140 and 812910, are in the bundle |
| `crs/PLAW-116publ260.pdf` | 1 | 5.6 | https://www.govinfo.gov/content/pkg/PLAW-116publ260/pdf/PLAW-116publ260.pdf | Read by hand for the tax-credit coding |
| `crs/PLAW-117publ169.pdf` | 1 | 0.9 | https://www.govinfo.gov/content/pkg/PLAW-117publ169/pdf/PLAW-117publ169.pdf | Same |
| `crs/CRS_R43453_2020-04-29.pdf` | 1 | 1.3 | https://crsreports.congress.gov/product/pdf/R/R43453 | Same ([`crs_reports.md`](data/receipts/crs_reports.md)) |
| `crs/CRS_R46865_2024-02-26.pdf` | 1 | 0.9 | https://crsreports.congress.gov/product/pdf/R/R46865 | Same |
| `crs/CRS_IF10479_2021-04-23.pdf` | 1 | 0.5 | https://crsreports.congress.gov/product/pdf/IF/IF10479 | Same |
| `costs/Lazard_LCOEplus_2026.pdf` | 1 | 1.2 | https://www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf | Read by hand for the Georgia box |
| `census_btos/State.xlsx` | 1 | 4.7 | https://www.census.gov/hfp/btos/downloads/State.xlsx | Not used: its AI question changed wording and 2024 is blank |
| `census_btos/AI_Question_Wording_Updates.pdf` | 1 | 0.5 | https://www.census.gov/hfp/btos/downloads/AI%20Question%20Wording%20Updates.pdf | Reference |
| `census/gaz_counties.zip` | 1 | 0.1 | https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip | The zip as downloaded; the extracted `.txt` is in the bundle |
| `eia/mer/mer_A_FULL.pdf` | 1 | 1.1 | https://www.eia.gov/totalenergy/data/monthly/pdf/mer_A_FULL.pdf | Reference |
| `eia/seds/seds_change_notice.html` | 1 | 0.05 | https://www.eia.gov/state/seds/seds-change/index.php | Saved copy of the notice cited in the text |
| `eia/seds_archive/archive_index.html` | 1 | 0.1 | https://www.eia.gov/state/seds/archive/ | Saved copy of the archive page |
| `aiindex/ed2026_fig_4.2.14.csv` | 1 | 0.01 | https://drive.google.com/uc?export=download&id=1HLzDyJ61GL50xmjsF2Bq-fyNI5inDJig | AI Index 2026 figure data |
| `aiindex/ed2026_fig_4.2.16.csv` | 1 | 0.01 | https://drive.google.com/uc?export=download&id=1ZswTrGZ3t5ImPaxdo4kGcCyRZnTuo4m3 | Same |
| `nsf/nsf27300-tab010.xlsx` | 1 | 0.02 | No URL recorded (supplied by the team) | Wrong table, rated red ([`nsf.md`](data/receipts/nsf.md)) |
| `owid/solar-pv-cumulative-capacity.metadata.json` | 1 | 0.001 | https://ourworldindata.org/grapher/solar-pv-cumulative-capacity | Series metadata |

Paths are under `data/raw/`. A few files that no script opens are in the bundle anyway: the saved Census and NOAA API responses that `acs_broadband.csv` and `noaa_degree_days.csv` were built from (the download scripts write them; rebuilding needs a key or network), NOAA's readme for its climate-division files, and the Epoch and OWID license notes.

Two effects of leaving these out: `verify_data.py` doesn't count them as extra if you have them, and `build_raw_file_shapes.py`, which describes every inventoried raw file for the workbook's Raw Files tab, marks a missing one as "unreadable" instead of giving its shape. Nothing else in the workbook or results changes.

### Rebuilding the bundle (maintainers)

```bash
python3 -I code/python/build_data_bundle.py <YYYY-MM-DD>
```

This writes `release/data_bundle_<date>.zip`, rewrites `data/MANIFEST.csv`, and writes the exclusion list and a check of every hash against the receipts to `logs/<date>/`. It stops if a file disagrees with its receipt or contains the Census key. Commit the new manifest, then upload the zip to Drive.

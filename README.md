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
unzip ~/Downloads/data_bundle_2026-11-07.zip -d .
```

The bundle is about 1.5 GB zipped and 2.1 GB unzipped.

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
| `literature/Lazard_LCOE_Plus.pdf` | Kept with the literature | The same file is in the bundle as `data/raw/costs/Lazard_LCOEplus_2026.pdf` (free from Lazard: https://www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf) |
| `notes/Methods_Memo_*.pdf` | Course document | Ask the team |
| `notes/Grijalva_interview_transcript_*.txt` | Interview material, private | Not distributed; no script reads it |
| Bloomberg data (`data/raw/bloomberg/`) | Emory-licensed | No script reads it. If needed, Bloomberg terminals through Emory Libraries; don't share exports |
| SEC cache (`data/raw/sec/cache/`) | Built with a personal contact string | Optional. Set `SEC_USER_AGENT` to your own "Name email" and run `econ499r_starter/scripts/sec_fin.py`; the bundle already has its output, `data/out/sec_company_financials.csv` |
| `_to_delete/` folders | Duplicates and mistaken downloads | Not needed |
| `data/bea/`, `data/bls/`, `data/census/`, `data/eia/`, `data/ferc/`, `data/data_download_all_pt1.zip` | Phase 1 copies of `data/raw/` | Not needed; no script reads them |
| `outputs/`, `release/` | Built by script | `code/python/build_master_workbook.py` and companions, see [`data/receipts/master_workbook.md`](data/receipts/master_workbook.md) |

The full list of what was left out, file by file, is in `logs/<date>/data_bundle_exclusions.csv`.

### Rebuilding the bundle (maintainers)

```bash
python3 -I code/python/build_data_bundle.py <YYYY-MM-DD>
```

This writes `release/data_bundle_<date>.zip`, rewrites `data/MANIFEST.csv`, and writes the exclusion list and a check of every hash against the receipts to `logs/<date>/`. It stops if a file disagrees with its receipt or contains the Census key. Commit the new manifest, then upload the zip to Drive.

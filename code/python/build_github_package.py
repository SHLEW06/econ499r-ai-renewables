#!/usr/bin/env python3
"""Build the clean GitHub copy in release/github/econ499r-ai-renewables/ from an allowlist, scan it, and make one commit. No remote, no push.
Usage: python3 code/python/build_github_package.py --date YYYY-MM-DD"""
import argparse, glob, json, os, re, shutil, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); D = ap.parse_args().date
ROOT = os.getcwd(); OUT = "release/github/econ499r-ai-renewables"; REL = "release/github"
if os.path.exists(OUT): shutil.rmtree(OUT)  # built output only; rebuilt from the allowlist below
os.makedirs(OUT)
def copy(src):
    dst = os.path.join(OUT, src); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst); return dst
ALLOW = []
for pat in ["code/R/*.R", "code/python/*.py", "econ499r_starter/scripts/*.py", "econ499r_starter/R/*.R", "econ499r_starter/download_all.py", "econ499r_starter/README.md", "econ499r_starter/data_links.md", "econ499r_starter/reference/expected_values.md", "econ499r_starter/reference/prelim_*.csv", "notebooks/*.ipynb", "docs/*/*.md", "docs/*/*.tex", "data/receipts/*.md", "data/DATA_DICTIONARY.md", "data/variable_registry.csv", "data/DATA_VALIDATION.md", "data/INDEPENDENT_AUDIT_2026-11-04.md", "data/DATA_INDEX.md", "data/DATA_AUDIT.md", "data/data_links.md", "data/FILE_INVENTORY.csv", "EXPERIMENTS.md"]:
    ALLOW += sorted(glob.glob(pat))
for r, _, fs in os.walk("results"):
    ALLOW += [os.path.join(r, f) for f in fs if os.path.splitext(f)[1].lower() in (".csv", ".tex", ".png", ".md", ".txt") and f != ".DS_Store"]
CLEAN_IN = {"data/out/state_panel_2015_2025.csv": "EIA, BLS, BEA, Census", "data/out/W_border_binary.csv": "Census", "data/out/W_inverse_distance_rowstd.csv": "Census", "data/out/W_distance_miles.csv": "Census", "data/out/state_centroids_land.csv": "Census", "data/ai_allown_518210.csv": "BLS", "data/seds_renewables_state.csv": "EIA", "data/ncses_bachelors_state.csv": "NCSES (NSF)", "data/nsf_state_rd.csv": "NCSES (NSF)", "data/acs_broadband.csv": "Census", "data/fang_split_vars.csv": "EIA, NSF, BEA, Census", "data/fang_net_producer_definitions.csv": "EIA", "data/noaa_degree_days.csv": "NOAA NCEI", "data/epu_state_annual.csv": "Baker, Davis and Levy, CC BY 4.0", "data/epoch_ai_campuses_by_state.csv": "Epoch AI, CC BY", "data/out/ferc1_utility_financials.csv": "PUDL, CC BY 4.0", "data/out/ferc1_cost_by_technology.csv": "PUDL, CC BY 4.0", "data/out/ferc1_plant_costs.csv": "PUDL, CC BY 4.0"}
ALLOW += list(CLEAN_IN)
ALLOW = [f for f in ALLOW if os.path.basename(f) not in ("build_github_package.py", "build_results_package.py")]
_tracked = set(subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n"))
_untracked = [f for f in ALLOW if f.startswith("docs/") and f not in _tracked]; ALLOW = [f for f in ALLOW if f not in _untracked]  # uncommitted local docs stay out
print("left out (docs not tracked in git):", _untracked)  # hold the scan patterns; stay in the working repo
for f in ALLOW: copy(f)
# ---- remove local paths from the copies ----
SCR = re.compile(r"/private/tmp/[^\s\"'`|)]*"); TEXT = (".md", ".py", ".R", ".csv", ".tex", ".ipynb", ".txt")
n = 0
for r, _, fs in os.walk(OUT):
    for f in fs:
        p = os.path.join(r, f)
        if not f.endswith(TEXT): continue
        t = open(p, errors="surrogateescape").read(); u = t.replace(ROOT + "/", "").replace(ROOT, "."); u = SCR.sub("<scratch_dir>", u); u = re.sub(r"/opt/homebrew/bin/", "", u); u = re.sub(r"/opt/anaconda3/[^\s\"'`|)]*", "<python_env>", u); u = re.sub(r"(?<![\w.])/tmp/", "<tmp>/", u); u = re.sub(r"/Users/[A-Za-z0-9_.-]+/[^\s\"'`|)]*", "<local_path>", u)
        if u != t: open(p, "w", errors="surrogateescape").write(u); n += 1
print("files with local paths removed:", n)
# ---- docs ----
S = open(f"docs/{D}/project-summary.md").read(); res = S[S.index("## The results"):S.index("## What we can rule out")]; rule = S[S.index("## What we can rule out"):S.index("## What it means")]; mean = S[S.index("## What it means"):S.index("## Status and next")]
readme = f"""# AI and renewable energy across U.S. states, 2015-2025

ECON 499R, Emory University, Fall 2026. **Authors:** Shunji Lewandowski and Alexander Hendricks. **Advisor:** Prof. Fohlin.

All results are associations. Nothing here shows that AI causes a change.

## The question

Is growth in AI-related activity associated with more or less electricity use, energy efficiency and renewable energy across U.S. states? We test Zhang et al. (2026), "Blessing or Peril?", and Fang, Lee and Li (2025) on the same state panel, and add a Georgia case box.

## Data

50 states and DC, 2015-2025. Sources: EIA, BLS QCEW, BEA, Census, Stanford AI Index, NCSES, LBNL, the state EPU index, NOAA, Epoch AI, and FERC Form 1 through PUDL. Every variable, with its source, script line, coverage, rating and limitations, is in [`data/DATA_DICTIONARY.md`](data/DATA_DICTIONARY.md). Checks are in [`data/DATA_VALIDATION.md`](data/DATA_VALIDATION.md). Provenance by source is in [`data/receipts/`](data/receipts/).

**Raw data aren't here.** This repo holds cleaned tables only where every source allows redistribution: see [`DATA_LICENSES.md`](DATA_LICENSES.md). The rest rebuild from the download scripts.

## Methods

- **Zhang test:** two-way fixed effects (state and year), last year's private data-center jobs per 1,000 workers, four controls, SEs clustered by state, N = 550. Driscoll-Kraay is a sensitivity check only. Then mediation with Sobel tests and a cluster bootstrap, and spatial Durbin models with inverse-distance and border weights.
- **Timing test:** next year's AI in place of last year's, and both in one model. This changes the reading of H1 and H3.
- **Fang test:** replication of Fang's Table 2, then a bridge to our design, one change at a time, using postings and data-center jobs side by side.
- **Stretch:** shift-share IV; broadband and R&D moderation. The Hansen threshold wasn't run.
- **Georgia:** learning-curve arithmetic for solar on cited IEA paths. Not a forecast of ours.

Details and every deviation from the plan: [`docs/{D}/methods_section.tex`](docs/{D}/methods_section.tex), [`docs/{D}/memo-to-paper.md`](docs/{D}/memo-to-paper.md), [`EXPERIMENTS.md`](EXPERIMENTS.md).

{res}{rule}{mean}Full summary with every number traced to a result tag: [`docs/{D}/project-summary.md`](docs/{D}/project-summary.md). Findings: [`results/{D}/paper/findings.md`](results/{D}/paper/findings.md). Tables and figures: [`results/{D}/paper/`](results/{D}/paper/).

## How to reproduce

Needs Python 3.13 (pandas 3.0, numpy 2.3, openpyxl 3.1, pyarrow 21, matplotlib 3.11, nbconvert 7.16), and R 4.6 (fixest, modelsummary, spdep, splm, SDPDmod, spatialreg, boot, data.table, ggplot2, sf, IRkernel). LibreOffice recalculates a copy of the workbook; it never saves the final file.

```bash
# 1. Download. Scripted files land in data/raw/
mkdir -p data && cd data && python3 ../econ499r_starter/download_all.py --with-eia-forms && cd ..
S=econ499r_starter/scripts
python3 $S/download_nsf_tab10.py data/raw/nsf
python3 $S/download_fang_sources.py data/raw logs/YYYY-MM-DD/fang_downloads.csv
# Census key: put CENSUS_KEY=... in a local .env (never commit it). Then:
python3 $S/download_acs_broadband.py .env data/raw/acs data/acs_broadband.csv logs/YYYY-MM-DD/acs_spot_check.csv
```

Some files need a browser: LBNL, Epoch, OWID, EPU, RMI, and Georgia PSC filings. Links and exact file names are in [`data/data_links.md`](data/data_links.md) and [`data/receipts/README.md`](data/receipts/README.md). SEC data needs `SEC_USER_AGENT` set to your own contact string.

```bash
# 2. Build the panel and side tables: full list in data/receipts/README.md
python3 $S/build_panel.py data/raw data/out

# 3. Models. Each driver takes --date; results go to results/<date>/, append-only
Rscript code/R/04b_step1_twfe.R --date YYYY-MM-DD
Rscript code/R/04c_step2_mediation.R --date YYYY-MM-DD
Rscript code/R/04d_step3_spatial.R --date YYYY-MM-DD
Rscript code/R/04e_robustness.R --date YYYY-MM-DD
Rscript code/R/04e2_spillover_placebo.R --date YYYY-MM-DD
Rscript code/R/04e3_stretch.R --date YYYY-MM-DD
Rscript code/R/04e4_weather_check.R --date YYYY-MM-DD
Rscript code/R/04h_fang_test.R --date YYYY-MM-DD
Rscript code/R/04h2_fang_net_producer.R --date YYYY-MM-DD
python3 code/python/04f_georgia_solar.py --date YYYY-MM-DD

# 3b. Prompts 08-09 (Nov 7): side tables, then models (see data/receipts/README.md for downloads)
python3 $S/build_finalize_tables.py data/raw data logs/YYYY-MM-DD
python3 $S/build_extend_tables.py data/raw data logs/YYYY-MM-DD
python3 $S/build_drivers_tables.py data/raw data logs/YYYY-MM-DD
python3 $S/build_ai_index.py data/raw data logs/YYYY-MM-DD
Rscript code/R/04h3_fang_finalize.R --date YYYY-MM-DD
Rscript code/R/09a_fang_crosscheck.R --date YYYY-MM-DD
Rscript code/R/09b_by_type.R --date YYYY-MM-DD
Rscript code/R/09c_ai_impact.R --date YYYY-MM-DD
Rscript code/R/09d_national_drivers.R --date YYYY-MM-DD
Rscript code/R/09e_pass2_checks.R --date YYYY-MM-DD
Rscript code/R/09f_index_addon.R --date YYYY-MM-DD
Rscript code/R/09g_land_sensitivity.R --date YYYY-MM-DD
python3 code/python/04h3_fang_finalize_tables.py --date YYYY-MM-DD
for n in 1 2 3 4 25 5; do python3 code/python/09_extend_tables.py --date YYYY-MM-DD --section $n; done
python3 code/python/04g_results_pack.py --date YYYY-MM-DD

# 4. Master workbook: steps in data/receipts/master_workbook.md
```

Some scripts read results from earlier dated folders, so check the paths at the top of a driver when you change dates. Notebooks (`notebooks/`) walk through each phase in plain English, and they read the saved results.

## What's not here

Raw data, licensed data, interview material, journal PDFs, the Lazard PDF and keys. See [`DATA_LICENSES.md`](DATA_LICENSES.md).
"""
open(f"{OUT}/README.md", "w").write(readme)
open(f"{OUT}/.gitignore", "w").write(".env\n*.env\ndata/raw/\narchive/\nliterature/\noutputs/\nrelease/\nlogs/\n_to_delete/\n*.pdf\n*.zip\n*.xlsx\n.DS_Store\n__pycache__/\n*.pyc\n.ipynb_checkpoints/\n*.part\n")
rows = [("EIA: state electricity data, SEDS", "`state_panel_2015_2025.csv`, `seds_renewables_state.csv`, `fang_split_vars.csv`, `fang_net_producer_definitions.csv`", "In", "Public domain. EIA: \"U.S. government publications are in the public domain\" (https://www.eia.gov/about/copyrights_reuse.php, read Nov 4, 2026). Cite EIA"),
 ("BLS QCEW", "`state_panel_2015_2025.csv`, `ai_allown_518210.csv`", "In", "U.S. government work, public domain (17 U.S.C. 105). BLS's copyright page returned 403 to the script, so it wasn't read. Cite BLS"),
 ("BEA", "`state_panel_2015_2025.csv`, `fang_split_vars.csv`", "In", "U.S. government work, public domain (17 U.S.C. 105). Cite BEA"),
 ("Census: Gazetteer, adjacency, ACS", "panel, `W_*`, centroids, `acs_broadband.csv`", "In", "U.S. government work, public domain (17 U.S.C. 105). Cite Census"),
 ("NOAA NCEI", "`noaa_degree_days.csv`", "In", "U.S. government work, public domain (17 U.S.C. 105). Cite NOAA NCEI"),
 ("NCSES, NSF", "`nsf_state_rd.csv`, `ncses_bachelors_state.csv`", "In", "U.S. government work, public domain (17 U.S.C. 105). Cite NCSES"),
 ("PUDL (FERC Form 1)", "`ferc1_*.csv`", "In", "CC BY 4.0, per the PUDL README (read Nov 4, 2026). Cite Catalyst Cooperative"),
 ("Epoch AI", "`epoch_ai_campuses_by_state.csv`", "In", "CC BY, per Epoch's data README. Cite Epoch AI"),
 ("State EPU (Baker, Davis, Levy)", "`epu_state_annual.csv`", "In", "CC BY 4.0, per the page footer at policyuncertainty.com (read Nov 4, 2026). Cite the authors"),
 ("Stanford AI Index postings", "`ai_job_postings_state.csv`, `fang_panel.csv`", "**Out**", "Vendor data published in Stanford reports. Redistribution not cleared. Rebuild with `download_fang_sources.py`"),
 ("LBNL RPS and solar", "`lbnl_rps_targets.csv`, `lbnl_utility_solar.csv`", "**Out**", "No license found on the publication page. Rebuild from browser downloads"),
 ("IRENA via OWID", "`owid_global_solar_capacity.csv`", "**Out**", "The OWID readme says copyright IRENA 2026. Rebuild from a browser download"),
 ("SEC company facts", "`sec_company_financials.csv`", "**Out**", "No raw copy and no hash, so it can't be checked. Rebuild with `sec_fin.py`"),
 ("Georgia PSC and Georgia Power filings", "`georgia_*.csv`", "**Out**", "Regulatory filings; redistribution not checked. Rebuild with `build_georgia_tables.py` after a download"),
 ("RMI", "None", "**Out**", "License not checked; download date unknown. Not in any result"),
 ("Lazard, journal PDFs, IEA WEO", "None", "**Out**", "Copyrighted documents. Results cite figures with their pages"),
 ("Bloomberg", "None", "**Out**", "Licensed through Emory. Never included"),
 ("Interview recordings or transcripts", "None", "**Out**", "Never included")]
lic = "# Data licenses\n\nA cleaned table is here only if every source behind it allows redistribution. Anything unclear is left out: use the download scripts. This is our reading of each source's terms, as of " + D + ", not legal advice.\n\n| Source | Files | In this repo? | Terms |\n|---|---|---|---|\n" + "".join("| " + " | ".join(r) + " |\n" for r in rows) + "\nResult tables and figures contain estimates from these sources. A few Georgia results rows carry small cited figures from LBNL and IEA, with their source and page. Executed notebooks may print a few values from a source that's out, such as postings checks.\n"
open(f"{OUT}/DATA_LICENSES.md", "w").write(lic)
# ---- scan ----
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"); PATH = re.compile(r"/Users/|/private/tmp|/opt/homebrew|/opt/anaconda|C:\\\\Users"); SEC = re.compile(r"(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|CENSUS_KEY=[A-Za-z0-9]{8,}|[?&]key=[0-9a-f]{20,})"); key = None
if os.path.exists(".env"):
    for ln in open(".env"):
        if ln.startswith("CENSUS_KEY="): key = ln.split("=", 1)[1].strip().strip('"')
BAN = (".pdf", ".xlsx", ".xls", ".docx", ".zip", ".parquet", ".env", ".mp3", ".m4a", ".wav", ".mp4"); hits = dict(key=[], secret=[], email=[], path=[], banned=[], big=[], interview=[]); total = 0; nfiles = 0; rows2 = []
for r, ds, fs in os.walk(OUT):
    ds[:] = [d for d in ds if d != ".git"]
    for f in fs:
        p = os.path.join(r, f); sz = os.path.getsize(p); total += sz; nfiles += 1; rel = os.path.relpath(p, OUT)
        if f.lower().endswith(BAN) or f == ".env": hits["banned"].append(rel)
        if sz > 50e6: hits["big"].append((rel, sz))
        if p.endswith(".png"): continue
        t = open(p, errors="ignore").read()
        if p.endswith(".ipynb"): t = re.sub(r'"image/png": "[^"]*"', "", t)
        if key and key in t: hits["key"].append(rel)
        if SEC.search(t): hits["secret"].append(rel)
        m = EM.findall(t)
        if m: hits["email"].append((rel, sorted(set(m))[:3]))
        if PATH.search(t): hits["path"].append((rel, PATH.search(t).group(0)))
        if re.search(r"grijalva", t, re.I): hits["interview"].append(rel)
for k, v in hits.items(): print(k, len(v), v[:6])
if hits["key"] or hits["secret"] or hits["email"] or hits["path"] or hits["banned"] or hits["interview"]: sys.exit("scan failed; nothing committed")
for r, _, fs in os.walk(OUT):
    for f in fs:
        if f.endswith(".py"): compile(open(os.path.join(r, f)).read(), f, "exec")
# ---- one commit, no remote ----
env = ["-c", "user.name=SHLEW06", "-c", "user.email=SHLEW06@users.noreply.github.com"]
subprocess.run(["git", "init", "-q", "-b", "main"], cwd=OUT, check=True); subprocess.run(["git", "add", "-A"], cwd=OUT, check=True)
subprocess.run(["git", *env, "commit", "-q", "-m", f"ECON 499R: AI and renewable energy across U.S. states, as of {D}\n\nCode, executed notebooks, docs, receipts, data dictionary, result tables and figures, and cleaned data where sources allow.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], cwd=OUT, check=True)
remotes = subprocess.run(["git", "remote"], cwd=OUT, capture_output=True, text=True).stdout.strip(); nt = subprocess.run(["git", "ls-files"], cwd=OUT, capture_output=True, text=True).stdout.count("\n"); head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=OUT, capture_output=True, text=True).stdout.strip()
out_csv = "\n".join(f"- `{k}` ({v})" for k, v in CLEAN_IN.items())
ck = f"""# GitHub checklist

Clean copy: `release/github/econ499r-ai-renewables/`. One commit, `{head}`, on `main`, {nt} files, {total / 1e6:.1f} MB. No remote is set{'' if not remotes else ' (UNEXPECTED: ' + remotes + ')'}, and nothing has been pushed. **This isn't the working repo:** that one has copyrighted PDFs in its history and shouldn't be pushed.

## Scan results, run {D}
| Scan | Result |
|---|---|
| Census key, by value, not printed | {len(hits['key'])} files |
| Token patterns (GitHub, API, AWS, `CENSUS_KEY=`, `key=` in URLs) | {len(hits['secret'])} files |
| Email addresses in any text file | {len(hits['email'])} files |
| Absolute paths (`/Users/`, `/private/tmp`, `/opt/...`) | {len(hits['path'])} files, after {n} files were cleaned |
| PDF, Excel, Word, zip, parquet, audio, video, `.env` | {len(hits['banned'])} files |
| Interviewee's name | {len(hits['interview'])} files |
| Files over 50 MB | {len(hits['big'])} |

The commit's author email is `SHLEW06@users.noreply.github.com`, so no personal address is in the history. That's based on the git username `SHLEW06`. If your GitHub login differs, amend the commit before pushing.

## What's in
- **Code:** `code/R/`, `code/python/`, `econ499r_starter/` (`download_all.py`, scripts, starter R, `data_links.md`, check values)
- **Executed notebooks:** all 9 in `notebooks/`, local paths removed from their output
- **Docs:** `docs/`, including the methods draft, project summary, memo differences and handoffs; `EXPERIMENTS.md`
- **Data documentation:** `data/receipts/`, `data/DATA_DICTIONARY.md`, `data/variable_registry.csv`, `data/DATA_VALIDATION.md`, audit, inventory, links
- **Results:** `results/` tables, figures, findings and number checks
- **Top level:** `README.md`, `DATA_LICENSES.md`, `.gitignore`
- **Cleaned data, every source allows redistribution:**
{out_csv}

## What's out, and why
| Left out | Why |
|---|---|
| `data/raw/` | Raw data: never included. `download_all.py` and the other download scripts rebuild it |
| `fang_panel.csv`, `ai_job_postings_*.csv` | AI Index postings: redistribution not cleared |
| `lbnl_*.csv` | LBNL: no license found |
| `owid_global_solar_capacity.csv` | Copyright IRENA |
| `sec_company_financials.csv` | No raw copy to check against |
| `georgia_*.csv`, `prelim_*.csv` | Filings not cleared; prelim results superseded |
| Master workbook, results PDF | Local only; includes data that can't be redistributed |
| `literature/`, memo and Zhang PDFs, Lazard PDF | Copyrighted documents |
| `notes/`, `archive/` | Interview transcript, saved chats |
| Bloomberg | Licensed |
| `.env`, any key | Secrets |
| `prompts/`, `CLAUDE.md`, `logs/`, `_to_delete/` | Internal working files |

## Before you push
1. Decide public or private. A public repo can be cached and indexed even if deleted later.
2. Skim `DATA_LICENSES.md`: it's our reading of each source's terms, not legal advice.
3. Decide on a license for your code. None is included, so by default nobody else gets reuse rights.
4. Check with Prof. Fohlin that the course allows posting.

## Push commands
With the GitHub CLI, private by default:
```bash
cd "release/github/econ499r-ai-renewables"
git log --stat -1 | head -20
gh repo create econ499r-ai-renewables --private --source=. --remote=origin --push
```
Or create an empty repo on github.com first, then:
```bash
cd "release/github/econ499r-ai-renewables"
git remote add origin https://github.com/SHLEW06/econ499r-ai-renewables.git
git push -u origin main
```
## The repo already on GitHub
Checked 2026-11-04: `SHLEW06/econ499r-ai-renewables` is private and its `main` holds the **working repo's** history, not this clean copy. That includes the interview transcript in `notes/`, and the memo and Zhang PDFs in past commits. So `gh repo create` above will fail, and pushing this copy over `main` needs a force-push that replaces that history. That's your call; nothing here does it. The workbook's receipt links use `blob/main/data/receipts/<file>`, which exists in both histories. Anyone clicking them needs access to the repo.

To rebuild, run `python3 code/python/build_github_package.py --date {D}` from the working repo. It deletes and recreates this folder and its commit.
"""
open(f"{REL}/CHECKLIST.md", "w").write(ck); print("files", nt, "MB", round(total / 1e6, 1), "head", head, "remotes", repr(remotes))

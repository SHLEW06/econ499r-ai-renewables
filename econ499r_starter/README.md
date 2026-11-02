# ECON 499R starter: AI and renewable energy, U.S. states 2015-2025

Shunji Lewandowski and Alexander Hendricks, ECON 499R (Prof. Fohlin), Emory. Built Nov 1, 2026.

1. Unzip this folder where you keep the project, open a terminal in it, and start Claude Code.
2. Paste the prompt in CLAUDE_CODE_PROMPT.md.
3. Or run it yourself: `python download_all.py` then `python scripts/build_panel.py raw out`.
   Needs Python 3.10+ with pandas, numpy, openpyxl, pyarrow (for the PUDL files) and pyfixest (for prelim.py).

| File | What it is |
| --- | --- |
| data_links.md | Every data source with direct links (Script = download_all.py gets it; Browser = download by hand) |
| download_all.py | Fetches about 170 files into raw/ (add --with-eia-forms for EIA-860/923/861) |
| scripts/build_panel.py | Builds out/state_panel_2015_2025.csv plus the spatial weight matrices |
| scripts/ferc_fin.py | Utility and plant financials from FERC Form 1 (PUDL) |
| scripts/sec_fin.py | Company financials for 58 SEC filers (set SEC_USER_AGENT="Your Name your@email") |
| scripts/prelim.py | First-pass Step 1, SLX, Step 2b, Moran's I |
| scripts/build_xlsx.py | Rebuilds the Excel workbook for Alexander |
| R/econ499r_step1_to_3.R | R version of Steps 1 to 3 (not yet run) |
| reference/ | Methods Memo, Zhang et al. (2026), and check values |

#!/usr/bin/env python3
"""Build the master data workbook, data/variable_registry.csv and data/DATA_DICTIONARY.md.
Usage: python3 code/python/build_master_workbook.py --date YYYY-MM-DD   (run from the project root)

Reads cleaned outputs, receipts and validation files. Copies whole raw tables under the size rule, read-only. Edits no data.
Run code/python/build_cross_source_checks.py, build_raw_file_shapes.py and build_georgia_tables.py first.
Output is not yet recalculated; code/python/check_master_workbook.py recalculates it with LibreOffice and checks it."""
import argparse, csv, glob, os, re, sys
import numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.cell.cell import ERROR_CODES
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L
from openpyxl.utils.indexed_list import IndexedList
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import master_workbook_meta as M

ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--out", default=None); A = ap.parse_args()
DATE = A.date; XL = A.out or f"outputs/ECON499R_Master_Data_{DATE}.xlsx"
for f in ("data/out/state_panel_2015_2025.csv", f"logs/{DATE}/cross_source_checks.csv", f"logs/{DATE}/raw_file_shapes.csv", "data/georgia_large_load_table2.csv", "data/FILE_INVENTORY.csv"):
    if not os.path.exists(f): sys.exit(f"missing input: {f}")
F = "Arial"; HDR = Font(name=F, bold=True, color="FFFFFF", size=10); HFILL = PatternFill("solid", fgColor="1F3864")
BODY = Font(name=F, size=10); BLUE = Font(name=F, size=10, color="0000FF"); BOLD = Font(name=F, size=10, bold=True); TITLE = Font(name=F, size=14, bold=True); LINK = Font(name=F, size=10, color="0563C1", underline="single")
FILL = {"green": PatternFill("solid", fgColor="C6EFCE"), "yellow": PatternFill("solid", fgColor="FFEB9C"), "red": PatternFill("solid", fgColor="FFC7CE"), "grey": PatternFill("solid", fgColor="E7E6E6")}
SOURCES = {s["key"]: s for s in M.SOURCES}
inv = pd.read_csv("data/FILE_INVENTORY.csv"); SHA = dict(zip(inv.path, inv.sha256)); shapes = pd.read_csv(f"logs/{DATE}/raw_file_shapes.csv")
p = pd.read_csv("data/out/state_panel_2015_2025.csv"); p = p.sort_values(["state", "year"]).reset_index(drop=True)
wb = Workbook(); wb._fonts = IndexedList([BODY]); wb._named_styles["Normal"].font = BODY; wb.remove(wb.active)

# ---- helpers ----
def clean(v):
    if v is None: return None
    if isinstance(v, (float, np.floating)):
        return None if np.isnan(v) else float(v)
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.bool_,)): return bool(v)
    if isinstance(v, str):
        v = ILLEGAL_CHARACTERS_RE.sub("", v)
        return v[:32000] if len(v) > 32000 else v
    return v
def fix_text(ws, r, row):  # keep literal text that looks like a formula or error as text
    for j, v in enumerate(row, 1):
        if isinstance(v, str) and (v.startswith("=") or v in ERROR_CODES): ws.cell(r, j).data_type = "s"
def header(ws, cols, row=1, freeze=None):
    for j, c in enumerate(cols, 1):
        x = ws.cell(row, j); x.value = c; x.font = HDR; x.fill = HFILL; x.alignment = Alignment(wrap_text=True, vertical="center")
    ws.freeze_panes = freeze or f"{L(3 if len(cols) > 6 else 1)}{row + 1}"  # a string: ws.cell() here would create a row and shift ws.append down
def write_df(name, df, fmt=None, widths=None, freeze=None, font=None):
    ws = wb.create_sheet(name); header(ws, list(df.columns), freeze=freeze)
    for i, rec in enumerate(df.itertuples(index=False), 2):
        row = [clean(v) for v in rec]; ws.append(row); fix_text(ws, i, row)
    if fmt or font:
        for j, c in enumerate(df.columns, 1):
            nf = fmt.get(c) if fmt else None
            for i in range(2, len(df) + 2):
                if nf: ws.cell(i, j).number_format = nf
                if font and j > 2: ws.cell(i, j).font = font
    for j, c in enumerate(df.columns, 1): ws.column_dimensions[L(j)].width = max(10, min(18, len(str(c)) + 2)) if j > 2 else 12
    for k, w in (widths or {}).items(): ws.column_dimensions[k].width = w
    ws.auto_filter.ref = f"A1:{L(len(df.columns))}{len(df) + 1}"; return ws
def link(c, url, internal=False):
    if url: c.hyperlink = url; c.font = LINK
def read_csv_rows(path):
    for enc in ("utf-8-sig", "latin1"):
        try:
            with open(path, encoding=enc, newline="") as fh: return list(csv.reader(fh))
        except UnicodeDecodeError: continue
NUM = re.compile(r"^-?(0|[1-9]\d*)(\.\d+)?$")
def conv(v):
    if v == "": return None
    if NUM.match(v):
        x = float(v); return int(x) if "." not in v and abs(x) < 1e15 else x
    return ILLEGAL_CHARACTERS_RE.sub("", v)[:32000]
def write_raw(name, rows):
    """Exact copy: same rows and columns as the file, so a cell's address here is its address there. Header row detected for styling and filter."""
    ws = wb.create_sheet(name); n = max(len(r) for r in rows[:40])
    hdr = next(i for i, r in enumerate(rows[:40]) if sum(x not in (None, "") for x in r) >= max(2, 0.8 * n))
    for i, r in enumerate(rows, 1):
        ws.append(r); fix_text(ws, i, r)
    for j in range(1, n + 1):
        x = ws.cell(hdr + 1, j); x.font = HDR; x.fill = HFILL; x.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[L(j)].width = 14
    ws.freeze_panes = ws.cell(hdr + 2, 1); ws.auto_filter.ref = f"A{hdr + 1}:{L(n)}{len(rows)}"
    return ws, [("" if rows[hdr][j] in (None, "") else str(rows[hdr][j])) if j < len(rows[hdr]) else "" for j in range(n)]

# ---- Core Panel ----
raw = ["state", "year", "population", "sales_mwh", "revenue_kusd", "gdp_real_musd2017", "gdp_nom_musd", "gdp_farm_musd", "gdp_manuf_musd", "gen_total_mwh", "gen_renew_mwh", "gen_fossil_mwh", "gen_solar_mwh", "cap_renew_mw", "dc_jobs", "tech5415_jobs", "total_jobs", "land_sqmi", "ai_dc_per1000_lag1"]
der = [("sales_mwh_pc", "=D{r}/C{r}", "0.00"), ("ln_ec", "=LN(T{r})", "0.000"), ("ee_usd_per_mwh", "=F{r}*1000000/D{r}", "#,##0"), ("ln_ee", "=LN(V{r})", "0.000"), ("renew_share", "=K{r}/J{r}", "0.0%"), ("solar_share", "=M{r}/J{r}", "0.0%"), ("fossil_to_renew", '=IF(K{r}>0,L{r}/K{r},"")', "0.00"), ("ai_dc_per1000", '=IF(O{r}="","",1000*O{r}/Q{r})', "0.000"), ("tech_share", '=IF(P{r}="","",P{r}/Q{r})', "0.00%"), ("price_c_kwh", "=100*E{r}/D{r}", "0.00"), ("ln_gdp_pc", "=LN(F{r}*1000000/C{r})", "0.000"), ("manuf_share", "=I{r}/G{r}", "0.0%"), ("ea_nonfarm_gdp_per_sqmi", "=(G{r}-H{r})*1000000/R{r}", "#,##0")]
raw2 = ["gen_wind_mwh", "gen_coal_mwh", "co2_power_t"]
N = len(p) + 1
der2 = [("ln_ea", "=LN(AF{r})", "0.000"), ("pop_growth", "=C{r}/AJ{r}-1", "0.00%"), ("wind_share", "=AG{r}/J{r}", "0.0%"), ("coal_share", "=AH{r}/J{r}", "0.0%"), ("co2_per_mwh", '=IF(AI{r}="","",AI{r}/J{r})', "0.000"), ("new_renew_mw", "=N{r}-AK{r}", "#,##0.0"),
        ("net_exporter_2015", "=IF(INDEX($J$1:$J$%d,ROW()-(B{r}-2015))>INDEX($D$1:$D$%d,ROW()-(B{r}-2015)),1,0)" % (N, N), "0"),
        ("energy_equity", "=(G{r}/SUMIF($B$2:$B$%d,B{r},$G$2:$G$%d))/(D{r}/SUMIF($B$2:$B$%d,B{r},$D$2:$D$%d))" % (N, N, N, N), "0.000"), ("in_zhang_sample", '=IF(A{r}<>"DC",1,0)', "0"), ("in_fang_sample", "=IF(AND(B{r}>=2018,B{r}<=2021),1,0)", "0")]
core_cols = raw + [d[0] for d in der] + raw2 + ["population_prev", "cap_renew_prev"] + [d[0] for d in der2]
ws = wb.create_sheet("Core Panel"); header(ws, core_cols)
FORMULAS = {}
for i, rec in enumerate(p.itertuples(index=False), 2):
    d = rec._asdict()
    for j, c in enumerate(raw, 1):
        x = ws.cell(i, j, clean(d[c])); x.font = BLUE if j > 2 else BODY
        if j > 2: x.number_format = "#,##0" if c != "ai_dc_per1000_lag1" else "0.000"
    for k, (nm, f, nf) in enumerate(der, len(raw) + 1):
        x = ws.cell(i, k, f.format(r=i)); x.number_format = nf
    b = len(raw) + len(der) + 1
    for k, c in enumerate(raw2, b):
        x = ws.cell(i, k, clean(d[c])); x.font = BLUE; x.number_format = "#,##0"
    if d["year"] == 2015:  # 2014 isn't on the sheet: value backed out of the panel
        x = ws.cell(i, b + 3, int(round(d["population"] / (1 + d["pop_growth"])))); x.font = BLUE
        y = ws.cell(i, b + 4, round(d["cap_renew_mw"] - d["new_renew_mw"], 1)); y.font = BLUE
    else:
        x = ws.cell(i, b + 3, f"=C{i - 1}"); y = ws.cell(i, b + 4, f"=N{i - 1}")
    x.number_format = "#,##0"; y.number_format = "#,##0.0"
    for k, (nm, f, nf) in enumerate(der2, b + 5):
        x = ws.cell(i, k, f.format(r=i)); x.number_format = nf
for nm, f, _ in der + der2: FORMULAS[nm] = f.format(r=2)
FORMULAS["population_prev"] = "2015: value; later: =C{r-1}"; FORMULAS["cap_renew_prev"] = "2015: value; later: =N{r-1}"
for j in range(1, len(core_cols) + 1): ws.column_dimensions[L(j)].width = 8 if j <= 2 else 15
ws.auto_filter.ref = f"A1:{L(len(core_cols))}{N}"
ws["S1"].comment = Comment("Last year's data-center jobs per 1,000 workers, from the panel. 2015 uses 2014 QCEW. Values, because 2014 isn't on this sheet.", "Build")
ws["O1"].comment = Comment("QCEW NAICS 518210, private ownership, annual average employment. Blank = suppressed by BLS.", "Build")

# ---- data tabs ----
RD = lambda f: pd.read_csv(f)
fang = RD("data/fang_panel.csv").sort_values(["state", "year"])
CLEAN = [  # tab, file, sources rule, script, receipt
 ("Full Panel", "data/out/state_panel_2015_2025.csv", None, "econ499r_starter/scripts/build_panel.py", "README.md"),
 ("Fang Panel", "data/fang_panel.csv", None, "econ499r_starter/scripts/build_fang_tables.py", "fang_panel.md"),
 ("RPS Targets", "data/lbnl_rps_targets.csv", ["lbnl_rps"], "econ499r_starter/scripts/build_side_tables_nov4.py", "lbnl_rps.md"),
 ("ACS Broadband", "data/acs_broadband.csv", ["acs"], "econ499r_starter/scripts/build_side_tables_nov4.py", "acs.md"),
 ("EPU Annual", "data/epu_state_annual.csv", ["epu"], "econ499r_starter/scripts/build_side_tables_nov4.py", "epu.md"),
 ("NSF State RD", "data/nsf_state_rd.csv", ["nsf"], "econ499r_starter/scripts/build_side_tables_nov4.py", "nsf.md"),
 ("OWID Solar", "data/owid_global_solar_capacity.csv", ["owid"], "econ499r_starter/scripts/build_side_tables_nov4.py", "owid.md"),
 ("LBNL Solar Projects", "data/lbnl_utility_solar.csv", ["lbnl_solar"], "econ499r_starter/scripts/build_side_tables_nov4.py", "lbnl_solar.md"),
 ("Epoch by State", "data/epoch_ai_campuses_by_state.csv", ["epoch"], "econ499r_starter/scripts/build_side_tables_nov4.py", "epoch.md"),
 ("AI All Ownerships", "data/ai_allown_518210.csv", ["qcew"], "econ499r_starter/scripts/build_ai_allown.py", "bls_qcew.md"),
 ("AI Job Postings", "data/ai_job_postings_state.csv", M.SOURCE_KEYS_AI, "econ499r_starter/scripts/build_fang_tables.py", "ai_index.md"),
 ("AI Postings Overlap", "data/ai_job_postings_overlap_rows.csv", M.SOURCE_KEYS_AI, "econ499r_starter/scripts/build_fang_tables.py", "ai_index.md"),
 ("SEDS Renewables", "data/seds_renewables_state.csv", ["seds", "seds_prices"], "econ499r_starter/scripts/build_fang_tables.py", "seds_fang.md"),
 ("NCSES Bachelors", "data/ncses_bachelors_state.csv", ["ncses"], "econ499r_starter/scripts/build_fang_tables.py", "ncses.md"),
 ("Fang Split Vars", "data/fang_split_vars.csv", None, "econ499r_starter/scripts/build_fang_tables.py", "fang_panel.md"),
 ("Net Producer Defs", "data/fang_net_producer_definitions.csv", ["seds", "seds_prod", "eia_gen", "eia_sales"], "econ499r_starter/scripts/build_net_producer_defs.py", "seds_fang.md"),
 ("NOAA Degree Days", "data/noaa_degree_days.csv", ["noaa"], "econ499r_starter/scripts/download_noaa_degree_days.py", "noaa.md"),
 ("FERC1 Utilities", "data/out/ferc1_utility_financials.csv", ["pudl"], "econ499r_starter/scripts/ferc_fin.py", "ferc_pudl.md"),
 ("FERC1 Cost by Tech", "data/out/ferc1_cost_by_technology.csv", ["pudl"], "econ499r_starter/scripts/ferc_fin.py", "ferc_pudl.md"),
 ("FERC1 Plants", "data/out/ferc1_plant_costs.csv", ["pudl"], "econ499r_starter/scripts/ferc_fin.py", "ferc_pudl.md"),
 ("SEC Companies", "data/out/sec_company_financials.csv", ["sec"], "econ499r_starter/scripts/sec_fin.py", "README.md"),
 ("State Centroids", "data/out/state_centroids_land.csv", ["census_gaz"], "econ499r_starter/scripts/build_panel.py", "census.md"),
]
DFS = {}
for tab, f, *_ in CLEAN:
    d = RD(f); DFS[tab] = d
    fmt = {c: "#,##0.0" for c in d.columns if c.endswith("_musd")} if tab in ("FERC1 Utilities", "SEC Companies") else None
    write_df(tab, d, fmt=fmt, font=BLUE if tab == "Fang Panel" else None)
for name, f in (("W Inverse Distance", "data/out/W_inverse_distance_rowstd.csv"), ("W Border", "data/out/W_border_binary.csv"), ("W Distance Miles", "data/out/W_distance_miles.csv")):
    d = pd.read_csv(f, index_col=0); DFS[name] = d; ws = wb.create_sheet(name); header(ws, ["state"] + list(d.columns), freeze="B2")
    for i, (idx, rec) in enumerate(d.iterrows(), 2):
        ws.append([idx] + [float(v) for v in rec.values]); ws.cell(i, 1).font = BOLD
    for j in range(1, d.shape[1] + 2): ws.column_dimensions[L(j)].width = 7
    ws.auto_filter.ref = f"A1:{L(d.shape[1] + 1)}{len(d) + 1}"

# ---- whole raw tables (size rule) ----
RAWTABS = [  # tab, file, sheet, source, used as
 ("Raw EIA Generation", "data/raw/eia/annual_generation_state.xlsx", 0, "eia_gen", "Input to Full Panel"), ("Raw EIA Capacity", "data/raw/eia/existcapacity_annual.xlsx", 0, "eia_cap", "Input to Full Panel"), ("Raw EIA Sales", "data/raw/eia/HS861_2010-.xlsx", "Total Electric Industry", "eia_sales", "Input to Full Panel"), ("Raw EIA Emissions", "data/raw/eia/emission_annual.xlsx", 0, "eia_emis", "Input to Full Panel"), ("Raw EIA Plan Capacity", "data/raw/eia/plancapacity_annual.xlsx", 0, "eia_plan", "Not used"),
 ("Raw SEDS Use", "data/raw/eia/seds/use_all_btu.csv", None, "seds", "Input to Full Panel and SEDS Renewables"), ("Raw SEDS Prices", "data/raw/eia/seds/pr_all.csv", None, "seds_prices", "Input to SEDS Renewables"),
 ("Raw BEA SAGDP2", "data/raw/bea/sagdp/SAGDP2__ALL_AREAS_1997_2025.csv", None, "bea_gdp", "Input to Full Panel"), ("Raw BEA SAGDP9", "data/raw/bea/sagdp/SAGDP9__ALL_AREAS_1997_2025.csv", None, "bea_gdp", "Input to Full Panel"), ("Raw BEA SAINC1", "data/raw/bea/sainc/SAINC1__ALL_AREAS_1929_2025.csv", None, "bea_inc", "Input to Full Panel"),
 ("Raw Census Pop V2025", "data/raw/census_pop/NST-EST2025-ALLDATA.csv", None, "census_pop", "Check of population"), ("Raw Census Gazetteer", "data/raw/census/2020_Gaz_counties_national.txt", "tab", "census_gaz", "Input to land_sqmi and centroids"), ("Raw Census Adjacency", "data/raw/census/county_adj.txt", "pipe", "census_adj", "Input to W Border"),
 ("Raw EPU Monthly", "data/raw/epu/State_Policy_Uncertainty.xlsx", 0, "epu", "Input to EPU Annual"), ("Raw OWID Solar", "data/raw/owid/solar-pv-cumulative-capacity.csv", None, "owid", "Input to OWID Solar"),
 ("Raw Epoch Sites", "data/raw/epoch/data_centers.csv", None, "epoch", "Input to Epoch by State; Georgia"), ("Raw Epoch Timelines", "data/raw/epoch/data_center_timelines.csv", None, "epoch", "Input to Epoch by State; Georgia"), ("Raw Epoch Chips", "data/raw/epoch/data_center_chip_quantities.csv", None, "epoch", "Not used"), ("Raw Epoch Chip Types", "data/raw/epoch/chip_types.csv", None, "epoch", "Not used"), ("Raw Epoch Chillers", "data/raw/epoch/data_center_chillers.csv", None, "epoch", "Not used"), ("Raw Epoch Cooling Towers", "data/raw/epoch/data_center_cooling_towers.csv", None, "epoch", "Not used"),
 ("Raw RMI Customers Sales", "data/raw/rmi/customers_sales.csv", None, "rmi", "Not used"), ("Raw RMI Net Plant", "data/raw/rmi/net_plant_balance.csv", None, "rmi", "Not used"), ("Raw RMI Reliability", "data/raw/rmi/reliability.csv", None, "rmi", "Not used"), ("Raw RMI Housing Income", "data/raw/rmi/housing_units_income.csv", None, "rmi", "Not used"), ("Raw RMI Emission Targets", "data/raw/rmi/emissions_targets.csv", None, "rmi", "Not used"), ("Raw RMI Debt Equity", "data/raw/rmi/debt_equity_returns.csv", None, "rmi", "Not used")]
RAWHEAD = {}; RAWROWS = {}
for tab, f, sh, key, used in RAWTABS:
    if f.endswith(".xlsx"):
        d = pd.read_excel(f, sheet_name=sh, header=None, dtype=object); rows = [[clean(v) if not (isinstance(v, float) and np.isnan(v)) else None for v in r] for r in d.values.tolist()]
    else:
        delim = {"tab": "\t", "pipe": "|"}.get(sh, ",")
        for enc in ("utf-8-sig", "latin1"):
            try:
                with open(f, encoding=enc, newline="") as fh: rows = [[conv(x.strip() if delim == "\t" else x) for x in r] for r in csv.reader(fh, delimiter=delim)]
                break
            except UnicodeDecodeError: continue
    ws, head = write_raw(tab, rows); RAWHEAD[tab] = head; RAWROWS[tab] = len(rows)
RAWMAP = {f: tab for tab, f, *_ in RAWTABS}

# ---- registry ----
VAL = open("data/DATA_VALIDATION.md").read()
def md_table(text, start_heading):
    """All rows of the first pipe table after a heading."""
    i = text.index(start_heading); out = []; head = None
    for ln in text[i:].split("\n")[1:]:
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "): continue
            if head is None: head = cells
            else: out.append(dict(zip(head, cells)))
        elif head is not None: break
    return out
strip = lambda s: re.sub(r"[*`]", "", s).strip()
VERDICT = {strip(r["Variable"]): (strip(r["Ready"]), r["Note"]) for r in md_table(VAL, "## Verdict table")}
AUD = open("data/INDEPENDENT_AUDIT_2026-11-04.md").read()
CITE = {strip(r["Source"]): strip(r["Citation"]) for r in md_table(AUD, "## 4. Sources")}
def citation(s): return s.get("cite") or CITE.get(s.get("audit", ""), "")
for s in M.SOURCES:
    if not citation(s): sys.exit(f"no citation: {s['key']}")
code = {}
def codetext(pats):
    t = ""
    for pt in pats:
        for f in glob.glob(pt): t += open(f, errors="ignore").read()
    return t
ZT = codetext(["code/R/load_panel.R", "code/R/04b*.R", "code/R/04c*.R", "code/R/04d*.R", "code/R/04e*.R"]); FT = codetext(["code/R/04h*.R"]); GT = codetext(["code/python/04f*.py"])
ZINPUT = {"gen_total_mwh", "gen_renew_mwh", "gen_fossil_mwh", "gen_solar_mwh", "gen_wind_mwh", "gen_coal_mwh", "sales_mwh", "revenue_kusd", "population", "population_prev", "cap_renew_prev", "cap_renew_mw", "gdp_real_musd2017", "gdp_nom_musd", "gdp_farm_musd", "gdp_manuf_musd", "dc_jobs", "tech5415_jobs", "total_jobs", "land_sqmi", "sales_mwh_pc", "ee_usd_per_mwh", "ea_nonfarm_gdp_per_sqmi", "dc_suppressed", "co2_power_t"}
def used_in(tab, v, rawused=None):
    if rawused: return rawused
    if tab in ("FERC1 Utilities", "FERC1 Cost by Tech", "FERC1 Plants", "SEC Companies"): return "finance"
    if tab in ("Epoch by State", "Georgia"): return "Georgia"
    if tab in ("OWID Solar", "LBNL Solar Projects"): return "Georgia"
    if tab in ("W Inverse Distance", "W Border", "W Distance Miles", "State Centroids"): return "Zhang"
    if tab == "AI Postings Overlap": return "Fang (check)"
    if tab == "NOAA Degree Days" and v not in ("state", "year"): return "Zhang (check)"
    if tab == "Net Producer Defs" and v not in ("state", "year"): return "Fang (check)"
    if v in ("state", "year"): return "Key"
    wd = lambda t: re.search(rf"\b{re.escape(v)}\b", t) is not None
    out = []
    if wd(ZT) or v in ZINPUT and tab in ("Core Panel", "Full Panel"): out.append("Zhang")
    if tab in ("Fang Panel", "AI Job Postings", "SEDS Renewables", "NCSES Bachelors", "Fang Split Vars") or wd(FT): out.append("Fang")
    if tab in ("RPS Targets", "AI All Ownerships") and "Zhang" not in out: out.append("Zhang")
    if tab in ("ACS Broadband", "NSF State RD", "EPU Annual") and not out: out.append("Stretch")
    return " / ".join(out) or "not used"
def src_keys(tab, v):
    for t, _, rule, *_ in CLEAN:
        if t == tab and rule:
            if tab == "RPS Targets" and v == "target_pct_ed2023": return ["lbnl_rps23"]
            if tab == "SEDS Renewables" and v == "ep_tetcd": return ["seds_prices"]
            return rule
    if tab in ("W Inverse Distance", "W Distance Miles"): return ["census_gaz"]
    if tab == "W Border": return ["census_adj"]
    fx = [("re_bbtu wind_bbtu solar_bbtu geothermal_bbtu hydro_bbtu biomass_bbtu total_energy_bbtu", ["seds"]), ("ep_tetcd", ["seds_prices"]), ("edu_bach_per1000", ["ncses"]), ("epu_composite epu_national epu_state", ["epu"]), ("target_pct", ["lbnl_rps"]), ("rd_total_musd", ["nsf"]), ("income_pc_usd", ["bea_inc"]), ("census_region", ["census_region"]), ("elec_consumption_mwh elec_price_c_kwh", ["eia_sales"]), ("net_producer net_exporter_2015", ["eia_gen", "eia_sales"]), ("extreme_weather extreme_weather_note", ["noaa"]), ("ai_postings ai_share_us_pct ai_share_source ai_share_of_state_pct ai_edition ai_vendor ai_vintage", M.SOURCE_KEYS_AI),
          ("in_zhang_sample in_fang_sample state year contig48 is_dc", []), ("co2_power_t", ["eia_emis"]), ("co2_per_mwh_t co2_per_mwh", ["eia_emis", "eia_gen"]), ("seds_total_energy_bbtu", ["seds"]), ("seds_mmbtu_pc", ["seds", "bea_inc"]), ("population population_prev pop_growth", ["bea_inc"]), ("land_sqmi", ["census_gaz"]), ("sales_mwh_pc ln_ec", ["eia_sales", "bea_inc"]), ("ee_usd_per_mwh ln_ee energy_equity", ["bea_gdp", "eia_sales"]), ("ln_gdp_pc", ["bea_gdp", "bea_inc"]), ("manuf_share", ["bea_gdp"]), ("ea_nonfarm_gdp_per_sqmi ln_ea", ["bea_gdp", "census_gaz"]), ("renew_share solar_share wind_share coal_share clean_share fossil_to_renew", ["eia_gen"])]
    for names, k in fx:
        if v in names.split(): return k
    if v.startswith("gen_"): return ["eia_gen"]
    if v.startswith(("cap_", "new_")): return ["eia_cap"]
    if v.startswith(("sales_", "revenue", "price_")): return ["eia_sales"]
    if v.startswith(("dc_", "tech", "total_jobs", "ai_dc", "hma")): return ["qcew"]
    if v.startswith("gdp_"): return ["bea_gdp"]
    sys.exit(f"no source rule: {tab} {v}")
FAMILY = [("gen_", "green", "N01 fuels sum to total; N02 states sum to U.S."), ("cap_", "green", "C.4 trace; audit cells for new_renew_mw"), ("new_", "green", "C.4 trace; audit cells for new_renew_mw"), ("sales_", "green", "Audit: 3 of 3 sales_mwh cells exact; cross-source vs SEDS"), ("revenue", "green", "D08 price identity"), ("price_com", "green", "D08 price identity"), ("population", "green", "Cross-source: 561 of 561 match Census"), ("gdp_", "green", "N05 states vs U.S.; audit raw-file cells"), ("dc_", "green", "N03 state vs national; R07 top states; audit cells"), ("tech5415", "green", "Audit: 3 of 3 cells exact"), ("total_jobs", "green", "N04 state vs national; audit cells"), ("land_sqmi", "green", "D18"), ("co2_power_t", "yellow", "Ends 2024"), ("seds_total", "yellow", "Ends 2024"), ("sales_mwh_pc", "green", "D12"), ("ee_usd", "green", "D14"), ("ea_nonfarm", "green", "D18"), ("contig48", "green", "P08"), ("is_dc", "green", "P09"), ("state", "green", "P02-P07 keys"), ("year", "green", "P02-P07 keys")]
SIDE_RATING = {"NOAA Degree Days": ("green", "Cross-source: Climate at a Glance matches nClimDiv on all 528 state-years"), "Net Producer Defs": ("yellow", "Cross-source: none of the rules reaches Fang's 76"), "RPS Targets": ("yellow", "New data, Nov 4: LBNL RPS"), "ACS Broadband": ("yellow", "New data, Nov 4: ACS"), "EPU Annual": ("green", "New data, Nov 4: EPU"), "NSF State RD": ("yellow", "New data, Nov 4: NSF"), "OWID Solar": ("green", "New data, Nov 4: OWID"), "LBNL Solar Projects": ("green", "New data, Nov 4: LBNL solar"), "Epoch by State": ("green, context only", "New data, Nov 4: Epoch"), "AI Job Postings": ("yellow", "Fang data, Nov 4: AI Index"), "AI Postings Overlap": ("yellow", "Fang data, Nov 4: AI Index"), "SEDS Renewables": ("green", "Fang data, Nov 4: SEDS"), "NCSES Bachelors": ("green", "Fang data, Nov 4: NCSES")}
def rating(tab, v):
    if v == "extreme_weather" or v == "extreme_weather_note": return "not run", "Fang's count of extreme hot and cold occurrences wasn't built"
    if tab.startswith("Raw "): return "not rated", "Raw as published; hash on Raw Files tab"
    if tab in SIDE_RATING: return SIDE_RATING[tab]
    if tab in ("FERC1 Utilities", "FERC1 Cost by Tech", "FERC1 Plants", "SEC Companies"): return "not rated", "Finance tables aren't used in any model and have no Part C rating"
    if tab == "AI All Ownerships": return "not rated", "Checked in logs/2026-11-04/gov_518210_shares.csv; audit fix 1"
    if tab.startswith(("W ", "State Centroids")): return "green", "C.5 and audit; centroid and border sources differ from memo (minor)"
    if tab == "Georgia": return "yellow", "Each figure checked against its cited page by build_georgia_tables.py"
    vv = {"co2_per_mwh": "co2_per_mwh_t"}.get(v, v)
    if vv in VERDICT: return VERDICT[vv][0], "Verdict table, DATA_VALIDATION.md"
    if v in ("price_c_kwh", "elec_consumption_mwh", "elec_price_c_kwh", "net_producer", "net_exporter_2015", "coal_share", "population_prev", "cap_renew_prev", "in_zhang_sample", "in_fang_sample", "income_pc_usd", "census_region", "gen_total_mwh"): return "green", "Part C identities; recalculated values match the panel"
    if tab in ("Fang Panel", "Fang Split Vars"):
        if v.startswith("ai_") and v not in ("ai_dc_per1000", "ai_dc_per1000_lag1"): return "yellow", "Fang data, Nov 4: AI Index"
        if v in ("rd_total_musd",): return "yellow", "New data, Nov 4: NSF"
        if v == "target_pct": return "yellow", "New data, Nov 4: LBNL RPS"
        if v.startswith("epu"): return "green", "New data, Nov 4: EPU"
        if v == "dc_jobs_lag1": return "green", "D21; N03"
        if v in FANG_SEDS: return "green", "Fang data, Nov 4: SEDS"
        if v == "edu_bach_per1000": return "green", "Fang data, Nov 4: NCSES"
    for pre, r, chk in FAMILY:
        if v.startswith(pre): return r, chk
    sys.exit(f"no rating rule: {tab} {v}")
FANG_SEDS = set(M.SIDE_DEFS["SEDS Renewables"])
def gap_reason(tab, v):
    rules = [(("co2_power_t", "co2_per_mwh_t", "co2_per_mwh"), "EIA emissions end in 2024"), (("seds_total_energy_bbtu", "seds_mmbtu_pc", "re_bbtu", "wind_bbtu", "solar_bbtu", "geothermal_bbtu", "hydro_bbtu", "biomass_bbtu", "total_energy_bbtu", "ep_tetcd"), "SEDS ends in 2024"), (("edu_bach_per1000",), "NCSES table ends in 2024"),
             (("dc_jobs", "dc_wages_usd", "ai_dc_per1000", "hma", "dc_jobs_private", "dc_jobs_allown", "gov_share_pct", "ai_allown_per1000"), "BLS suppressed AK, ND, SD and WY in 2025"), (("ai_postings", "ai_share_us_pct", "ai_share_source", "ai_share_of_state_pct", "ai_edition", "ai_vendor", "ai_vintage"), "No state postings published before 2018"), (("rd_total_musd",), "The NSF editions used cover 2017-2023"),
             (("broadband_pct", "broadband_pct_moe", "broadband_households", "total_households", "census_var"), "No ACS 1-year release for 2020"), (("ta_achievement_pct",), "LBNL gives no achievement value; ta_status says why"), (("rd_nonprofit_musd", "rd_state_internal_musd"), "NSF printed a non-numeric cell; text in published_not_numeric"), (("published_not_numeric",), "Filled only where a cell is non-numeric"), (("extreme_weather",), "Not run: Fang's count of extreme hot and cold occurrences wasn't built")]
    if v == "note": return "Text column; blank means no note"
    if tab == "EPU Annual": return "Blank in the publisher's file before the state's series starts; complete in 2015-2025"
    if v == "page": return "No report prints 2019-2020"
    for names, why in rules:
        if v in names: return why
    if tab == "LBNL Solar Projects": return "Blank in LBNL's file (for example, no storage or no PPA, or the plant wasn't operating that year)"
    if tab == "FERC1 Utilities": return "Accounts for solar, wind, storage and other renewable start in 2021" if v in ("plant_solar_musd", "plant_wind_musd", "plant_storage_musd", "plant_other_renewable_musd", "production_renewable_share") else "Blank in PUDL for that filer-year"
    if tab in ("FERC1 Cost by Tech", "FERC1 Plants"): return "Blank in PUDL or not computable for that plant-year"
    if tab == "SEC Companies": return "No fact under the XBRL tags used. NEE, DTE and HASI capex use company-specific tags" if v == "capex_musd" else "No fact under the XBRL tags used, or field not applicable"
    if tab == "AI Postings Overlap": return "Text column; blank means no note"
    return None
UNKNOWN_GAPS = []
def def_of(tab, v):
    if tab in ("Core Panel", "Full Panel", "Fang Panel", "Fang Split Vars"):
        for dct in (M.CORE_EXTRA if tab == "Core Panel" else {}, M.FANG_DEFS if tab.startswith("Fang") else {}, M.PANEL_DEFS):
            if v in dct: return dct[v]
        if v.startswith("gen_"): return (f"Net generation from {v[4:-4]}", "MWh")
        if v.startswith("cap_"): return (f"Nameplate capacity, {v[4:-3]}", "MW")
    if tab == "LBNL Solar Projects":
        m = re.match(r"(\d{4})_capacity_factor", v)
        if m: return (f"Capacity factor, {m.group(1)}", "share")
        if v in M.LBNL: return (M.LBNL[v], "see definition")
    if tab == "State Centroids": return {"USPS": ("State code", ""), "lat": ("Land-weighted latitude of county centroids", "degrees"), "lon": ("Land-weighted longitude of county centroids", "degrees"), "land_sqmi": ("Land area", "sq mi")}[v]
    if tab == "AI Postings Overlap": return {"postings": ("AI postings as printed in the other edition", "count"), "st_share": ("State share", "percent"), "edition": ("Edition", "year"), "note": ("Note", "text")}.get(v, ("Key", ""))
    d = M.SIDE_DEFS.get(tab, {})
    if v in d: return d[v]
    if v in M.PANEL_DEFS: return M.PANEL_DEFS[v]
    sys.exit(f"no definition: {tab} {v}")
PL = {t: os.path.basename(s) for t, _, _, s, _ in CLEAN}; SCRIPTS = {t: s for t, _, _, s, _ in CLEAN}; RECEIPT = {t: r for t, _, _, _, r in CLEAN}
ST = {}
def lines(script, v):
    if script not in ST: ST[script] = open(script, errors="ignore").read().split("\n")
    hit = [str(i + 1) for i, ln in enumerate(ST[script]) if re.search(rf"\b{re.escape(v)}\b", ln)]
    return ("L" + ", L".join(hit[:5]) + (f" (+{len(hit) - 5} more)" if len(hit) > 5 else "")) if hit else "No literal name: copied or built in a loop"
def src_fields(keys):
    ss = [SOURCES[k] for k in keys]
    paths = []
    for s in ss: paths += s["raw"]
    shas = []
    for pth in paths:
        ms = [x for x in inv.path if x == pth or (pth.endswith(("/", "_")) and x.startswith(pth))]
        shas += [SHA[x] for x in ms if x == pth]
        if pth.endswith(("/", "_")): shas.append(f"{len(ms)} files; see Raw Files tab")
    if len(paths) > 6: paths = paths[:6] + ["..."]
    if len(shas) > 4: shas = shas[:4] + [f"+{len(shas) - 4} more; see Raw Files tab"]
    return dict(source=" + ".join(s["dataset"] for s in ss[:3]) + (f" + {len(ss) - 3} more" if len(ss) > 3 else ""), publisher="; ".join(dict.fromkeys(s["publisher"] for s in ss)), file_link=ss[0]["link"] if ss else "", landing_page=ss[0]["landing"] if ss else "", raw_file_path="; ".join(paths), sha256="; ".join(shas), vintage_or_access="; ".join(dict.fromkeys(f"{s['vintage']} (accessed {s['access']})" for s in ss[:2])), receipt=ss[0]["receipt"] if ss else "", primary_secondary="; ".join(dict.fromkeys(s["ptype"] for s in ss)), citation=" | ".join(dict.fromkeys(citation(s) for s in ss[:2])))
LIM = {}
for sc, txt, eff, kind in M.LIMITS:
    for w in re.split(r"[, ]+", sc):
        LIM.setdefault(w, []).append(txt)
def limits_of(tab, v):
    out = LIM.get(v, [])[:2]
    if not out:
        for w, tx in LIM.items():
            if w.endswith("*") and v.startswith(w[:-1]): out = tx[:1]; break
    if not out and tab in ("AI Job Postings", "AI Postings Overlap") or (not out and v.startswith("ai_") and v not in ("ai_dc_per1000", "ai_dc_per1000_lag1")): out = LIM.get("ai_postings", [])[:2]
    if not out and tab == "RPS Targets": out = LIM.get("target_pct", [])[:1]
    return " ".join(out) if out else "See Limitations tab"
REG = []
def cov(d, v):
    if isinstance(d, pd.DataFrame) and v in d.columns:
        s = d[v]; yrs = f"{int(d.year.min())}-{int(d.year.max())}" if "year" in d.columns else ""
        st = f"{d.state.nunique()} areas" if "state" in d.columns else ""
        return yrs, st, int(s.isna().sum())
    return "", "", 0
GAPROWS = []
def add_var(tab, v, col, d=None, formula="", script=None, receipt=None):
    df, unit = def_of(tab, v); keys = src_keys(tab, v); yrs, st, miss = cov(d, v)
    why = ""
    if miss:
        why = gap_reason(tab, v)
        if why is None: UNKNOWN_GAPS.append((tab, v, miss)); why = "UNKNOWN"
    r, chk = rating(tab, v); sf = src_fields(keys)
    status = "Not available" if v.startswith("extreme_weather") else "Ready"
    sc = script or SCRIPTS.get(tab, "")
    REG.append(dict(variable=v, definition=df, unit=unit, formula=formula, **sf, script=sc, script_lines=lines(sc, v) if sc else "", tab=tab, column=col, years=yrs, states=st, missing_cells=miss, missing_reason=why, used_in=used_in(tab, v), validation_rating=r, validation_check=chk, limitations=limits_of(tab, v), status=status))
    if not REG[-1]["receipt"]: REG[-1]["receipt"] = RECEIPT.get(tab, "README.md")
core_df = p.copy(); core_df["co2_per_mwh"] = p.co2_per_mwh_t
BUILD = "code/python/build_master_workbook.py"
for j, v in enumerate(core_cols, 1):
    dd = core_df if v in core_df.columns else None
    add_var("Core Panel", v, L(j), dd, formula=FORMULAS.get(v, "Value from the panel"), script=BUILD if v in FORMULAS else "econ499r_starter/scripts/build_panel.py")
    if dd is None:
        for fk, y, s in (("in_zhang_sample", "2015-2025", "51 areas"), ("in_fang_sample", "2015-2025", "51 areas"), ("coal_share", "2015-2025", "51 areas"), ("net_exporter_2015", "2015-2025", "51 areas"), ("population_prev", "2015-2025", "51 areas"), ("cap_renew_prev", "2015-2025", "51 areas")):
            if fk == v: REG[-1]["years"], REG[-1]["states"] = y, s
for tab, f, *_ in CLEAN:
    d = DFS[tab]
    for j, v in enumerate(d.columns, 1):
        add_var(tab, v, L(j), d)
for tab, name in (("W Inverse Distance", "Row-standardized inverse-distance weight between two states"), ("W Border", "1 if two states share a border, from county adjacency"), ("W Distance Miles", "Distance between state centroids")):
    d = DFS[tab]; sf = src_fields(src_keys(tab, "x"))
    REG.append(dict(variable=f"{tab} (50 state columns)", definition=name, unit={"W Distance Miles": "miles"}.get(tab, "weight"), formula="", **sf, script="econ499r_starter/scripts/build_panel.py", script_lines=lines("econ499r_starter/scripts/build_panel.py", "W"), tab=tab, column=f"B:{L(d.shape[1] + 1)}", years="", states=f"{d.shape[1]} areas", missing_cells=int(d.isna().sum().sum()), missing_reason="", used_in="Zhang", validation_rating="green", validation_check="C.5 and audit; centroid and border sources differ from memo (minor)", limitations="See Limitations tab: W matrices", status="Ready"))
GEO = [("GA vs U.S. median", "A", "Georgia and the median of the 50 states, by year", "from Full Panel", "eia_gen"), ("Large-load Table 2", "A", "Pipeline, commitments and broken ground, approximate MW; Q2 2026 report, Table 2, PDF p. 8", "as filed", "ga_ll"), ("Large-load attachment by stage and segment", "A", "Projects and announced load by stage and segment; from the attachment, tab Main", "summed by build_georgia_tables.py", "ga_ll"), ("Cited filing figures", "A", "Figures from the IRP and large-load reports with document and PDF page", "as filed; each checked against its page", "ga_irp"), ("Epoch Georgia sites", "A", "Epoch AI sites in Georgia, latest timeline row", "from raw Epoch files", "epoch")]
for nm, col, dfn, fm, k in GEO:
    REG.append(dict(variable=nm, definition=dfn, unit="see section", formula=fm, **src_fields([k]), script="code/python/build_georgia_tables.py" if k != "eia_gen" else BUILD, script_lines="whole script", tab="Georgia", column=col, years="", states="GA", missing_cells=0, missing_reason="", used_in="Georgia", validation_rating="yellow" if k != "eia_gen" and k != "epoch" else "green", validation_check="Each figure checked against its cited page; attachment totals reconcile to the report" if k in ("ga_ll", "ga_irp") else "Part C; New data, Nov 4", limitations="See Limitations tab: Georgia IRP and large-load reports", status="Ready"))
for tab, f, sh, key, usedas in RAWTABS:
    head = RAWHEAD[tab]; sf = src_fields([key]); sf["raw_file_path"] = f; sf["sha256"] = SHA.get(f, ""); j = 0
    while j < len(head):
        v = head[j]
        if re.fullmatch(r"(19|20)\d{2}", v):
            k = j
            while k + 1 < len(head) and re.fullmatch(r"(19|20)\d{2}", head[k + 1]): k += 1
            vn, col = f"{v}-{head[k]} (year columns)", f"{L(j + 1)}:{L(k + 1)}"; j = k
        else: vn, col = (v or f"(column {L(j + 1)}, no header)"), L(j + 1)
        REG.append(dict(variable=re.sub(r"\s+", " ", vn), definition=f"Column as published in {os.path.basename(f)}. Not cleaned", unit="As published", formula="", **sf, script="", script_lines="", tab=tab, column=col, years="", states="", missing_cells="", missing_reason="", used_in=usedas, validation_rating="not rated", validation_check="Raw as published; hash on Raw Files tab", limitations="See Limitations tab", status="Ready")); j += 1
for v, dfn, k, stat, why in [("large_load_q1_q4_2024", "Georgia Power large-load reports for Q1-Q4 2024", "ga_ll_2024", "Pending", "Need a browser download; the PSC list returns 404 to scripts"), ]:
    REG.append(dict(variable=v, definition=dfn, unit="", formula="", **src_fields([k]), script="", script_lines="", tab="none", column="", years="", states="", missing_cells="", missing_reason=why, used_in="Georgia" if k == "ga_ll_2024" else "not used", validation_rating="not run", validation_check=why, limitations=why, status=stat))
if UNKNOWN_GAPS: sys.exit(f"gaps with no reason: {UNKNOWN_GAPS}")
reg = pd.DataFrame(REG); reg.to_csv("data/variable_registry.csv", index=False)
print("registry", reg.shape, reg.status.value_counts().to_dict())

# ---- Variable Finder ----
ws = wb.create_sheet("Variable Finder")
vf = ["variable", "tab", "column", "definition", "unit", "formula", "source", "source_url", "receipt", "validation_rating", "status", "used_in", "years", "states", "missing_cells", "missing_reason", "limitations"]
header(ws, vf, freeze="B2")
RCOL = {"green": "green", "yellow": "yellow", "red": "red"}
for i, r in enumerate(reg.to_dict("records"), 2):
    for j, c in enumerate(vf, 1):
        v = {"source_url": r["file_link"]}.get(c, r.get(c, "")); v = "" if isinstance(v, float) and np.isnan(v) else v
        x = ws.cell(i, j, ("'" + v if isinstance(v, str) and v.startswith("=") else v) if c != "formula" else (str(v).lstrip("=") if v else ""))
    if r["tab"] != "none":
        col1 = str(r["column"]).split(":")[0]; here = f"#'{r['tab']}'!{col1}1"
        link(ws.cell(i, 2), here); link(ws.cell(i, 3), here)
    if r["file_link"]: link(ws.cell(i, 8), r["file_link"])
    if r["receipt"]: link(ws.cell(i, 9), "../data/receipts/" + r["receipt"])
    rt = str(r["validation_rating"]); ws.cell(i, 10).fill = FILL.get(rt.split(",")[0], FILL["grey"])
    ws.cell(i, 11).fill = {"Ready": FILL["green"], "Pending": FILL["yellow"], "Not available": FILL["red"]}[r["status"]]
for k, w in zip("ABCDEFGHIJKLMNOPQ", (34, 22, 8, 60, 14, 28, 44, 44, 16, 14, 13, 14, 11, 9, 9, 40, 60)): ws.column_dimensions[k].width = w
ws.auto_filter.ref = f"A1:{L(len(vf))}{len(reg) + 1}"

# ---- Data dictionary ----
with open("data/DATA_DICTIONARY.md", "w") as fh:
    fh.write(f"# Data dictionary\n\nGenerated from `data/variable_registry.csv` by `code/python/build_master_workbook.py`, as of {DATE}. Don't edit by hand. The workbook's Variable Finder tab comes from the same registry.\n\nRatings come from `data/DATA_VALIDATION.md`. \"Not rated\" means no Part C or Nov 4 rating exists for that table.\n")
    for tab, g in reg.groupby("tab", sort=False):
        fh.write(f"\n## {tab}\n\n| Variable | Definition | Unit | Formula | Source | Years | Areas | Missing | Used in | Rating | Status |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
        for r in g.to_dict("records"):
            miss = f"{r['missing_cells']}: {r['missing_reason']}" if r["missing_cells"] not in ("", 0) else ("" if r["status"] == "Ready" else r["missing_reason"])
            cells = [r["variable"], r["definition"], r["unit"], str(r["formula"]).lstrip("="), r["source"], r["years"], r["states"], miss, r["used_in"], r["validation_rating"], r["status"]]
            fh.write("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in cells) + " |\n")

# ---- Sources ----
ws = wb.create_sheet("Sources")
sc = ["dataset", "publisher", "landing_page", "exact_download_link", "access_date", "vintage_or_release", "primary_or_secondary", "citation", "license_note", "raw_files_with_sha256", "receipt", "notes"]
header(ws, sc, freeze="B2")
for i, s in enumerate(M.SOURCES, 2):
    rf = []
    for pth in s["raw"]:
        ms = [x for x in inv.path if x == pth or (pth.endswith(("/", "_")) and x.startswith(pth))]
        if pth.endswith(("/", "_")): rf.append(f"{pth}* ({len(ms)} files; hashes on Raw Files tab)")
        else: rf.append(f"{pth} sha256 {SHA.get(pth, 'NOT IN INVENTORY')}")
        if not ms: sys.exit(f"source raw path not in inventory: {pth}")
    vals = [s["dataset"], s["publisher"], s["landing"], s["link"], s["access"], s["vintage"], s["ptype"], citation(s), s["license"], "; ".join(rf) or "No raw file", s["receipt"], s.get("note", "")]
    for j, v in enumerate(vals, 1): ws.cell(i, j, v)
    link(ws.cell(i, 3), s["landing"]); link(ws.cell(i, 4), s["link"]); link(ws.cell(i, 11), "../data/receipts/" + s["receipt"])
for k, w in zip("ABCDEFGHIJKL", (46, 30, 44, 44, 13, 26, 24, 70, 34, 60, 15, 50)): ws.column_dimensions[k].width = w
ws.auto_filter.ref = f"A1:{L(len(sc))}{len(M.SOURCES) + 1}"

# ---- Validation ----
V = []
def vrow(section, check, tested, result, evidence, rating, date): V.append(dict(section=section, check=check, what_it_tested=tested, result=result, evidence=evidence, rating=rating, date=date))
S = pd.read_csv("logs/2026-11-02/build/validation/validation_summary.csv")
LATER = {"D23": "Corrected Nov 4: the claim was false. Government 518210 rows exist; see AI All Ownerships and EXPERIMENTS.md item 24.", "N05": "Corrected Nov 4: BEA's footnote says the gap reflects overseas activity, not territories. The check still passes.", "N06": "Audit Nov 4: 'no systematic error is possible' was an overclaim; audit cells for 2016, 2020 and 2022 match.", "N07": "Corrected Nov 4: differs from older Census vintages by up to 95,554. Matches the current series exactly: see cross-source section.", "N08": "Audit Nov 4: matching totals alone can't confirm a share; sampled shares for other states match.", "V02": "Corrected Nov 4: EIA labels 2025 final, not preliminary.", "V03": "Corrected Nov 4: BEA file footers read last updated Sept 30, 2026."}
for r in S.itertuples():
    rt = "green" if r.result == "PASS" else "yellow"
    note = str(r.note)
    if r.id.startswith("R01") or r.id in ("P01", "P08", "P09"): rt = "green"
    if r.id in ("N06", "N07", "N08"): rt = "green"
    if r.id == "P10": rt = "yellow"; note += ". Flag count, not an error: all 200 were reviewed in C.5 (solar and wind from a near-zero base; 5 AI fluctuations checked one by one). The Part C verdict has no reds"
    if r.id in LATER: note += ". " + LATER[r.id]
    vrow("Phase 2 Part C", f"{r.id}: {r.check}", str(r.category), r.result, note, rt, "2026-11-02" if r.id not in LATER else "2026-11-02; corrected 2026-11-04")
vrow("Phase 2 Part C", "C.1b full rebuild comparison", "build_panel.py rerun; every cell compared with the saved panel", "PASS", "43,758 cells compared (78 columns x 561 rows), zero differences. Rerun Nov 4 after the dc_wages_usd fix: only that column's 4 suppressed cells changed; see logs/2026-11-04/c1b_dc_wages_changes.csv", "green", "2026-11-02; rerun 2026-11-04")
for r in md_table(VAL, "## Verdict table"):
    vrow("Part C verdict by variable", strip(r["Variable"]), f"Definition {strip(r['Right definition'])}; numbers {strip(r['Numbers check'])}; reproduces {strip(r['Reproduces'])}", strip(r["Ready"]), strip(r["Note"]), strip(r["Ready"]), "2026-11-02")
for r in md_table(VAL, "## New data, Nov 4"):
    vrow("New data, Nov 4", strip(r["File"]), strip(r["Spot checks"]), strip(r["Rating"]), f"{strip(r['Units and coverage'])}. Caveat: {strip(r['Main caveat'])}", strip(r["Rating"]).split(",")[0].lower(), "2026-11-04")
for r in md_table(VAL, "### RPS coverage check"):
    vrow("New data, Nov 4", f"RPS: {strip(r['Check on the 327 nonzero state-years'])}", "LBNL schedule vs Target Achievement and older editions", strip(r["Rows"]) + " rows", "logs/2026-11-04/rps_vintage_check.csv; data/receipts/lbnl_rps.md", "yellow" if "Conflict" in r["Check on the 327 nonzero state-years"] or "Differs" in r["Check on the 327 nonzero state-years"] else "green", "2026-11-04")
for r in md_table(AUD, "## Result by variable"):
    rs = strip(r["Result"]); vrow("Audit, Nov 4", f"{strip(r['Variable'])}: {strip(r['Sampled cells'])} sampled cells", f"Agency site: {strip(r['Against agency site'])}; raw file: {strip(r['Against raw file'])}; code vs memo: {strip(r['Code vs memo and codebook'])}", rs, "data/INDEPENDENT_AUDIT_2026-11-04.md section 1", "green" if rs.startswith("Pass") else "yellow", "2026-11-04")
i0 = AUD.index("Variables outside the 30-cell sample");
for r in md_table(AUD[i0:], "Variables outside the 30-cell sample"):
    rs = strip(r["Result"]); vrow("Audit, Nov 4", strip(r["Variable"]), f"Code check only: {strip(r['Code vs memo and codebook'])}", rs, "data/INDEPENDENT_AUDIT_2026-11-04.md", "green" if rs.startswith("Pass") else "yellow", "2026-11-04")
for r in md_table(AUD, "### 2.3 `DATA_VALIDATION.md` claims"):
    vrow("Audit, Nov 4", f"Claim {strip(r['Item'])}", strip(r["Claim"]), "Didn't hold up; corrected", strip(r["What I found"]), "yellow", "2026-11-04")
AP = pd.read_csv(f"logs/2026-11-04/ai_postings_checks.csv")
for r in AP.itertuples(): vrow("Fang Part A", f"{r.year}: {r.check}", "AI Index postings by state", r.result, str(r.detail), "green" if r.result == "ok" else "yellow", "2026-11-04")
for r in md_table(VAL, "## Fang test data, Nov 4"):
    vrow("Fang Part A", strip(r["File"]), strip(r["Spot checks"]), strip(r["Rating"]), f"{strip(r['Units and coverage'])}. Caveat: {strip(r['Main caveat'])}", strip(r["Rating"]).lower(), "2026-11-04")
for r in pd.read_csv(f"logs/{DATE}/cross_source_checks.csv").itertuples(): vrow("Cross-source consistency", r.check, r.what_it_tested, r.result, r.evidence, r.rating, r.date)
vd = pd.DataFrame(V); ws = write_df("Validation", vd, widths=dict(A=24, B=48, C=56, D=16, E=80, F=12, G=14), freeze="C2")
for i, r in enumerate(vd.rating, 2):
    ws.cell(i, 6).fill = FILL.get(str(r).split(",")[0], FILL["grey"])
if (vd.rating == "red").any(): print("RED ROWS:", vd[vd.rating == "red"][["check", "result"]].to_string())

# ---- Limitations ----
ws = write_df("Limitations", pd.DataFrame(M.LIMITS, columns=["applies_to", "limitation", "how_it_affects_interpretation", "kind"]).sort_values("kind", kind="stable"), widths=dict(A=32, B=90, C=80, D=14), freeze="A2")
ws2 = ws
for row in ws.iter_rows(min_row=2):
    for c in row[:3]: c.alignment = Alignment(wrap_text=True, vertical="top")

# ---- Missing Data ----
YS = list(range(2015, 2026)); MR = []
for tab, f, *_ in CLEAN:
    d = DFS[tab]
    if "year" not in d.columns or "state" not in d.columns: continue
    dd = d[d.year.between(2015, 2025)]
    for v in dd.columns:
        m = dd[v].isna()
        if m.any():
            g = dd[m].groupby("year").size().reindex(YS).fillna(0).astype(int); present = sorted(dd.year.unique())
            rec = dict(tab=tab, variable=v, table_years=f"{present[0]}-{present[-1]}"); rec.update({str(y): int(g[y]) for y in YS}); rec.update(total_missing=int(m.sum()), states=",".join(dd[m].state.unique()) if dd[m].state.nunique() <= 8 else f"{dd[m].state.nunique()} areas", reason=gap_reason(tab, v)); MR.append(rec)
md = pd.DataFrame(MR)
for tab, f, *_ in CLEAN:
    d = DFS[tab]
    if "year" in d.columns and "state" in d.columns: continue
    for v in d.columns:
        m = d[v].isna()
        if m.any():
            rec = dict(tab=tab, variable=v, table_years="not a state-year table"); rec.update({str(y): None for y in YS}); rec.update(total_missing=int(m.sum()), states="", reason=gap_reason(tab, v) or "UNKNOWN"); MR.append(rec)
md = pd.DataFrame(MR)
if (md.reason == "UNKNOWN").any() or md.reason.isna().any(): sys.exit("Missing Data reason gap:\n" + md[md.reason.isna() | (md.reason == "UNKNOWN")][["tab", "variable"]].to_string())
extra = pd.DataFrame([dict(tab="not in workbook", variable=v, table_years="none", total_missing="all", states="", reason=w) for v, w in (("Large-load reports Q1-Q4 2024", "Pending: PSC document list returns 404 to scripts; browser download needed"),)])
md = pd.concat([md, extra], ignore_index=True); write_df("Missing Data", md, widths=dict(A=20, B=30, C=14, Q=70), freeze="C2")

# ---- Georgia ----
ws = wb.create_sheet("Georgia"); ws["A1"] = "Georgia case box. Blue = transcribed or copied from a source; black = computed here."; ws["A1"].font = BOLD; ws.freeze_panes = "A2"
GV = ["renew_share", "solar_share", "new_renew_mw", "ai_dc_per1000", "dc_jobs", "price_c_kwh", "sales_mwh_pc", "ln_gdp_pc", "co2_per_mwh_t", "gen_total_mwh"]
r = 3
def section(title, sub=""):
    global r
    ws.cell(r, 1, title).font = BOLD; r += 1
    if sub: ws.cell(r, 1, sub); r += 1
def table(df, blue=True):
    global r
    for j, c in enumerate(df.columns, 1):
        x = ws.cell(r, j, c); x.font = HDR; x.fill = HFILL; x.alignment = Alignment(wrap_text=True, vertical="center")
    r += 1
    for rec in df.itertuples(index=False):
        for j, v in enumerate(rec, 1):
            x = ws.cell(r, j, clean(v)); x.font = BLUE if blue else BODY
        r += 1
    r += 2
ga = p[p.state == "GA"].set_index("year"); us = p[p.state != "DC"].groupby("year")[GV].median()
t = pd.DataFrame({"year": YS})
for v in GV:
    t[f"{v} GA"] = ga[v].reindex(YS).values; t[f"{v} U.S. median"] = us[v].reindex(YS).values
section("1. Georgia next to the U.S. median (median of the 50 states, DC excluded; Full Panel values)"); table(t, blue=False)
t2 = pd.read_csv("data/georgia_large_load_table2.csv")
section("2. Large-load pipeline: Q2 2026 report, Table 2 (approximate MW)", "Georgia Power, filed Aug 17, 2026. Document, PDF page and table in the columns. The large-load row prints +6,900 for Q2 vs Q1 where its rounded levels differ by 7,000. Q1-Q4 2024 reports are PENDING: https://psc.ga.gov/search/facts-docket/?docketId=55378"); table(t2)
section("3. Large-load attachment by stage and segment", "Project names, cities, counties and GPS are redacted by the company. Check: committed projects = 31 (Q1) and 32 (Q2), and committed announced load = 12,357 and 15,567 MW, in line with the reports' 12,400 and 15,600."); table(pd.read_csv("data/georgia_large_load_attachment.csv"))
section("4. Cited figures from the IRP and large-load reports", "Each figure's text was found on the cited PDF page by code/python/build_georgia_tables.py. PDF page is the page in the file, not the printed number. Docket: cite 56002 for the 2025 IRP (main document is an SELC-hosted copy), 55378 for the 2023 IRP Update."); table(pd.read_csv("data/georgia_filing_figures.csv"))
section("5. Epoch AI sites in Georgia (latest timeline row; context only, not a model variable)"); table(pd.read_csv("data/georgia_epoch_sites.csv"))
for j in range(1, 24): ws.column_dimensions[L(j)].width = 15
GEO_ROWS = r

# ---- Raw Files ----
RCPT = {"noaa": "noaa.md", "acs": "acs.md", "aiindex": "ai_index.md", "bea": "bea.md", "bls": "bls_qcew.md", "census": "census.md", "census_pop": "census_pop.md", "costs": "lazard.md", "eia_forms": "eia_forms.md", "epoch": "epoch.md", "epu": "epu.md", "georgia": "georgia_psc.md", "ncses": "ncses.md", "nsf": "nsf.md", "owid": "owid.md", "pudl": "ferc_pudl.md", "rmi": "rmi.md"}
CLEANED = {"noaa": "NOAA Degree Days", "acs": "ACS Broadband", "aiindex": "AI Job Postings", "ncses": "NCSES Bachelors", "nsf": "NSF State RD", "pudl": "FERC1 tabs"}
agg = {}
for s in shapes.itertuples():
    rc = f"{int(s.rows):,} x {int(s.cols)}" if pd.notna(s.rows) and pd.notna(s.cols) else (f"{int(s.rows):,} records" if pd.notna(s.rows) else "")
    agg.setdefault(s.path, []).append((s.table if isinstance(s.table, str) else "", rc, s.kind, s.rows if pd.notna(s.rows) else 0))
RF = []
for r0 in inv.to_dict("records"):
    pth = r0["path"]; top = pth.split("/")[2]; a = agg.get(pth, [("", "", "", 0)])
    if len(a) == 1: dims = a[0][1] or (str(a[0][2]) if str(a[0][2]) not in ("nan",) else "")
    else:
        big = max(a, key=lambda z: z[3]); dims = f"{len(a)} sheets; largest {big[0]}: {big[1]}"
    rcpt = "eia_seds.md" if pth.endswith("use_all_btu.csv") else "seds_fang.md" if pth.startswith("data/raw/eia/seds/") else "eia_state.md" if top == "eia" else "lbnl_solar.md" if "Utility Scale Solar" in pth else "lbnl_rps.md" if top == "lbnl" else RCPT.get(top, "README.md")
    b = os.path.basename(pth)
    if b.startswith("._"): where = "Not data"
    elif pth in RAWMAP: where = f"Whole: tab {RAWMAP[pth]}"
    elif b.lower().endswith(".pdf"): where = "Not a table: pointer only" if top != "georgia" else "Figures cited on the Georgia tab; PDF not copied"
    elif top == "georgia": where = "Summarized on the Georgia tab"
    elif top == "lbnl": where = "Cleaned table whole: RPS Targets" if "Solar" not in pth else "Cleaned table whole: LBNL Solar Projects"
    elif top in CLEANED: where = f"Summarized: Raw Table Summary; cleaned table whole: {CLEANED[top]}"
    else: where = "Summarized: Raw Table Summary"
    RF.append(dict(path=pth, size_bytes=r0["size"], sha256=r0["sha256"], source=r0["what_it_is"], rows_x_columns=dims, in_workbook=where, receipt=rcpt, disposition=r0["disposition"]))
rfd = pd.DataFrame(RF); ws = write_df("Raw Files", rfd, widths=dict(A=62, B=12, C=66, D=44, E=32, F=44, G=16, H=36), freeze="B2")

# ---- Raw Table Summary ----
def dims(prefix, pat=None):
    d = shapes[shapes.path.str.startswith(prefix)]
    if pat: d = d[d.path.str.contains(pat, regex=True)]
    return int(d.path.nunique()), int(d.rows.fillna(0).sum()), (int(d.cols.max()) if d.cols.notna().any() else None)
def collist(path, n=14):
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq; c = pq.read_schema(path).names
    else:
        with open(path, encoding="latin1", newline="") as fh: c = next(csv.reader(fh))
    return ", ".join(c[:n]) + (f", +{len(c) - n} more" if len(c) > n else "")
RS = []
def rs(table, path, why, years, kept, cols="", pat=None, where=""):
    nf, nr, nc = dims(path, pat); RS.append(dict(table=table, path=path + (f" ({pat})" if pat else ""), files=nf, total_rows=nr, max_columns=nc, columns=cols, years=years, what_we_kept=kept, cleaned_in=where, why_summarized=why))
BIGN = "Over the 200,000-row limit"
rs("BEA SAGDP files", "data/raw/bea/sagdp/", "1,000+ per-state and per-table files; a tab each isn't usable. The all-area tables the panel uses are whole on Raw BEA SAGDP2 and SAGDP9", "1997-2025", "Lines 1, 4, 12 of SAGDP2; line 1 of SAGDP9", "GeoFIPS, GeoName, Region, TableName, LineCode, IndustryClassification, Description, Unit, year columns", where="Full Panel")
rs("BEA SAINC files", "data/raw/bea/sainc/", "Per-state and per-table files. The all-area SAINC1 is whole on Raw BEA SAINC1", "1929-2025", "SAINC1 lines 2 and 3 (population, per capita income)", "GeoFIPS, GeoName, Region, TableName, LineCode, IndustryClassification, Description, Unit, year columns", where="Full Panel; Fang Split Vars")
for code_, name, kept in (("518210", "QCEW NAICS 518210 by year", "State rows: private (own 5), plus government rows for the check"), ("5415", "QCEW NAICS 5415 by year", "State rows, private"), ("10", "QCEW all industries by year", "State rows, total covered (own 0)")):
    rs(name, "data/raw/bls/", "County-level raw files; summarized as the size rule directs", "2014-2025", kept, collist(f"data/raw/bls/qcew_2025_{code_}.csv"), pat=f"_{code_}\\.csv$", where="Full Panel; AI All Ownerships")
rs("Form EIA-860, 2025", "data/raw/eia_forms/eia8602025", "Plant-level zip; summarized as the size rule directs", "2025", "Nothing; reference only", where="Not used")
rs("Form EIA-860, 2017", "data/raw/eia_forms/eia8602017", "Plant-level zip", "2017", "Only to identify the NE and NM 2017 blank-fuel capacity rows", where="Not used")
rs("Form EIA-860M, Sept 2026", "data/raw/eia_forms/september_generator2026", "Generator-level file", "Sept 2026", "Nothing; reference only", where="Not used")
rs("Form EIA-861, 2025", "data/raw/eia_forms/f8612025", "Utility-level zip", "2025", "Nothing; reference only", where="Not used")
rs("Form EIA-923, 2025", "data/raw/eia_forms/f923_2025", "Plant-level zip; summarized as the size rule directs", "2025", "Nothing; reference only", where="Not used")
for f_, kept in (("out_ferc1__yearly_income_statements_sched114", "Electric income lines by utility and year"), ("out_ferc1__yearly_plant_in_service_sched204", "Plant in service by type"), ("out_ferc1__yearly_all_plants", "Plant-level capacity, generation and cost"), ("out_ferc1__yearly_steam_plants_fuel_by_plant_sched402", "Fuel cost for steam plants"), ("out_eia__yearly_utilities", "Utility HQ state and entity type")):
    rs(f"PUDL {f_}", f"data/raw/pudl/{f_}", "Full PUDL table; summarized as the size rule directs", "Through 2025", kept, collist(f"data/raw/pudl/{f_}.parquet"), where="FERC1 tabs")
for f_ in ("operations_emissions", "operations_emissions_by_tech", "assets_earnings_investments", "expenditure_bills_burden"):
    rs(f"RMI {f_}", f"data/raw/rmi/{f_}.csv", BIGN, "See file", "Nothing; not in any result", collist(f"data/raw/rmi/{f_}.csv"), where="Not used")
rs("Census intercensal population", "data/raw/census_pop/sc-est2020int", BIGN, "2010-2020", "POPESTIMATE2015-2019 totals, for the BEA check only", collist("data/raw/census_pop/sc-est2020int-alldata6.csv"), where="Validation")
rs("NSF Table 10, editions", "data/raw/nsf/", "One small file per edition; every kept value is in the cleaned tab", "2017-2023", "One data year per edition", where="NSF State RD")
rs("ACS S2801 API responses", "data/raw/acs/", "One JSON per year; every kept value is in the cleaned tab", "2015-2024", "Broadband percent, MOE, households", where="ACS Broadband")
rs("NOAA degree-day files", "data/raw/noaa/", "One small file per state and measure, plus two nClimDiv files used as a check; every kept value is in the cleaned tab", "2015-2025", "Annual HDD and CDD, 48 states", where="NOAA Degree Days")
rs("NCSES API responses", "data/raw/ncses/", "JSON; every kept value is in the cleaned tab", "2000-2024", "2015-2024 by state", where="NCSES Bachelors")
rs("AI Index sheets, CSVs and PDFs", "data/raw/aiindex/", "One small file per figure and edition; every kept value is in the cleaned tab, with edition, figure and page", "2018-2025", "State postings and shares", where="AI Job Postings")
rs("LBNL RPS and CES files", "data/raw/lbnl/", "Wide multi-sheet workbooks; cleaned table holds what was kept", "2000-2050", "Total RPS and Total CES rows for 2015-2025, and target achievement", pat="RPS|rps", where="RPS Targets")
rs("LBNL Utility-Scale Solar", "data/raw/lbnl/", "One project table, whole in the cleaned tab", "Through 2025", "Project table", pat="Solar", where="LBNL Solar Projects")
rs("Georgia large-load attachments", "data/raw/georgia/", "Attachment rows are mostly redacted; summarized by stage and segment", "Q1, Q2 2026", "Stage, segment, announced load", pat="xlsx|zip", where="Georgia")
rs("Not raw tables: PDFs", "data/raw/costs/", "PDF. Lazard is pointed to, not copied", "July 2026", "Nothing copied", where="Not copied")
rsd = pd.DataFrame(RS); write_df("Raw Table Summary", rsd, widths=dict(A=40, B=46, F=60, H=46, I=26, J=60), freeze="B2")

# ---- Changelog ----
write_df("Changelog", pd.DataFrame(M.CHANGELOG, columns=["build_date", "file", "what_changed"]), widths=dict(A=12, B=52, C=130), freeze="A2")

# ---- README ----
ws = wb.create_sheet("README")
ORDER = ["README", "Variable Finder", "Core Panel", "Full Panel", "Fang Panel", "Georgia", "Validation", "Limitations", "Missing Data", "Sources", "Raw Files", "Raw Table Summary", "Changelog"] + [t for t, *_ in CLEAN if t not in ("Full Panel", "Fang Panel")] + ["W Inverse Distance", "W Border", "W Distance Miles"] + [t for t, *_ in RAWTABS]
DESC = {"Variable Finder": "Start here. Every variable in every tab, with links to its tab and column, source and receipt; rating and status colored. Comes from data/variable_registry.csv.", "Core Panel": "50 states + DC, 2015-2025. The memo variables. Blue = downloaded values; black = formulas you can audit. Includes sample flags.", "Full Panel": "Same rows, all 80 built variables. Values only. Same as data/out/state_panel_2015_2025.csv.", "Fang Panel": "Fang's variables, with AI postings and their edition and vendor. Same as data/fang_panel.csv.", "Georgia": "Georgia next to the U.S. median; large-load table; IRP figures with document and page; Epoch's Georgia sites.", "Validation": "Every check: Part C, Nov 4 new data, Nov 4 audit, Fang Part A, cross-source.", "Limitations": "Per variable and overall, with how each affects interpretation.", "Missing Data": "Variable x year, with the reason for each gap.", "Sources": "Every source: links, dates, citation, license note, raw files with hashes, receipt.", "Raw Files": "One row per file in data/raw/: size, sha256, shape, and whether it's here whole or summarized.", "Raw Table Summary": "Raw tables that aren't here whole: columns, rows, years, what we kept, path, why.", "Changelog": "What changed in each build."}
for t, *_ in CLEAN: DESC.setdefault(t, f"Cleaned table, whole. Same as {_[0]}.")
for t in ("W Inverse Distance", "W Border", "W Distance Miles"): DESC[t] = "Spatial matrix, whole, from data/out/."
for t, f, sh, key, used in RAWTABS: DESC[t] = f"Raw table, whole, exactly as in {f}{' (sheet: ' + sh + ')' if isinstance(sh, str) and sh not in ('tab', 'pipe') else ''}. {used}."
lines_ = [("ECON 499R master data workbook: U.S. state panel, Fang test data, Georgia case box, finance tables", TITLE), (f"As of {DATE}. Shunji Lewandowski and Alexander Hendricks, Prof. Fohlin, Emory University.", BODY), ("", BODY),
 ("What this is", BOLD), ("One workbook with all our cleaned data, showing where every variable came from, how it was checked and what limits it. Model results aren't here: see results/ and results/2026-11-04/paper/ (the results pack). The old Prelim Results tab stays in outputs/old/.", BODY), ("Read the Limitations tab before using any number.", BOLD), ("", BODY),
 ("How to rebuild", BOLD), (f"From the project root, after any data change: python3 code/python/build_cross_source_checks.py --date {DATE}; python3 code/python/build_raw_file_shapes.py --date {DATE}; python3 code/python/build_georgia_tables.py --date {DATE}; python3 code/python/build_master_workbook.py --date {DATE}; python3 code/python/check_master_workbook.py --date {DATE}", BODY), ("Panel: python3 econ499r_starter/scripts/build_panel.py data/raw data/out. Receipt links are relative: they work from outputs/ in the project, and from outputs/ in the results package.", BODY), ("", BODY),
 ("Pending or not available", BOLD), ("Pending: Georgia large-load reports Q1-Q4 2024 (browser download from https://psc.ga.gov/search/facts-docket/?docketId=55378 ; the PSC list returns 404 to scripts).", BODY), ("Not run: Fang's extreme weather split, which counts occurrences; NOAA degree days are in, for one check only (48 states).", BODY), ("Optional, not run: SEC company facts refresh. No raw copy of SEC data, so no hash.", BODY), ("Not in this workbook, by rule: licensed Bloomberg data, interview transcripts, keys and personal emails. The Lazard PDF and journal PDFs are pointed to, not copied.", BODY), ("", BODY),
 ("Size rule", BOLD), ("Every cleaned dataset is whole. Raw tables go in whole if they're under about 200,000 rows, except: county-level QCEW, EIA-860/923 and full PUDL tables, as the rule directs; and folders of many small files (BEA, NSF, ACS, NCSES, AI Index) whose kept values are whole in a cleaned tab. Those are on Raw Table Summary.", BODY), ("", BODY),
 ("Colors", BOLD), ("Blue = downloaded or transcribed inputs on Core Panel, Fang Panel and Georgia. Black = formulas or computed values. Other data tabs are plain copies in black, as in earlier builds. Green, yellow and red are validation ratings.", BODY), ("", BODY), ("Tabs", BOLD)]
for i, (t, f) in enumerate(lines_, 1):
    c = ws.cell(i, 1, t); c.font = f; c.alignment = Alignment(wrap_text=True, vertical="top")
i = len(lines_) + 1
for t in ORDER[1:]:
    c = ws.cell(i, 1, t); link(c, f"#'{t}'!A1"); ws.cell(i, 2, DESC[t]); i += 1
ws.column_dimensions["A"].width = 150 if False else 30; ws.column_dimensions["B"].width = 130
for j in range(1, len(lines_) + 1):
    ws.merge_cells(start_row=j, start_column=1, end_row=j, end_column=2)
    ln = len(str(lines_[j - 1][0])); ws.row_dimensions[j].height = max(14, 14 * (ln // 145 + 1)) if j > 1 else 20
wb._sheets = [wb[t] for t in ORDER]
for s in wb.worksheets: s.sheet_view.zoomScale = 90
os.makedirs(os.path.dirname(XL), exist_ok=True); wb.save(XL); print("saved", XL, round(os.path.getsize(XL) / 1e6, 1), "MB;", len(wb.sheetnames), "tabs; validation", len(vd), vd.rating.value_counts().to_dict())
pd.DataFrame({"tab": ORDER}).to_csv(f"logs/{DATE}/master_workbook_tabs.csv", index=False)

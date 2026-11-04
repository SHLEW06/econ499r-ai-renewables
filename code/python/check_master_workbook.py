#!/usr/bin/env python3
"""Recalculate the master workbook with LibreOffice, check it, and install the recalculated copy. Read-only for data.
Usage: python3 code/python/check_master_workbook.py --date YYYY-MM-DD [--skip-urls]"""
import argparse, csv, os, random, re, shutil, subprocess, sys, tempfile, time, urllib.request, ssl
import numpy as np, pandas as pd, openpyxl
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--skip-urls", action="store_true"); ap.add_argument("--tmp", default=None); a = ap.parse_args()
XL = f"outputs/ECON499R_Master_Data_{a.date}.xlsx"; T = a.tmp or tempfile.mkdtemp(); CH = []
def chk(name, ok, ev, rating=None): CH.append(dict(check=name, result="ok" if ok else "PROBLEM", evidence=ev)); print(("ok      " if ok else "PROBLEM ") + name + ": " + str(ev)[:300], flush=True)
t0 = time.time(); subprocess.run([shutil.which("soffice") or sys.exit("soffice not found"), "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", T, XL], check=True, capture_output=True, timeout=1500)
RC = os.path.join(T, os.path.basename(XL)); print("recalculated in", int(time.time() - t0), "s", round(os.path.getsize(RC) / 1e6, 1), "MB", flush=True)
wb = openpyxl.load_workbook(RC, data_only=True); wf = openpyxl.load_workbook(XL)  # wf: pre-recalc, for what was intended
# ---- formula errors, emails, key ----
ERR = {"#DIV/0!", "#N/A", "#NAME?", "#NULL!", "#NUM!", "#REF!", "#VALUE!"}; err = []; em = []; EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
key = None
if os.path.exists(".env"):
    for ln in open(".env"):
        if ln.startswith("CENSUS_KEY="): key = ln.split("=", 1)[1].strip().strip('"')
keyhit = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str):
                if v in ERR: err.append(f"{ws.title}!{c.coordinate}")
                if "@" in v and EM.search(v): em.append(f"{ws.title}!{c.coordinate}: {EM.search(v).group(0)}")
                if key and key in v: keyhit += 1
chk("Zero formula errors after recalculation", not err, f"{len(err)} error cells {err[:6]}")
chk("No Census key in any cell", keyhit == 0, f"{keyhit} cells; key checked without printing")
chk("No email addresses in any cell", not em, f"{len(em)} cells {em[:8]}")
# ---- recalculated Core Panel equals the panel ----
p = pd.read_csv("data/out/state_panel_2015_2025.csv").sort_values(["state", "year"]).reset_index(drop=True)
ws = wb["Core Panel"]; head = [c.value for c in ws[1]]; idx = {h: j for j, h in enumerate(head)}
rows = [[c.value for c in r] for r in ws.iter_rows(min_row=2, max_row=len(p) + 1)]; cd = pd.DataFrame(rows, columns=head).replace("", np.nan)
map_ = {"sales_mwh_pc": "sales_mwh_pc", "ln_ec": "ln_ec", "ee_usd_per_mwh": "ee_usd_per_mwh", "ln_ee": "ln_ee", "renew_share": "renew_share", "solar_share": "solar_share", "fossil_to_renew": "fossil_to_renew", "ai_dc_per1000": "ai_dc_per1000", "tech_share": "tech_share", "price_c_kwh": "price_c_kwh", "ln_gdp_pc": "ln_gdp_pc", "manuf_share": "manuf_share", "ea_nonfarm_gdp_per_sqmi": "ea_nonfarm_gdp_per_sqmi", "ln_ea": "ln_ea", "pop_growth": "pop_growth", "wind_share": "wind_share", "co2_per_mwh": "co2_per_mwh_t", "new_renew_mw": "new_renew_mw", "energy_equity": "energy_equity"}
bad = {}
for x, y in map_.items():
    a1 = pd.to_numeric(cd[x], errors="coerce").values; b1 = pd.to_numeric(p[y], errors="coerce").values
    nanbad = int((np.isnan(a1) != np.isnan(b1)).sum()); rel = np.nanmax(np.abs(a1 - b1) / np.maximum(1e-9, np.maximum(np.abs(b1), 1e-3)))
    if nanbad or rel > 1e-6: bad[x] = (nanbad, float(rel))
chk("Core Panel formulas equal the panel, every row", not bad, f"{len(map_)} formula columns x {len(p)} rows; differences: {bad}")
ne = p[p.year == 2015].assign(x=lambda d: (d.gen_total_mwh > d.sales_mwh).astype(int)).set_index("state").x; v = cd.net_exporter_2015.astype(float).values == cd.state.map(ne).values
chk("net_exporter_2015 is fixed per state and matches the 2015 rule", v.all(), f"{int(ne.sum())} net exporters; {int((~v).sum())} rows differ")
chk("Sample flags", cd.in_zhang_sample.sum() == 550 and cd.in_fang_sample.sum() == 204, f"in_zhang_sample {cd.in_zhang_sample.sum()} of 561 (DC excluded); in_fang_sample {cd.in_fang_sample.sum()} (N = 204)")
# ---- row counts ----
import ast
src = open("code/python/build_master_workbook.py").read()
CLEAN = re.findall(r'\("([^"]+)", "(data/[^"]+\.csv)", (?:None|\[[^\]]*\]|M\.SOURCE_KEYS_AI), "', src)
RAWT = re.findall(r'\("(Raw [^"]+)", "(data/raw/[^"]+)", ([^,]+), "', src)
def read_raw(f, sh):
    if f.endswith(".xlsx"):
        d = pd.read_excel(f, sheet_name=(0 if sh == "0" else sh.strip('"')), header=None, dtype=object); return d.values.tolist()
    dl = {'"tab"': "\t", '"pipe"': "|"}.get(sh, ",")
    for enc in ("utf-8-sig", "latin1"):
        try:
            with open(f, encoding=enc, newline="") as fh: return [r for r in csv.reader(fh, delimiter=dl)]
        except UnicodeDecodeError: continue
SRC = {}; bad = []
for tab, f in CLEAN:
    d = pd.read_csv(f); SRC[tab] = d; n = wb[tab].max_row - 1
    if n != len(d) or wb[tab].max_column != d.shape[1]: bad.append((tab, n, len(d), wb[tab].max_column, d.shape[1]))
for tab, f in (("W Inverse Distance", "data/out/W_inverse_distance_rowstd.csv"), ("W Border", "data/out/W_border_binary.csv"), ("W Distance Miles", "data/out/W_distance_miles.csv")):
    d = pd.read_csv(f); SRC[tab] = d
    if wb[tab].max_row - 1 != len(d): bad.append((tab, wb[tab].max_row - 1, len(d)))
RR = {}
for tab, f, sh in RAWT:
    r = read_raw(f, sh); RR[tab] = r; n = len(r)
    while n and all((x is None or x == "" or (isinstance(x, float) and np.isnan(x))) for x in r[n - 1]): n -= 1  # LibreOffice drops trailing blank rows
    if wb[tab].max_row != n: bad.append((tab, wb[tab].max_row, n))
if wb["Full Panel"].max_row != 562 or wb["Core Panel"].max_row != 562: bad.append("panel rows")
chk("Every tab's row count matches its source", not bad, f"{len(CLEAN) + 3 + len(RAWT)} data tabs checked; mismatches {bad}")
# ---- 30 random cells, seed 2026 ----
rng = random.Random(2026); res = []
tabs = [t for t, _ in CLEAN] + [t for t, *_ in RAWT]
def same(x, y):
    if x in (None, "") and (y in (None, "") or (isinstance(y, float) and np.isnan(y))): return True
    try: return abs(float(x) - float(y)) <= 1e-9 * max(1, abs(float(y)))
    except (TypeError, ValueError): return str(x).strip() == str(y).strip()
while len(res) < 30:
    t = rng.choice(tabs); ws = wb[t]
    if t in SRC:
        d = SRC[t]; i = rng.randrange(len(d)); j = rng.randrange(d.shape[1]); s = d.iloc[i, j]; x = ws.cell(i + 2, j + 1).value
    else:
        r = RR[t]; i = rng.randrange(len(r)); 
        if not r[i]: continue
        j = rng.randrange(len(r[i])); s = r[i][j]; x = ws.cell(i + 1, j + 1).value
    if isinstance(s, (pd.Timestamp,)) or hasattr(s, "year"): s = str(s); x = str(x)
    if isinstance(s, str): s = s.strip()
    res.append(dict(tab=t, cell=f"{L(j + 1)}{(i + 2) if t in SRC else (i + 1)}", workbook=x, source=s if not isinstance(s, np.generic) else s.item(), match=same(x, s)))
rd = pd.DataFrame(res); rd.to_csv(f"logs/{a.date}/master_workbook_30cells.csv", index=False)
chk("30 random cells (seed 2026) match their source files", rd.match.all(), f"{int(rd.match.sum())} of 30 match; {rd.tab.nunique()} tabs; logs/{a.date}/master_workbook_30cells.csv. Misses: {rd[~rd.match].to_dict('records')[:4]}")
# ---- registry to finder to real tab and column ----
reg = pd.read_csv(f"data/variable_registry.csv", keep_default_na=False)
vf = wb["Variable Finder"]; names = [(vf.cell(i, 1).value, vf.cell(i, 2).value, vf.cell(i, 3).value) for i in range(2, vf.max_row + 1)]
miss = []; wrong = []
for i, r in enumerate(reg.to_dict("records"), 2):
    if (str(names[i - 2][0]), str(names[i - 2][1])) != (str(r["variable"]), str(r["tab"])): miss.append(r["variable"])
    if r["tab"] == "none": continue
    if r["tab"] not in wb.sheetnames: wrong.append((r["variable"], r["tab"])); continue
    ws = wb[r["tab"]]; c0 = CI(str(r["column"]).split(":")[0])
    if r["tab"] == "Georgia" or r["tab"].startswith("W "): continue
    hdrrow = 1
    if r["tab"].startswith("Raw "):  # header row from the frozen pane
        hdrrow = ws.freeze_panes and int(re.sub(r"\D", "", ws.freeze_panes)) - 1 or 1
    h = ws.cell(hdrrow, c0).value; hs = re.sub(r"\s+", " ", str(h if h is not None else ""))
    v = str(r["variable"])
    if not (hs == v or v.startswith(hs + "-") or v.startswith("(column")): wrong.append((v, r["tab"], r["column"], hs))
lk = sum(1 for i in range(2, vf.max_row + 1) if vf.cell(i, 2).hyperlink is not None)
chk("Every registry variable is in the Variable Finder", not miss, f"{len(reg)} registry rows; missing {miss[:5]}")
chk("Every Finder row links to a real tab and column", not wrong and lk >= (reg.tab != "none").sum(), f"{lk} internal links survive recalculation; header mismatches {wrong[:6]}. Rows with tab 'none' are Pending or Not available: {list(reg[reg.tab == 'none'].variable)}")
# ---- formatting survives ----
ORDER = pd.read_csv(f"logs/{a.date}/master_workbook_tabs.csv").tab.tolist(); nofz = [s.title for s in wb.worksheets if s.title not in ("README",) and not s.freeze_panes]; nofl = [s.title for s in wb.worksheets if s.title not in ("README", "Georgia") and not s.auto_filter.ref]
wrongf = [s.title for s in wb.worksheets if s.title != "README" and (s.cell(1, 1).font.name != "Arial")]
cp = openpyxl.load_workbook(RC)["Core Panel"]; nform = sum(1 for r in cp.iter_rows(min_row=2) for c in r if c.data_type == "f"); blu = cp["C2"].font.color.rgb if cp["C2"].font.color else None
chk("Tabs, frozen headers, filters and Arial survive recalculation", wb.sheetnames == ORDER and not nofz and not nofl and not wrongf, f"{len(wb.sheetnames)} tabs in order; no freeze {nofz}; no filter {nofl}; not Arial {wrongf}")
chk("Live formulas and blue inputs survive", nform > 12000 and str(blu).endswith("0000FF"), f"{nform} live formulas on Core Panel; input color {blu}")
src_ws = wb["Sources"]; lks = sum(1 for r in src_ws.iter_rows(min_row=2, min_col=3, max_col=4) for c in r if c.hyperlink is not None)
chk("Sources: URLs are clickable and the filter covers all rows", lks == 2 * (src_ws.max_row - 1) and src_ws.auto_filter.ref.endswith(str(src_ws.max_row)), f"{lks} links; {src_ws.max_row - 1} sources; filter {src_ws.auto_filter.ref}")
# ---- receipts exist ----
nor = [r for r in reg.receipt.unique() if r and not os.path.exists("data/receipts/" + r)]
chk("Every receipt link points to a real file", not nor, f"{reg.receipt.nunique()} receipts; missing {nor}")
# ---- URLs ----
if not a.skip_urls:
    urls = []
    for i in range(2, src_ws.max_row + 1):
        for j in (3, 4):
            u = src_ws.cell(i, j).value
            if u and u not in urls: urls.append(u)
    ctx = ssl.create_default_context(); out = []
    for u in urls:
        st = None; why = ""
        for m in ("HEAD", "GET"):
            try:
                rq = urllib.request.Request(u, method=m, headers={"User-Agent": "Mozilla/5.0 (research data check)", "Range": "bytes=0-1023"} if m == "GET" else {"User-Agent": "Mozilla/5.0 (research data check)"})
                with urllib.request.urlopen(rq, timeout=25, context=ctx) as x: st = x.status
                break
            except urllib.error.HTTPError as e: st = e.code; why = str(e.reason)
            except Exception as e: st = None; why = type(e).__name__
        out.append(dict(url=u, status=st, note=why, kind="ok" if st and st < 400 else ("blocked to scripts" if st in (401, 403, 405, 406, 429, 503) else "CHECK")))
        print(st, u[:90], flush=True)
    ud = pd.DataFrame(out); ud.to_csv(f"logs/{a.date}/master_workbook_urls.csv", index=False)
    chk("URLs open (read-only)", not (ud.kind == "CHECK").any(), f"{len(ud)} URLs; {ud.kind.value_counts().to_dict()}; problems {ud[ud.kind == 'CHECK'][['url', 'status', 'note']].to_dict('records')}")
# ---- install ----
sz = os.path.getsize(RC)
if not [c for c in CH if c["result"] == "PROBLEM" and "URL" not in c["check"]]:
    shutil.copy(RC, XL); chk("Recalculated copy installed", True, f"{XL}, {sz / 1e6:.1f} MB")
else: print("NOT installed: problems above. Recalculated copy at", RC)
pd.DataFrame(CH).to_csv(f"logs/{a.date}/master_workbook_checks.csv", index=False)

#!/usr/bin/env python3
"""Georgia case-box tables for the master workbook, parsed from the raw filings (read-only). Every cited figure must appear on its cited PDF page.
Usage: python3 code/python/build_georgia_tables.py --date YYYY-MM-DD"""
import argparse, io, os, re, subprocess, sys, tempfile, zipfile
import numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); a = ap.parse_args()
G = "data/raw/georgia"; Z = f"{G}/dkt55378_large_load_report_q2_2026.zip"
Q1PDF = f"{G}/LargeLoad_Report_Q1_2026.pdf"; Q1X = f"{G}/dkt55378_large_load_report_q1_2026_attachment.xlsx"; IRP = f"{G}/2025_IRP_Main_Document.pdf"; ONE = f"{G}/2025_IRP_one_page_summary.pdf"
def pages(f): return subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True, check=True).stdout.split("\f")
tmp = tempfile.mkdtemp(); zipfile.ZipFile(Z).extractall(tmp)
find = lambda ext, pat: next(os.path.join(r, f) for r, _, fs in os.walk(tmp) for f in fs if f.endswith(ext) and pat in f)
Q2PDF = find(".pdf", "Lg Load"); Q2X = find(".xlsx", "Large Load"); ZN = "dkt55378_large_load_report_q2_2026.zip > " + os.path.basename(Q2PDF)
q1, q2, irp, one = pages(Q1PDF), pages(Q2PDF), pages(IRP), pages(ONE)
# ---- Table 2, Q2 2026 report, PDF p. 8 ----
cols = ["ifiling_2028_29", "ifiling_mid2030s", "q1_2026_2028_29", "q1_2026_mid2030s", "q2_2026_2028_29", "q2_2026_mid2030s", "q2_vs_q1_2028_29", "q2_vs_q1_mid2030s", "q2_vs_filing_2028_29", "q2_vs_filing_mid2030s"]
lab = {"Total Pipeline": "Total pipeline", "Pipeline": "Large load pipeline", "Commitments": "Commitments", "Broken Ground": "Broken ground"}
L = q2[7].split("\n"); rows = []
for ln in L:
    m = re.match(r"\s*(Total Pipeline|Commitments|Broken Ground|)\s*(-?\d.*)$", ln)  # the large-load row prints its label on the lines around its numbers
    if m:
        v = [int(x.replace(",", "")) for x in re.findall(r"-?\d[\d,]*", m.group(2))]
        if len(v) == 10: rows.append(dict(row=lab[m.group(1) or "Pipeline"], **dict(zip(cols, v)), unit="approximate MW", document=ZN, pdf_page=8, report_page=4, table="Table 2. Summary of Pipeline Changes"))
t2 = pd.DataFrame(rows)
if len(t2) != 4: sys.exit(f"Table 2 parse: {len(t2)} rows")
for r in t2.itertuples():  # published differences hold within rounding: levels are approximate (large-load row prints +6,900 where the levels differ by 7,000)
    if abs(r.q2_2026_mid2030s - r.q1_2026_mid2030s - r.q2_vs_q1_mid2030s) > 100 or abs(r.q2_2026_mid2030s - r.ifiling_mid2030s - r.q2_vs_filing_mid2030s) > 100: sys.exit(f"Table 2 arithmetic {r.row}")
t2.to_csv("data/georgia_large_load_table2.csv", index=False)
# ---- cited figures, each checked against the page text ----
F = [("Commitments, June 30, 2026", "15,600 MW across 32 customers", "reaching a total of 15,600 MW", ZN, q2, 5), ("Commitments by winter 2028/2029, Q2 2026", "8,700 MW", "load of 8,700 MW", ZN, q2, 5), ("Broken ground, Q2 2026", "8,500 MW of 15,600 MW", "8,500 MW out of 15,600 MW", ZN, q2, 5),
     ("Projects broken ground / pending, Q2 2026", "21 / 11 of 32", "Twenty-one of these projects have broken", ZN, q2, 7), ("Total pipeline, Q2 2026", "84,800 MW", "84,800 MW", ZN, q2, 8),
     ("Commitments, March 31, 2026", "12,400 MW across 31 customers", "reaching a total of 12,400 MW", "LargeLoad_Report_Q1_2026.pdf", q1, 5), ("Commitments by winter 2028/2029, Q1 2026", "7,800 MW", "load of 7,800 MW", "LargeLoad_Report_Q1_2026.pdf", q1, 5),
     ("Total pipeline, Q1 2026", "76,200 MW; 73,100 MW large load", "73,100 MW", "LargeLoad_Report_Q1_2026.pdf", q1, 5), ("Commitments added in April 2026, after the Q1 cutoff", "3,200 MW", "commitments added totaling 3,200 MW", "LargeLoad_Report_Q1_2026.pdf", q1, 5),
     ("Commitments at the 2023 IRP Update, Oct 2023", "3,600 MW", "from 3,600 MW to 12,400 MW", "LargeLoad_Report_Q1_2026.pdf", q1, 8), ("Pipeline at the 2023 IRP Update, Oct 2023", "about 17,000 MW", "approximately 17,000 MW", "LargeLoad_Report_Q1_2026.pdf", q1, 8),
     ("2025 IRP: renewable procurement", "up to 4,000 MW by 2035", "up to 4,000 MW of renewable resources by 2035", "2025_IRP_Main_Document.pdf", irp, 67), ("2025 IRP: 2026 Utility Scale RFP", "1,000 MW", "2026 Utility Scale RFP targeting 1,000 MW", "2025_IRP_Main_Document.pdf", irp, 67), ("2025 IRP: incremental renewables, Executive Summary", "up to 4,000 MW", "up to 4,000 MW of incremental", "2025_IRP_Main_Document.pdf", irp, 10), ("2025 IRP: battery storage in progress", "more than 2,065 MW", "2,065 MW of battery energy storage", "2025_IRP_Main_Document.pdf", irp, 10),
     ("2025 IRP summary: load growth, next six years", "about 8,500 MW", "8,500 megawatts (MW) of electrical load growth", "2025_IRP_one_page_summary.pdf", one, 1), ("2025 IRP summary: higher peak by end of 2030 vs 2023 IRP Update", "about 2,600 MW", "2,600 MW in peak demand", "2025_IRP_one_page_summary.pdf", one, 1), ("2025 IRP summary: customers", "2.8 million", "2.8 million customers", "2025_IRP_one_page_summary.pdf", one, 1)]
out = []
for fig, val, q, d, T, p in F:
    txt = re.sub(r"\s+", " ", T[p - 1]); 
    if q not in txt: sys.exit(f"Not on cited page: {q!r} {d} p. {p}")
    out.append(dict(figure=fig, value=val, text_on_page=q, document=d, pdf_page=p))
pd.DataFrame(out).to_csv("data/georgia_filing_figures.csv", index=False)
# ---- attachment: stage x segment; project names and locations are redacted by the company ----
def att(x, q):
    d = pd.read_excel(x, sheet_name="Main", header=1); d = d[d["Facility Type"].notna()].copy(); d["stage"] = d["Project Stage"].astype(str).str.rstrip("*"); d["load"] = pd.to_numeric(d["Announced Load*"], errors="coerce")
    g = d.groupby(["stage", "Segment"]).agg(projects=("load", "size"), announced_load_mw=("load", "sum")).reset_index(); g.insert(0, "report", q); return g, d
g1, d1 = att(Q1X, "Q1 2026"); g2, d2 = att(Q2X, "Q2 2026"); g = pd.concat([g2, g1]); g["source"] = g.report.map({"Q1 2026": os.path.basename(Q1X) + ", tab Main", "Q2 2026": "dkt55378_large_load_report_q2_2026.zip > " + os.path.basename(Q2X) + ", tab Main"})
g.to_csv("data/georgia_large_load_attachment.csv", index=False)
for q, d, cm in (("Q1", d1, 31), ("Q2", d2, 32)):
    c = d[d.stage.isin(["Contract for Electric Service", "Request for Service"])]; print(q, "projects", len(d), "committed", len(c), "announced MW", round(c.load.sum()), "all stages", round(d.load.sum()), "data center share of MW %.1f%%" % (100 * d[d.Segment == "Data Center/Crypto"].load.sum() / d.load.sum()))
    if len(c) != cm: sys.exit(f"{q}: {len(c)} committed projects vs {cm} in the report")
# ---- Epoch sites in Georgia ----
e = pd.read_csv("data/raw/epoch/data_centers.csv"); t = pd.read_csv("data/raw/epoch/data_center_timelines.csv")
s = e[e.Address.astype(str).str.contains(r"\b(?:Georgia|GA)\b", regex=True) & e.Country.astype(str).str.contains("United States|USA|US", regex=True)].copy()
rows = []
for r in s.itertuples():
    x = t[t["Data center"] == r.Name].copy(); x["Date"] = pd.to_datetime(x.Date, errors="coerce"); x = x.sort_values("Date")
    rows.append(dict(site=r.Name, owner=r.Owner, users=r.Users, address=r.Address, latest_timeline_date=str(x.Date.max().date()), latest_it_mw=x["IT power (MW)"].iloc[-1], latest_facility_mw=x["Power (MW)"].iloc[-1], latest_status=x["Construction status"].iloc[-1], source="data/raw/epoch/data_centers.csv; data_center_timelines.csv"))
ep = pd.DataFrame(rows); ep.to_csv("data/georgia_epoch_sites.csv", index=False); print(ep[["site", "owner", "latest_it_mw", "latest_facility_mw", "latest_status"]].to_string()); print("sum", ep.latest_it_mw.sum(), ep.latest_facility_mw.sum())

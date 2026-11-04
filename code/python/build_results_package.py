#!/usr/bin/env python3
"""Build release/results_and_data_<date>/ and its zip, for the team. Stays local. It mirrors the project layout so the workbook's receipt links work.
Usage: python3 code/python/build_results_package.py --date YYYY-MM-DD"""
import argparse, glob, os, re, shutil, subprocess, sys, zipfile
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); D = ap.parse_args().date
ROOT = os.getcwd(); OUT = f"release/results_and_data_{D}"
if os.path.exists(OUT): shutil.rmtree(OUT)  # built output only
os.makedirs(OUT)
def cp(src, dst=None):
    d = os.path.join(OUT, dst or src); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(src, d)
need = [f"outputs/ECON499R_Results_{D}.pdf", f"outputs/ECON499R_Master_Data_{D}.xlsx", f"docs/{D}/project-summary.md", f"docs/{D}/methods_section.tex", f"results/{D}/paper/findings.md"]
for f in need:
    if not os.path.exists(f): sys.exit(f"missing: {f}")
cp(need[0], os.path.basename(need[0])); cp(f"outputs/ECON499R_Results_{D}.html", f"ECON499R_Results_{D}.html"); cp(need[1])  # workbook sits in outputs/ so its ../data/receipts links work
for f in sorted(glob.glob("data/*.csv") + glob.glob("data/out/*.csv") + glob.glob("data/*.md") + glob.glob("data/receipts/*.md")): cp(f)
for r, _, fs in os.walk("results"):
    for f in fs:
        if f != ".DS_Store": cp(os.path.join(r, f))
for f in (f"docs/{D}/project-summary.md", f"docs/{D}/methods_section.tex", f"docs/{D}/memo-to-paper.md"): cp(f, "summary_and_methods/" + os.path.basename(f))
cp(f"results/{D}/paper/findings.md", "summary_and_methods/findings.md")
os.makedirs(f"{OUT}/notebooks_html", exist_ok=True)
for nb in sorted(glob.glob("notebooks/*.ipynb")):
    subprocess.run(["jupyter", "nbconvert", "--to", "html", "--log-level=ERROR", "--output-dir", os.path.abspath(f"{OUT}/notebooks_html"), nb], check=True)
for h in glob.glob(f"{OUT}/notebooks_html/*.html"):
    t = open(h, errors="surrogateescape").read(); u = t.replace(ROOT + "/", "").replace(ROOT, ".")
    if u != t: open(h, "w", errors="surrogateescape").write(u)
open(f"{OUT}/README.txt", "w").write(f"""ECON 499R results and data, as of {D}. Shunji Lewandowski and Alexander Hendricks. Local only: don't post this folder. It holds tables whose sources don't clear redistribution.

Start here
  ECON499R_Results_{D}.pdf            12-page readable report (the .html is the same report)
  summary_and_methods/project-summary.md   2-page plain-English summary, with every number traced
  summary_and_methods/findings.md, methods_section.tex, memo-to-paper.md

Data
  outputs/ECON499R_Master_Data_{D}.xlsx   Master workbook. Start at README, then Variable Finder. It's in outputs/ so its receipt links work
  data/                                   Cleaned CSVs, data dictionary, registry, validation
  data/out/                               Panel, W matrices, finance tables
  data/receipts/                          Where each source came from

Results
  results/{D}/paper/                       Tables (CSV and LaTeX), figures, captions, number checks
  results/                                 Every result file, by date
  notebooks_html/                          All 9 notebooks, executed

Not here: raw data, Bloomberg, interview material, journal PDFs, the Lazard PDF, .env or any key.
""")
# ---- scan ----
key = None
if os.path.exists(".env"):
    for ln in open(".env"):
        if ln.startswith("CENSUS_KEY="): key = ln.split("=", 1)[1].strip().strip('"')
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"); h = dict(key=[], email=[], path=[], barred=[])
for r, _, fs in os.walk(OUT):
    for f in fs:
        p = os.path.join(r, f); rel = os.path.relpath(p, OUT)
        if f == ".env" or (re.search(r"transcript|bloomberg|lazard|zhang_et_al", f, re.I) and not f.endswith(".md")): h["barred"].append(rel)  # receipts are .md notes about a source
        if f.endswith((".xlsx", ".pdf", ".png")): continue
        t = open(p, errors="ignore").read(); t = re.sub(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+", "", t)
        if key and key in t: h["key"].append(rel)
        m = [x for x in EM.findall(t) if not x.endswith(("@2x.png", ".js", ".css")) and not re.search(r"@\d|example\.|\.(js|min|css|ipynb)$", x)]
        if m: h["email"].append((rel, sorted(set(m))[:3]))
        if re.search(r"/Users/|/private/tmp", t): h["path"].append(rel)
print({k: (len(v), v[:4]) for k, v in h.items()})
if h["key"] or h["barred"]: sys.exit("scan failed: no zip made")
Z = f"release/results_and_data_{D}.zip"
if os.path.exists(Z): os.remove(Z)
with zipfile.ZipFile(Z, "w", zipfile.ZIP_DEFLATED) as z:
    for r, _, fs in os.walk(OUT):
        for f in sorted(fs): p = os.path.join(r, f); z.write(p, os.path.relpath(p, "release"))
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs); n = sum(len(fs) for _, _, fs in os.walk(OUT))
bad = zipfile.ZipFile(Z).testzip(); print("files", n, "folder MB", round(tot / 1e6, 1), "zip MB", round(os.path.getsize(Z) / 1e6, 1), "zip test", bad or "ok")

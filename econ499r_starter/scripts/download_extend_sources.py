#!/usr/bin/env python3
"""Download the raw sources for prompts/09_extend.md, by stage.

Usage: download_extend_sources.py <raw_dir> <log_csv> <stage> [naics ...]

Stages
  placebo-select  QCEW annual industry files, 2018 and 2021, for the 12 pre-registered placebo candidates
                  (EXPERIMENTS.md section 14.1, E4)
  placebo         QCEW annual industry files, 2014-2024, for the NAICS codes given after the stage
  drivers         National drivers for section 4 (EXPERIMENTS.md section 14.4)

Existing files are left alone. Appends url, path, bytes, sha256 and stage to <log_csv>. No key is needed.
"""
import csv, hashlib, os, subprocess, sys

UA = "Mozilla/5.0 (ECON499R research data pull)"
CANDIDATES = ["621610", "624120", "621511", "812910", "541940", "621493", "561612", "621420", "812199", "621340", "541613", "312140"]
QCEW = "https://data.bls.gov/cew/data/api/{y}/a/industry/{c}.csv"
DRIVERS = [
    ("crs/R43453.pdf", "https://crsreports.congress.gov/product/pdf/R/R43453"),
    ("crs/IF10479.pdf", "https://crsreports.congress.gov/product/pdf/IF/IF10479"),
    ("crs/PLAW-117publ169.pdf", "https://www.congress.gov/117/plaws/publ169/PLAW-117publ169.pdf"),
    ("eia/henry_hub/RNGWHHDa.xls", "https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDa.xls"),
]


def curl(url, path, max_time=300):
    tmp = path + ".part"
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", str(max_time), "--retry", "2", "-A", UA, "-w", "%{http_code}", "-o", tmp, url],
                       capture_output=True, text=True)
    if r.stdout.strip() != "200" or not os.path.exists(tmp) or os.path.getsize(tmp) < 100:
        if os.path.exists(tmp):
            os.remove(tmp)
        sys.exit(f"FAILED {r.stdout.strip()} {url} {r.stderr[:160]}")
    os.replace(tmp, path)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(raw, log_csv, stage, codes):
    if stage == "placebo-select":
        files = [(f"bls/placebo/qcew_{y}_{c}.csv", QCEW.format(y=y, c=c)) for c in CANDIDATES for y in (2018, 2021)]
    elif stage == "placebo":
        if not codes:
            sys.exit("placebo stage needs NAICS codes")
        files = [(f"bls/placebo/qcew_{y}_{c}.csv", QCEW.format(y=y, c=c)) for c in codes for y in range(2014, 2025)]
    elif stage == "drivers":
        files = DRIVERS
    else:
        sys.exit(f"unknown stage {stage}")
    rows = []
    for rel, url in files:
        path = os.path.join(raw, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            curl(url, path)
        rows.append({"stage": stage, "url": url, "path": path, "bytes": os.path.getsize(path), "sha256": sha(path)})
        print(f"{rows[-1]['bytes']:>12,}  {rel}")
    os.makedirs(os.path.dirname(log_csv), exist_ok=True)
    new = not os.path.exists(log_csv)
    old = [] if new else list(csv.DictReader(open(log_csv)))
    keep = [r for r in old if r["path"] not in {x["path"] for x in rows}] + rows
    with open(log_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["stage", "url", "path", "bytes", "sha256"])
        w.writeheader(); w.writerows(keep)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])

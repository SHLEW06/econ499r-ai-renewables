#!/usr/bin/env python3
"""Download the raw sources for prompts/08_finalize.md section 1.

Usage: download_finalize_sources.py <raw_dir> <log_csv>

- EIA Monthly Energy Review Table A6 (heat rates; fossil-fueled plant heat rate by year)
- EIA SEDS change notice page (the Oct 2023 accounting change), saved for citation
- EIA SEDS archive, consolidated 2021 release (data through 2021, published before the change)
- NOAA NCEI Storm Events Database, details files for 2015-2024

Existing files are left alone. Logs url, path, bytes and sha256. No key is needed.
"""
import csv, hashlib, os, re, subprocess, sys

UA = "Mozilla/5.0 (ECON499R research data pull)"
NOAA = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
FILES = [
    # NOTE: this URL returns MER Table 1.1, not A6 (kept as downloaded on 2026-11-07, unused; see data/receipts/mer_heat_rates.md)
    ("eia/mer/MER_TA6.xlsx", "https://www.eia.gov/totalenergy/data/monthly/query/mer_data_excel.asp?table=TA6"),
    ("eia/mer/mer_a.pdf", "https://www.eia.gov/totalenergy/data/monthly/pdf/mer_a.pdf"),  # Appendix A tables A1+ (renumbered); not A6
    ("eia/mer/mer_A_FULL.pdf", "https://www.eia.gov/totalenergy/data/monthly/pdf/mer_A_FULL.pdf"),  # Table A6 source notes, PDF p. 15
    ("eia/mer/full_data_MER.zip", "https://www.eia.gov/totalenergy/data/monthly/full_data_MER.zip"),  # turned out to be EV-charging microdata (MER Appendix F); unused
    ("eia/mer/TOTAL.zip", "https://api.eia.gov/bulk/TOTAL.zip"),  # EIA bulk MER series, no key; fossil-fuel-equivalent and captured series by fuel
    ("eia/seds/seds_change_notice.html", "https://www.eia.gov/state/seds/seds-change/index.php"),
    ("eia/seds/use_all_phy.csv", "https://www.eia.gov/state/seds/sep_use/total/csv/use_all_phy.csv"),  # SOR7P: residential small-scale PV, million kWh
    ("eia/seds_archive/complete_seds_2021.zip", "https://www.eia.gov/state/seds/archive/complete_seds_2021.zip"),
    ("eia/seds_archive/archive_index.html", "https://www.eia.gov/state/seds/archive/"),
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


def main(raw, log_csv):
    listing = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", UA, NOAA], capture_output=True, text=True).stdout
    for y in range(2015, 2025):
        m = sorted(set(re.findall(rf"StormEvents_details-ftp_v1\.0_d{y}_c\d+\.csv\.gz", listing)))
        if len(m) != 1:
            sys.exit(f"Storm Events {y}: expected one details file, found {m}")
        FILES.append((f"noaa/storm_events/{m[0]}", NOAA + m[0]))
    rows = []
    for rel, url in FILES:
        path = os.path.join(raw, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            curl(url, path)
        rows.append({"url": url, "path": os.path.join(raw, rel), "bytes": os.path.getsize(path), "sha256": sha(path)})
        print(f"{rows[-1]['bytes']:>12,}  {rel}")
    os.makedirs(os.path.dirname(log_csv), exist_ok=True)
    with open(log_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "path", "bytes", "sha256"])
        w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

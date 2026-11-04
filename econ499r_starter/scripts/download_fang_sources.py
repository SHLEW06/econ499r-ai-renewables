#!/usr/bin/env python3
"""Download the raw sources for the Fang et al. (2025) test (Phase 4h, Part A).

Usage: download_fang_sources.py <raw_dir> <log_csv>

Writes into <raw_dir>/aiindex, <raw_dir>/ncses and <raw_dir>/eia/seds. Existing files are left
alone. Logs url, path, bytes and sha256. Google Sheets are exported as xlsx; Drive CSVs are found
by listing each edition's public-data folder. No key is needed for any source.
"""
import csv, hashlib, html, os, re, subprocess, sys

AI = "https://hai-production.s3.amazonaws.com/files/"
FILES = [
    ("eia/seds/pr_all.csv", "https://www.eia.gov/state/seds/sep_prices/total/csv/pr_all.csv"),
    ("eia/seds/Codes_and_Descriptions.xlsx", "https://www.eia.gov/state/seds/CDF/Codes_and_Descriptions.xlsx"),
    ("eia/seds/Prod_dataset.xlsx", "https://www.eia.gov/state/seds/sep_prod/xls/Prod_dataset.xlsx"),
    ("ncses/bachelors-degrees-per-1000-18-24-year-olds.json", "https://ncses.nsf.gov/indicators/states/api/v2/indicators/bachelors-degrees-per-1000-18-24-year-olds.json"),
    ("ncses/degconferred-bach.json", "https://ncses.nsf.gov/indicators/states/api/v2/dataseries/degconferred-bach.json"),
    ("ncses/population18-24.json", "https://ncses.nsf.gov/indicators/states/api/v2/dataseries/population18-24.json"),
    ("aiindex/ai_index_2019_report.pdf", AI + "ai_index_2019_report.pdf"),
    ("aiindex/2021-ai-index-report_master.pdf", AI + "2021-ai-index-report_master.pdf"),
    ("aiindex/2022-ai-index-report_chapter-4.pdf", AI + "2022-ai-index-report_chapter-4.pdf"),
    ("aiindex/hai_ai-index-report-2023_chapter_4.pdf", AI + "hai_ai-index-report-2023_chapter_4.pdf"),
    ("aiindex/hai_ai-index-report-2024_chapter4.pdf", AI + "hai_ai-index-report-2024_chapter4.pdf"),
    ("aiindex/hai_ai-index-report-2025_chapter4_final.pdf", AI + "hai_ai-index-report-2025_chapter4_final.pdf"),
    ("aiindex/ai_index_report_2026_chapter_4_economy.pdf", "https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf"),
    ("aiindex/ed2019_ai_postings_by_state.xlsx", "https://docs.google.com/spreadsheets/d/1SAQzv3bUew1pCvW2JtrkYq3ny2Viqj4usQLyFl38P6A/export?format=xlsx"),
    ("aiindex/ed2021_burning_glass.xlsx", "https://docs.google.com/spreadsheets/d/1n09zmj_nlzuIiGio8Q8Ja3OPlY_tVjqhELg0mn2nEsQ/export?format=xlsx"),
    ("aiindex/ed2022_emsi_burning_glass.xlsx", "https://docs.google.com/spreadsheets/d/19UGjvQW-PcnWoHEPe9Wd1Eib5z6S5II7lu1tE92fK3M/export?format=xlsx"),
]
# Public-data folders: edition -> (folder id, figures wanted)
FOLDERS = {"ed2023": ("1K1s2dG0XYzBO4yjczomxqNhniPwhXwZR", r"fig_4\.1\.(6|7|8|10)\.csv"),
           "ed2024": ("13--hgcZtjxPcVNvRSbWxMNAYH7l6B_Gg", r"fig_4\.2\.(7|8|9|11)\.csv"),
           "ed2025": ("1oGKD04Iyw9EVhOTs5DsyrO568DORZnBS", r"fig_4\.2\.(8|9|10|12)\.csv"),
           "ed2026": ("1zJTOg0iR0j5SijCwFutwWvDt143lW277", r"fig_4\.4\.(10|11|12|13)\.csv")}
UA = "Mozilla/5.0 (ECON499R research data pull)"


def curl(url, path):
    tmp = path + ".part"
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "180", "--retry", "2", "-A", UA, "-w", "%{http_code}", "-o", tmp, url], capture_output=True, text=True)
    if r.stdout.strip() != "200" or not os.path.exists(tmp):
        if os.path.exists(tmp):
            os.remove(tmp)
        sys.exit(f"FAILED {r.stdout.strip()} {url} {r.stderr[:160]}")
    os.replace(tmp, path)


def listing(fid):
    s = subprocess.run(["curl", "-sS", "-L", "--max-time", "30", "-A", UA, f"https://drive.google.com/embeddedfolderview?id={fid}#list"], capture_output=True, text=True).stdout
    return list(zip(re.findall(r'id="entry-([A-Za-z0-9_-]+)"', s), [html.unescape(x) for x in re.findall(r'flip-entry-title">([^<]+)<', s)]))


def main(raw, log_csv):
    rows = []
    def fetch(rel, url):
        path = os.path.join(raw, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            curl(url, path)
        b = open(path, "rb").read()
        rows.append(dict(path="data/raw/" + rel, url=url, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()))
        print(rel, len(b))
    for rel, url in FILES:
        fetch(rel, url)
    for ed, (fid, pat) in FOLDERS.items():
        items = listing(fid)
        for _ in range(4):  # Folder depth differs by edition: descend until the figure files appear
            if any(re.fullmatch(pat, n) for _, n in items):
                break
            nxt = [i for i, n in items if n == "Data"] or [i for i, n in items if re.search(r"(chapter|ch)[ _-]*4|econ", n, re.I)]
            if not nxt:
                break
            items = listing(nxt[0])
        got = 0
        for i, n in items:
            if re.fullmatch(pat, n):
                fetch(f"aiindex/{ed}_{n}", f"https://drive.google.com/uc?export=download&id={i}")
                got += 1
        print(ed, "figures found", got, "of listing", len(items), [n for _, n in items][:6])
    with open(log_csv, "w", newline="") as f:
        w = csv.DictWriter(f, ["path", "url", "bytes", "sha256"])
        w.writeheader(); w.writerows(rows)
    print("logged", len(rows))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])

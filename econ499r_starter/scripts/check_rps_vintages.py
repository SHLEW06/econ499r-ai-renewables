#!/usr/bin/env python3
"""Test whether LBNL rewrites past RPS/CES target years between editions.

Usage: check_rps_vintages.py <june_2026_targets_xlsx> <scratch_download_dir> <out_csv>

Downloads the June 2023, Aug 2024 and Aug 2025 target files into the scratch folder
(not into data/raw) and compares each "Total RPS" and "Total CES" row with the
June 2026 file for 2015-2025. Writes one row per state-program-year-edition where
the values differ by more than 0.05 percentage points, and prints a summary.
"""
import hashlib, os, subprocess, sys, warnings
import openpyxl, pandas as pd

warnings.filterwarnings("ignore")
BASE = "https://eta-publications.lbl.gov/sites/default/files/"
EDITIONS = {"2023-06": "rps_ces_nominal_percentage_targets_june_2023.xlsx",
            "2024-08": "rps_and_ces_nominal_percentage_targets_august_2024.xlsx",
            "2025-08": "2025-08/rps_ces_targets_and_demand_august_2025.xlsx"}
YEARS = range(2015, 2026)


def read(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        for i, r in enumerate(rows):
            labels = [str(x).strip() for x in r if x is not None]
            yrs = {}
            for j, x in enumerate(r):
                if str(x).split(".")[0] in {str(y) for y in range(2000, 2051)}:
                    yrs[int(str(x).split(".")[0])] = j
            if "State" in labels and 2015 in yrs:
                if "target" not in ws.title.lower() and "%" not in ws.title and len(wb.worksheets) > 1:
                    break
                sc = [str(x).strip() if x else "" for x in r].index("State")
                lab = next(j for j, x in enumerate(r) if x and any(k in str(x) for k in ("Tier", "Carve", "Technology", "Total")))
                out, cur = [], None
                for rr in rows[i + 1:]:
                    if rr[sc]:
                        cur = str(rr[sc]).strip()
                    t = str(rr[lab]).strip() if rr[lab] else ""
                    prog = "RPS" if t.startswith("Total RPS") else "CES" if t.startswith("Total CES") else None
                    if not prog:
                        continue
                    for y in YEARS:
                        if y in yrs:
                            v = rr[yrs[y]]
                            out.append((cur, prog, y, float(v) * 100 if isinstance(v, (int, float)) else None))
                return pd.DataFrame(out, columns=["state", "program", "year", "pct"])
    raise SystemExit(f"no target table found in {path}")


def main(now_path, scratch, out_csv):
    os.makedirs(scratch, exist_ok=True)
    now = read(now_path).rename(columns={"pct": "pct_2026_06"})
    print("June 2026 rows", len(now))
    diffs = []
    for ed, rel in EDITIONS.items():
        p = os.path.join(scratch, os.path.basename(rel))
        if not os.path.exists(p):
            subprocess.run(["curl", "-sSL", "--max-time", "90", "-A", "Mozilla/5.0", "-o", p, BASE + rel], check=True)
        print(ed, BASE + rel, hashlib.sha256(open(p, "rb").read()).hexdigest())
        old = read(p).rename(columns={"pct": "pct_old"})
        m = now.merge(old, on=["state", "program", "year"], how="inner")
        m = m.dropna(subset=["pct_2026_06", "pct_old"])
        # A year counts as "past" if it is the edition year or earlier: that value was the current target when published.
        cut = int(ed[:4])
        m["past"] = m.year <= cut
        m["d"] = m.pct_2026_06 - m.pct_old
        for lab, s in (("edition year or earlier", m[m.past]), ("later years", m[~m.past])):
            n_diff = int((s.d.abs() > 0.05).sum())
            print(f"  {lab}: {len(s)} compared, {n_diff} differ; states: {sorted(s[s.d.abs() > 0.05].state.unique())}")
        d = m[m.d.abs() > 0.05].copy()
        d["edition"] = ed
        diffs.append(d)
    out = pd.concat(diffs)[["edition", "state", "program", "year", "past", "pct_old", "pct_2026_06", "d"]].round(3)
    out.to_csv(out_csv, index=False)
    print("wrote", out_csv, len(out))
    print(out[out.past].to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

#!/usr/bin/env python3
"""Download NOAA NCEI annual heating and cooling degree days for the 48 contiguous states.

Usage: download_noaa_degree_days.py <raw_noaa_dir> <out_csv>

Uses Climate at a Glance statewide time series (12-month totals ending December), 2015-2025.
Stops without writing the table if NCEI can't be reached. Each file's title line is checked
against the expected state name. First run on real NCEI output: 2026-11-04. All 528 state-years
match the monthly nClimDiv files summed over the year (data/receipts/noaa.md).
"""
import os, subprocess, sys
import pandas as pd

ST = ["Alabama:AL","Arizona:AZ","Arkansas:AR","California:CA","Colorado:CO","Connecticut:CT","Delaware:DE","Florida:FL","Georgia:GA",
      "Idaho:ID","Illinois:IL","Indiana:IN","Iowa:IA","Kansas:KS","Kentucky:KY","Louisiana:LA","Maine:ME","Maryland:MD","Massachusetts:MA",
      "Michigan:MI","Minnesota:MN","Mississippi:MS","Missouri:MO","Montana:MT","Nebraska:NE","Nevada:NV","New Hampshire:NH","New Jersey:NJ",
      "New Mexico:NM","New York:NY","North Carolina:NC","North Dakota:ND","Ohio:OH","Oklahoma:OK","Oregon:OR","Pennsylvania:PA","Rhode Island:RI",
      "South Carolina:SC","South Dakota:SD","Tennessee:TN","Texas:TX","Utah:UT","Vermont:VT","Virginia:VA","Washington:WA","West Virginia:WV",
      "Wisconsin:WI","Wyoming:WY"]
URL = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/{c}/{m}/12/12/2015-2025.csv"


def main(raw, out_csv):
    os.makedirs(raw, exist_ok=True)
    rec = []
    for i, entry in enumerate(ST, 1):
        name, ab = entry.split(":")
        for m in ("hdd", "cdd"):
            p = os.path.join(raw, f"{ab}_{m}_2015_2025.csv")
            if not os.path.exists(p):
                r = subprocess.run(["curl", "-sSL", "--max-time", "45", "-A", "Mozilla/5.0", "-w", "%{http_code}", "-o", p + ".part", URL.format(c=i, m=m)], capture_output=True, text=True)
                if r.stdout.strip() != "200":
                    if os.path.exists(p + ".part"):
                        os.remove(p + ".part")
                    sys.exit(f"NCEI unreachable at {ab} {m}: http {r.stdout.strip()} {r.stderr.strip()[:120]}; table not written")
                os.replace(p + ".part", p)
            lines = open(p, errors="ignore").read().splitlines()
            if name.lower() not in lines[0].lower():
                sys.exit(f"wrong state in {p}: {lines[0][:80]}")
            start = next(j for j, l in enumerate(lines) if l.lower().startswith("date"))
            for l in lines[start + 1:]:
                f = l.split(",")
                if len(f) >= 2 and f[0][:4].isdigit():
                    rec.append(dict(state=ab, year=int(f[0][:4]), measure=m, value=float(f[1])))
    df = pd.DataFrame(rec).pivot(index=["state", "year"], columns="measure", values="value").reset_index()
    df.to_csv(out_csv, index=False)
    print("wrote", out_csv, df.shape, "states", df.state.nunique(), "years", df.year.min(), df.year.max())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])

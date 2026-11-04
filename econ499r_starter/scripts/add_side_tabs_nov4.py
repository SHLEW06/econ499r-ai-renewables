#!/usr/bin/env python3
"""Copy the data workbook and add one tab per Nov 4 side table. The input is not changed.

Usage: add_side_tabs_nov4.py <in_xlsx> <side_table_dir> <out_xlsx>
"""
import os, sys
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

TABS = [("RPS Targets", "lbnl_rps_targets.csv"), ("ACS Broadband", "acs_broadband.csv"), ("EPU Annual", "epu_state_annual.csv"),
        ("NSF State RD", "nsf_state_rd.csv"), ("OWID Solar", "owid_global_solar_capacity.csv"), ("LBNL Solar Projects", "lbnl_utility_solar.csv"),
        ("Epoch by State", "epoch_ai_campuses_by_state.csv")]
SOURCES = [
 ("LBNL RPS and CES targets and achievement (June 2026)", "https://eta-publications.lbl.gov/publications/us-state-electricity-resource-0", "LBNL current RPS/CES schedule; see data/receipts/lbnl_rps.md"),
 ("LBNL Utility-Scale Solar, 2026 Edition", "https://eta-publications.lbl.gov/publications/us-utility-scale-solar-2026-edition", "Individual_Project_Data tab"),
 ("State EPU (Baker, Davis, Levy)", "https://www.policyuncertainty.com/state_epu.html", "Monthly values averaged to years"),
 ("NSF National Patterns Table 10", "https://ncses.nsf.gov/pubs/nsf26313/assets/data-tables/tables/nsf26313-tab010.xlsx", "One edition per data year, 2017-2023"),
 ("IRENA via Our World in Data", "https://ourworldindata.org/grapher/solar-pv-cumulative-capacity", "On-grid solar PV, GW"),
 ("Census ACS 1-year S2801", "https://api.census.gov/data/2024/acs/acs1/subject", "S2801_C02_012E for 2015; S2801_C02_014E from 2016; no 2020 release"),
 ("Epoch AI data centers", "https://epoch.ai/data/ai-data-centers", "Context only; not a model variable"),
 ("NOAA degree days", "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", "NOT DONE on 2026-11-04: NCEI unreachable; no table"),
]


def main(in_xlsx, side, out_xlsx):
    if os.path.abspath(in_xlsx) == os.path.abspath(out_xlsx):
        sys.exit("output must be a new file")
    wb = load_workbook(in_xlsx)
    hdr, fill, body = Font(name="Arial", bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864"), Font(name="Arial", size=10)
    for name, csvf in TABS:
        d = pd.read_csv(os.path.join(side, csvf))
        ws = wb.create_sheet(name)
        ws.append(list(d.columns))
        for c in ws[1]:
            c.font, c.fill = hdr, fill
        for row in d.astype(object).where(d.notna(), None).itertuples(index=False):
            ws.append(list(row))
        ws.freeze_panes = "A2"
        print(name, d.shape)
    s = wb["Sources"]
    for r in SOURCES:
        s.append(list(r))
        for c in s[s.max_row]:
            c.font = body
    wb.save(out_xlsx)
    chk = load_workbook(out_xlsx, read_only=True)
    print("sheets:", chk.sheetnames)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

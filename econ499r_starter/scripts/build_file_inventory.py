#!/usr/bin/env python3
"""Write data/FILE_INVENTORY.csv: one row per file under data/raw.

Usage: build_file_inventory.py <raw_dir> <baseline_manifest_csv> <out_csv>

Columns: path, size, sha256, type, what_it_is, disposition. Stops if any file in the
baseline manifest is missing or has a different hash, since raw files must not change.
"""
import csv, hashlib, os, sys

OLD = {"bea": "BEA state GDP and personal income", "bls": "BLS QCEW annual employment by NAICS", "census": "Census county Gazetteer and adjacency",
       "costs": "Lazard LCOE+ report", "eia": "EIA state electricity and SEDS data", "eia_forms": "EIA Forms 860, 861, 923",
       "georgia": "Georgia Power IRP and large-load filings", "pudl": "FERC Form 1 via PUDL", "rmi": "RMI Utility Transition Hub"}
NEW = {
 "lbnl/RPS & CES Targets and Demand_June 2026.xlsx": ("LBNL RPS and CES target schedule and demand, June 2026", "Used: lbnl_rps_targets.csv"),
 "lbnl/Historical RPS & CES Target Achievement and Compliance Costs_June 2026.xlsx": ("LBNL share of target achieved and compliance costs, June 2026; no target levels", "Used: cross-check columns in lbnl_rps_targets.csv"),
 "lbnl/rps_ces_nominal_percentage_targets_june_2023.xlsx": ("LBNL RPS and CES target schedule, June 2023 edition", "Used: target_pct_ed2023 check in lbnl_rps_targets.csv"),
 "eia_forms/eia8602017.zip": ("EIA Form 860 data, 2017", "Reference: identifies the NE and NM 2017 blank-fuel capacity rows"),
 "lbnl/Utility Scale Solar 2026 Edition Datafile.xlsx": ("LBNL Utility-Scale Solar, Oct 2026; 2,005 projects", "Used: lbnl_utility_solar.csv"),
 "epu/State_Policy_Uncertainty.xlsx": ("Baker, Davis and Levy state EPU, monthly, 1985-2025", "Used: epu_state_annual.csv"),
 "nsf/nsf27300-tab010.xlsx": ("NSF business R&D by industry and company size, 2024; no states; wrong table", "NOT USED: rated red"),
 "owid/solar-pv-cumulative-capacity.csv": ("OWID on-grid solar PV capacity, IRENA data, 2000-2025", "Used: owid_global_solar_capacity.csv"),
 "owid/solar-pv-cumulative-capacity.metadata.json": ("OWID metadata for the capacity file", "Reference"),
 "owid/readme.md": ("OWID readme for the capacity file", "Reference"),
 "epoch/data_centers.csv": ("Epoch AI sites, downloaded Nov 4, 2026", "Used: epoch_ai_campuses_by_state.csv; context only"),
 "epoch/data_center_timelines.csv": ("Epoch AI power and status over time by site", "Used: epoch_ai_campuses_by_state.csv; context only"),
 "epoch/data_center_chip_quantities.csv": ("Epoch AI chips by site", "Not used"),
 "epoch/data_center_cooling_towers.csv": ("Epoch AI cooling towers by site", "Not used"),
 "epoch/data_center_chillers.csv": ("Epoch AI chillers by site", "Not used"),
 "epoch/chip_types.csv": ("Epoch AI chip reference table", "Not used"),
 "epoch/README.md": ("Epoch AI license and citation", "Reference"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main(raw, manifest, out_csv):
    base = {r["path"]: r["sha256"] for r in csv.DictReader(open(manifest, newline=""))}
    rows, seen = [], set()
    for d, _, fs in os.walk(raw):
        for f in sorted(fs):
            if f == ".DS_Store":
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, raw)
            path = "data/raw/" + rel
            h = sha(p)
            if path in base and base[path] != h:
                sys.exit(f"RAW FILE CHANGED: {path}")
            seen.add(path)
            top = rel.split(os.sep)[0]
            if rel in NEW:
                what, disp = NEW[rel]
            elif top == "nsf":
                what, disp = "NSF National Patterns Table 10, R&D by state, one data year per edition", "Used: nsf_state_rd.csv"
            elif top == "acs":
                what, disp = "Census ACS 1-year S2801 API response or code list; contains no key", "Used: acs_broadband.csv"
            elif top == "aiindex":
                what, disp = "Stanford AI Index: report PDF, public-data sheet or figure CSV", "Used: ai_job_postings_state.csv; Fang test"
            elif top == "ncses":
                what, disp = "NCSES State Indicators API response: bachelor's degrees per 1,000 age 18-24", "Used: ncses_bachelors_state.csv; Fang test"
            elif rel in ("eia/seds/pr_all.csv", "eia/seds/Codes_and_Descriptions.xlsx"):
                what, disp = "EIA SEDS prices or code list", "Used: seds_renewables_state.csv; Fang test"
            elif f.startswith("._"):
                what, disp = "macOS metadata file that came with a zip", "Not data; harmless"
            else:
                what, disp = OLD.get(top, top), "Phase 2 raw file; see data/receipts/"
            rows.append(dict(path=path, size=os.path.getsize(p), sha256=h, type=os.path.splitext(f)[1].lstrip(".").lower() or "none", what_it_is=what, disposition=disp))
    missing = set(base) - seen
    if missing:
        sys.exit(f"RAW FILES MISSING: {sorted(missing)[:5]}")
    rows.sort(key=lambda r: r["path"])
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} files; baseline {len(base)} all unchanged; added since baseline {len(rows) - len(base)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

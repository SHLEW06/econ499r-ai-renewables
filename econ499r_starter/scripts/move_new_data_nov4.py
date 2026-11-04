#!/usr/bin/env python3
"""Move the Nov 4 data files into data/raw/<source>/ and log each move.

Usage: move_new_data_nov4.py <project_root> <log_csv>

Hashes each file before and after the move and stops on any mismatch. Refuses
to overwrite. Original file names are kept. Run once; a rerun finds nothing to move.
"""
import csv, hashlib, os, shutil, sys

MOVES = [
    ("RPS & CES Targets and Demand_June 2026.xlsx", "lbnl"),
    ("Historical RPS & CES Target Achievement and Compliance Costs_June 2026.xlsx", "lbnl"),
    ("Utility Scale Solar 2026 Edition Datafile.xlsx", "lbnl"),
    ("State_Policy_Uncertainty.xlsx", "epu"),
    ("nsf27300-tab010.xlsx", "nsf"),
    ("solar-pv-cumulative-capacity/solar-pv-cumulative-capacity.csv", "owid"),
    ("solar-pv-cumulative-capacity/solar-pv-cumulative-capacity.metadata.json", "owid"),
    ("solar-pv-cumulative-capacity/readme.md", "owid"),
    ("data_centers/data_centers.csv", "epoch"),
    ("data_centers/data_center_timelines.csv", "epoch"),
    ("data_centers/data_center_chip_quantities.csv", "epoch"),
    ("data_centers/data_center_cooling_towers.csv", "epoch"),
    ("data_centers/data_center_chillers.csv", "epoch"),
    ("data_centers/chip_types.csv", "epoch"),
    ("data_centers/README.md", "epoch"),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(root, log_csv):
    rows = []
    for rel, src in MOVES:
        old = os.path.join(root, rel)
        new_rel = os.path.join("data", "raw", src, os.path.basename(rel))
        new = os.path.join(root, new_rel)
        if not os.path.exists(old):
            sys.exit(f"missing source: {rel}")
        if os.path.exists(new):
            sys.exit(f"refusing to overwrite: {new_rel}")
        before = sha(old)
        os.makedirs(os.path.dirname(new), exist_ok=True)
        shutil.move(old, new)
        after = sha(new)
        if before != after:
            sys.exit(f"hash changed in move: {rel}")
        rows.append({"old_path": rel, "new_path": new_rel, "sha256": after})
        print(f"moved {rel} -> {new_rel}")
    os.makedirs(os.path.dirname(log_csv), exist_ok=True)
    with open(log_csv, "w", newline="") as f:
        w = csv.DictWriter(f, ["old_path", "new_path", "sha256"])
        w.writeheader()
        w.writerows(rows)
    print(f"logged {len(rows)} moves to {log_csv}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

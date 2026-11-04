#!/usr/bin/env python3
"""C.1b rebuild comparison: compare two build folders cell by cell.

Usage: compare_panel_builds.py <before_dir> <after_dir> <out_csv>

Prints whether each file is byte-identical. For the panel, compares every non-key cell with
no tolerance, including the missing-value pattern, and writes each changed cell to <out_csv>.
"""
import filecmp, os, sys
import numpy as np, pandas as pd

FILES = ["state_panel_2015_2025.csv", "W_inverse_distance_rowstd.csv", "W_distance_miles.csv", "W_border_binary.csv", "state_centroids_land.csv"]


def main(a, b, out_csv):
    for f in FILES:
        print(f"{f}: {'byte-identical' if filecmp.cmp(os.path.join(a, f), os.path.join(b, f), shallow=False) else 'DIFFERENT'}")
    k = ["state", "year"]
    x = pd.read_csv(os.path.join(a, FILES[0])).sort_values(k).reset_index(drop=True)
    y = pd.read_csv(os.path.join(b, FILES[0])).sort_values(k).reset_index(drop=True)
    if list(x.columns) != list(y.columns) or not x[k].equals(y[k]):
        sys.exit("columns or keys differ")
    cols = [c for c in x.columns if c not in k]
    print(f"cells compared: {len(cols) * len(x):,} ({len(cols)} non-key columns x {len(x)} rows)")
    print(f"blank cells: before {int(x[cols].isna().sum().sum())}, after {int(y[cols].isna().sum().sum())}")
    rec = []
    for c in cols:
        u, v = x[c], y[c]
        if pd.api.types.is_numeric_dtype(u) and pd.api.types.is_numeric_dtype(v):
            ch = ~((u == v) | (u.isna() & v.isna()))
        else:
            ch = ~((u.astype(str) == v.astype(str)))
        for i in np.where(ch)[0]:
            rec.append(dict(state=x.state[i], year=int(x.year[i]), column=c, before=u[i], after=v[i]))
    d = pd.DataFrame(rec, columns=["state", "year", "column", "before", "after"])
    d.to_csv(out_csv, index=False)
    print(f"changed cells: {len(d)}; columns changed: {sorted(d.column.unique())}")
    print(d.to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

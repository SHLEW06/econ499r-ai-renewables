#!/usr/bin/env python3
"""Rows x columns for every raw file (read-only), for the workbook's Raw Files tab and the size rule.
Usage: python3 code/python/build_raw_file_shapes.py --date YYYY-MM-DD"""
import argparse, csv, json, os, zipfile
import openpyxl, pandas as pd, pyarrow.parquet as pq
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); a = ap.parse_args()
inv = pd.read_csv("data/FILE_INVENTORY.csv"); out = []
def csv_shape(p, sep=","):
    with open(p, "rb") as fh: n = sum(1 for _ in fh)
    with open(p, encoding="latin1", newline="") as fh:
        rows = []
        for r in csv.reader(fh, delimiter=sep):
            rows.append(len(r))
            if len(rows) > 12: break
    return n, max(rows) if rows else 0
for p in inv.path:
    e = os.path.splitext(p)[1].lower(); b = os.path.basename(p); rec = dict(path=p, table="", rows=None, cols=None, kind=e.lstrip("."))
    try:
        if b.startswith("._"): rec["kind"] = "macOS sidecar"; out.append(rec); continue
        if e == ".csv": rec["rows"], rec["cols"] = csv_shape(p); out.append(rec)
        elif e == ".txt": rec["rows"], rec["cols"] = csv_shape(p, "|"); out.append(rec)
        elif e == ".parquet":
            m = pq.read_metadata(p); rec["rows"], rec["cols"] = m.num_rows, m.num_columns; out.append(rec)
        elif e in (".xlsx", ".xlsm"):
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                r = dict(rec); r["table"] = ws.title; r["rows"], r["cols"] = ws.max_row, ws.max_column; out.append(r)
            wb.close()
        elif e == ".zip":
            with zipfile.ZipFile(p) as z: rec["kind"] = f"zip, {len(z.namelist())} members"
            out.append(rec)
        elif e == ".json":
            d = json.load(open(p)); rec["rows"] = len(d) if isinstance(d, list) else None; out.append(rec)
        else: out.append(rec)
    except Exception as ex:
        rec["kind"] = f"{e} (unreadable: {type(ex).__name__})"; out.append(rec)
pd.DataFrame(out).to_csv(f"logs/{a.date}/raw_file_shapes.csv", index=False)

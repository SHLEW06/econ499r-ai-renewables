#!/usr/bin/env python3
"""Check a local data/ folder against data/MANIFEST.csv.

Usage (from the project root, after unzipping the data bundle there):
    python3 -I code/python/verify_data.py            # checks the repo you're in
    python3 -I code/python/verify_data.py <repo_root>

For every file in the manifest it checks that the file exists, has the listed size
and has the listed SHA-256. It reports:
    MISSING    in the manifest, not on disk
    SIZE       on disk, wrong size (hash not computed)
    HASH       right size, wrong SHA-256
    EXTRA      under data/raw/ or data/out/ but not in the manifest (info only)

Raw files listed in data/raw_unused.csv aren't in the bundle (no script reads them);
if you have them anyway, they're counted, not listed as EXTRA.

Exit code 0 when nothing is missing or mismatched, 1 otherwise. EXTRA files don't fail
the check: rebuilding the panel or adding downloads can create them.

Note: build_panel.py rewrites data/out/. If you rebuild and then see HASH lines for
data/out/ files, the rebuild differs from the shared build; data/raw/ lines mean a raw
file is damaged or a different vintage.
"""
import csv
import hashlib
import os
import sys
from pathlib import Path


def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(buf), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) > 2:
        sys.exit("usage: verify_data.py [repo_root]")
    root = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
    man = root / "data" / "MANIFEST.csv"
    if not man.exists():
        sys.exit(f"no manifest at {man}; run from the project root or pass it as the argument")

    with open(man, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or set(rows[0]) != {"path", "size", "sha256"}:
        sys.exit(f"{man} must have columns path,size,sha256")

    problems = {"MISSING": [], "SIZE": [], "HASH": []}
    listed = set()
    for i, r in enumerate(rows, 1):
        p = r["path"]
        listed.add(p)
        fp = root / p
        if not fp.is_file():
            problems["MISSING"].append(p)
        elif fp.stat().st_size != int(r["size"]):
            problems["SIZE"].append(f"{p}  (expected {int(r['size']):,} bytes, found {fp.stat().st_size:,})")
        elif sha256(fp) != r["sha256"]:
            problems["HASH"].append(p)
        if i % 250 == 0:
            print(f"  checked {i:,} of {len(rows):,}", file=sys.stderr)

    unused = set()
    if (root / "data" / "raw_unused.csv").exists():
        with open(root / "data" / "raw_unused.csv", newline="") as f:
            unused = {r["path"] for r in csv.DictReader(f)}
    extra, n_unused = [], 0
    junk = {".DS_Store"}
    for top in ("data/raw", "data/out"):
        for dirpath, _, names in os.walk(root / top):
            for n in names:
                p = (Path(dirpath) / n).relative_to(root).as_posix()
                if p in unused:
                    n_unused += 1
                elif p not in listed and n not in junk and not n.startswith(("._", "~$")) \
                        and "/_to_delete/" not in p:
                    extra.append(p)

    n_bad = sum(len(v) for v in problems.values())
    for k, v in problems.items():
        for line in v:
            print(f"{k:8s} {line}")
    for p in sorted(extra):
        print(f"EXTRA    {p}")
    ok = len(rows) - n_bad
    print(f"\n{ok:,} of {len(rows):,} files OK; {len(problems['MISSING'])} missing, "
          f"{len(problems['SIZE'])} wrong size, {len(problems['HASH'])} wrong hash; "
          f"{len(extra)} extra (not checked)"
          + (f"; {n_unused} unused raw files present (data/raw_unused.csv)" if n_unused else ""))
    print("RESULT: PASS" if n_bad == 0 else "RESULT: FAIL")
    sys.exit(0 if n_bad == 0 else 1)


if __name__ == "__main__":
    main()

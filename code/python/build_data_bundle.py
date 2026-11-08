#!/usr/bin/env python3
"""Build the collaborator data bundle, data/MANIFEST.csv and the exclusion list.

Usage (from the project root):
    python3 -I code/python/build_data_bundle.py <YYYY-MM-DD>

Writes:
    release/data_bundle_<date>.zip                 gitignored data the pipeline needs, repo-relative paths
    data/MANIFEST.csv                              path, size, sha256 of every file in the zip (committed)
    logs/<date>/data_bundle_exclusions.csv         every file left out, with the rule and reason
    logs/<date>/data_manifest_receipt_check.csv    each bundled file's hash against the receipts

What goes in: every file under data/raw/ and data/out/, plus the gitignored side
tables in data/ (data/*.csv) that the R and Python scripts read. Nothing that git
tracks goes in; the collaborator gets those from the clone.

The hashes are checked against what the receipts recorded: data/FILE_INVENTORY.csv,
logs/2026-11-04/raw_sha256_manifest.csv and the SHA-256 values in data/receipts/*.md.
A file whose hash disagrees with a receipt stops the build (exit 1). Files no receipt
records (mostly derived tables, which change on rebuild) are listed as not_recorded.

The build also stops if any bundled file contains the Census key from .env (the key
is read into memory only, never printed) or if a file matches an exclusion rule.
"""
import csv
import fnmatch
import hashlib
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path.cwd()

# Exclusion rules: (glob on repo-relative path, category, reason). First match wins.
# Applied to the candidate set (data/raw, data/out, data/*.csv).
EXCLUDE_RULES = [
    ("*/_to_delete/*", "_to_delete", "Holding folder for files awaiting deletion; duplicates or mistaken downloads, not used"),
    ("*/_unsorted/*", "_unsorted", "Unfiled material; not used by the pipeline"),
    ("data/raw/bloomberg/*", "licensed", "Bloomberg data, Emory-licensed; can't be redistributed"),
    ("data/raw/sec/cache/*", "licensed/personal", "SEC API cache; carries the personal SEC_USER_AGENT; rebuild with sec_fin.py"),
    ("*.env", "secret", "Environment file with keys"),
    ("*/.DS_Store", "os_junk", "macOS folder metadata"),
    ("*/._*", "os_junk", "macOS AppleDouble resource-fork file, not data"),
    ("*/~$*", "os_junk", "Office lock file left by an open workbook, not data"),
]

# Files outside the candidate set that are deliberately not shared. Listed so the
# exclusion log is complete; none of them is under data/raw or data/out.
NOT_SHARED = [
    # (glob, category, reason, itemize): itemize=False writes one row per folder with a file count.
    (".env", "secret", "Census API key; each collaborator makes their own from .env.example", True),
    ("literature/*", "journal_pdf", "Journal articles and publisher supplements (Emory Libraries access); get them by DOI, see README", True),
    ("notes/Grijalva_interview_transcript_*", "interview", "Interview transcript; private to the team", True),
    ("notes/*.pdf", "methods_memo", "Methods Memo PDF; course document, ask the team", True),
    ("archive/*", "private", "Saved Claude chats", False),
    ("_to_delete/*", "_to_delete", "Holding folder for files awaiting deletion", True),
    ("data/data_download_all_pt1.zip", "duplicate", "Phase 1 zip of downloads; duplicates data/raw/, no script reads it", True),
    ("data/bea/*", "duplicate", "Phase 1 human-readable copy of data/raw/bea/; no script reads it", False),
    ("data/bls/*", "duplicate", "Phase 1 human-readable copy of data/raw/bls/; no script reads it", False),
    ("data/census/*", "duplicate", "Phase 1 human-readable copy of data/raw/census/; no script reads it", False),
    ("data/eia/*", "duplicate", "Phase 1 human-readable copy of data/raw/eia/; no script reads it", False),
    ("data/ferc/*", "duplicate", "Phase 1 human-readable copy of data/raw/pudl/ outputs; no script reads it", False),
    ("outputs/*", "rebuilt", "Workbooks and reports; rebuilt by code/python/build_master_workbook.py and companions", False),
    ("release/*", "rebuilt", "Packages; rebuilt by script", False),
]

HEX64 = re.compile(r"\b[0-9a-f]{64}\b")
TOKEN = re.compile(r"`([^`]+)`")


def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(buf), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return p.relative_to(ROOT).as_posix()


def git_ignored(paths):
    """Return the subset of repo-relative paths that git ignores."""
    if not paths:
        return set()
    out = subprocess.run(["git", "check-ignore", "--stdin", "-z"], input="\0".join(paths) + "\0",
                         capture_output=True, text=True, cwd=ROOT)
    return {p for p in out.stdout.split("\0") if p}


def rule_for(path, rules):
    for pat, cat, why in rules:
        if fnmatch.fnmatchcase(path, pat) or fnmatch.fnmatchcase("./" + path, pat):
            return cat, why
    return None


def candidates():
    files = []
    for top in ("data/raw", "data/out"):
        for dirpath, _, names in os.walk(ROOT / top):
            for n in names:
                files.append(rel(Path(dirpath) / n))
    files += [rel(p) for p in (ROOT / "data").glob("*.csv")]
    return sorted(set(files))


def receipt_hashes():
    """Map path (or bare filename) -> set of hashes recorded in the receipts."""
    by_path, by_name = {}, {}

    def add(key, h, table):
        table.setdefault(key, set()).add(h)

    inv = ROOT / "data/FILE_INVENTORY.csv"
    with open(inv, newline="") as f:
        for r in csv.DictReader(f):
            add(r["path"], r["sha256"], by_path)
    base = ROOT / "logs/2026-11-04/raw_sha256_manifest.csv"
    if base.exists():
        with open(base, newline="") as f:
            for r in csv.DictReader(f):
                add(r["path"], r["sha256"], by_path)
    for md in sorted((ROOT / "data/receipts").glob("*.md")):
        for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
            hs = HEX64.findall(line)
            if not hs:
                continue
            for tok in TOKEN.findall(line):
                if HEX64.fullmatch(tok):
                    continue
                for h in hs:
                    if tok.startswith("data/"):
                        add(tok, h, by_path)
                    else:
                        add(Path(tok).name, h, by_name)
    return by_path, by_name


def census_key():
    env = ROOT / ".env"
    if not env.exists():
        return None
    for ln in env.read_text().splitlines():
        m = re.match(r"\s*CENSUS_KEY\s*=\s*(.*?)\s*$", ln)
        if m and m.group(1).strip('"\''):
            return m.group(1).strip('"\'').encode()
    return None


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        sys.exit("usage: build_data_bundle.py <YYYY-MM-DD>   (run from the project root)")
    date = sys.argv[1]
    for need in ("data/raw", "data/out", "data/receipts", "data/FILE_INVENTORY.csv", ".git"):
        if not (ROOT / need).exists():
            sys.exit(f"missing {need}: run from the project root")

    cand = candidates()
    ignored = git_ignored(cand)
    include, excluded = [], []
    for p in cand:
        hit = rule_for(p, EXCLUDE_RULES)
        if hit:
            excluded.append((p, *hit))
        elif p not in ignored:
            pass  # tracked by git: the collaborator gets it from the clone
        else:
            include.append(p)

    # Out-of-scope items that are not shared, expanded to the files that exist.
    for pat, cat, why, itemize in NOT_SHARED:
        g = pat[:-1] + "**/*" if pat.endswith("/*") else pat
        hits = sorted(rel(q) for q in ROOT.glob(g) if q.is_file() and q.name != ".DS_Store")
        if not hits:
            continue
        if itemize:
            excluded += [(h, cat, why) for h in hits if not any(h == e[0] for e in excluded)]
        else:
            excluded.append((pat, cat, f"{why} ({len(hits)} files)"))
    # Rules that matched nothing still go in the log so the reader sees they were applied.
    for pat, cat, why, *_ in EXCLUDE_RULES + NOT_SHARED:
        if not any(e[0] == pat or fnmatch.fnmatchcase(e[0], pat) for e in excluded):
            excluded.append((pat + "  (no such file here)", cat, why))

    # Hash, size, receipt check.
    by_path, by_name = receipt_hashes()
    rows, checks, bad = [], [], []
    for p in include:
        fp = ROOT / p
        h, n = sha256(fp), fp.stat().st_size
        rows.append((p, n, h))
        rec = by_path.get(p) or by_name.get(Path(p).name)
        if not rec:
            status, recorded = "not_recorded", ""
        elif h in rec:
            status, recorded = "match", h
        else:
            status, recorded = "MISMATCH", ";".join(sorted(rec))
            bad.append(p)
        checks.append((p, h, recorded, status))

    # Secret scan: the Census key must not appear in any bundled file.
    key = census_key()
    leaks = []
    if key:
        for p, _, _ in rows:
            with open(ROOT / p, "rb") as f:
                if key in f.read():
                    leaks.append(p)

    logdir = ROOT / "logs" / date
    logdir.mkdir(parents=True, exist_ok=True)
    with open(logdir / "data_manifest_receipt_check.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "sha256", "receipt_sha256", "status"])
        w.writerows(checks)
    with open(logdir / "data_bundle_exclusions.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "category", "reason"])
        w.writerows(sorted(excluded, key=lambda e: (e[1], e[0])))

    if leaks:
        sys.exit(f"STOP: the Census key appears in {len(leaks)} bundled file(s): {leaks}")
    if bad:
        sys.exit(f"STOP: {len(bad)} file(s) disagree with their receipt hash; see "
                 f"{rel(logdir / 'data_manifest_receipt_check.csv')}: {bad[:10]}")

    with open(ROOT / "data/MANIFEST.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["path", "size", "sha256"])
        w.writerows(rows)

    out = ROOT / "release" / f"data_bundle_{date}.zip"
    out.parent.mkdir(exist_ok=True)
    tmp = out.with_suffix(".zip.part")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        for p, _, _ in rows:
            z.write(ROOT / p, arcname=p)
    tmp.replace(out)

    tot = sum(n for _, n, _ in rows)
    st = {s: sum(1 for c in checks if c[3] == s) for s in ("match", "not_recorded", "MISMATCH")}
    print(f"bundle: {rel(out)}  {out.stat().st_size / 1e6:,.1f} MB zipped, "
          f"{len(rows)} files, {tot / 1e6:,.1f} MB unzipped")
    print(f"receipt check: {st['match']} match, {st['not_recorded']} not recorded, {st['MISMATCH']} mismatch")
    print(f"excluded: {len(excluded)} entries -> {rel(logdir / 'data_bundle_exclusions.csv')}")
    print(f"census key scan: {'clean' if key else 'no key in .env, scan skipped'}")


if __name__ == "__main__":
    main()

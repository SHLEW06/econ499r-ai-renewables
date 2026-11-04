#!/usr/bin/env python3
"""Check every hyperlink in an .xlsx by reading its XML. Read-only. Works on a copy under any name, anywhere.
Usage: python3 code/python/check_workbook_links.py <workbook.xlsx>

Fails (exit 1) if a hyperlink:
  - has a target containing a local home path, "file:" or "../"
  - has "%" in its location
  - points to a sheet that doesn't exist, or outside that sheet's used range
  - has both a location and a target (how LibreOffice rewrites internal links)
  - has an unquoted location, a target that isn't http(s), or a relationship id that doesn't resolve
Also fails if any part of the file holds a local home path or an external workbook link.
Reports counts by type: internal, github_receipt, web, and any local or broken links."""
import collections, html, posixpath, re, sys, zipfile
import xml.etree.ElementTree as ET

REPO_BLOB = "https://github.com/SHLEW06/econ499r-ai-renewables/blob/main/"
HOME = "/" + "Users/"  # split so the clean-copy path scan doesn't flag this file
BAD_TARGET = (HOME, "file:", "../")
LOCATION = re.compile(r"^'((?:[^']|'')+)'!\$?([A-Z]{1,3})\$?([0-9]+)$")
RECEIPT = re.compile(re.escape(REPO_BLOB) + r"data/receipts/[A-Za-z0-9_.-]+\.md$")
NS_M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_P = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CELL = re.compile(rb'<c\b[^>]*?\br="([A-Z]+)([0-9]+)"')


def col_num(s):
    n = 0
    for ch in s:
        n = n * 26 + ord(ch) - 64
    return n


def sheet_parts(z):
    """{sheet name: part path inside the zip}, in workbook order."""
    rel = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    out = {}
    for s in ET.fromstring(z.read("xl/workbook.xml")).find(f"{NS_M}sheets"):
        t = rel[s.get(f"{NS_R}id")]
        out[s.get("name")] = t.lstrip("/") if t.startswith("/") else posixpath.join("xl", t)
    return out


def _used(z, part, cache):
    if part not in cache:
        hits = CELL.findall(z.read(part))
        if hits:
            cols = {c for c, _ in hits}; rows = [int(r) for _, r in hits]
            nums = [col_num(c.decode()) for c in cols]
            cache[part] = (min(nums), max(nums), min(rows), max(rows))
        else:
            cache[part] = None
    return cache[part]


def _hyperlinks(data):
    m = re.search(rb"<hyperlinks>.*?</hyperlinks>", data, re.S)
    if not m:
        return []
    root = ET.fromstring(b'<x xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">' + m.group(0) + b"</x>")
    return list(root.iter("hyperlink")) + list(root.iter(f"{NS_M}hyperlink"))


def check(path):
    """Returns dict(counts, by_sheet, problems, links). links: sheet, ref, type, target, location."""
    links, problems = [], []
    used = {}
    with zipfile.ZipFile(path) as z:
        parts = sheet_parts(z)
        names = set(z.namelist())
        for sheet, part in parts.items():
            data = z.read(part)
            relp = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
            rels = {}
            if relp in names:
                rels = {r.get("Id"): r for r in ET.fromstring(z.read(relp)) if r.tag == f"{NS_P}Relationship"}
            for h in _hyperlinks(data):
                ref, rid, loc = h.get("ref"), h.get(f"{NS_R}id"), h.get("location")
                target = None
                row = dict(sheet=sheet, ref=ref, type="", target="", location=loc or "")
                bad = lambda why: problems.append(f"{sheet}!{ref}: {why}")
                if rid:
                    if rid not in rels:
                        bad(f"relationship {rid} doesn't resolve")
                    else:
                        target = rels[rid].get("Target"); row["target"] = target
                if target is not None:
                    low = html.unescape(target).lower()
                    for b in BAD_TARGET:
                        if b.lower() in low:
                            bad(f"target contains {b!r}: {target[:90]}")
                    if not low.startswith(("https://", "http://")):
                        bad(f"target isn't http(s): {target[:90]}")
                    if loc:
                        bad(f"has both a target and a location: {target[:60]} + {loc}")
                    row["type"] = "github_receipt" if target.startswith(REPO_BLOB) else ("web" if low.startswith(("https://", "http://")) else "local")
                    if target.startswith(REPO_BLOB) and not RECEIPT.match(target):
                        bad(f"GitHub link isn't a receipt path: {target}")
                elif loc:
                    row["type"] = "internal"
                else:
                    if rid is None:
                        bad("no location and no target")
                    row["type"] = "broken"
                if loc:
                    if "%" in loc:
                        bad(f"'%' in location: {loc}")
                    m = LOCATION.match(loc)
                    if not m:
                        bad(f"location isn't 'Sheet Name'!A1: {loc}")
                    else:
                        dest = m.group(1).replace("''", "'")
                        if dest not in parts:
                            bad(f"sheet doesn't exist: {dest}")
                        else:
                            u = _used(z, parts[dest], used)
                            c, r = col_num(m.group(2)), int(m.group(3))
                            if u is None:
                                bad(f"target sheet is empty: {loc}")
                            elif not (u[0] <= c <= u[1] and u[2] <= r <= u[3]):
                                bad(f"outside used range of {dest}: {loc}")
                links.append(row)
        # the rest of the package
        for n in sorted(names):
            if n.startswith("xl/externalLinks/"):
                problems.append(f"{n}: external workbook link")
            elif z.read(n).find(HOME.encode()) >= 0:
                problems.append(f"{n}: holds a local home path")
    counts = collections.Counter(l["type"] for l in links)
    by_sheet = collections.Counter((l["sheet"], l["type"]) for l in links)
    return dict(counts=dict(counts), by_sheet=dict(by_sheet), problems=problems, links=links)


def report(res, out=sys.stdout):
    c = res["counts"]
    print("Links by type:", file=out)
    for k in ("internal", "github_receipt", "web", "local", "broken"):
        if k in c or k not in ("local", "broken"):
            print(f"  {k:<15}{c.get(k, 0):>7,}", file=out)
    print(f"  {'total':<15}{sum(c.values()):>7,}", file=out)
    print("By sheet:", file=out)
    for (s, t), n in sorted(res["by_sheet"].items()):
        print(f"  {s:<18}{t:<15}{n:>7,}", file=out)
    print(f"Problems: {len(res['problems'])}", file=out)
    for p in res["problems"][:25]:
        print("  " + p, file=out)
    if len(res["problems"]) > 25:
        print(f"  ... and {len(res['problems']) - 25} more", file=out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    r = check(sys.argv[1]); report(r)
    print("LINK CHECK", "PASSED" if not r["problems"] else "FAILED")
    sys.exit(1 if r["problems"] else 0)

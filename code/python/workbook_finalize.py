"""Write the final workbook without LibreOffice ever saving it.

LibreOffice rewrites internal hyperlinks into external links to the file's own path. So:
  1. Recalculate a COPY of the openpyxl build with LibreOffice.
  2. Read only the formula results from that copy, and stop on any formula error.
  3. Copy those results into the openpyxl build's XML as cached values. Nothing else changes.
  4. Run the link check on the result. Install it over the final path only if it passes.
Used by build_master_workbook.py."""
import csv, os, re, shutil, subprocess, sys, tempfile, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_workbook_links as CL

FCELL = re.compile(r'<c\b([^>]*)>(<f\b[^>]*?(?:/>|>.*?</f>))(?:<v>(.*?)</v>|<v\s*/>)?</c>', re.S)
COORD = re.compile(r'\br="([A-Z]+[0-9]+)"')
TYPE = re.compile(r'\s+t="(\w+)"')


def recalc_copy(src, outdir):
    """LibreOffice converts a copy into outdir, with its own throwaway profile. src isn't touched."""
    soffice = shutil.which("soffice") or sys.exit("soffice not found")
    work = os.path.join(outdir, "input"); os.makedirs(work, exist_ok=True)
    copy = os.path.join(work, os.path.basename(src)); shutil.copy(src, copy)
    profile = "-env:UserInstallation=file://" + os.path.abspath(os.path.join(outdir, "lo_profile"))
    subprocess.run([soffice, profile, "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", outdir, copy], check=True, capture_output=True, timeout=1500)
    out = os.path.join(outdir, os.path.basename(src))
    if not os.path.exists(out):
        sys.exit("LibreOffice produced no recalculated copy")
    return out


def formula_cache(path):
    """{sheet: {cell: (type, raw value xml)}} for every formula cell."""
    out = {}
    with zipfile.ZipFile(path) as z:
        for sheet, part in CL.sheet_parts(z).items():
            s = z.read(part).decode("utf-8")
            if "<f" not in s:
                continue
            d = {}
            for m in FCELL.finditer(s):
                t = TYPE.search(m.group(1))
                d[COORD.search(m.group(1)).group(1)] = (t.group(1) if t else "n", m.group(3))
            if d:
                out[sheet] = d
    return out


def inject(built, cache, out):
    """Copy built to out, adding cached values to its formula cells. Returns dict of counts and problems."""
    st = dict(formula_cells=0, injected=0, missing=[], errors=[], by_sheet={})
    with zipfile.ZipFile(built) as zi, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
        part_sheet = {p: n for n, p in CL.sheet_parts(zi).items()}
        for item in zi.infolist():
            data = zi.read(item.filename)
            sheet = part_sheet.get(item.filename)
            if sheet is not None and b"<f" in data:
                vals = cache.get(sheet, {})
                count = [0]

                def rep(m):
                    attrs, f = m.group(1), m.group(2)
                    coord = COORD.search(attrs).group(1)
                    count[0] += 1; st["formula_cells"] += 1
                    t, v = vals.get(coord, (None, None))
                    if v is None and t != "str":
                        st["missing"].append(f"{sheet}!{coord}")
                        return m.group(0)
                    if t == "e":
                        st["errors"].append(f"{sheet}!{coord}: {v}")
                    st["injected"] += 1
                    a = TYPE.sub("", attrs)
                    tt = "" if t == "n" else f' t="{t}"'
                    return f"<c{a}{tt}>{f}<v>{v or ''}</v></c>"

                data = FCELL.sub(rep, data.decode("utf-8")).encode("utf-8")
                if count[0]:
                    st["by_sheet"][sheet] = count[0]
            zo.writestr(item, data)
    return st


def uncached(path):
    """Formula cells with no cached value, and cached formula errors, in a final file."""
    miss, err, n = [], [], 0
    with zipfile.ZipFile(path) as z:
        for sheet, part in CL.sheet_parts(z).items():
            s = z.read(part).decode("utf-8")
            if "<f" not in s:
                continue
            for m in FCELL.finditer(s):
                n += 1
                t = TYPE.search(m.group(1)); t = t.group(1) if t else "n"
                if m.group(3) is None or (m.group(3) == "" and t != "str"):
                    miss.append(f"{sheet}!{COORD.search(m.group(1)).group(1)}")
                if t == "e":
                    err.append(f"{sheet}!{COORD.search(m.group(1)).group(1)}")
    return dict(formula_cells=n, missing=miss, errors=err)


def app_name(path):
    with zipfile.ZipFile(path) as z:
        m = re.search(r"<Application>(.*?)</Application>", z.read("docProps/app.xml").decode("utf-8"))
    return m.group(1) if m else ""


def finalize(built, final, links_csv):
    """built: openpyxl's file. final: the installed path. Exits nonzero, leaving final as it was, on any failure."""
    tmp = tempfile.mkdtemp(prefix="wb_recalc_")
    candidate = final + ".building"
    try:
        t0 = time.time(); rc = recalc_copy(built, tmp)
        print(f"recalculated a copy in {int(time.time() - t0)} s; LibreOffice's file is used only for checks and cached values", flush=True)
        st = inject(built, formula_cache(rc), candidate)
        print(f"formula cells {st['formula_cells']:,}; cached values added {st['injected']:,}; by sheet {st['by_sheet']}", flush=True)
        if st["errors"]:
            sys.exit(f"formula errors after recalculation, not installed: {st['errors'][:8]}")
        if st["missing"]:
            sys.exit(f"formula cells with no recalculated value, not installed: {st['missing'][:8]}")
        res = CL.check(candidate); CL.report(res)
        with open(links_csv, "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["sheet", "type", "links"])
            for (s, t), n in sorted(res["by_sheet"].items()):
                w.writerow([s, t, n])
        if res["problems"]:
            sys.exit(f"link check failed, not installed: {len(res['problems'])} problems")
        os.replace(candidate, final)  # atomic: a reader never sees a partial file
        print("installed", final, round(os.path.getsize(final) / 1e6, 1), "MB", flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        if os.path.exists(candidate):
            os.remove(candidate)

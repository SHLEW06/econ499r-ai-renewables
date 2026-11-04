"""Shared lookup for every number in findings, the project summary and the PDF report.

Each number is read from a result file at the moment it's inserted, and logged with its source and tag.
check() then re-reads the source, confirms the text appears in the document, and lists any decimal or
comma number in the document that was not logged, so a typed number can't slip through.
"""
import os, re
import pandas as pd

_cache = {}
def table(path):
    if path not in _cache:
        _cache[path] = pd.read_csv(path)
    return _cache[path]


class Ledger:
    def __init__(self, doc):
        self.doc = doc; self.rows = []

    def _row(self, _src, **f):
        d = table(_src)
        for k, v in f.items():
            d = d[d[k] == v]
        if len(d) != 1:
            raise ValueError(f"{_src} {f}: {len(d)} rows")
        return d.iloc[0]

    def n(self, _src, col, fmt="{:.4f}", scale=1.0, **f):
        r = self._row(_src, **f); raw = float(r[col]) * scale; s = fmt.format(raw)
        self.rows.append(dict(document=self.doc, number=s, source_file=_src, tag=r.get("tag", str(f)), column=col, scale=scale, filters=repr(f), fmt=fmt)); return s

    def p(self, _src, col="pval", **f):
        r = self._row(_src, **f); v = float(r[col]); s = "p < 0.001" if v < .001 else f"p = {v:.3f}"
        self.rows.append(dict(document=self.doc, number=s.split(" ")[-1], source_file=_src, tag=r.get("tag", str(f)), column=col, scale=1.0, filters=repr(f), fmt="p")); return s

    def typed(self, s, source):
        """A published number from a paper or report, with its location."""
        self.rows.append(dict(document=self.doc, number=s, source_file=source, tag="published", column="", scale=1.0, filters="", fmt="typed")); return s

    def check(self, text):
        out = []
        for r in self.rows:
            ok_doc = r["number"] in text
            if r["fmt"] == "typed":
                match = "published; check by hand"
            else:
                row = self._row(r["source_file"], **eval(r["filters"])); v = float(row[r["column"]])
                if r["fmt"] == "p":
                    match = "yes" if (r["number"] == "0.001" and v < .001) or f"{v:.3f}" == r["number"] else "NO"
                else:
                    match = "yes" if r["fmt"].format(v * r["scale"]) == r["number"] else "NO"
            out.append(dict(number=r["number"], document=r["document"], source_file=r["source_file"], source_tag=r["tag"], column=r["column"], in_document="yes" if ok_doc else "NO", match=match))
        logged = {r["number"].lstrip("+-−$") for r in self.rows} | {"1,000"}  # "per 1,000" is a unit, not a result
        for tok in sorted(set(re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+", text))):
            if tok not in logged and not any(tok in x for x in logged):
                out.append(dict(number=tok, document=self.doc, source_file="", source_tag="", column="", in_document="yes", match="UNLOGGED"))
        return pd.DataFrame(out)

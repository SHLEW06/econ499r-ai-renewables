"""Helpers for notebooks/ECON499R_explained.ipynb.

Every number shown in the notebook's text and tables goes through a Tracer method, which
reads it from a results file at the moment it is written and logs the file, the row
filters, the column and the format. check() re-reads every source, confirms the shown
text still matches, and lists any decimal number in the notebook text that was not
logged. Acronyms are spelled out automatically on first use in each section and in
every table.
"""
import json, math, os, re, html as _html
import pandas as pd, numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML

# ---- colors: the dataviz reference palette, first three categorical slots (validated all-pairs) ----
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"

mpl.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 10, "axes.titlesize": 11,
    "axes.titleweight": "bold", "axes.labelsize": 10, "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "legend.frameon": False, "legend.fontsize": 9.5, "font.family": "DejaVu Sans",
})

# ---- acronyms: spelled out on first use in each section and in each table ----
ACRONYMS = {
    "NAICS 518210": "North American Industry Classification System code 518210, Computing Infrastructure Providers, Data Processing, Web Hosting",
    "NAICS": "North American Industry Classification System",
    "AI": "artificial intelligence",
    "EIA": "U.S. Energy Information Administration",
    "SEDS": "State Energy Data System",
    "BLS": "Bureau of Labor Statistics",
    "QCEW": "Quarterly Census of Employment and Wages",
    "BEA": "Bureau of Economic Analysis",
    "EPU": "Economic Policy Uncertainty index",
    "LBNL": "Lawrence Berkeley National Laboratory",
    "RPS": "Renewable Portfolio Standard",
    "CES": "Clean Energy Standard",
    "NOAA": "National Oceanic and Atmospheric Administration",
    "HDD": "heating degree days",
    "CDD": "cooling degree days",
    "PTC": "Production Tax Credit",
    "ITC": "Investment Tax Credit",
    "IRP": "Integrated Resource Plan",
    "PSC": "Public Service Commission",
    "IEA": "International Energy Agency",
    "LCOE": "levelized cost of energy",
    "OEWS": "Occupational Employment and Wage Statistics",
    "BTOS": "Business Trends and Outlook Survey",
    "USPTO": "U.S. Patent and Trademark Office",
    "NCSES": "National Center for Science and Engineering Statistics",
    "NSF": "National Science Foundation",
    "ACS": "American Community Survey",
    "CRS": "Congressional Research Service",
    "OWID": "Our World in Data",
    "IRENA": "International Renewable Energy Agency",
    "WEO": "World Energy Outlook",
    "GDP": "gross domestic product",
    "CO2": "carbon dioxide",
    "R&D": "research and development",
    "SD": "standard deviation",
    "IV": "instrumental variable",
    "SLX": "spatial lag of X model",
    "SDM": "spatial Durbin model",
    "OLS": "ordinary least squares",
    "RFP": "request for proposals",
    "PV": "photovoltaic",
    "MWh": "megawatt-hours",
    "MW": "megawatts",
    "GW": "gigawatts",
    "TWh": "terawatt-hours",
    "kWh": "kilowatt-hour",
    "Btu": "British thermal units",
    "DC": "District of Columbia",
    "PDF": "Portable Document Format",
    "FAQ": "frequently asked questions",
    "CC BY": "Creative Commons Attribution license",
}
_KEYS = sorted(ACRONYMS, key=len, reverse=True)
_PROTECT = re.compile(r"(\$\$.+?\$\$|\$[^$\n]+?\$|`[^`]*`|\]\([^)]*\)|<[^>]+>|https?://\S+)", re.S)


def _expand(text, seen):
    bad = [c for c in "\t\r\b\f\a\v" if c in text]
    if bad:   # a LaTeX command lost its backslash to a Python escape (\times -> tab)
        raise ValueError(f"control character {bad!r} in text: {text[:120]!r}")
    parts = _PROTECT.split(text)
    out = []
    for i, seg in enumerate(parts):
        if i % 2 == 1:          # protected: math, code, link targets, HTML tags, URLs
            out.append(seg); continue
        for k in _KEYS:
            if k in seen:
                continue
            m = re.search(r"(?<![\w&])" + re.escape(k) + r"(?![\w&])", seg)
            if not m:
                continue
            full = ACRONYMS[k]
            before = ("".join(out) + seg[:m.start()]).lower()
            if before.rstrip().endswith(full.lower() + " (") or seg[m.end():].lower().startswith(f" ({full.lower()})"):
                seen.add(k)                    # already written as "full name (ACR)" or "ACR (full name)"
                if k == "NAICS 518210":
                    seen.add("NAICS")
                continue
            seg = seg[:m.end()] + f" ({full})" + seg[m.end():]
            seen.add(k)
            if k == "NAICS 518210":
                seen.add("NAICS")
        out.append(seg)
    return "".join(out)


def deexpand(text):
    """Text with the inserted ' (full name)' expansions removed, for matching logged strings."""
    for k in _KEYS:
        text = text.replace(f" ({ACRONYMS[k]})", "")
    return text


# ---- number formatting ----
MINUS = "−"

def fmt(x, sig=3, dec=None, plus=False, kind="num"):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    if kind == "int":
        s = f"{int(round(x)):,}"
    elif dec is not None:
        s = f"{abs(x):,.{dec}f}"
    elif x == 0:
        s = "0"
    else:
        d = max(0, sig - 1 - int(math.floor(math.log10(abs(x)))))
        s = f"{abs(round(x, d)):,.{d}f}"
    if kind != "int":
        if x < 0 and s.strip("0.,") != "":
            s = MINUS + s
        elif plus and x > 0:
            s = "+" + s
    return s


def fmt_p(v):
    return "p < 0.001" if v < 0.001 else f"p = {v:.3f}"


_cache = {}
def tbl(path):
    if path not in _cache:
        _cache[path] = pd.read_csv(path)
    return _cache[path]


class Tracer:
    def __init__(self, doc, outdir):
        self.doc, self.outdir = doc, outdir
        self.rows, self.texts = [], []
        self.sec, self.seen = "0", set()
        self.n_tables = self.n_figs = 0

    # -- reading --
    def row(self, src, **f):
        d = tbl(src)
        for k, val in f.items():
            d = d[d[k].astype(str) == val] if isinstance(val, str) else d[d[k] == val]
        if len(d) != 1:
            raise ValueError(f"{src} {f}: {len(d)} rows")
        return d.iloc[0]

    def _log(self, number, src, col, f, spec):
        r = self.row(src, **f)
        self.rows.append(dict(document=self.doc, section=self.sec, number=number, source_file=src,
                              tag=str(r["tag"]) if "tag" in r.index else json.dumps(f), column=col,
                              filters=json.dumps(f), spec=json.dumps(spec)))
        return number

    def v(self, src, col, sig=3, dec=None, scale=1.0, plus=False, **f):
        """A number, 3 significant figures by default (or fixed decimals), times scale."""
        x = float(self.row(src, **f)[col]) * scale
        s = fmt(x, sig=sig, dec=dec, plus=plus)
        return self._log(s, src, col, f, dict(kind="num", sig=sig, dec=dec, scale=scale, plus=plus))

    def n(self, src, col, **f):
        s = fmt(float(self.row(src, **f)[col]), kind="int")
        return self._log(s, src, col, f, dict(kind="int"))

    def p(self, src, col="pval", **f):
        s = fmt_p(float(self.row(src, **f)[col]))
        return self._log(s, src, col, f, dict(kind="p"))

    def s(self, src, col, **f):
        """A text cell from a file (filing figures and page numbers), shown verbatim."""
        s = str(self.row(src, **f)[col])
        return self._log(s, src, col, f, dict(kind="text"))

    def raw(self, src, col, **f):
        """A value for charts or arithmetic; not shown as text, so not logged."""
        return float(self.row(src, **f)[col])

    # -- display --
    def section(self, num, title):
        self.sec, self.seen = str(num), set()
        self.md(f"# {num}. {title}" if num != "" else f"# {title}")

    def md(self, text):
        text = _expand(text, self.seen)
        self.texts.append(dict(section=self.sec, kind="md", text=text))
        display(Markdown(text))

    def table(self, header, rows, caption, note=None, widths=None):
        self.n_tables += 1
        seen = set()
        cap = _expand(f"Table {self.n_tables}. {caption}", seen)
        hdr = [_expand(h, seen) for h in header]
        body = [[_expand(str(c), seen) for c in r] for r in rows]
        nt = _expand(note, seen) if note else None
        def esc(s):
            s = _html.escape(s)
            return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        if widths is None and len(header) == 2:
            widths = [27, 73]
        style = ' style="table-layout: fixed"' if widths else ""
        h = [f'<table class="ex"{style}>', f'<caption>{esc(cap)}</caption>']
        if widths:
            h.append("<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>")
        h.append("<thead><tr>")
        h += [f"<th>{esc(x)}</th>" for x in hdr] + ["</tr></thead><tbody>"]
        for r in body:
            h.append("<tr>" + "".join(f'<td class="nw">{esc(c)}</td>' if len(c) <= 14 and " " not in c.strip() or re.fullmatch(r"p [=<] [\d.]+|\d{4}-\d{4}", c) else f"<td>{esc(c)}</td>" for c in r) + "</tr>")
        h.append("</tbody></table>")
        if nt:
            h.append(f'<p class="tnote">{esc(nt)}</p>')
        txt = "\n".join([cap, " | ".join(hdr)] + [" | ".join(r) for r in body] + ([nt] if nt else []))
        self.texts.append(dict(section=self.sec, kind="table", text=txt))
        display(HTML("\n".join(h)))

    def deflist(self, items, caption):
        """A two-column list of term: definition (used for the glossary)."""
        seen = set()
        cap = _expand(caption, seen)
        out, txt = [], [cap]
        for term, d in items:
            t2, d2 = _expand(term, seen), _expand(d, seen)
            out.append(f"<p class='gl'><b>{_html.escape(t2)}.</b> {_html.escape(d2)}</p>")
            txt.append(f"{t2}. {d2}")
        self.texts.append(dict(section=self.sec, kind="list", text="\n".join(txt)))
        display(HTML(f"<p class='tnote'><b>{_html.escape(cap)}</b></p><div class='glossary'>" + "".join(out) + "</div>"))

    def fig(self, fig, caption):
        self.n_figs += 1
        fig.tight_layout()
        plt.show()
        cap = _expand(f"Figure {self.n_figs}. {caption}", set())
        self.texts.append(dict(section=self.sec, kind="figcap", text=cap))
        display(HTML(f'<p class="figcap">{_html.escape(cap)}</p>'))

    # -- checking --
    CONVENTIONS = {"0.05", "0.10", "0.1", "0.25", "1.645", "1.96", "0.025", "0.975"}

    def check(self):
        out = []
        for r in self.rows:
            f, spec = json.loads(r["filters"]), json.loads(r["spec"])
            row = self.row(r["source_file"], **f)
            if spec["kind"] == "text":
                again = str(row[r["column"]])
            elif spec["kind"] == "p":
                again = fmt_p(float(row[r["column"]]))
            elif spec["kind"] == "int":
                again = fmt(float(row[r["column"]]), kind="int")
            else:
                again = fmt(float(row[r["column"]]) * spec["scale"], sig=spec["sig"], dec=spec["dec"], plus=spec["plus"])
            alltext = deexpand("\n".join(t["text"] for t in self.texts))
            out.append(dict(r, recomputed=again, match="yes" if again == r["number"] else "NO",
                            in_notebook_text="yes" if r["number"] in alltext else "NO"))
        ck = pd.DataFrame(out)
        logged = {re.sub(r"^p [=<] ", "", x).lstrip("+" + MINUS + "-$") for x in ck.number}
        unlogged = []
        for t in self.texts:
            body = re.sub(r"Table \d+\.|Figure \d+\.|^#+ [\d.]+|[Ss]ections? \d+(\.\d+)?", "", t["text"], flags=re.M)
            for tok in set(re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+", body)):
                if tok in self.CONVENTIONS or tok in logged or any(tok in x for x in logged):
                    continue
                unlogged.append(dict(section=t["section"], token=tok, context=body[max(0, body.find(tok) - 60): body.find(tok) + 40]))
        os.makedirs(self.outdir, exist_ok=True)
        ck["status"] = np.where((ck.match == "yes") & (ck.in_notebook_text == "yes"), "ok", "FAILED")
        ck.to_csv(os.path.join(self.outdir, "number_check.csv"), index=False)
        pd.DataFrame(unlogged, columns=["section", "token", "context"]).to_csv(os.path.join(self.outdir, "number_check_unlogged.csv"), index=False)
        return ck, pd.DataFrame(unlogged)


# ---- charts ----
def coefplot(ax, labels, est, lo, hi, colors=None, unit="", ref=None, ref_label=None):
    """Horizontal coefficient plot: dot = estimate, line = 95% confidence interval, zero line."""
    y = np.arange(len(labels))[::-1]
    colors = colors or [BLUE] * len(labels)
    ax.axvline(0, color=INK2, lw=1.1, zorder=1)
    if ref is not None:
        ax.axvline(ref, color=ORANGE, lw=1.4, ls="--", zorder=1)
        if ref_label:
            ax.annotate(ref_label, (ref, 1.0), xycoords=("data", "axes fraction"), xytext=(4, -2),
                        textcoords="offset points", fontsize=8.5, color=INK2, va="top")
    for yi, e, l, h, c in zip(y, est, lo, hi, colors):
        ax.plot([l, h], [yi, yi], color=c, lw=2.2, solid_capstyle="round", zorder=2)
        ax.plot([e], [yi], "o", color=c, ms=7, mec="white", mew=1.5, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.grid(axis="y", visible=False)
    if unit:
        ax.set_xlabel(unit)
    return ax

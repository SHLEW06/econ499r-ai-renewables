#!/usr/bin/env python3
"""Build the Fang test side tables and panel (Phase 4h, Part A). Does not change the master panel.

Usage: build_fang_tables.py <raw_dir> <data_dir> <log_dir>

Writes to <data_dir>: ai_job_postings_state.csv, ai_job_postings_overlap_rows.csv,
seds_renewables_state.csv, ncses_bachelors_state.csv, fang_split_vars.csv, fang_panel.csv.
Writes to <log_dir>: ai_postings_checks.csv, ai_postings_overlap.csv, ai_postings_select_states.csv,
fang_coverage.csv. Stops if a state table doesn't parse to 51 rows. Prints every check.
"""
import json, os, re, subprocess, sys, warnings
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
NAME = {"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
ABBR = sorted(NAME.values()); FULL = {v: k for k, v in NAME.items()}
FIPS = {'01':'AL','02':'AK','04':'AZ','05':'AR','06':'CA','08':'CO','09':'CT','10':'DE','11':'DC','12':'FL','13':'GA','15':'HI','16':'ID','17':'IL','18':'IN','19':'IA','20':'KS','21':'KY','22':'LA','23':'ME','24':'MD','25':'MA','26':'MI','27':'MN','28':'MS','29':'MO','30':'MT','31':'NE','32':'NV','33':'NH','34':'NJ','35':'NM','36':'NY','37':'NC','38':'ND','39':'OH','40':'OK','41':'OR','42':'PA','44':'RI','45':'SC','46':'SD','47':'TN','48':'TX','49':'UT','50':'VT','51':'VA','53':'WA','54':'WV','55':'WI','56':'WY'}
REGION = {"Northeast":"CT ME MA NH RI VT NJ NY PA","Midwest":"IL IN MI OH WI IA KS MN MO NE ND SD","South":"DE DC FL GA MD NC SC VA WV AL KY MS TN AR LA OK TX","West":"AZ CO ID MT NV NM UT WY AK CA HI OR WA"}
Y = list(range(2015, 2026))


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def pages(pdf):
    return subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout.split("\f")


def words(pdf, page):
    x = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf, "-"], capture_output=True, text=True).stdout
    return [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>', x)]


def title_y(w, title):
    tk = title.lower().split()
    low = [z[4].lower().strip(",.:") for z in w]
    for i in range(len(w) - len(tk) + 1):
        if low[i:i + len(tk)] == tk:
            return w[i][1]
    return None


def parse_map(pdf, page, title, stop=None, pct=False):
    """Pair each state label with the number just below it, inside one map on the page."""
    w = words(pdf, page)
    y0 = title_y(w, title)
    if y0 is None:
        sys.exit(f"title not found {pdf} p{page}: {title}")
    y1 = title_y(w, stop) if stop else None
    if y1 is None or y1 <= y0:
        y1 = 1e9
    w = [z for z in w if y0 < z[1] < y1]
    rx = re.compile(r"\d+(\.\d+)?%$") if pct else re.compile(r"\d[\d,]*$")
    labs = [z for z in w if z[4] in ABBR]
    nums = [z for z in w if rx.fullmatch(z[4])]
    out = {}
    for l in labs:
        cx = (l[0] + l[2]) / 2
        c = [n for n in nums if 0 < n[1] - l[1] < (l[3] - l[1]) * 2.6 and abs((n[0] + n[2]) / 2 - cx) < 30]
        if c and l[4] not in out:
            b = min(c, key=lambda n: abs((n[0] + n[2]) / 2 - cx) + abs(n[1] - l[1]))
            out[l[4]] = float(b[4].replace(",", "").replace("%", ""))
    if len(out) != 51:
        sys.exit(f"{pdf} p{page} {title}: parsed {len(out)} states; missing {[s for s in ABBR if s not in out]}")
    return out


def num(x):
    return pd.to_numeric(pd.Series(x).astype(str).str.replace(",", "").str.replace("%", ""), errors="coerce")


def code(series):
    s = series.astype(str).str.strip()
    return s.map(lambda v: "DC" if "D.C" in v else NAME.get(v, v if v in ABBR else None))


def fig(path, val=-1, st=0):
    d = pd.read_csv(path, encoding="utf-8-sig")
    out = pd.DataFrame({"state": code(d.iloc[:, st]), "v": num(d.iloc[:, val]).values})
    return out.dropna(subset=["state"]).set_index("state").v


def build_postings(raw, data, logd):
    A = f"{raw}/aiindex/"
    P22, P23, P24, P25, P26 = [A + f for f in ("2022-ai-index-report_chapter-4.pdf", "hai_ai-index-report-2023_chapter_4.pdf", "hai_ai-index-report-2024_chapter4.pdf", "hai_ai-index-report-2025_chapter4_final.pdf", "ai_index_report_2026_chapter_4_economy.pdf")]
    chk = []
    def add(year, check, result, detail):
        chk.append(dict(year=year, check=check, result=result, detail=detail)); print(f"  {year} | {check} | {result} | {detail}")

    # ---- Sheets ----
    e19 = pd.read_excel(A + "ed2019_ai_postings_by_state.xlsx", header=1)
    e19.columns = [str(c).strip() for c in e19.columns]
    e19["state"] = code(e19["State"]); e19 = e19.dropna(subset=["state"])
    e19["postings"] = num(e19["AI Postings"]).values; e19["st_share"] = num(e19["AI Share of Total"]).values * 100; e19["year"] = pd.to_numeric(e19["Year"]).astype(int)
    e21 = pd.read_excel(A + "ed2021_burning_glass.xlsx", sheet_name="3.1.7")
    e21 = e21.iloc[:, :3]; e21.columns = ["State", "postings", "st_share"]; e21["state"] = code(e21["State"]); e21 = e21.dropna(subset=["state", "postings"]); e21["st_share"] = e21.st_share * 100
    e22 = pd.read_excel(A + "ed2022_emsi_burning_glass.xlsx", sheet_name="AI Job Postings by State")
    e22.columns = [str(c).strip() for c in e22.columns]; e22["state"] = code(e22["State"]); e22 = e22.dropna(subset=["state", "Year"])
    e22["year"] = e22["Year"].astype(int); e22["postings"] = e22["AI Postings"]; e22["st_share"] = e22["AI Share of Total"] * 100
    for nm, d, y in [("2019 edition", e19[e19.year == 2018], 2018), ("2019 edition", e19[e19.year == 2019], 2019), ("2021 edition", e21, 2020), ("2022 edition", e22[e22.year == 2019], 2019), ("2022 edition", e22[e22.year == 2020], 2020), ("2022 edition", e22[e22.year == 2021], 2021)]:
        if d.state.nunique() != 51 or d.postings.isna().any():
            sys.exit(f"{nm} {y}: {d.state.nunique()} states")

    # ---- PDF maps ----
    M = {}
    M[2021] = dict(c=parse_map(P22, 9, "NUMBER of AI JOB POSTINGS in the UNITED STATES by STATE"), s=None)
    M[2022] = dict(c=parse_map(P23, 10, "Number of AI Job Postings in the United States by State", "Percentage of U.S. States Job Postings"), s=parse_map(P23, 11, "Percentage of United States AI Job Postings by State", pct=True))
    M[2023] = dict(c=parse_map(P24, 17, "Number of AI job postings in the United States by state", "Percentage of US states job postings"), s=parse_map(P24, 18, "Percentage of US AI job postings by state", pct=True))
    M[2024] = dict(c=parse_map(P25, 16, "Number of AI job postings in the United States by state", "Percentage of US states job postings"), s=parse_map(P25, 17, "Percentage of US AI job postings by state", pct=True))
    M[2025] = dict(c=parse_map(P26, 40, "Number of AI job postings in the United States by state", "Percentage of US AI job postings by state"), s=parse_map(P26, 40, "Percentage of US AI job postings by state", pct=True))

    META = {2018: ("2019", "Burning Glass", "ed2019_bg", "Fig. 4.1.8 shows a scatter; values from its linked sheet", 82, "ed2019_ai_postings_by_state.xlsx"),
            2019: ("2022", "Emsi Burning Glass", "ed2022_ebg", "Public-data sheet, tab AI Job Postings by State; not printed in the report", None, "ed2022_emsi_burning_glass.xlsx"),
            2020: ("2022", "Emsi Burning Glass", "ed2022_ebg", "Public-data sheet, tab AI Job Postings by State; not printed in the report", None, "ed2022_emsi_burning_glass.xlsx"),
            2021: ("2022", "Emsi Burning Glass", "ed2022_ebg", "Fig. 4.1.6", 9, "2022-ai-index-report_chapter-4.pdf"),
            2022: ("2023", "Lightcast", "ed2023_lc", "Fig. 4.1.6; share Fig. 4.1.8 (p. 11)", 10, "hai_ai-index-report-2023_chapter_4.pdf"),
            2023: ("2024", "Lightcast", "ed2024_lc", "Fig. 4.2.7; share Fig. 4.2.9 (p. 18)", 17, "hai_ai-index-report-2024_chapter4.pdf"),
            2024: ("2025", "Lightcast", "ed2025_lc", "Fig. 4.2.8; share Fig. 4.2.10 (p. 17)", 16, "hai_ai-index-report-2025_chapter4_final.pdf"),
            2025: ("2026", "Lightcast", "ed2026_lc", "Fig. 4.4.10; share Fig. 4.4.11 (p. 40)", 40, "ai_index_report_2026_chapter_4_economy.pdf")}
    rows = []
    stsh = {2018: e19[e19.year == 2018].set_index("state").st_share, 2019: e22[e22.year == 2019].set_index("state").st_share, 2020: e22[e22.year == 2020].set_index("state").st_share, 2021: e22[e22.year == 2021].set_index("state").st_share}
    stsh[2022] = fig(A + "ed2023_fig_4.1.7.csv") * 100; stsh[2023] = fig(A + "ed2024_fig_4.2.8.csv"); stsh[2024] = fig(A + "ed2025_fig_4.2.9.csv")
    p13 = A + "ed2026_fig_4.4.13.csv"
    stsh[2025] = fig(p13) * 100 if os.path.exists(p13) else pd.Series(dtype=float)  # stored as a fraction
    for y, v in stsh.items():  # All in percent, about 0.05 to 6.5, with no blanks
        if not (len(v.reindex(ABBR).dropna()) == 51 and 0.01 < v.reindex(ABBR).median() < 6):
            sys.exit(f"state-share scale or coverage problem in {y}: median {v.median()}, n {len(v.reindex(ABBR).dropna())}")
    cnt = {2018: e19[e19.year == 2018].set_index("state").postings, 2019: e22[e22.year == 2019].set_index("state").postings, 2020: e22[e22.year == 2020].set_index("state").postings}
    for y in M:
        cnt[y] = pd.Series(M[y]["c"])
    for y in sorted(META):
        ed, vend, vin, f, pg, src = META[y]
        c = cnt[y]; tot = c.loc[ABBR].sum(); pub = M.get(y, {}).get("s")
        for s in ABBR:
            rows.append(dict(state=s, year=y, postings=c[s], share_pct=pub[s] if pub is not None else round(100 * c[s] / tot, 4), share_source="published" if pub is not None else "derived: state / sum of 51",
                             ai_share_of_state_postings_pct=stsh[y].get(s, np.nan), edition=ed, vendor=vend, vintage=vin, figure=f, page=pg, source_file=src,
                             note="Older vintage than 2019-2021; Burning Glass expanded coverage in 2020" if y == 2018 else ""))
    d = pd.DataFrame(rows).sort_values(["state", "year"])
    d.to_csv(f"{data}/ai_job_postings_state.csv", index=False)
    print("== AI postings:", d.shape, "states", d.state.nunique(), "years", d.year.min(), d.year.max())

    # ---- Overlap rows kept separately ----
    alt = pd.concat([e19[e19.year == 2019][["state", "year", "postings", "st_share"]].assign(edition="2019", note="Jan-Sep 2019 only"), e21[["state", "postings", "st_share"]].assign(year=2020, edition="2021", note="Full year; 2021 edition vintage")])
    alt.to_csv(f"{data}/ai_job_postings_overlap_rows.csv", index=False)

    # ---- Checks ----
    print("-- Checks")
    tots = d.groupby("year").postings.sum()
    for y in tots.index:
        add(y, "51 rows", "ok", f"sum of 51 = {tots[y]:,.0f}; yoy {'' if y == 2018 else f'{100 * (tots[y] / tots[y - 1] - 1):+.0f}%'}")
    # Published-share implied national total
    for y in (2022, 2023, 2024, 2025):
        g = d[d.year == y]; big = g.nlargest(15, "postings"); imp = (big.postings / (big.share_pct / 100)).median()
        add(y, "sum vs national total implied by published shares", "ok" if abs(imp / tots[y] - 1) < .005 else "CHECK", f"implied {imp:,.0f}; sum {tots[y]:,.0f}; gap {100 * (imp / tots[y] - 1):+.2f}%; max |published - derived share| {(g.share_pct - 100 * g.postings / tots[y]).abs().max():.3f} pts")
    for y in (2018, 2019, 2020, 2021):
        g = d[d.year == y]; a = (g.ai_share_of_state_postings_pct).notna().sum()
        add(y, "national total", "not published", "No national count or US-share table in this edition; share_pct is derived from the 51-state sum")
    # PDF vs public CSV
    for y, f, st_col in ((2022, "ed2023_fig_4.1.6.csv", 0), (2023, "ed2024_fig_4.2.7.csv", 0), (2024, "ed2025_fig_4.2.8.csv", 0), (2025, "ed2026_fig_4.4.10.csv", 0)):
        if os.path.exists(A + f):
            v = fig(A + f); dd = (pd.Series(M[y]["c"]) - v.reindex(ABBR)).abs()
            add(y, f"PDF counts vs public CSV {f}", "ok" if dd.max() == 0 else "CHECK", f"51 states; max diff {dd.max():.0f}")
        else:
            add(y, f"PDF counts vs public CSV {f}", "not available", "file not in public folder")
    dd = (pd.Series(M[2021]["c"]) - cnt_sheet(e22, 2021)).abs()
    add(2021, "PDF counts vs 2022-edition sheet", "ok" if dd.max() == 0 else "CHECK", f"51 states; max diff {dd.max():.0f}")
    for y, f in ((2022, "ed2023_fig_4.1.8.csv"), (2024, "ed2025_fig_4.2.10.csv"), (2025, "ed2026_fig_4.4.11.csv")):
        if os.path.exists(A + f):
            v = fig(A + f); v = v * 100 if v.max() < 1 else v; dd = (pd.Series(M[y]["s"]) - v.reindex(ABBR)).abs()
            add(y, f"PDF shares vs public CSV {f}", "ok" if dd.max() < .006 else "CHECK", f"max diff {dd.max():.4f} pts")
    # Report text
    T = {y: norm(" ".join(pages(p))) for y, p in ((2021, P22), (2022, P23), (2023, P24), (2024, P25), (2025, P26))}
    for y in T:
        top = d[d.year == y].nlargest(3, "postings")
        for _, r in top.iterrows():
            hit = f"{FULL[r.state]} ({r.postings:,.0f})" in T[y] or f"{r.postings:,.0f}" in T[y]
            add(y, f"spot check {r.state} against report", "ok" if hit else "CHECK", f"{r.postings:,.0f} {'appears in the report text' if f'{FULL[r.state]} ({r.postings:,.0f})' in T[y] else 'appears on the map; state name not beside it in text'}")
    t21 = norm(" ".join(pages(A + "2021-ai-index-report_master.pdf")[89:90]))
    for st, v in (("CA", 63433), ("TX", 22539), ("NY", 18580)):
        s21 = int(e21.set_index("state").postings[st]); m = cnt[2020][st]
        add(2020, f"spot check {st}: 2021 edition text", "ok" if f"{v:,}" in t21 and s21 == v else "CHECK", f"text {v:,}; 2021-edition sheet {s21:,}; table uses 2022 edition {m:,.0f} ({100 * (m / v - 1):+.1f}%)")
    t19 = norm(" ".join(pages(A + "ai_index_2019_report.pdf")[81:82]))
    e = e19.pivot(index="state", columns="year", values="postings")
    for st, txt in (("CA", "93,000"), ("NY", "30,000"), ("TX", "24,")):
        add(2018, f"spot check {st}: 2019 edition text, 2018 + Jan-Sep 2019", "ok" if txt.split(",")[0] in t19 else "CHECK", f"sheet 2018 {e.loc[st, 2018]:,.0f} + 2019 {e.loc[st, 2019]:,.0f} = {e.loc[st].sum():,.0f}; text gives about {txt if st != 'TX' else '24,000'}")

    # ---- Edition overlap ----
    ov = []
    def overlap(y, la, a, lb, b, kind):
        a = a.reindex(ABBR); b = b.reindex(ABBR); sa = 100 * a / a.sum(); sb = 100 * b / b.sum(); ld = np.log(sa / sb)
        worst = ld.abs().sort_values(ascending=False).head(3).index.tolist()
        ov.append(dict(year=y, edition_a=la, edition_b=lb, comparison=kind, n_states=len(sa), pearson_share=sa.corr(sb), spearman_share=sa.corr(sb, method="spearman"), pearson_ln_share=np.log(sa).corr(np.log(sb)), level_ratio_b_over_a=b.sum() / a.sum(), sd_ln_share_ratio=ld.std(), median_abs_pct_gap=100 * (np.exp(ld.abs()) - 1).median(), largest_gaps="; ".join(f"{s} {100 * (np.exp(ld[s]) - 1):+.0f}%" for s in worst)))
    overlap(2019, "2019 edition, Jan-Sep", e19[e19.year == 2019].set_index("state").postings, "2022 edition, full year", e22[e22.year == 2019].set_index("state").postings, "different editions; partial vs full year")
    overlap(2020, "2021 edition", e21.set_index("state").postings, "2022 edition", e22[e22.year == 2020].set_index("state").postings, "different editions; both full year")
    overlap(2021, "2022 edition, PDF map", pd.Series(M[2021]["c"]), "2022 edition, sheet", cnt_sheet(e22, 2021), "same edition; parse check, not an edition test")
    ovd = pd.DataFrame(ov).round(4); ovd.to_csv(f"{logd}/ai_postings_overlap.csv", index=False)
    print("-- Overlap\n", ovd.drop(columns=["comparison"]).to_string(index=False))

    # ---- Four-state share history published across editions, against each year's table ----
    S = []
    for ed, f in (("2023", "ed2023_fig_4.1.10.csv"), ("2024", "ed2024_fig_4.2.11.csv"), ("2025", "ed2025_fig_4.2.12.csv"), ("2026", "ed2026_fig_4.4.12.csv")):
        if not os.path.exists(A + f):
            continue
        x = pd.read_csv(A + f, encoding="utf-8-sig"); x.columns = ["year", "v", "name"]
        x["v"] = num(x.v).values; x["v"] = x.v * 100 if x.v.max() < 1 else x.v; x["state"] = code(x.name); x["series_edition"] = ed
        S.append(x)
    S = pd.concat(S).dropna(subset=["state"])
    w = S[S.year >= 2018].pivot_table(index=["state", "year"], columns="series_edition", values="v")
    w.columns = [f"series_{c}" for c in w.columns]
    tb = d.set_index(["state", "year"]).share_pct.rename("table_share_pct")
    w = w.join(tb).reset_index()
    w["table_edition"] = w.year.map(lambda v: META[v][0])
    w["alt_share_pct"] = np.nan
    a19 = e19[e19.year == 2019].set_index("state").postings; a21 = e21.set_index("state").postings
    w.loc[w.year == 2019, "alt_share_pct"] = w[w.year == 2019].state.map(100 * a19 / a19.sum())
    w.loc[w.year == 2020, "alt_share_pct"] = w[w.year == 2020].state.map(100 * a21 / a21.sum())
    w = w.round(3); w.to_csv(f"{logd}/ai_postings_select_states.csv", index=False)
    print("-- Select-state share history\n", w.to_string(index=False))
    for st in ("CA", "NY", "TX"):  # 2019 full-year values aren't printed in any report, so compare shares with the published series
        r = w[(w.state == st) & (w.year == 2019)].iloc[0]
        add(2019, f"spot check {st}: share vs Lightcast's published series", "ok" if abs(r.table_share_pct - r.series_2026) < .5 else "CHECK", f"table {r.table_share_pct:.2f}%; series {r.series_2026:.2f}%. No report prints this count")
    sc = [c for c in w.columns if c.startswith("series_")]
    if len(sc) > 1:
        print("max spread across editions' printed series:", (w[sc].max(axis=1) - w[sc].min(axis=1)).max())
    pd.DataFrame(chk).to_csv(f"{logd}/ai_postings_checks.csv", index=False)

    # ---- How much do state shares move across each year-to-year step? ----
    # Same-edition steps give a benchmark. Data-center jobs (one BLS series) give a second one.
    p = pd.read_csv(f"{os.path.dirname(raw.rstrip('/'))}/out/state_panel_2015_2025.csv")
    pj = p[p.dc_suppressed == 0].pivot(index="state", columns="year", values="dc_jobs")
    sh = d.pivot(index="state", columns="year", values="postings"); sh = sh / sh.sum()
    pjs = pj / pj.sum()
    tr = []
    for y in range(2019, 2026):
        ld = np.log(sh[y] / sh[y - 1])
        ok = pj[[y - 1, y]].dropna().index
        lj = np.log(pj.loc[ok, y] / pj.loc[ok, y].sum()) - np.log(pj.loc[ok, y - 1] / pj.loc[ok, y - 1].sum())
        worst = ld.abs().sort_values(ascending=False).head(3).index.tolist()
        tr.append(dict(step=f"{y - 1}->{y}", editions=f"{META[y - 1][0]}->{META[y][0]}", same_edition=META[y - 1][0] == META[y][0], national_change_pct=100 * (tots[y] / tots[y - 1] - 1), sd_ln_share_change_postings=ld.std(), median_abs_ln_share_change=ld.abs().median(), sd_ln_share_change_dc_jobs=lj.std(), n_dc_jobs=len(ok), largest="; ".join(f"{s} {100 * (np.exp(ld[s]) - 1):+.0f}%" for s in worst)))
    tr = pd.DataFrame(tr).round(4); tr.to_csv(f"{logd}/ai_postings_share_changes.csv", index=False)
    print("-- Year-to-year change in ln(state share)\n", tr.to_string(index=False))
    return d


def cnt_sheet(e22, y):
    return e22[e22.year == y].set_index("state").postings.reindex(ABBR)


def build_seds(raw, data):
    u = pd.read_csv(f"{raw}/eia/seds/use_all_btu.csv")
    p = pd.read_csv(f"{raw}/eia/seds/pr_all.csv")
    codes = pd.read_excel(f"{raw}/eia/seds/Codes_and_Descriptions.xlsx", sheet_name="MSN descriptions", header=None)
    want = dict(RETCB="re_bbtu", WYTCB="wind_bbtu", SOTCB="solar_bbtu", GETCB="geothermal_bbtu", HYTCB="hydro_bbtu", BMTCB="biomass_bbtu", TETCB="total_energy_bbtu")
    mc = next(c for c in codes.columns if codes[c].astype(str).isin(["RETCB"]).any())
    desc = codes[codes[mc].isin(list(want) + ["TETCD"])].dropna(axis=1, how="all")
    print("== SEDS code list\n", desc.to_string(index=False, header=False))
    if len(desc) != 8:
        sys.exit("SEDS code list check failed")
    yrs = [str(y) for y in range(2015, 2025)]
    rec = []
    for m, nm in want.items():
        x = u[(u.MSN == m) & u.State.isin(ABBR)].melt(id_vars=["State"], value_vars=yrs, var_name="year", value_name=nm).assign(key=lambda t: t.State + t.year).set_index("key")
        rec.append(x[[nm]])
    x = p[(p.MSN == "TETCD") & p.State.isin(ABBR)].melt(id_vars=["State"], value_vars=yrs, var_name="year", value_name="ep_tetcd").assign(key=lambda t: t.State + t.year).set_index("key")
    d = pd.concat(rec + [x[["ep_tetcd", "State", "year"]]], axis=1).rename(columns={"State": "state"}).reset_index(drop=True)
    d["year"] = d.year.astype(int); d = d[["state", "year"] + list(want.values()) + ["ep_tetcd"]].sort_values(["state", "year"])
    d.to_csv(f"{data}/seds_renewables_state.csv", index=False)
    print("SEDS rows", d.shape, "NA", int(d.isna().sum().sum()))
    z = d[d.year.between(2018, 2021)]
    print("nonzero state-years 2018-21 vs Fang N:", {k: (int((z[k] > 0).sum()), v) for k, v in dict(re_bbtu=204, wind_bbtu=164, solar_bbtu=204, geothermal_bbtu=204, biomass_bbtu=204, hydro_bbtu=192).items()})
    print("zero cells 2015-24:", {k: int((d[k] == 0).sum()) for k in want.values()})
    s = (d.wind_bbtu + d.solar_bbtu + d.geothermal_bbtu + d.hydro_bbtu + d.biomass_bbtu) / d.re_bbtu
    print("sum of five types / RETCB: min", round(s.min(), 4), "max", round(s.max(), 4))
    return d


def build_ncses(raw, data):
    K = "bachelors-degrees-per-1000-18-24-year-olds"
    v = pd.DataFrame(json.load(open(f"{raw}/ncses/{K}.json"))["data_points"])
    a = pd.DataFrame(json.load(open(f"{raw}/ncses/degconferred-bach.json"))["data_points"])[["region", "year", "value"]].rename(columns={"value": "degrees"})
    b = pd.DataFrame(json.load(open(f"{raw}/ncses/population18-24.json"))["data_points"])[["region", "year", "value"]].rename(columns={"value": "pop_18_24"})
    v["region"] = v.region.astype(str).str.zfill(2); a["region"] = a.region.astype(str).str.zfill(2); b["region"] = b.region.astype(str).str.zfill(2)
    print("== NCSES years", int(v.year.min()), int(v.year.max()), "regions per year", v.groupby("year").region.nunique().iloc[-1], "non-state regions", sorted(set(v.region) - set(FIPS)))
    print("flags 2015-2024:", {c: int(v[v.year.between(2015, 2024)][c].fillna(False).astype(bool).sum()) for c in ("not_available", "suppressed", "rounds_to_zero")})
    d = v[v.region.isin(FIPS)].rename(columns={"value": "edu_bach_per1000"})[["region", "year", "edu_bach_per1000"]].merge(a, on=["region", "year"], how="left").merge(b, on=["region", "year"], how="left")
    d["state"] = d.region.map(FIPS); d = d[d.year >= 2015][["state", "year", "edu_bach_per1000", "degrees", "pop_18_24"]].sort_values(["state", "year"])
    d.to_csv(f"{data}/ncses_bachelors_state.csv", index=False)
    print("NCSES rows", d.shape, "years", d.year.min(), d.year.max(), "NA", int(d.edu_bach_per1000.isna().sum()), "| max |indicator - 1000*deg/pop|:", round((d.edu_bach_per1000 - 1000 * d.degrees / d.pop_18_24).abs().max(), 6))
    print(d[(d.state == "GA") & d.year.isin([2018, 2021])].to_string(index=False))
    return d


def main(raw, data, logd):
    for f in (f"{data}/out/state_panel_2015_2025.csv", f"{data}/epu_state_annual.csv", f"{data}/nsf_state_rd.csv", f"{data}/lbnl_rps_targets.csv"):
        if not os.path.exists(f):
            sys.exit(f"missing input {f}")
    post = build_postings(raw, data, logd)
    seds = build_seds(raw, data)
    edu = build_ncses(raw, data)
    p = pd.read_csv(f"{data}/out/state_panel_2015_2025.csv")
    # Income per capita: BEA SAINC1 line 3
    pi = pd.read_csv(f"{raw}/bea/sainc/SAINC1__ALL_AREAS_1929_2025.csv", encoding="latin1", low_memory=False, dtype={"GeoFIPS": str})
    pi["GeoFIPS"] = pi.GeoFIPS.str.strip().str.strip('"').str.strip()
    pi = pi[(pd.to_numeric(pi.LineCode, errors="coerce") == 3) & pi.GeoFIPS.str[:2].isin(FIPS) & pi.GeoFIPS.str.endswith("000")]
    pi["state"] = pi.GeoFIPS.str[:2].map(FIPS)
    inc = pi.melt(id_vars=["state"], value_vars=[str(y) for y in Y], var_name="year", value_name="income_pc_usd"); inc["year"] = inc.year.astype(int); inc["income_pc_usd"] = pd.to_numeric(inc.income_pc_usd, errors="coerce")
    rd = pd.read_csv(f"{data}/nsf_state_rd.csv")[["state", "year", "rd_total_musd"]]
    reg = {s: k for k, v in REGION.items() for s in v.split()}
    if len(reg) != 51:
        sys.exit("region map")
    sp = p[["state", "year", "sales_mwh", "price_c_kwh", "gen_total_mwh"]].rename(columns={"sales_mwh": "elec_consumption_mwh", "price_c_kwh": "elec_price_c_kwh"})
    sp["net_producer"] = (sp.gen_total_mwh > sp.elec_consumption_mwh).astype(int)
    sp = sp.merge(rd, on=["state", "year"], how="left").merge(inc, on=["state", "year"], how="left")
    sp["census_region"] = sp.state.map(reg); sp["extreme_weather"] = np.nan; sp["extreme_weather_note"] = "not run: Fang's count of extreme hot and cold occurrences wasn't built"
    sp.to_csv(f"{data}/fang_split_vars.csv", index=False)
    print("== Regions:", pd.Series(reg).value_counts().to_dict(), "| net producers 2021:", int(sp[sp.year == 2021].net_producer.sum()), "| income NA", int(sp.income_pc_usd.isna().sum()))
    # dc_jobs lag needs 2014, which the panel doesn't carry
    q = pd.read_csv(f"{raw}/bls/qcew_2014_518210.csv", dtype={"area_fips": str}, low_memory=False)
    q = q[q.area_fips.str.endswith("000") & q.area_fips.str[:2].isin(FIPS) & (q.own_code == 5) & (q.agglvl_code == 58)]
    j14 = pd.DataFrame({"state": q.area_fips.str[:2].map(FIPS), "year": 2014, "dc_jobs": q.annual_avg_emplvl.astype(float)})
    j = pd.concat([j14, p[["state", "year", "dc_jobs"]]]).sort_values(["state", "year"]); j["dc_jobs_lag1"] = j.groupby("state").dc_jobs.shift(1)
    epu = pd.read_csv(f"{data}/epu_state_annual.csv")[["state", "year", "epu_composite", "epu_national", "epu_state"]]
    rps = pd.read_csv(f"{data}/lbnl_rps_targets.csv")[["state", "year", "target_pct"]]
    keep = ["state", "year", "gdp_real_musd2017", "population", "dc_jobs", "total_jobs", "ai_dc_per1000", "ai_dc_per1000_lag1", "dc_suppressed", "ln_gdp_pc", "manuf_share", "price_c_kwh", "pop_growth", "is_dc"]
    f = p[keep].merge(j[["state", "year", "dc_jobs_lag1"]], on=["state", "year"], how="left")
    pp = post[["state", "year", "postings", "share_pct", "share_source", "ai_share_of_state_postings_pct", "edition", "vendor", "vintage"]].rename(columns={"postings": "ai_postings", "share_pct": "ai_share_us_pct", "share_source": "ai_share_source", "ai_share_of_state_postings_pct": "ai_share_of_state_pct", "edition": "ai_edition", "vendor": "ai_vendor", "vintage": "ai_vintage"})
    for t in (seds, edu[["state", "year", "edu_bach_per1000"]], epu, pp, rps, sp.drop(columns=["extreme_weather", "extreme_weather_note", "gen_total_mwh"])):
        f = f.merge(t, on=["state", "year"], how="left")
    f = f.sort_values(["state", "year"])
    if len(f) != 561 or f.duplicated(["state", "year"]).any():
        sys.exit("fang_panel keys")
    f.to_csv(f"{data}/fang_panel.csv", index=False)
    print("== fang_panel", f.shape)
    V = ["re_bbtu", "wind_bbtu", "solar_bbtu", "geothermal_bbtu", "hydro_bbtu", "biomass_bbtu", "total_energy_bbtu", "ep_tetcd", "edu_bach_per1000", "gdp_real_musd2017", "population", "epu_composite", "epu_national", "epu_state", "ai_postings", "ai_share_us_pct", "ai_share_of_state_pct", "dc_jobs", "dc_jobs_lag1", "ai_dc_per1000", "elec_consumption_mwh", "elec_price_c_kwh", "net_producer", "rd_total_musd", "income_pc_usd", "census_region", "target_pct", "ln_gdp_pc", "manuf_share", "price_c_kwh", "pop_growth"]
    cov = f.groupby("year")[V].apply(lambda g: g.notna().sum()).T
    cov.index.name = "variable"; cov["first"] = [f[f[v].notna()].year.min() for v in V]; cov["last"] = [f[f[v].notna()].year.max() for v in V]
    cov.to_csv(f"{logd}/fang_coverage.csv")
    print(cov.to_string())
    print("Samples: postings on 2018-21 complete:", int(f[f.year.between(2018, 2021)][["re_bbtu", "ai_postings", "epu_composite", "ep_tetcd", "gdp_real_musd2017", "population", "edu_bach_per1000"]].dropna().shape[0]))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

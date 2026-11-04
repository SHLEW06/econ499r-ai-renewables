#!/usr/bin/env python3
"""Clean the Nov 4 sources into side tables. Does not touch the master panel.

Usage: build_side_tables_nov4.py <raw_dir> <out_dir> <vintage_check_csv> <panel_csv>

Writes to <out_dir>: lbnl_rps_targets.csv, owid_global_solar_capacity.csv,
epu_state_annual.csv, nsf_state_rd.csv, lbnl_utility_solar.csv, epoch_ai_campuses_by_state.csv.
Prints rows in and out plus checks; the receipts quote this output.
"""
import os, re, sys, warnings
import numpy as np, openpyxl, pandas as pd

warnings.filterwarnings("ignore")
STATES = {"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT",
 "Delaware":"DE","District of Columbia":"DC","Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN",
 "Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
 "Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ",
 "New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA",
 "Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA",
 "Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
ABBR = sorted(STATES.values())
YEARS = list(range(2015, 2026))


def rows_of(path, sheet):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    return list(ws.iter_rows(values_only=True))


def build_rps(raw, out, vintage_csv, panel):
    t = rows_of(f"{raw}/lbnl/RPS & CES Targets and Demand_June 2026.xlsx", "RPS & CES Targets (%)")
    h = next(r for r in t if r[0] == "State")
    yi = {int(x): j for j, x in enumerate(h) if str(x).isdigit()}
    rps, ces, cur = {}, {}, None
    for r in t[t.index(h) + 1:]:
        cur = r[0] or cur
        lab = str(r[2]).strip() if r[2] else ""
        d = rps if lab.startswith("Total RPS") else ces if lab.startswith("Total CES") else None
        if d is None:
            continue
        for y in YEARS:
            if not isinstance(r[yi[y]], (int, float)):
                sys.exit(f"non-numeric target {cur} {y}")
            d[(cur, y)] = float(r[yi[y]]) * 100
    in_file = {k[0] for k in list(rps) + list(ces)}

    a = rows_of(f"{raw}/lbnl/Historical RPS & CES Target Achievement and Compliance Costs_June 2026.xlsx", "Target Achievement")
    h = next(r for r in a if r[0] == "RPS States")
    ai = {int(x): j for j, x in enumerate(h) if str(x).isdigit()}
    ta = {}
    for r in a[a.index(h) + 1:]:
        if r[0] and str(r[3]).strip().startswith("Total"):
            for y in YEARS:
                ta[(r[0], y)] = r[ai[y]]
    ta_states = {k[0] for k in ta}

    v = pd.read_csv(vintage_csv)
    revised = {(s, y) for s, y in v[v.past][["state", "year"]].itertuples(index=False)}

    rec = []
    for st in ABBR:
        for y in YEARS:
            rp, ce = rps.get((st, y), 0.0), ces.get((st, y), 0.0)
            tgt = max(rp, ce)
            raw_ta = ta.get((st, y))
            if st not in ta_states:
                status = "state_not_in_file"
            elif isinstance(raw_ta, (int, float)):
                status = "reported"
            elif str(raw_ta).strip() == "-":
                status = "no_obligation"
            elif str(raw_ta).strip().lower() == "no data":
                status = "no_data"
            elif str(raw_ta).strip().lower() == "n/a":
                status = "not_applicable"
            else:
                status = "blank"
            if tgt > 0:
                chk = {"reported": "obligation_confirmed", "no_obligation": "conflict_target_but_no_obligation"}.get(status, "not_checkable")
            else:
                chk = {"reported": "conflict_obligation_but_no_target", "no_obligation": "zero_consistent",
                       "state_not_in_file": "zero_no_policy"}.get(status, "zero_not_checkable")
            rec.append(dict(state=st, year=y, target_pct=round(tgt, 4), rps_target_pct=round(rp, 4), ces_target_pct=round(ce, 4),
                            target_basis="todays_schedule_june2026" if st in in_file else "not_in_lbnl_file_zero",
                            ta_status=status, ta_achievement_pct=round(raw_ta * 100, 2) if status == "reported" else np.nan,
                            in_force_check=chk, revised_vs_older_edition=int((st, y) in revised)))
    df = pd.DataFrame(rec)
    df.to_csv(f"{out}/lbnl_rps_targets.csv", index=False)
    print("== RPS: rows", len(df), "states", df.state.nunique(), "years", df.year.min(), df.year.max(), "NA target", int(df.target_pct.isna().sum()),
          "dupes", int(df.duplicated(["state", "year"]).sum()))
    keys = panel[["state", "year"]].merge(df, on=["state", "year"], how="outer", indicator=True)
    print("panel key match:", keys._merge.value_counts().to_dict())
    print("in LBNL file:", len(in_file), "absent:", [s for s in ABBR if s not in in_file])
    print("not in Target Achievement:", [s for s in sorted(in_file) if s not in ta_states])
    print("states with target>0 by year:", df[df.target_pct > 0].groupby("year").state.nunique().to_dict())
    print("cells where CES>RPS:", df[df.ces_target_pct > df.rps_target_pct].groupby("state").year.agg(["min", "max", "count"]).to_dict("index"))
    print("in_force_check:", df.in_force_check.value_counts().to_dict())
    print("in_force_check by year:\n", pd.crosstab(df.year, df.in_force_check).to_string())
    print("conflicts:\n", df[df.in_force_check.str.startswith("conflict")][["state", "year", "target_pct", "ta_status", "in_force_check"]].to_string(index=False))
    print("revised cells:", int(df.revised_vs_older_edition.sum()), "of nonzero", int((df.target_pct > 0).sum()), "states", sorted(df[df.revised_vs_older_edition == 1].state.unique()))
    w = df[df.target_pct > 0].sort_values(["state", "year"]).copy()
    w["chg"] = w.groupby("state").target_pct.diff()
    print("year-over-year drops >2 pts in target_pct:\n", w[w.chg < -2][["state", "year", "target_pct", "chg"]].to_string(index=False))
    z = df.sort_values(["state", "year"]).copy(); z["chg"] = z.groupby("state").target_pct.diff()
    print("drops to zero:\n", z[(z.target_pct == 0) & (z.chg < 0)][["state", "year", "chg"]].to_string(index=False))
    for s in ["GA", "VA", "AZ", "MI", "WI", "TX", "KS", "MT"]:
        print(s, df[df.state == s].target_pct.round(1).tolist())


def build_owid(raw, out):
    d = pd.read_csv(f"{raw}/owid/solar-pv-cumulative-capacity.csv")
    k = d[d.Entity.isin(["World", "United States"])].copy()
    k.columns = ["entity", "code", "year", "solar_pv_ongrid_gw"]
    k["source"] = "IRENA (2026), Renewable Energy Statistics; processed by Our World in Data"
    k.to_csv(f"{out}/owid_global_solar_capacity.csv", index=False)
    print("== OWID: rows in", len(d), "rows out", len(k), "years", k.year.min(), k.year.max())
    print(k[k.year >= 2023].drop(columns=["source", "code"]).to_string(index=False))


def build_epu(raw, out):
    x = pd.read_excel(f"{raw}/epu/State_Policy_Uncertainty.xlsx")
    m = x.melt(id_vars=["year", "month"], var_name="v", value_name="epu")
    m["state"] = m.v.str[-2:]
    m["measure"] = m.v.str[4:-2].str.lower()
    y = m.groupby(["state", "year", "measure"]).epu.agg(["mean", "count"]).reset_index()
    p = y.pivot(index=["state", "year"], columns="measure", values="mean").add_prefix("epu_")
    n = y[y.measure == "state"].set_index(["state", "year"])["count"].rename("n_months_state")
    out_df = p.join(n).reset_index()
    out_df["year"] = out_df.year.astype(int)
    out_df.to_csv(f"{out}/epu_state_annual.csv", index=False)
    print("== EPU: monthly rows", len(x), "cols", x.shape[1], "annual rows", len(out_df), "states", out_df.state.nunique(), "years", out_df.year.min(), out_df.year.max())
    print("months per state-year:", out_df.n_months_state.value_counts().to_dict())
    w = out_df[out_df.year.between(2015, 2025)]
    print("2015-25 NA:", w[["epu_state", "epu_national", "epu_composite"]].isna().sum().to_dict())
    print(w[w.state == "GA"][["year", "epu_state", "epu_national", "epu_composite"]].round(1).to_string(index=False))
    g = x[x.year == 2025]["EPU_StateGA"].mean()
    print("hand check GA 2025 epu_state from monthly:", round(g, 4), "table:", round(float(w[(w.state == "GA") & (w.year == 2025)].epu_state.iloc[0]), 4))


NSF = {2017: ("nsf20307", "old"), 2018: ("nsf21325", "old"), 2019: ("nsf22320", "old"), 2020: ("nsf23321", "old"),
       2021: ("nsf24318", "new"), 2022: ("nsf25326", "new"), 2023: ("nsf26313", "new")}
COLS = {"old": dict(rd_total_musd=1, rd_federal_musd=4, rd_ffrdc_musd=5, rd_business_musd=8, rd_higher_ed_musd=12, rd_nonprofit_musd=19, rd_state_internal_musd=20, gdp_nsf_musd=21, rd_intensity_pct=23),
        "new": dict(rd_total_musd=2, rd_federal_musd=3, rd_ffrdc_musd=4, rd_business_musd=7, rd_higher_ed_musd=11, rd_nonprofit_musd=18, rd_state_internal_musd=19, gdp_nsf_musd=20, rd_intensity_pct=22)}


def build_nsf(raw, out, panel):
    rec, flags = [], []
    names = sorted(STATES, key=len, reverse=True)
    for y, (pub, lay) in NSF.items():
        rows = rows_of(f"{raw}/nsf/{pub}-tab010.xlsx", "Table 10")
        title = str(rows[1][0])
        if "by state" not in title or str(y) not in title:
            sys.exit(f"wrong table {pub}: {title}")
        got = 0
        for r in rows[6:]:
            lab = str(r[0]).strip() if r[0] else ""
            nm = next((n for n in names if lab.startswith(n) and len(lab) - len(n) <= 2), None)
            if nm is None:
                continue
            got += 1
            d = dict(state=STATES[nm], year=y, nsf_edition=pub)
            for c, j in COLS[lay].items():
                v = r[j]
                if isinstance(v, (int, float)):
                    d[c] = float(v)
                else:
                    d[c] = np.nan
                    flags.append(dict(state=STATES[nm], year=y, column=c, published=str(v).strip()))
            rec.append(d)
        if got != 51:
            sys.exit(f"{pub}: {got} states")
    df = pd.DataFrame(rec).sort_values(["state", "year"])
    fl = pd.DataFrame(flags)
    note = fl.groupby(["state", "year"]).apply(lambda g: "; ".join(f"{a}={b}" for a, b in zip(g.column, g.published))).rename("published_not_numeric").reset_index() if len(fl) else pd.DataFrame(columns=["state", "year", "published_not_numeric"])
    df = df.merge(note, on=["state", "year"], how="left")
    df.to_csv(f"{out}/nsf_state_rd.csv", index=False)
    print("== NSF: rows", len(df), "states", df.state.nunique(), "years", df.year.min(), df.year.max(), "dupes", int(df.duplicated(["state", "year"]).sum()))
    print("non-numeric cells by column:", fl.groupby("column").published.apply(lambda s: s.value_counts().to_dict()).to_dict() if len(fl) else {})
    print("NA rd_total:", df[df.rd_total_musd.isna()][["state", "year", "published_not_numeric"]].to_string(index=False))
    print("NA intensity:", int(df.rd_intensity_pct.isna().sum()))
    df["calc"] = 100 * df.rd_total_musd / df.gdp_nsf_musd
    print("max |published intensity - rd/gdp|:", round((df.calc - df.rd_intensity_pct).abs().max(), 3))
    m = df.merge(panel[["state", "year", "gdp_nom_musd"]], on=["state", "year"])
    print("NSF GDP / current BEA nominal GDP, by year:", (m.gdp_nsf_musd / m.gdp_nom_musd).groupby(m.year).agg(["min", "max"]).round(3).to_dict("index"))
    for y, (pub, lay) in NSF.items():
        rows = rows_of(f"{raw}/nsf/{pub}-tab010.xlsx", "Table 10")
        row = next(r for r in rows if r[0] and str(r[0]).startswith("States total"))
        print(f"  {y}: sum of 51 = {df[df.year == y].rd_total_musd.sum():,.0f}; published States total = {float(row[COLS[lay]['rd_total_musd']]):,.0f}")
    w = df.pivot(index="state", columns="year", values="rd_total_musd")
    print(w.loc[["GA", "VA", "CA", "WY"]].to_string())
    print("largest yoy % swings in rd_total:")
    l = df.sort_values(["state", "year"]).copy(); l["pct"] = l.groupby("state").rd_total_musd.pct_change() * 100
    print(l.loc[l.pct.abs().nlargest(6).index, ["state", "year", "rd_total_musd", "pct"]].round(1).to_string(index=False))


def snake(c):
    return re.sub(r"_+", "_", re.sub(r"[^0-9a-z]+", "_", str(c).lower())).strip("_")


def build_solar(raw, out, panel):
    d = pd.read_excel(f"{raw}/lbnl/Utility Scale Solar 2026 Edition Datafile.xlsx", sheet_name="Individual_Project_Data")
    n_in = len(d)
    d.columns = [snake(c) for c in d.columns]
    d = d.dropna(how="all")
    d.to_csv(f"{out}/lbnl_utility_solar.csv", index=False)
    print("== LBNL solar: rows in", n_in, "rows out", len(d), "cols", d.shape[1])
    print(list(d.columns)[:30])
    print("states", d.state.nunique(), "| COD years", d.solar_cod_year.min(), d.solar_cod_year.max())
    print("tech:", d.solar_tech_main.value_counts(dropna=False).to_dict())
    print("region:", d.region.value_counts(dropna=False).to_dict())
    print("ID duplicates:", int(d.eia_id.duplicated().sum()), "blank ID:", int(d.eia_id.isna().sum()), "IDs ending ret:", int(d.eia_id.astype(str).str.endswith("ret").sum()))
    ac = "solar_capacity_mw_ac"
    print("total MW-AC:", round(d[ac].sum(), 0), "PV only:", round(d[d.solar_tech_main != "CSP"][ac].sum(), 0))
    ga = d[d.state == "GA"]
    print("Georgia projects:", len(ga), "MW-AC", round(ga[ac].sum(), 1), "COD", ga.solar_cod_year.min(), ga.solar_cod_year.max(), "region", ga.region.value_counts().to_dict())
    print("Georgia with PPA:", int(ga.filter(like="ppa").notna().any(axis=1).sum()))
    se = d[d.region.astype(str).str.contains("Southeast", case=False)]
    print("Southeast region projects:", len(se), "MW-AC", round(se[ac].sum(), 1), "states", se.state.value_counts().to_dict())
    c = d.groupby("state")[ac].sum()
    e = panel[panel.year == 2025].set_index("state").cap_solar_mw
    for s in ["GA", "TX", "CA", "NC", "FL"]:
        print(f"  {s}: LBNL {c.get(s, 0):,.0f} MW-AC vs EIA panel 2025 cap_solar_mw {e[s]:,.0f} ratio {c.get(s, 0) / e[s]:.2f}")


MANUAL_STATE = {  # Address is missing or lacks a state; reason in the receipt.
    "Google Mesa": "AZ", "Google Storey County": "NV", "OpenAI Stargate Michigan": "MI", "OpenAI Stargate Milam": "TX",
    "OpenAI Stargate New Mexico": "NM", "OpenAI Stargate Wisconsin": "WI", "Anthropic Barber Lake": "TX",
    "AWS New Albany": "OH", "Stream Phoenix": "AZ", "Google Kansas City East": None}


def site_state(name, addr):
    if name in MANUAL_STATE:
        return MANUAL_STATE[name], "from site name" if MANUAL_STATE[name] else "unresolved"
    a = str(addr)
    m = re.findall(r"\b([A-Z]{2})\b[\s,]*\d{0,5}(?:-\d+)?[\s,]*(?:USA)?", a)
    m = [x for x in m if x in ABBR]
    if m:
        return m[-1], "address"
    n = [v for k, v in STATES.items() if k in a]
    return (n[-1], "address") if n else (None, "unresolved")


def build_epoch(raw, out):
    e = pd.read_csv(f"{raw}/epoch/data_centers.csv")
    t = pd.read_csv(f"{raw}/epoch/data_center_timelines.csv")
    u = e[e.Country == "United States"].copy()
    u[["state", "state_source"]] = [site_state(n, a) for n, a in zip(u.Name, u.Address)]
    g = t.groupby("Data center").agg(planned_it_mw=("IT power (MW)", "max"), planned_facility_mw=("Power (MW)", "max"), last_timeline_date=("Date", "max"))
    u = u.merge(g, left_on="Name", right_index=True, how="left")
    u["operating"] = (u["Current power (MW)"] > 0).astype(int)
    u["state"] = u.state.fillna("UNRESOLVED")
    s = u.groupby("state").agg(n_sites=("Name", "count"), n_operating=("operating", "sum"), current_it_mw=("Current power (MW)", "sum"),
                                planned_it_mw=("planned_it_mw", "sum"), planned_facility_mw=("planned_facility_mw", "sum")).reset_index().sort_values("planned_facility_mw", ascending=False)
    s["note"] = "Context only; not a model variable. Largest AI campuses only, about 45% of global AI compute per Epoch."
    s.to_csv(f"{out}/epoch_ai_campuses_by_state.csv", index=False)
    print("== Epoch: sites", len(e), "US", len(u), "states", s.state.nunique(), "state source", u.state_source.value_counts().to_dict())
    print(s.drop(columns="note").round(0).to_string(index=False))
    print("Georgia sites:\n", u[u.state == "GA"][["Name", "Address", "Current power (MW)", "planned_it_mw", "planned_facility_mw", "last_timeline_date"]].to_string(index=False))
    print("Timeline dates", t.Date.min(), t.Date.max(), "| NA planned", int(u.planned_it_mw.isna().sum()))
    print("page says TX 14, OH 7, VA 7, NE 4, IA 4:", u.state.value_counts()[["TX", "OH", "VA", "NE", "IA"]].to_dict())


def main(raw, out, vintage_csv, panel_csv):
    for f in [vintage_csv, panel_csv]:
        if not os.path.exists(f):
            sys.exit(f"missing input {f}")
    panel = pd.read_csv(panel_csv)
    build_rps(raw, out, vintage_csv, panel)
    build_owid(raw, out)
    build_epu(raw, out)
    build_nsf(raw, out, panel)
    build_epoch(raw, out)
    build_solar(raw, out, panel)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])

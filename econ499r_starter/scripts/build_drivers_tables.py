#!/usr/bin/env python3
"""National and state drivers for prompts/09_extend.md section 4 (EXPERIMENTS.md section 14.4).

Usage: build_drivers_tables.py <raw_dir> <data_dir> <log_dir>

Writes
  <data_dir>/extend_drivers_national.csv  2015-2025: solar LCOE (LBNL), solar ITC and wind PTC (coded, with citations),
                                          Henry Hub price (EIA), national AI totals; wind LCOE blank until the LBNL wind file arrives
  <data_dir>/extend_drivers_state.csv     50 states: 2015 wind and solar capacity factors (EIA, fallback for NREL), 2015 gas share
  <log_dir>/drivers_build.log
"""
import os, shutil, subprocess, sys, tempfile
import numpy as np, pandas as pd

Y0, Y1 = 2015, 2025
IRA = "P.L. 117-169 (data/raw/crs/PLAW-117publ169.pdf)"
# Solar ITC by year construction begins (percent). Each value carries its citation.
ITC = {y: (30.0, f"{IRA}, PDF p. 98 (136 Stat. 1914): sec. 13102(d)(1) strikes the prior-law '30 percent' base for solar; the 2020-2021 phase-down applies from 2020") for y in range(2015, 2020)}
ITC.update({y: (26.0, f"{IRA}, PDF p. 98 (136 Stat. 1914): new 48(a)(6), construction begins after Dec. 31, 2019 and placed in service before Jan. 1, 2022: 26 percent") for y in (2020, 2021)})
ITC.update({y: (30.0, f"{IRA}, PDF p. 98 (136 Stat. 1914) base 6 percent x 5 for projects meeting wage and apprenticeship rules, PDF p. 103 (136 Stat. 1919); placed in service after Dec. 31, 2021") for y in range(2022, Y1 + 1)})
# Wind PTC as a share of the full credit, by year construction begins. 2017-2021 need CRS R43453 (blocked to scripts).
PTC = {y: (np.nan, "pending CRS R43453 (crsreports.congress.gov returned HTTP 403 to scripts on 2026-11-07)") for y in range(Y0, 2022)}
PTC.update({y: (100.0, f"{IRA}, PDF p. 90 (136 Stat. 1906): sec. 13101(e)(2) limits the 45(b)(5) phaseout to wind placed in service before Jan. 1, 2022") for y in range(2022, Y1 + 1)})


def main(raw, out, logd):
    log = []
    # Henry Hub, annual average, $/MMBtu
    # .xls needs xlrd, which isn't installed; LibreOffice converts a temporary copy to .xlsx (the raw file is untouched)
    soffice = shutil.which("soffice") or sys.exit("soffice not found")
    with tempfile.TemporaryDirectory() as td:
        cp = os.path.join(td, "RNGWHHDa.xls"); shutil.copy(os.path.join(raw, "eia/henry_hub/RNGWHHDa.xls"), cp)
        subprocess.run([soffice, f"-env:UserInstallation=file://{td}/profile", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", td, cp], check=True, capture_output=True, timeout=300)
        hh = pd.read_excel(os.path.join(td, "RNGWHHDa.xlsx"), sheet_name="Data 1", skiprows=2)
    hh.columns = ["date", "hh_usd_mmbtu"]; hh["year"] = pd.to_datetime(hh.date).dt.year
    hh = hh[hh.year.between(Y0, Y1)][["year", "hh_usd_mmbtu"]]
    log.append(f"Henry Hub: {dict(zip(hh.year, hh.hh_usd_mmbtu.round(2)))}")
    # Solar LCOE: capacity-weighted mean of PV projects' LCOE without tax credits (2025 $/MWh) by commercial-operation year
    s = pd.read_csv(os.path.join(out, "lbnl_utility_solar.csv"))
    s = s[(s.solar_tech_main == "PV") & s.pv_lcoe_no_tax_credits_2025_mwh.notna() & s.solar_capacity_mw_ac.notna() & s.solar_cod_year.between(Y0, Y1)]
    sl = s.groupby("solar_cod_year").apply(lambda g: pd.Series({"solar_lcoe_2025usd_mwh": np.average(g.pv_lcoe_no_tax_credits_2025_mwh, weights=g.solar_capacity_mw_ac),
                                                                 "solar_lcoe_projects": len(g), "solar_lcoe_mw_ac": g.solar_capacity_mw_ac.sum()}), include_groups=False).reset_index().rename(columns={"solar_cod_year": "year"})
    log.append("Solar LCOE (2025 $/MWh, MW-weighted): " + ", ".join(f"{int(r.year)} {r.solar_lcoe_2025usd_mwh:.1f} (n={int(r.solar_lcoe_projects)})" for r in sl.itertuples()))
    # national AI totals and state drivers from the panel and the Fang panel
    P = pd.read_csv(os.path.join(out, "out", "state_panel_2015_2025.csv")); P = P[P.is_dc == 0]
    fp = pd.read_csv(os.path.join(out, "fang_panel.csv")); fp = fp[fp.is_dc == 0]
    ai = P.groupby("year").agg(us_dc_jobs_50=("dc_jobs", "sum"), n_states_dc=("dc_jobs", "count")).reset_index()
    ai = ai.merge(fp.groupby("year").agg(us_ai_postings_50=("ai_postings", "sum"), n_states_post=("ai_postings", "count")).reset_index(), on="year")
    ai.loc[ai.n_states_post == 0, "us_ai_postings_50"] = np.nan
    nat = pd.DataFrame({"year": range(Y0, Y1 + 1)})
    nat["itc_pct"] = nat.year.map(lambda y: ITC[y][0]); nat["itc_source"] = nat.year.map(lambda y: ITC[y][1])
    nat["ptc_pct_of_full"] = nat.year.map(lambda y: PTC[y][0]); nat["ptc_source"] = nat.year.map(lambda y: PTC[y][1])
    nat["wind_lcoe_2025usd_mwh"] = np.nan; nat["wind_lcoe_source"] = "pending LBNL Land-Based Wind Market Report data file (emp.lbl.gov returned HTTP 403 to scripts on 2026-11-07)"
    nat = nat.merge(sl, on="year", how="left").merge(hh, on="year", how="left").merge(ai, on="year", how="left")
    nat.to_csv(os.path.join(out, "extend_drivers_national.csv"), index=False)
    # state: 2015 capacity factors (fallback for NREL resource), 2015 gas share
    # nameplate 2014-2025 from the raw EIA file (same filter as build_panel.py), for the full-year capacity factor (deviation X4)
    c = pd.read_excel(os.path.join(raw, "eia/existcapacity_annual.xlsx"), header=1)
    c.columns = ["year", "state", "producer", "source", "generators", "facilities", "nameplate_mw", "summer_mw"]
    c = c[(c.producer == "Total Electric Power Industry") & c.state.isin(P.state.unique()) & c.year.between(2014, Y1) & c.source.isin(["Wind", "Solar Thermal and Photovoltaic"])]
    c["nameplate_mw"] = pd.to_numeric(c.nameplate_mw, errors="coerce")
    cap = c.pivot_table(index=["state", "year"], columns="source", values="nameplate_mw", aggfunc="sum").fillna(0).rename(columns={"Wind": "wind", "Solar Thermal and Photovoltaic": "solar"})
    st = []
    for s_, g in P.sort_values("year").groupby("state"):
        row = {"state": s_}
        for k in ["wind", "solar"]:
            cs = cap.loc[s_][k].reindex(range(2014, Y1 + 1), fill_value=0) if s_ in cap.index.get_level_values(0) else pd.Series(0.0, index=range(2014, Y1 + 1))
            row[f"{k}_cf"], row[f"{k}_cf_year"], row[f"{k}_cf_flag"] = 0.0, np.nan, "never qualifies; set to 0"
            for y in range(Y0, Y1 + 1):
                if cs[y - 1] >= 10:
                    gen = g.loc[g.year == y, f"gen_{k}_mwh"].iloc[0]
                    row[f"{k}_cf"] = gen / ((cs[y - 1] + cs[y]) / 2 * 8760); row[f"{k}_cf_year"] = y
                    row[f"{k}_cf_flag"] = "" if y == 2015 else "later year"
                    break
        g15 = g[g.year == 2015].iloc[0]; row["gas_share_2015"] = g15.gen_gas_mwh / g15.gen_total_mwh
        st.append(row)
    st = pd.DataFrame(st); st.to_csv(os.path.join(out, "extend_drivers_state.csv"), index=False)
    log.append(f"State drivers: {len(st)} states. Wind CF from 2015: {(st.wind_cf_flag == '').sum()}, later year: {(st.wind_cf_flag == 'later year').sum()}, zero: {(st.wind_cf_flag.str.startswith('never')).sum()} ({', '.join(st[st.wind_cf_flag.str.startswith('never')].state)})")
    log.append(f"Solar CF from 2015: {(st.solar_cf_flag == '').sum()}, later year: {(st.solar_cf_flag == 'later year').sum()}, zero: {(st.solar_cf_flag.str.startswith('never')).sum()} ({', '.join(st[st.solar_cf_flag.str.startswith('never')].state)})")
    log.append(f"Wind CF range {st[st.wind_cf > 0].wind_cf.min():.3f}-{st.wind_cf.max():.3f}; solar CF range {st[st.solar_cf > 0].solar_cf.min():.3f}-{st.solar_cf.max():.3f}")
    os.makedirs(logd, exist_ok=True); open(os.path.join(logd, "drivers_build.log"), "w").write("\n".join(log) + "\n"); print("\n".join(log))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

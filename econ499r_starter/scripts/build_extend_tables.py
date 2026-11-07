#!/usr/bin/env python3
"""Outcomes for prompts/09_extend.md sections 2-3 (EXPERIMENTS.md sections 14.2-14.3), from files already in data/raw.

Usage: build_extend_tables.py <raw_dir> <data_dir> <log_dir>

Writes
  <data_dir>/extend_outcomes.csv      51 areas x 2015-2025: by-type shares, ln generation, MW added per 1,000 MW of 2015 capacity,
                                      sector sales per person and prices, net imports, power-sector CO2, SEDS by type
  <data_dir>/extend_restructured.csv  51 areas: 2015 energy-only providers' share of retail sales, restructured flag (>= 10%)
  <log_dir>/extend_tables_build.log
Generation, capacity, sales and CO2 use the same EIA files and filters as build_panel.py (Total Electric Power Industry; nameplate MW).
"""
import os, sys
import numpy as np, pandas as pd

Y0, Y1 = 2015, 2025
CUTOFF = 10.0


def main(raw, out, logd):
    log = []
    P = pd.read_csv(os.path.join(out, "out", "state_panel_2015_2025.csv")) if os.path.exists(os.path.join(out, "out", "state_panel_2015_2025.csv")) else pd.read_csv("data/out/state_panel_2015_2025.csv")
    states = sorted(P.state.unique()); assert len(states) == 51
    # ---------- capacity, 2014-2025, as build_panel.py ----------
    c = pd.read_excel(os.path.join(raw, "eia/existcapacity_annual.xlsx"), header=1)
    c.columns = ["year", "state", "producer", "source", "generators", "facilities", "nameplate_mw", "summer_mw"]
    c = c[(c.producer == "Total Electric Power Industry") & c.state.isin(states) & c.year.between(2014, Y1)]
    c["nameplate_mw"] = pd.to_numeric(c.nameplate_mw, errors="coerce")
    cp = c.pivot_table(index=["state", "year"], columns="source", values="nameplate_mw", aggfunc="sum").fillna(0)
    log.append(f"Capacity sources: {sorted(cp.columns)}")
    cp["bio"] = cp.get("Wood and Wood Derived Fuels", 0) + cp.get("Other Biomass", 0)
    m = {"wind": "Wind", "solar": "Solar Thermal and Photovoltaic", "hydro": "Hydroelectric", "geo": "Geothermal", "bio": "bio", "gas": "Natural Gas"}
    cap = pd.DataFrame(index=cp.index)
    for k, src in m.items():
        cap[f"cap_{k}"] = cp[src]
    cap["cap_total"] = cp["All Sources"]
    cap = cap.reset_index().sort_values(["state", "year"])
    base = cap[cap.year == 2015].set_index("state").cap_total
    for k in m:
        cap[f"add_{k}_per1000"] = cap.groupby("state")[f"cap_{k}"].diff() / cap.state.map(base) * 1000
    cap = cap[cap.year.between(Y0, Y1)]
    # gate against the panel's new_solar_mw and new_wind_mw
    chk = P.merge(cap, on=["state", "year"])
    for k in ["solar", "wind"]:
        d = (chk[f"new_{k}_mw"] - chk[f"add_{k}_per1000"] * chk.state.map(base) / 1000).abs().max()
        log.append(f"Gate: MW added, {k}, vs panel new_{k}_mw: max |diff| = {d:.6f} MW"); assert d < 1e-6, d
    # ---------- generation-based outcomes from the panel ----------
    o = P[["state", "year", "is_dc", "population", "gen_total_mwh", "sales_mwh", "sales_res_mwh", "sales_com_mwh", "sales_ind_mwh", "co2_power_t", "co2_per_mwh_t"]].copy()
    gen = {"wind": P.gen_wind_mwh, "solar": P.gen_solar_mwh, "hydro": P.gen_hydro_mwh, "geo": P.gen_geothermal_mwh, "bio": P.gen_wood_mwh + P.gen_otherbio_mwh,
           "gas": P.gen_gas_mwh, "coal": P.gen_coal_mwh, "nuclear": P.gen_nuclear_mwh}
    for k, v in gen.items():
        o[f"share_{k}"] = v / P.gen_total_mwh
        if k in ("wind", "solar", "hydro", "geo", "bio"):
            o[f"ln_gen_{k}"] = np.where(v > 0, np.log(v.where(v > 0)), np.nan)
    for s in ["res", "com", "ind"]:
        o[f"ln_sales_{s}_pc"] = np.log(P[f"sales_{s}_mwh"] / P.population)
    o["net_imports"] = (P.sales_mwh - P.gen_total_mwh) / P.sales_mwh
    o["ln_co2_power"] = np.log(P.co2_power_t.where(P.co2_power_t > 0))
    o = o.merge(cap.drop(columns=[c_ for c_ in cap.columns if c_.startswith("cap_")]), on=["state", "year"], how="left")
    # ---------- prices by sector, EIA-861 ----------
    def sheet(name):
        d = pd.read_excel(os.path.join(raw, "eia/HS861_2010-.xlsx"), sheet_name=name, header=None, skiprows=3)
        d = d.iloc[:, :22]; d.columns = ["year", "state"] + [f"{s}_{v}" for s in ["res", "com", "ind", "trn", "tot"] for v in ["rev", "sales", "cust", "price"]]
        d = d[pd.to_numeric(d.year, errors="coerce").notna()].copy(); d["year"] = d.year.astype(int)
        for col in d.columns[2:]:
            d[col] = pd.to_numeric(d[col], errors="coerce")
        return d
    t = sheet("Total Electric Industry")
    t = t[t.state.isin(states) & t.year.between(Y0, Y1)]
    o = o.merge(t[["state", "year", "res_price", "com_price", "ind_price", "tot_sales"]].rename(columns={"res_price": "price_res_c_kwh", "com_price": "price_com861_c_kwh", "ind_price": "price_ind_c_kwh", "tot_sales": "sales861_mwh"}), on=["state", "year"], how="left")
    d = (o.sales861_mwh - o.sales_mwh).abs().max(); log.append(f"Check: EIA-861 total sales vs panel sales_mwh, max |diff| = {d:,.0f} MWh")
    pc = P[["state", "year", "price_com_c_kwh"]].merge(o[["state", "year", "price_com861_c_kwh"]]); log.append(f"Check: commercial price vs panel price_com_c_kwh, max |diff| = {(pc.price_com_c_kwh - pc.price_com861_c_kwh).abs().max():.4f}")
    o = o.drop(columns=["sales861_mwh"])
    # ---------- SEDS by type (current basis) ----------
    sb = pd.read_csv(os.path.join(out, "seds_old_basis.csv"))
    sb["ln_seds_woodwaste"] = np.log(sb.WWTCB.where(sb.WWTCB > 0)); sb["ln_seds_biofuels"] = np.log(sb.BFTCB.where(sb.BFTCB > 0))
    sb["ln_seds_re_exbiomass"] = np.log(sb.re_excl_biomass_current.where(sb.re_excl_biomass_current > 0))
    sb["ln_seds_re_exbiofuels"] = np.log(sb.re_excl_biofuels_current.where(sb.re_excl_biofuels_current > 0))
    sb["ln_seds_re_total"] = np.log(sb.re_bbtu_current)
    o = o.merge(sb[["state", "year", "ln_seds_woodwaste", "ln_seds_biofuels", "ln_seds_re_exbiomass", "ln_seds_re_exbiofuels", "ln_seds_re_total"]], on=["state", "year"], how="left")
    assert len(o) == 51 * 11
    o.sort_values(["state", "year"]).to_csv(os.path.join(out, "extend_outcomes.csv"), index=False)
    nz = {k: int((o[o.is_dc == 0][f"ln_gen_{k}"].notna()).sum()) for k in ["wind", "solar", "hydro", "geo", "bio"]}
    log.append(f"extend_outcomes.csv: {len(o)} rows x {o.shape[1]} cols; nonzero generation state-years (50 states): {nz}")
    # ---------- restructured ----------
    e = sheet("Energy Only Providers")
    e15 = e[(e.year == 2015)].groupby("state").tot_sales.sum()
    t15 = t[t.year == 2015].set_index("state").tot_sales
    r = pd.DataFrame({"state": states})
    r["energy_only_sales_mwh_2015"] = r.state.map(e15).fillna(0); r["total_sales_mwh_2015"] = r.state.map(t15)
    r["energy_only_share_pct_2015"] = 100 * r.energy_only_sales_mwh_2015 / r.total_sales_mwh_2015
    r["restructured"] = (r.energy_only_share_pct_2015 >= CUTOFF).astype(int)
    r["near_cutoff_flag"] = ((r.energy_only_share_pct_2015 - CUTOFF).abs() <= 5).astype(int)
    r["restructured_prereg_rule"] = r.restructured
    # Deviation X1 (EXPERIMENTS.md 14.3): Texas's competitive retailers are bundled "Retail Power Marketers", absent from the summary sheets
    import zipfile
    with zipfile.ZipFile(os.path.join(raw, "eia_forms/f8612025.zip")) as z:
        v = pd.read_excel(z.open("Sales_Ult_Cust_2025.xlsx"), sheet_name="States", header=None, skiprows=3)
    v = v.iloc[:, [4, 6, 7, 21]]; v.columns = ["svc", "state", "own", "tot_sales"]; v["tot_sales"] = pd.to_numeric(v.tot_sales, errors="coerce")
    v = v[v.svc.isin(["Bundled", "Energy"])]
    rpm = 100 * v[v.own == "Retail Power Marketer"].groupby("state").tot_sales.sum() / v.groupby("state").tot_sales.sum()
    r["rpm_share_pct_2025"] = r.state.map(rpm).fillna(0)
    r.loc[r.state == "TX", "restructured"] = 1
    r["restructured_check_rpm2025"] = (r.rpm_share_pct_2025 >= CUTOFF).astype(int)
    r["near_cutoff_flag_check"] = ((r.rpm_share_pct_2025 - CUTOFF).abs() <= 5).astype(int)
    r["source"] = "EIA-861 HS861_2010-.xlsx (Energy Only Providers / Total Electric Industry, 2015); TX set to restructured (deviation X1); check from f8612025.zip Sales_Ult_Cust_2025.xlsx"
    r.sort_values("energy_only_share_pct_2015", ascending=False).to_csv(os.path.join(out, "extend_restructured.csv"), index=False)
    rr = r.sort_values("energy_only_share_pct_2015", ascending=False)
    log.append("Restructured (>= 10%): " + ", ".join(f"{a} {b:.1f}" for a, b in zip(rr[rr.restructured == 1].state, rr[rr.restructured == 1].energy_only_share_pct_2015)))
    log.append("Near cutoff (5-15%): " + ", ".join(f"{a} {b:.1f}" for a, b in zip(rr[rr.near_cutoff_flag == 1].state, rr[rr.near_cutoff_flag == 1].energy_only_share_pct_2015)))
    log.append("Main classification (with TX, deviation X1): " + ", ".join(sorted(r[r.restructured == 1].state)))
    log.append("Check, retail power marketers 2025 >= 10%: " + ", ".join(sorted(r[r.restructured_check_rpm2025 == 1].state)) + "; near cutoff: " + ", ".join(f"{a} {b:.1f}" for a, b in zip(r[r.near_cutoff_flag_check == 1].state, r[r.near_cutoff_flag_check == 1].rpm_share_pct_2025)))
    log.append("Regulated, share > 0: " + ", ".join(f"{a} {b:.1f}" for a, b in zip(rr[(rr.restructured == 0) & (rr.energy_only_share_pct_2015 > 0)].state, rr[(rr.restructured == 0) & (rr.energy_only_share_pct_2015 > 0)].energy_only_share_pct_2015)))
    os.makedirs(logd, exist_ok=True)
    open(os.path.join(logd, "extend_tables_build.log"), "w").write("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

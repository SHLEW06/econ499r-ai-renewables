#!/usr/bin/env python3
"""Side tables for prompts/08_finalize.md section 1 and prompts/09_extend.md section 2.

Usage: build_finalize_tables.py <raw_dir> <data_dir> <log_dir>

Writes
  <data_dir>/seds_old_basis.csv      51 states x 2015-2024: current SEDS renewables by component, the year-by-year
                                     rebuild on the old fossil-fuel-equivalence basis, the archived (June 2023) values
                                     for 2015-2021, fossil fuels, total energy, and biomass split into wood/waste vs biofuels
  <data_dir>/storm_events_state.csv  51 states x 2015-2024: extreme heat and cold event counts (NOAA Storm Events)
  <log_dir>/seds_rebuild_check.csv   rebuild vs archive, by state-year (2015-2021)
  <log_dir>/seds_rebuild_national.csv  rebuild summed over states vs EIA's national fossil-fuel-equivalent series
  <log_dir>/finalize_tables_build.log

Rebuild rule (follows the SEDS archive component by component; see data/receipts/seds_old_basis.md):
  old = BMTCB + k_t * (WYTCB + HYTCB + GEEGB + SOEGB + SOCCB + SOICB + PVres) + (GECCB + GEICB + GERCB) + (SORCB - PVres)
  k_t = HR_t / 3.412, HR_t = EIA's fossil-fueled plant heat rate (thousand Btu/kWh), PVres = SOR7P x 3.412 (billion Btu)
"""
import glob, json, os, sys, zipfile
import numpy as np, pandas as pd

ST = {"ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA", "COLORADO": "CO", "CONNECTICUT": "CT",
      "DELAWARE": "DE", "DISTRICT OF COLUMBIA": "DC", "FLORIDA": "FL", "GEORGIA": "GA", "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL",
      "INDIANA": "IN", "IOWA": "IA", "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
      "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS", "MISSOURI": "MO", "MONTANA": "MT", "NEBRASKA": "NE",
      "NEVADA": "NV", "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ", "NEW MEXICO": "NM", "NEW YORK": "NY", "NORTH CAROLINA": "NC",
      "NORTH DAKOTA": "ND", "OHIO": "OH", "OKLAHOMA": "OK", "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI",
      "SOUTH CAROLINA": "SC", "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", "VERMONT": "VT", "VIRGINIA": "VA",
      "WASHINGTON": "WA", "WEST VIRGINIA": "WV", "WISCONSIN": "WI", "WYOMING": "WY"}
HEAT = ["Excessive Heat", "Heat"]
COLD = ["Extreme Cold/Wind Chill", "Cold/Wind Chill"]
Y0, Y1 = 2015, 2024
MSN = ["WYTCB", "HYTCB", "SOTCB", "SOEGB", "SOCCB", "SOICB", "SORCB", "GETCB", "GEEGB", "GECCB", "GEICB", "GERCB", "BMTCB", "WWTCB",
       "BFTCB", "EMTCB", "BDTCB", "B1TCB", "RETCB", "FFTCB", "TETCB"]


def long(df, msns, valname):
    d = df[df.MSN.isin(msns) & df.State.isin(ST.values())].drop(columns=["Data_Status"])
    d = d.melt(id_vars=["State", "MSN"], var_name="year", value_name=valname)
    d = d[d.year.str.isnumeric()]
    d["year"] = d.year.astype(int)
    d[valname] = pd.to_numeric(d[valname], errors="coerce")
    return d[d.year.between(Y0, Y1)]


def main(raw, out, logd):
    os.makedirs(logd, exist_ok=True)
    log = []
    # ---- heat rate: EIA bulk MER, wind fossil-fuel-equivalent / wind captured x 3.412 ----
    D = {}
    with zipfile.ZipFile(os.path.join(raw, "eia/mer/TOTAL.zip")) as z:
        for line in z.open("TOTAL.txt"):
            j = json.loads(line)
            sid = j.get("series_id", "")
            if j.get("f") == "A" and sid in {f"TOTAL.{s}.A" for s in ["WYFFBUS", "WYTCBUS", "HVFFBUS", "HVTCBUS", "REFFBUS", "RETCBUS"]}:
                D[sid.split(".")[1]] = {int(k): float(v) for k, v in j["data"] if v not in ("NA", "- -", "--", "W", "NM")}
    hr = {y: round(3.412 * D["WYFFBUS"][y] / D["WYTCBUS"][y], 3) for y in range(Y0, Y1 + 1)}
    hr_h = {y: round(3.412 * D["HVFFBUS"][y] / D["HVTCBUS"][y], 3) for y in range(Y0, Y1 + 1)}
    assert all(abs(hr[y] - hr_h[y]) < 0.002 for y in hr), "wind and hydro implied heat rates differ"
    # ---- archive (June 2023 release, data through 2021) ----
    with zipfile.ZipFile(os.path.join(raw, "eia/seds_archive/complete_seds_2021.zip")) as z:
        a = pd.read_csv(z.open("complete_seds_2021.csv"))
    ff = a[(a.MSN == "FFETK") & (a.StateCode == "US") & a.Year.between(Y0, 2021)].set_index("Year").Data.to_dict()
    for y, v in ff.items():
        assert abs(v - hr[y]) < 0.0015, f"heat rate {y}: MER-implied {hr[y]} vs archived FFETK {v}"
    log.append(f"Heat rate (thousand Btu/kWh): {hr}; matches archived SEDS FFETK 2015-2021 to 0.001")
    arc = a[a.MSN.isin(["RETCB", "WYTCB", "HYTCB", "SOTCB", "GETCB", "BMTCB", "TETCB"]) & a.StateCode.isin(ST.values()) & a.Year.between(Y0, 2021)]
    arc = arc.pivot_table(index=["StateCode", "Year"], columns="MSN", values="Data").add_suffix("_arch2021").reset_index()
    arc = arc.rename(columns={"StateCode": "state", "Year": "year"})
    # ---- current SEDS ----
    u = pd.read_csv(os.path.join(raw, "eia/seds/use_all_btu.csv"))
    ph = pd.read_csv(os.path.join(raw, "eia/seds/use_all_phy.csv"))
    w = pd.concat([long(u, MSN, "v"), long(ph, ["SOR7P"], "v")]).pivot_table(index=["State", "year"], columns="MSN", values="v").reset_index()
    w = w.rename(columns={"State": "state"}).fillna({"SOR7P": 0.0})
    w.columns.name = None
    assert len(w) == 51 * (Y1 - Y0 + 1), len(w)
    w["hr_kbtu_kwh"] = w.year.map(hr)
    w["k_t"] = w.hr_kbtu_kwh / 3.412
    w["pv_res_bbtu"] = w.SOR7P * 3.412
    elec = w.WYTCB + w.HYTCB + w.GEEGB + w.SOEGB + w.SOCCB + w.SOICB + w.pv_res_bbtu
    direct = (w.GECCB + w.GEICB + w.GERCB) + (w.SORCB - w.pv_res_bbtu)
    w["re_bbtu_current"] = w.RETCB
    w["re_bbtu_rebuilt"] = w.BMTCB + w.k_t * elec + direct
    w["re_bbtu_k26"] = w.BMTCB + 2.6 * (w.WYTCB + w.HYTCB + w.SOTCB + w.GETCB)
    w["re_bbtu_rebuilt_allconv"] = w.BMTCB + w.k_t * (w.WYTCB + w.HYTCB + w.SOTCB + w.GETCB)  # 08's literal wording, a check
    w["noncomb_elec_bbtu_current"] = elec
    w["fossil_bbtu"] = w.FFTCB
    w["fossil_share_total"] = w.FFTCB / w.TETCB
    w["biofuels_bbtu"] = w.BFTCB
    w["woodwaste_bbtu"] = w.WWTCB
    w["re_excl_biomass_current"] = w.RETCB - w.BMTCB
    w["re_excl_biofuels_current"] = w.RETCB - w.BFTCB
    # current-basis identity check
    chk = (w.WYTCB + w.HYTCB + w.SOTCB + w.GETCB + w.BMTCB - w.RETCB).abs().max()
    log.append(f"Current SEDS: max |WY+HY+SO+GE+BM - RETCB| = {chk:.1f} billion Btu")
    chk2 = (w.WWTCB + w.BFTCB - w.BMTCB).abs()
    log.append(f"Biomass split: max |WWTCB + BFTCB - BMTCB| = {chk2.max():.1f}; share of state-years off by > 1%: {(chk2 / w.BMTCB.clip(lower=1) > 0.01).mean():.3f}")
    w = w.merge(arc, on=["state", "year"], how="left")
    # ---- check against archive ----
    c = w[w.year <= 2021][["state", "year", "re_bbtu_rebuilt", "re_bbtu_rebuilt_allconv", "re_bbtu_k26", "re_bbtu_current", "RETCB_arch2021", "BMTCB", "BMTCB_arch2021"]].copy()
    for col in ["re_bbtu_rebuilt", "re_bbtu_rebuilt_allconv", "re_bbtu_k26", "re_bbtu_current"]:
        c[f"pct_diff_{col}"] = 100 * (c[col] / c.RETCB_arch2021 - 1)
    # same rebuild with the archive's own biomass, to separate method from data revisions
    c["re_rebuilt_archbiomass"] = c.re_bbtu_rebuilt - c.BMTCB + c.BMTCB_arch2021
    c["pct_diff_rebuilt_archbiomass"] = 100 * (c.re_rebuilt_archbiomass / c.RETCB_arch2021 - 1)
    c.to_csv(os.path.join(logd, "seds_rebuild_check.csv"), index=False)
    for col in ["re_bbtu_rebuilt", "re_bbtu_rebuilt_allconv", "re_bbtu_k26", "re_bbtu_current", "rebuilt_archbiomass"]:
        x = c[f"pct_diff_{col}"].abs()
        log.append(f"vs archive, {col}: median |diff| {x.median():.2f}%, 90th pct {x.quantile(.9):.2f}%, max {x.max():.2f}%; "
                   f"corr of logs {np.corrcoef(np.log(c[col if col != 'rebuilt_archbiomass' else 're_rebuilt_archbiomass']), np.log(c.RETCB_arch2021))[0,1]:.5f}")
    # ---- national check vs EIA fossil-fuel-equivalent renewables (REFFBUS) ----
    n = w.groupby("year")[["re_bbtu_rebuilt", "re_bbtu_current"]].sum().reset_index()
    n["eia_reffbus_bbtu"] = n.year.map(lambda y: D["REFFBUS"][y] * 1000)
    n["eia_retcbus_bbtu"] = n.year.map(lambda y: D["RETCBUS"][y] * 1000)
    n["pct_diff_rebuilt_vs_eia_ffe"] = 100 * (n.re_bbtu_rebuilt / n.eia_reffbus_bbtu - 1)
    n["pct_diff_current_vs_eia_captured"] = 100 * (n.re_bbtu_current / n.eia_retcbus_bbtu - 1)
    n.to_csv(os.path.join(logd, "seds_rebuild_national.csv"), index=False)
    log.append("National: rebuilt sum of 51 vs EIA REFFBUS, % diff by year: " + ", ".join(f"{int(r.year)} {r.pct_diff_rebuilt_vs_eia_ffe:+.2f}" for r in n.itertuples()))
    keep = ["state", "year", "hr_kbtu_kwh", "k_t", "re_bbtu_current", "re_bbtu_rebuilt", "re_bbtu_rebuilt_allconv", "re_bbtu_k26", "RETCB_arch2021",
            "WYTCB", "HYTCB", "SOTCB", "GETCB", "BMTCB", "WWTCB", "BFTCB", "EMTCB", "BDTCB", "B1TCB", "SOR7P", "pv_res_bbtu", "noncomb_elec_bbtu_current",
            "fossil_bbtu", "TETCB", "fossil_share_total", "re_excl_biomass_current", "re_excl_biofuels_current"]
    w[keep].sort_values(["state", "year"]).to_csv(os.path.join(out, "seds_old_basis.csv"), index=False)
    log.append(f"seds_old_basis.csv: {len(w)} rows, {w.state.nunique()} states, {Y0}-{Y1}; NA in re_bbtu_rebuilt: {int(w.re_bbtu_rebuilt.isna().sum())}")
    # ---- storm events ----
    rows = []
    for y in range(Y0, Y1 + 1):
        f = glob.glob(os.path.join(raw, f"noaa/storm_events/StormEvents_details-ftp_v1.0_d{y}_c*.csv.gz"))
        assert len(f) == 1, f
        e = pd.read_csv(f[0], usecols=["BEGIN_YEARMONTH", "EPISODE_ID", "EVENT_ID", "STATE", "EVENT_TYPE"], low_memory=False)
        e = e[e.STATE.isin(ST) & e.EVENT_TYPE.isin(HEAT + COLD)].copy()
        assert (e.BEGIN_YEARMONTH // 100 == y).all()
        e["state"] = e.STATE.map(ST)
        e["kind"] = np.where(e.EVENT_TYPE.isin(HEAT), "heat", "cold")
        g = e.groupby(["state", "kind"]).agg(events=("EVENT_ID", "nunique"), episodes=("EPISODE_ID", "nunique")).unstack("kind", fill_value=0)
        g.columns = [f"{a}_{b}" for a, b in g.columns]
        g = g.reindex(sorted(ST.values()), fill_value=0).reset_index().rename(columns={"index": "state"})
        g["year"] = y
        rows.append(g)
    s = pd.concat(rows)
    for c_ in ["events_heat", "events_cold", "episodes_heat", "episodes_cold"]:
        if c_ not in s:
            s[c_] = 0
    s["extreme_events"] = s.events_heat + s.events_cold
    s["extreme_episodes"] = s.episodes_heat + s.episodes_cold
    s = s[["state", "year", "events_heat", "events_cold", "extreme_events", "episodes_heat", "episodes_cold", "extreme_episodes"]].sort_values(["state", "year"])
    assert len(s) == 51 * (Y1 - Y0 + 1)
    s.to_csv(os.path.join(out, "storm_events_state.csv"), index=False)
    z = s[s.year.between(2018, 2021)].groupby("state").extreme_events.mean()
    log.append(f"storm_events_state.csv: {len(s)} rows. 2018-2021 state mean events: mean {z.mean():.1f}, median {z.median():.1f}; "
               f"states above mean {int((z > z.mean()).sum())}, zero-event states {list(z[z == 0].index)}")
    with open(os.path.join(logd, "finalize_tables_build.log"), "w") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

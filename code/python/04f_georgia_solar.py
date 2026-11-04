#!/usr/bin/env python3
"""Georgia solar cost module: learning-curve arithmetic to 2035 (Phase 4f). Not a forecast of ours, and no AI variable.
Usage: python3 code/python/04f_georgia_solar.py --date YYYY-MM-DD

C_t = C_base x (X_t / X_base)^b, b = ln(1 - LR) / ln 2 (Bolinger, Wiser and O'Shaughnessy 2022).
Capacity paths use published IEA scenario growth, applied to IRENA's series. Years between 2025 and 2035 are log-linear
interpolation, which is our arithmetic and not IEA's.
"""
import argparse, math, os, sys
import numpy as np, openpyxl, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); a = ap.parse_args()
for f in ("data/lbnl_utility_solar.csv", "data/owid_global_solar_capacity.csv", "data/raw/lbnl/Utility Scale Solar 2026 Edition Datafile.xlsx"):
    if not os.path.exists(f): sys.exit(f"Missing input: {f}")
R = f"results/{a.date}/georgia_solar"; F = f"results/{a.date}/figures"; os.makedirs(R, exist_ok=True); os.makedirs(F, exist_ok=True)
L, K = "pv_lcoe_no_tax_credits_2025_mwh", "solar_capacity_mw_ac"
d = pd.read_csv("data/lbnl_utility_solar.csv"); pv = d[(d.solar_tech_main == "PV") & d[L].notna()].copy()
o = pd.read_csv("data/owid_global_solar_capacity.csv"); X = o[o.entity == "World"].set_index("year").solar_pv_ongrid_gw
cw = lambda g: (g[L] * g[K]).sum() / g[K].sum()

# ---- Base cost ----
rows = []
for nm, g in (("Georgia", pv[pv.state == "GA"]), ("Southeast (non-ISO)", pv[pv.region.astype(str).str.contains("Southeast")]), ("United States", pv)):
    w = g[g.solar_cod_year.between(2023, 2025)]
    rows.append(dict(area=nm, window="COD 2023-2025", n_projects=len(w), mw_ac=round(w[K].sum(), 1), lcoe_capacity_weighted=round(cw(w), 2), lcoe_median=round(w[L].median(), 2), lcoe_p25=round(w[L].quantile(.25), 2), lcoe_p75=round(w[L].quantile(.75), 2), x_base_gw=round(((w.solar_cod_year.map(X)) * w[K]).sum() / w[K].sum(), 1), source="LBNL Utility-Scale Solar 2026 Edition, Individual_Project_Data, PV LCOE no Tax Credits (2025$/MWh)"))
base = pd.DataFrame(rows); base.to_csv(f"{R}/base_cost.csv", index=False)
ga = base[base.area == "Georgia"].iloc[0]; Cb, Xb = float(ga.lcoe_capacity_weighted), float(ga.x_base_gw)
print(base.drop(columns="source").to_string(index=False))

# ---- Capacity paths: IEA growth 2024 to 2035, applied to IRENA 2024 ----
IEA24 = 2164
SC = [("Low", "IEA WEO 2025 Current Policies", 8067, "Table A.3a, p. 417"), ("Central", "IEA WEO 2025 Stated Policies", 8855, "Table A.3b, p. 423"), ("High", "IEA WEO 2025 Net Zero Emissions by 2050", 12499, "Table A.3c, p. 429")]
paths = []
for nm, src, v, pg in SC:
    x35 = X[2024] * v / IEA24
    for y in range(2025, 2036):
        val = X[2025] * (x35 / X[2025]) ** ((y - 2025) / 10)
        paths.append(dict(path=nm, source=src, source_location=pg, iea_2024_gw=IEA24, iea_2035_gw=v, growth_ratio_2024_2035=round(v / IEA24, 4), year=y, global_pv_gw=round(val, 1), basis="2025 is IRENA actual; 2035 is IRENA 2024 x IEA growth ratio; years between are log-linear interpolation (our arithmetic)"))
pa = pd.DataFrame(paths); pa.to_csv(f"{R}/capacity_paths.csv", index=False)

# ---- Projection ----
LR = [(.12, "12%"), (.19, "19% (CapEx)"), (.24, "24% (main)"), (.45, "45% (2014-2020 epoch)")]
pr = []
for nm, _, _, _ in SC:
    g = pa[pa.path == nm].set_index("year").global_pv_gw
    for lr, lab in LR:
        b = math.log(1 - lr) / math.log(2)
        for y in range(2025, 2036):
            pr.append(dict(tag=f"ga_solar_lc_lr{int(lr * 100)}_cap-{nm.lower()}_{y}", path=nm, learning_rate=lr, lr_label=lab, b=round(b, 4), year=y, global_pv_gw=g[y], lcoe_2025usd_mwh=round(Cb * (g[y] / Xb) ** b, 2), status="ok"))
p = pd.DataFrame(pr); p.to_csv(f"{R}/projection_long.csv", index=False)
wide = p[p.year.isin([2025, 2030, 2035])].pivot_table(index=["lr_label", "path"], columns="year", values="lcoe_2025usd_mwh").reset_index()
wide["change_2025_2035_pct"] = (100 * (wide[2035] / wide[2025] - 1)).round(1)
wide["lr_order"] = wide.lr_label.str[:2].astype(int); wide["p_order"] = wide.path.map({"Low": 0, "Central": 1, "High": 2}); wide = wide.sort_values(["lr_order", "p_order"]).drop(columns=["lr_order", "p_order"]); wide.columns = [str(c) for c in wide.columns]
wide.to_csv(f"{R}/projection_table.csv", index=False)
print(wide.to_string(index=False))

# ---- Re-estimate Bolinger eq. 2 ----
ws = openpyxl.load_workbook("data/raw/lbnl/Utility Scale Solar 2026 Edition Datafile.xlsx", read_only=True, data_only=True)["LCOE Trend (PV only)"]
rw = list(ws.iter_rows(values_only=True)); print("LCOE tab rows", len(rw)); [print(i + 1, [str(round(x, 1) if isinstance(x, float) else x)[:22] for x in r[:8] if x is not None]) for i, r in enumerate(rw) if i < 32 and any(v is not None for v in r[:8]) and i > 18]
nat = pv.groupby("solar_cod_year").apply(lambda g: pd.Series(dict(n=len(g), mw=g[K].sum(), lcoe=cw(g))), include_groups=False).reset_index().rename(columns={"solar_cod_year": "year"}); nat["x"] = nat.year.map(X)
def fit(n, lab):
    x = np.log(n.x); y = np.log(n.lcoe); B = np.polyfit(x, y, 1); e = y - np.polyval(B, x); s2 = (e ** 2).sum() / (len(n) - 2); se = math.sqrt(s2 / ((x - x.mean()) ** 2).sum()); t = 2.2281 if len(n) == 12 else None
    return dict(window=lab, n_years=len(n), b=round(B[0], 4), se_b=round(se, 4), learning_rate_pct=round(100 * (1 - 2 ** B[0]), 1), r2=round(1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum(), 3), note="Capacity-weighted national LCOE by COD year, from LBNL project data, on IRENA global capacity. Conventional SE. Not normalized, unlike Bolinger's 24%")
hdr = next(i for i, r in enumerate(rw) if r[0] and str(r[0]).startswith("Commercial Operation"))
print("tab header:", [str(x)[:60] for x in rw[hdr][:5]], "| above:", [str(x)[:60] for x in rw[hdr - 1][:5]])
tb = pd.DataFrame([dict(year=int(r[0]), n=r[1], mw=r[2], lcoe=r[3], lcoe_with_tax_credit=r[4]) for r in rw[hdr + 1:] if isinstance(r[0], (int, float)) and 2000 < r[0] < 2030 and isinstance(r[3], (int, float))]); tb["x"] = tb.year.map(X)
tb.round(2).to_csv(f"{R}/national_lcoe_lbnl_tab.csv", index=False); print(tb.round(1).to_string(index=False))
def note(f, t): f["note"] = t; return f
TAB = "LBNL's published generation-weighted national LCOE, tab LCOE Trend (PV only), on IRENA global capacity. Conventional SE. Not normalized, unlike Bolinger's 24%"
ws_ = [dict(series="LBNL tab", **note(fit(tb[tb.year.between(y0, y1)], f"{y0}-{y1}"), TAB)) for y0, y1 in ((tb.year.min(), 2024), (tb.year.min(), 2021), (tb.year.min(), tb.year.max()))] + [dict(series="Rebuilt from projects", **fit(nat[nat.year.between(2013, 2024)], "2013-2024"))]
re = pd.DataFrame(ws_); re.to_csv(f"{R}/learning_rate_check.csv", index=False); nat.round(2).to_csv(f"{R}/national_lcoe_series.csv", index=False); print(re.drop(columns="note").to_string(index=False)); print(nat.round(1).to_string(index=False))

# ---- Fan chart ----
BLUE, INK, MUTE, GRID, SURF, GR = "#2a78d6", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#a3a29d"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "text.color": INK, "axes.labelcolor": MUTE, "xtick.color": MUTE, "ytick.color": MUTE})
fig, ax = plt.subplots(1, 3, figsize=(12, 4.3), sharey=True, facecolor=SURF)
for A, (nm, src, v, pg) in zip(ax, SC):
    A.set_facecolor(SURF)
    for lr, lab in LR:
        g = p[(p.path == nm) & (p.learning_rate == lr)]; main = lr == .24
        A.plot(g.year, g.lcoe_2025usd_mwh, color=BLUE if main else GR, lw=2.6 if main else 1.6, zorder=3 if main else 2)
        A.text(2035.2, g.lcoe_2025usd_mwh.iloc[-1], f"{lab.split(' ')[0]}  ${g.lcoe_2025usd_mwh.iloc[-1]:.0f}", va="center", fontsize=8.5, color=INK if main else MUTE)
    A.set_title(f"{nm}: {src.replace('IEA WEO 2025 ', '')}\n{v:,} GW in 2035 on IEA's basis", loc="left", fontsize=9.5); A.set_xlim(2025, 2038.3); A.set_xticks([2025, 2030, 2035]); A.grid(axis="y", color=GRID, lw=.8); A.set_ylim(0, 75)
    for s in ("top", "right", "left"): A.spines[s].set_visible(False)
    A.tick_params(axis="y", length=0)
ax[0].set_ylabel("LCOE, 2025 $/MWh, no tax credits")
fig.suptitle("What learning-curve arithmetic implies for Georgia utility-scale solar", x=.012, y=.985, ha="left", fontsize=13, fontweight="bold")
fig.text(.012, .895, f"Starts from ${Cb:.2f}/MWh (17 Georgia projects, 2023-2025). Labels show learning rate and 2035 cost. These are not forecasts of ours; 24% is the main rate.", fontsize=9.5, color=MUTE)
fig.tight_layout(rect=(0, 0, 1, .875), w_pad=1.5); fig.savefig(f"{F}/04f_georgia_fan.png", dpi=180, facecolor=SURF)
print("DONE")

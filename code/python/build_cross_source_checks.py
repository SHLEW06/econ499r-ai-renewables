#!/usr/bin/env python3
"""Cross-source consistency checks for the master workbook. Reads raw and cleaned files; writes one log.
Usage: python3 code/python/build_cross_source_checks.py --date YYYY-MM-DD"""
import argparse, sys
import numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); a = ap.parse_args()
p = pd.read_csv("data/out/state_panel_2015_2025.csv"); NAME = {}
rows = []
def add(check, what, result, evidence, rating): rows.append(dict(check=check, what_it_tested=what, result=result, evidence=evidence, rating=rating, date=a.date)); print(f"{rating:7} {check}: {result} | {evidence}")
# ---- BEA vs Census population ----
n = pd.read_csv("data/raw/census_pop/NST-EST2025-ALLDATA.csv", encoding="latin1"); n = n[(n.SUMLEV == 40)]
FIPS = {1:'AL',2:'AK',4:'AZ',5:'AR',6:'CA',8:'CO',9:'CT',10:'DE',11:'DC',12:'FL',13:'GA',15:'HI',16:'ID',17:'IL',18:'IN',19:'IA',20:'KS',21:'KY',22:'LA',23:'ME',24:'MD',25:'MA',26:'MI',27:'MN',28:'MS',29:'MO',30:'MT',31:'NE',32:'NV',33:'NH',34:'NJ',35:'NM',36:'NY',37:'NC',38:'ND',39:'OH',40:'OK',41:'OR',42:'PA',44:'RI',45:'SC',46:'SD',47:'TN',48:'TX',49:'UT',50:'VT',51:'VA',53:'WA',54:'WV',55:'WI',56:'WY'}
n["state"] = n.STATE.map(FIPS); n = n.dropna(subset=["state"]); c = n.melt(id_vars="state", value_vars=[f"POPESTIMATE{y}" for y in range(2020, 2026)], var_name="y", value_name="census"); c["year"] = c.y.str[-4:].astype(int)
i = pd.read_csv("data/raw/census_pop/sc-est2020int-alldata6.csv", encoding="latin1"); i = i[(i.SEX == 0) & (i.ORIGIN == 0)]; i = i[i.AGE == 999] if (i.AGE == 999).any() else i  # the file has six race groups and no race total, so sum them
vy = [f"POPESTIMATE{y}" for y in range(2015, 2020)]; i = i.groupby("STATE", as_index=False)[vy].sum()
i["state"] = i.STATE.map(FIPS); ci = i.melt(id_vars="state", value_vars=[f"POPESTIMATE{y}" for y in range(2015, 2020)], var_name="y", value_name="census"); ci["year"] = ci.y.str[-4:].astype(int)
cc = pd.concat([ci, c])[["state", "year", "census"]]; m = p[["state", "year", "population"]].merge(cc, on=["state", "year"], how="left"); m["gap"] = m.population - m.census; m["pct"] = 100 * m.gap / m.census
print(m.groupby("year").agg(n=("census", "count"), max_abs=("gap", lambda s: s.abs().max()), exact=("gap", lambda s: int((s == 0).sum()))).to_string())
add("BEA vs Census population", "Panel population (BEA SAINC1) against Census: 2010-2020 intercensal for 2015-2019; Vintage 2025 for 2020-2025", "ok" if m.pct.abs().max() < .5 else "CHECK", f"{int(m.census.notna().sum())} state-years; {int((m.gap == 0).sum())} exact; largest gap {m.gap.abs().max():,.0f} people ({m.pct.abs().max():.3f}%)", "green" if m.pct.abs().max() < .5 else "yellow")
# ---- EIA retail vs SEDS electricity ----
u = pd.read_csv("data/raw/eia/seds/use_all_btu.csv"); ys = [str(y) for y in range(2015, 2025)]; e = u[u.MSN == "ESTCB"].melt(id_vars="State", value_vars=ys, var_name="year", value_name="seds"); e["year"] = e.year.astype(int); e = e.rename(columns={"State": "state"})
x = p[["state", "year", "sales_mwh"]].merge(e, on=["state", "year"]); x["eia"] = x.sales_mwh * 3.412 / 1000; x["pct"] = 100 * (x.eia / x.seds - 1); w = x.loc[x.pct.abs().idxmax()]
add("EIA retail sales vs SEDS electricity", "sales_mwh x 3.412 MMBtu/MWh against SEDS ESTCB, 2015-2024", "ok" if x.pct.abs().max() < 2 else "CHECK", f"{len(x)} state-years; median gap {x.pct.abs().median():.3f}%; largest {x.pct.abs().max():.2f}% ({w.state} {int(w.year)})", "green" if x.pct.abs().max() < 2 else "yellow")
# ---- From Part C logs ----
V = "logs/2026-11-02/build/validation/"
for f, chk, what, thr in (("n03_qcew_518210_state_vs_national.csv", "QCEW 518210 state sums vs national row", "Sum of state private rows against the national row", None), ("n04_qcew_10_state_vs_national.csv", "QCEW all-industry state sums vs national row", "Sum of state totals against the national row", 5.0), ("n02_eia_states_vs_us_total.csv", "EIA generation: states vs US total", "Sum of 51 against US-TOTAL", 5.0), ("n05_bea_state_vs_us.csv", "BEA GDP: states vs US row", "Sum of 51 against the US row. BEA footnote: the gap reflects overseas activity", 1.0)):
    d = pd.read_csv(V + f)
    if "gap" in d: d["pct_diff"] = 100 * d.gap / d.national
    mx = d.pct_diff.abs().max()
    if thr is None:  # 518210: suppression and unallocated jobs make the gap larger, so report it
        add(chk, what, "reported", f"Largest gap {mx:.2f}% across {len(d)} years. Suppressed state cells and jobs not assigned to a state are in the national row", "yellow" if mx > 5 else "green")
    else:
        add(chk, what, "ok" if mx < thr else "CHECK", f"Largest gap {mx:.3f}% across {len(d)} years", "green" if mx < thr else "yellow")
# ---- EIA fuel sums vs total ----
gc = [c for c in p.columns if c.startswith("gen_") and c not in ("gen_total_mwh", "gen_renew_mwh", "gen_fossil_mwh")]
g = p.copy(); g["s"] = g[gc].sum(axis=1); g["pct"] = 100 * (g.s / g.gen_total_mwh - 1); w = g.loc[g.pct.abs().idxmax()]
add("EIA fuel sums vs total generation", "Sum of generation by fuel, including negative pumped storage, against gen_total_mwh", "ok" if g.pct.abs().max() < .5 else "CHECK", f"561 state-years; largest gap {g.pct.abs().max():.4f}% ({w.state} {int(w.year)})", "green" if g.pct.abs().max() < .5 else "yellow")
# ---- codes and years across tabs ----
base = set(p.state.unique()); tabs = {"fang_panel":"data/fang_panel.csv","lbnl_rps_targets":"data/lbnl_rps_targets.csv","epu_state_annual":"data/epu_state_annual.csv","nsf_state_rd":"data/nsf_state_rd.csv","acs_broadband":"data/acs_broadband.csv","ai_allown_518210":"data/ai_allown_518210.csv","ai_job_postings_state":"data/ai_job_postings_state.csv","seds_renewables_state":"data/seds_renewables_state.csv","ncses_bachelors_state":"data/ncses_bachelors_state.csv","fang_split_vars":"data/fang_split_vars.csv"}
bad = []; ev = []
for k, f in tabs.items():
    d = pd.read_csv(f); sc = "state" if "state" in d else [c for c in d.columns if c.lower() in ("st", "state_abbr", "abbr")][0]; extra = set(d[sc].dropna().unique()) - base; miss = base - set(d[sc].dropna().unique())
    yr = (int(d.year.min()), int(d.year.max())) if "year" in d else None; ev.append(f"{k}: {d[sc].nunique()} codes, years {yr}")
    if extra or miss: bad.append(f"{k}: extra {sorted(map(str, extra))[:6]} missing {sorted(miss)[:6]}")
add("State codes and years across tabs", "Every state-level side table uses the panel's 51 codes and years inside 2015-2025", "ok" if not bad else "reported", ("All match. " if not bad else "; ".join(bad) + ". ") + "; ".join(ev), "green" if not bad else "yellow")
pd.DataFrame(rows).to_csv(f"logs/{a.date}/cross_source_checks.csv", index=False)

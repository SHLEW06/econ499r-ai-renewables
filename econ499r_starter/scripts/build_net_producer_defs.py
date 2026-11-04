#!/usr/bin/env python3
"""Net-producer definitions side by side for the Fang check, 51 states/district, 2018-2021. Reads raw files read-only; edits nothing.
Usage: build_net_producer_defs.py <seds_dir> <fang_split_vars.csv> <out_csv>
Rules, each on the state's 2018-2021 average (Fang's period isn't stated; EXPERIMENTS.md F6):
  gen_gt_sales      EIA generation above retail sales: our main definition
  teprb_gt_tetcb    SEDS total primary energy production above total energy consumption
  elisb_negative    SEDS net interstate flow of electricity below zero (negative = flow out of state)
"""
import os, sys
import pandas as pd
if len(sys.argv) != 4: sys.exit(__doc__)
SD, SPLIT, OUT = sys.argv[1:]
Y = [2018, 2019, 2020, 2021]
s = pd.read_csv(SPLIT); s = s[s.year.isin(Y)][["state", "year", "gen_total_mwh", "elec_consumption_mwh"]].rename(columns=dict(elec_consumption_mwh="retail_sales_mwh"))
u = pd.read_csv(os.path.join(SD, "use_all_btu.csv")); u = u[u.MSN.isin(["TETCB", "ELISB"])].rename(columns=dict(State="state"))
u = u.melt(id_vars=["state", "MSN"], value_vars=[str(y) for y in Y], var_name="year", value_name="v"); u["year"] = u.year.astype(int)
u = u.pivot(index=["state", "year"], columns="MSN", values="v").reset_index().rename(columns=dict(TETCB="seds_total_consumption_bbtu", ELISB="seds_net_interstate_flow_bbtu"))
p = pd.read_excel(os.path.join(SD, "Prod_dataset.xlsx"), sheet_name="Data"); p.columns = [int(c) if isinstance(c, float) else c for c in p.columns]
p = p[p.MSN == "TEPRB"].rename(columns=dict(StateCode="state")).melt(id_vars=["state"], value_vars=Y, var_name="year", value_name="seds_total_production_bbtu"); p["year"] = p.year.astype(int)
d = s.merge(u, on=["state", "year"], how="left", validate="1:1").merge(p, on=["state", "year"], how="left", validate="1:1")
assert len(d) == 204 and d.state.nunique() == 51 and not d.isna().any().any(), "gap in the merge"
m = d.groupby("state")[["gen_total_mwh", "retail_sales_mwh", "seds_total_production_bbtu", "seds_total_consumption_bbtu", "seds_net_interstate_flow_bbtu"]].transform("mean")
d["gen_gt_sales"] = (m.gen_total_mwh > m.retail_sales_mwh).astype(int)
d["teprb_gt_tetcb"] = (m.seds_total_production_bbtu > m.seds_total_consumption_bbtu).astype(int)
d["elisb_negative"] = (m.seds_net_interstate_flow_bbtu < 0).astype(int)
d = d.sort_values(["state", "year"]); d.to_csv(OUT, index=False)
print("wrote", OUT, d.shape, "| state-years:", {k: int(d[k].sum()) for k in ("gen_gt_sales", "teprb_gt_tetcb", "elisb_negative")})

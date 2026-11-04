#!/usr/bin/env python3
"""Build the all-ownership NAICS 518210 check and government-share table from raw QCEW.

Usage: build_ai_allown.py <raw_dir> <panel_csv> <out_csv> <gov_share_csv>

The main AI measure stays private only, in the master panel: private data-center jobs per
1,000 workers. This side table adds published government rows (own_code 1 federal, 2 state,
3 local) for one labeled robustness row. Government rows that BLS suppresses show 0 jobs
and can't be recovered, so all-ownership counts are lower bounds; the number of suppressed
rows is carried in the table. Where the private cell is suppressed, the measure stays NA.
"""
import sys
import numpy as np, pandas as pd

FIPS = {'01':'AL','02':'AK','04':'AZ','05':'AR','06':'CA','08':'CO','09':'CT','10':'DE','11':'DC','12':'FL','13':'GA','15':'HI','16':'ID','17':'IL','18':'IN','19':'IA','20':'KS','21':'KY','22':'LA','23':'ME','24':'MD','25':'MA','26':'MI','27':'MN','28':'MS','29':'MO','30':'MT','31':'NE','32':'NV','33':'NH','34':'NJ','35':'NM','36':'NY','37':'NC','38':'ND','39':'OH','40':'OK','41':'OR','42':'PA','44':'RI','45':'SC','46':'SD','47':'TN','48':'TX','49':'UT','50':'VT','51':'VA','53':'WA','54':'WV','55':'WI','56':'WY'}


def read(raw, y, code):
    q = pd.read_csv(f"{raw}/bls/qcew_{y}_{code}.csv", dtype={"area_fips": str, "disclosure_code": str}, low_memory=False)
    q = q[q.area_fips.str.endswith("000") & q.area_fips.str[:2].isin(FIPS)].copy()
    q["state"] = q.area_fips.str[:2].map(FIPS)
    q["year"] = y
    return q


def main(raw, panel_csv, out_csv, share_csv):
    rec = []
    for y in range(2014, 2026):
        dc = read(raw, y, "518210"); dc = dc[dc.agglvl_code == 58]
        tt = read(raw, y, "10"); tt = tt[(tt.own_code == 0) & (tt.agglvl_code == 50)].set_index("state").annual_avg_emplvl
        for st in FIPS.values():
            d = dc[dc.state == st]
            p = d[d.own_code == 5]
            supp = len(p) == 0 or str(p.disclosure_code.iloc[0]) == "N"
            g = d[d.own_code.isin([1, 2, 3])]
            gs = g[g.disclosure_code != "N"]
            rec.append(dict(state=st, year=y, dc_jobs_private=np.nan if supp else float(p.annual_avg_emplvl.iloc[0]),
                            dc_jobs_gov_federal=float(gs[gs.own_code == 1].annual_avg_emplvl.sum()),
                            dc_jobs_gov_state=float(gs[gs.own_code == 2].annual_avg_emplvl.sum()),
                            dc_jobs_gov_local=float(gs[gs.own_code == 3].annual_avg_emplvl.sum()),
                            n_gov_rows_suppressed=int((g.disclosure_code == "N").sum()), total_jobs=float(tt[st])))
    d = pd.DataFrame(rec)
    d["dc_jobs_gov_published"] = d[["dc_jobs_gov_federal", "dc_jobs_gov_state", "dc_jobs_gov_local"]].sum(axis=1)
    d["dc_jobs_allown"] = d.dc_jobs_private + d.dc_jobs_gov_published
    d["gov_share_pct"] = 100 * d.dc_jobs_gov_published / d.dc_jobs_allown
    d["ai_allown_per1000"] = 1000 * d.dc_jobs_allown / d.total_jobs
    d = d.sort_values(["state", "year"])
    d["ai_allown_per1000_lag1"] = d.groupby("state").ai_allown_per1000.shift(1)
    out = d[d.year >= 2015].copy()

    # The private numerator and denominator must reproduce the panel exactly.
    p = pd.read_csv(panel_csv)
    m = out.merge(p[["state", "year", "dc_jobs", "total_jobs", "ai_dc_per1000"]], on=["state", "year"], suffixes=("", "_panel"))
    if len(m) != 561 or (m.dc_jobs_private.isna() != m.dc_jobs.isna()).any() or (m.dc_jobs_private - m.dc_jobs).abs().max() > 0 or (m.total_jobs - m.total_jobs_panel).abs().max() > 0:
        sys.exit("private numerator or denominator does not match the panel")
    print("matches panel dc_jobs and total_jobs on", len(m), "rows")

    out.drop(columns=["ai_allown_per1000_lag1"]).assign(ai_allown_per1000_lag1=out.ai_allown_per1000_lag1).to_csv(out_csv, index=False)
    u = out[out.dc_jobs_private.notna()]
    s = u.groupby("state").agg(private_jobs=("dc_jobs_private", "sum"), gov_jobs=("dc_jobs_gov_published", "sum"), federal=("dc_jobs_gov_federal", "sum"), state_gov=("dc_jobs_gov_state", "sum"), local=("dc_jobs_gov_local", "sum"),
                               years_with_gov=("dc_jobs_gov_published", lambda x: int((x > 0).sum())), suppressed_gov_rows=("n_gov_rows_suppressed", "sum"))
    s["gov_share_pct"] = 100 * s.gov_jobs / (s.gov_jobs + s.private_jobs)
    pk = u.loc[u.groupby("state").gov_share_pct.idxmax()].set_index("state")
    s["peak_year"] = pk.year; s["peak_share_pct"] = pk.gov_share_pct; s["peak_gov_jobs"] = pk.dc_jobs_gov_published
    s = s.sort_values("gov_share_pct", ascending=False).round(2).reset_index()
    s.to_csv(share_csv, index=False)
    print(s.head(12).to_string(index=False))
    print("states with any published government jobs:", int((s.gov_jobs > 0).sum()), "of 51; overall share", round(100 * s.gov_jobs.sum() / (s.gov_jobs.sum() + s.private_jobs.sum()), 2))
    y = out.groupby("year").agg(gov=("dc_jobs_gov_published", "sum"), rows=("dc_jobs_gov_published", lambda x: int((x > 0).sum())), suppressed=("n_gov_rows_suppressed", "sum"))
    print(y.T.to_string())
    w = out[(out.state != "DC") & out.ai_allown_per1000.notna()]
    print("max ai_allown - ai_private:", round((m.ai_allown_per1000 - m.ai_dc_per1000).max(), 3), "| median where gov>0:", round((m.ai_allown_per1000 - m.ai_dc_per1000)[m.dc_jobs_gov_published > 0].median(), 3))
    print("corr(allown, private), 50 states, within state:", round(w.assign(a=w.ai_allown_per1000 - w.groupby("state").ai_allown_per1000.transform("mean"), b=lambda t: 1000 * t.dc_jobs_private / t.total_jobs - (1000 * t.dc_jobs_private / t.total_jobs).groupby(t.state).transform("mean"))[["a", "b"]].corr().iloc[0, 1], 3))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])

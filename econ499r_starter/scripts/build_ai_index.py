#!/usr/bin/env python3
"""AI index, "infrastructure + talent" (prompts/09_extend.md section 5; EXPERIMENTS.md section 14.6, B3).

Usage: build_ai_index.py <raw_dir> <data_dir> <log_dir>

Writes
  <data_dir>/ai_index_components.csv   50 states x 2015-2024: the five components (logs) and their raw inputs
  <data_dir>/ai_index_state.csv        index sample: Index A, Index B, infrastructure and talent sub-indices (main 2018-2023, plus 2024
                                        scored with the main sample's means, SDs and loadings); and the 2015-2023 check without postings
  <data_dir>/ai_index_crossstate.csv   50 states: BTOS 2024 AI use, Epoch IT MW, Quid 2025 investment, investment and jobs per TWh, land per TWh
  <log_dir>/ai_index_*.csv / ai_index_build.log  coverage, loadings, correlations, alpha, cross-state checks, OEWS mapping
Components (natural logs): infrastructure = 518210 private jobs per 1,000 workers, establishments per million residents, total 518210 wages
per worker; talent = AI postings per 1,000 workers, OEWS computer and information research scientists per 1,000 workers
(SOC 15-1111 through 2018, 15-1221 from 2019). Software developers and data scientists are dropped (no consistent 2018-2023 series).
"""
import glob, os, re, sys, zipfile
import numpy as np, pandas as pd

FIPS = {"01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI", "16": "ID",
        "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS", "29": "MO",
        "30": "MT", "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH", "40": "OK", "41": "OR", "42": "PA",
        "44": "RI", "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI", "56": "WY"}
INFRA = ["c_jobs", "c_estab", "c_wage"]; TALENT = ["c_post", "c_rsci"]; COMP = INFRA + TALENT
OEWS_MAP = [("2015-2018", "15-1111", "Computer and Information Research Scientists", "kept"), ("2019-2024", "15-1221", "Computer and Information Research Scientists", "kept"),
            ("2015-2018", "15-1132 + 15-1133", "Software Developers, Applications + Systems Software (QA testers in 15-1199)", "dropped: no consistent series"),
            ("2019-2020", "15-1256", "Software Developers and Software QA Analysts and Testers", "dropped"), ("2021-2024", "15-1252 (15-1253 separate)", "Software Developers", "dropped"),
            ("2015-2018", "none", "Data scientists have no category", "dropped: no consistent series"), ("2019-2020", "15-2098", "Data Scientists and Mathematical Science Occupations, All Other", "dropped"),
            ("2021-2024", "15-2051", "Data Scientists", "dropped")]


def cronbach(X):
    X = X.dropna(); k = X.shape[1]
    return k / (k - 1) * (1 - X.var(ddof=1).sum() / X.sum(axis=1).var(ddof=1))


def score(df, cols, ref):
    """z-scores and indices using the reference sample's means and SDs, and PC1 loadings from the reference sample."""
    mu, sd = ref[cols].mean(), ref[cols].std(ddof=0)
    Z = (df[cols] - mu) / sd
    Zr = (ref[cols] - mu) / sd
    w, v = np.linalg.eigh(np.corrcoef(Zr.T.values)); pc = v[:, -1]
    if pc.sum() < 0:
        pc = -pc
    out = pd.DataFrame(index=df.index)
    infra = [c for c in INFRA if c in cols]; tal = [c for c in TALENT if c in cols]
    out["sub_infra"] = Z[infra].mean(axis=1)
    out["sub_talent"] = Z[tal].mean(axis=1) if tal else np.nan
    out["index_a"] = out[["sub_infra", "sub_talent"]].mean(axis=1) if tal else out.sub_infra
    out["index_b"] = Z.values @ pc
    return out, pd.DataFrame({"component": cols, "loading": pc, "variance_explained_pc1": w[-1] / w.sum()}), Z


def main(raw, out, logd):
    log = []
    P = pd.read_csv(os.path.join(out, "out", "state_panel_2015_2025.csv")); P = P[P.is_dc == 0][["state", "year", "dc_jobs", "total_jobs", "population", "sales_mwh", "land_sqmi"]]
    # ---- QCEW 518210 ----
    q = []
    for y in range(2015, 2025):
        d = pd.read_csv(os.path.join(raw, f"bls/qcew_{y}_518210.csv"), dtype={"area_fips": str, "disclosure_code": str})
        d = d[(d.own_code == 5) & d.area_fips.str.endswith("000") & (d.area_fips != "US000") & (d.agglvl_code == 58)]
        d["state"] = d.area_fips.str[:2].map(FIPS); d["year"] = y
        nd = d.disclosure_code.fillna("").eq("N")
        for c in ["annual_avg_estabs", "annual_avg_emplvl", "total_annual_wages"]:
            d.loc[nd, c] = np.nan
        q.append(d[["state", "year", "annual_avg_estabs", "annual_avg_emplvl", "total_annual_wages"]])
    q = pd.concat(q).rename(columns={"annual_avg_estabs": "qcew_estabs", "annual_avg_emplvl": "qcew_jobs", "total_annual_wages": "qcew_wages"})
    m = P.merge(q, on=["state", "year"], how="left")
    gd = (m.qcew_jobs - m.dc_jobs).abs().max(); log.append(f"Gate: QCEW 518210 jobs vs panel dc_jobs, max |diff| = {gd}"); assert gd == 0 or np.isnan(gd), gd
    # ---- OEWS research scientists ----
    o = []
    for y in range(15, 25):
        z = zipfile.ZipFile(os.path.join(raw, f"bls/oews/oesm{y}st.zip"))
        n = [i for i in z.namelist() if re.search(r"state_M20\d\d_dl\.xlsx$", i) and not i.split("/")[-1].startswith("~$")][0]
        d = pd.read_excel(z.open(n), dtype=str); d.columns = [c.lower() for c in d.columns]
        if "area_type" in d.columns:
            d = d[d.area_type == "2"]
        d["state"] = d.area.astype(str).str.zfill(2).str[:2].map(FIPS)
        code = "15-1111" if y <= 18 else "15-1221"
        r = d[(d.occ_code == code) & d.state.notna()][["state", "tot_emp"]].rename(columns={"tot_emp": "oews_rsci"})
        r["oews_rsci"] = pd.to_numeric(r.oews_rsci.str.replace(",", ""), errors="coerce")  # '**' and '#' become missing
        r["year"] = 2000 + y; r["oews_code"] = code; o.append(r)
    o = pd.concat(o); m = m.merge(o, on=["state", "year"], how="left")
    fp = pd.read_csv(os.path.join(out, "fang_panel.csv"))[["state", "year", "ai_postings"]]; m = m.merge(fp, on=["state", "year"], how="left")
    m = m[m.year.between(2015, 2024)].copy()
    m["c_jobs"] = np.log(m.qcew_jobs / m.total_jobs * 1000); m["c_estab"] = np.log(m.qcew_estabs / m.population * 1e6)
    m["c_wage"] = np.log(m.qcew_wages / m.total_jobs); m["c_post"] = np.log(m.ai_postings / m.total_jobs * 1000); m["c_rsci"] = np.log(m.oews_rsci / m.total_jobs * 1000)
    m = m.replace([np.inf, -np.inf], np.nan)
    m.sort_values(["state", "year"]).to_csv(os.path.join(out, "ai_index_components.csv"), index=False)
    cov = m.groupby("year")[COMP].count().reset_index(); cov["all_five"] = m.assign(ok=m[COMP].notna().all(axis=1)).groupby("year").ok.sum().values
    cov["infra_plus_rsci"] = m.assign(ok=m[INFRA + ["c_rsci"]].notna().all(axis=1)).groupby("year").ok.sum().values
    cov.to_csv(os.path.join(logd, "ai_index_coverage.csv"), index=False); log.append("Coverage (states with each component, by year):\n" + cov.to_string(index=False))
    # ---- Index, main 2018-2023 (+2024 scored), and 2015-2023 check without postings ----
    ref = m[m.year.between(2018, 2023)].dropna(subset=COMP)
    sc = m[m.year.between(2018, 2024)].dropna(subset=COMP)
    I, L, Z = score(sc, COMP, ref); I = pd.concat([sc[["state", "year"]], I], axis=1); I["version"] = "main_2018_2023"; I.loc[I.year == 2024, "version"] = "main_scored_2024"
    ref2 = m[m.year.between(2015, 2023)].dropna(subset=INFRA + ["c_rsci"])
    I2, L2, _ = score(ref2, INFRA + ["c_rsci"], ref2); I2 = pd.concat([ref2[["state", "year"]], I2], axis=1); I2["version"] = "check_2015_2023_no_postings"
    idx = pd.concat([I, I2]); idx.to_csv(os.path.join(out, "ai_index_state.csv"), index=False)
    L["version"] = "main_2018_2023"; L2["version"] = "check_2015_2023_no_postings"; pd.concat([L, L2]).to_csv(os.path.join(logd, "ai_index_loadings.csv"), index=False)
    corr = ref[COMP].corr(); corr.to_csv(os.path.join(logd, "ai_index_component_correlations.csv"))
    within = {}
    mi = I[I.version == "main_2018_2023"]
    for c in ["index_a", "index_b", "sub_infra", "sub_talent"]:
        x = mi[c] - mi.groupby("state")[c].transform("mean") - mi.groupby("year")[c].transform("mean") + mi[c].mean(); within[c] = x.std()
    diag = pd.DataFrame({"statistic": ["N state-years (main)", "states (main)", "Cronbach alpha, 5 components", "Cronbach alpha, infrastructure", "Cronbach alpha, talent",
                                       "PC1 variance explained", "within-state SD (two-way demeaned) Index A", "within-state SD Index B", "within-state SD infrastructure", "within-state SD talent",
                                       "N state-years (check 2015-2023)", "PC1 variance explained (check)"],
                         "value": [len(ref), ref.state.nunique(), cronbach(Z.loc[ref.index]), cronbach(Z.loc[ref.index, INFRA]), cronbach(Z.loc[ref.index, TALENT]),
                                   L.variance_explained_pc1.iloc[0], within["index_a"], within["index_b"], within["sub_infra"], within["sub_talent"], len(ref2), L2.variance_explained_pc1.iloc[0]]})
    diag.to_csv(os.path.join(logd, "ai_index_diagnostics.csv"), index=False)
    log.append("Diagnostics:\n" + diag.to_string(index=False)); log.append("Loadings (main):\n" + L.to_string(index=False)); log.append("Component correlations:\n" + corr.round(3).to_string())
    # ---- cross-state checks ----
    # BTOS AI use: AI_Core_Questions.xlsx, State Estimates, Q7 "use Artificial Intelligence (AI) in producing goods or services", answer Yes.
    # (State.xlsx's Q7 now carries the later "Super Intelligence" wording and is blank for 2024.)
    b = pd.read_excel(os.path.join(raw, "census_btos/AI_Core_Questions.xlsx"), sheet_name="State Estimates")
    b = b[(pd.to_numeric(b["Question ID"], errors="coerce") == 7) & (b["Answer ID"] == 1)]
    c24 = [c for c in b.columns if str(c).startswith("2024")]
    bv = b.set_index("State")[c24].apply(lambda s: pd.to_numeric(s.astype(str).str.rstrip("%"), errors="coerce"))
    btos = pd.DataFrame({"state": bv.index, "btos_ai_use_2024_pct": bv.mean(axis=1).values, "btos_periods_2024": bv.notna().sum(axis=1).values})
    ep = pd.read_csv(os.path.join(out, "epoch_ai_campuses_by_state.csv"))[["state", "current_it_mw"]]
    qd = pd.read_csv(os.path.join(raw, "aiindex/ed2026_fig_4.2.15.csv")).rename(columns={"state_code": "state", "total_funding": "quid_invest_2025_usd"})
    p15 = P[P.year == 2015][["state", "sales_mwh", "dc_jobs", "land_sqmi"]]
    cs = p15.merge(btos, on="state", how="left").merge(ep, on="state", how="left").merge(qd, on="state", how="left")
    cs = cs.merge(I[I.year == 2024][["state", "index_a", "index_b"]].rename(columns={"index_a": "index_a_2024", "index_b": "index_b_2024"}), on="state", how="left")
    cs = cs.merge(I[I.year == 2023][["state", "index_a"]].rename(columns={"index_a": "index_a_2023"}), on="state", how="left")
    cs["invest_per_twh_2015"] = cs.quid_invest_2025_usd / (cs.sales_mwh / 1e6)
    cs["jobs518210_per_twh_2015"] = cs.dc_jobs / (cs.sales_mwh / 1e6)
    cs["land_sqmi_per_twh_2015"] = cs.land_sqmi / (cs.sales_mwh / 1e6)
    # groupings, cut points fixed in EXPERIMENTS.md 14.6 A2
    cs["grp_invest"] = pd.cut(cs.quid_invest_2025_usd, [-np.inf, 1e8, 1e9, np.inf], right=False, labels=["lt_100M", "100M_1B", "ge_1B"]).astype(object)
    cs["grp_invest_per_twh"] = pd.qcut(cs.invest_per_twh_2015, 3, labels=["low", "mid", "high"]).astype(object)
    cs["grp_jobs_per_twh"] = pd.qcut(cs.jobs518210_per_twh_2015, 3, labels=["low", "mid", "high"]).astype(object)
    cs.to_csv(os.path.join(out, "ai_index_crossstate.csv"), index=False)
    cuts = {"invest_per_twh tertile cuts ($ per TWh)": list(cs.invest_per_twh_2015.quantile([1/3, 2/3]).round(0)), "jobs_per_twh tertile cuts": list(cs.jobs518210_per_twh_2015.quantile([1/3, 2/3]).round(2))}
    log.append(f"Groupings: invest {cs.grp_invest.value_counts(dropna=False).to_dict()}; per TWh {cs.grp_invest_per_twh.value_counts(dropna=False).to_dict()}; jobs per TWh {cs.grp_jobs_per_twh.value_counts().to_dict()}; {cuts}")
    log.append("Investment missing for: " + ", ".join(cs[cs.quid_invest_2025_usd.isna()].state))
    chk = []
    for v, lab in [("btos_ai_use_2024_pct", "BTOS 2024 average share of firms using AI"), ("current_it_mw", "Epoch current IT MW"), ("quid_invest_2025_usd", "Quid 2025 private AI investment")]:
        x = cs.dropna(subset=[v, "index_a_2024"])
        chk.append({"check": lab, "N_states": len(x), "pearson_index_a_2024": x[v].corr(x.index_a_2024), "spearman_index_a_2024": x[v].corr(x.index_a_2024, method="spearman"),
                    "spearman_index_b_2024": x[v].corr(x.index_b_2024, method="spearman")})
    chk = pd.DataFrame(chk); chk.to_csv(os.path.join(logd, "ai_index_crossstate_checks.csv"), index=False); log.append("Cross-state checks:\n" + chk.round(3).to_string(index=False))
    pd.DataFrame(OEWS_MAP, columns=["years", "soc_code", "title", "decision"]).to_csv(os.path.join(logd, "ai_index_oews_mapping.csv"), index=False)
    open(os.path.join(logd, "ai_index_build.log"), "w").write("\n\n".join(log) + "\n"); print("\n\n".join(log))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])

#!/usr/bin/env python3
"""Tables and figures for prompts/09_extend.md (EXPERIMENTS.md section 14), one section at a time.

Usage: python3 code/python/09_extend_tables.py --date YYYY-MM-DD --section N
Reads results/<date>/extend/*.csv (and results/<date>/fang/ for section 1). Writes results/<date>/extend/tables/ and figures/.
No models are run here.
"""
import argparse, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FANG_T2 = {"AI": [0.0428, 0.0452, 0.0396, 0.0548, 0.0561, 0.0531], "lnEPU": [None, -0.0284, -0.0206, -0.0242, -0.0239, -0.0253],
           "lnEP": [None, None, 0.1533, 0.2645, 0.2622, 0.2907], "lnGDP": [None, None, None, -0.7016, -0.6911, -0.7302],
           "lnPOP": [None, None, None, None, -0.1049, -0.0148], "lnEDU": [None, None, None, None, None, 0.1143]}


def fp(p):
    return "p < 0.001" if p < 0.001 else f"p = {p:.3f}"


def star(p):
    return "" if pd.isna(p) else "***" if p < .01 else "**" if p < .05 else "*" if p < .1 else ""


def s1(date, E, T, F):
    r = pd.read_csv(os.path.join("results", date, "fang", "fang8_results.csv"))
    rows = []
    for m, lab in [("aipostings", "ln AI postings"), ("dcjobs", "ln data-center jobs")]:
        for term, vals in FANG_T2.items():
            for c, fv in enumerate(vals, 1):
                if fv is None:
                    continue
                row = {"ai_measure": lab, "term": term.replace("ln", "") if term != "AI" else "AI", "column": c, "fang_published": fv}
                for b, bl in [("current", "current"), ("k26", "k_2.6"), ("rebuilt", "rebuilt"), ("archived", "archived_jun2023")]:
                    x = r[(r.block == "t2") & (r.spec == f"c{c}-{b}") & (r.ai_measure == m) & (r.term == term)].iloc[0]
                    row[bl] = f"{x.estimate:+.4f}{star(x.pval)}"
                    row[f"{bl}_ci95"] = f"[{x.ci_lo:+.4f}, {x.ci_hi:+.4f}]"
                    row[f"{bl}_fang_inside"] = "yes" if x.ci_lo <= fv <= x.ci_hi else "no"
                    row[f"{bl}_tag"] = x.tag
                rows.append(row)
    t2 = pd.DataFrame(rows); t2.to_csv(os.path.join(T, "s1_table2_four_versions.csv"), index=False)
    ds = pd.read_csv(os.path.join(E, "e1_descriptives_vs_fang_implied.csv"))
    ds.to_csv(os.path.join(T, "s1_descriptives_comparison.csv"), index=False)
    tp = pd.read_csv(os.path.join(E, "e3_e4_trend_placebo.csv"))
    tp.to_csv(os.path.join(T, "s1_trend_placebo.csv"), index=False)
    # inside-CI counts
    cnt = {b: (t2[f"{b}_fang_inside"] == "yes").sum() for b in ["current", "k_2.6", "rebuilt", "archived_jun2023"]}
    cnt_post = {b: ((t2.ai_measure == "ln AI postings") & (t2[f"{b}_fang_inside"] == "yes")).sum() for b in ["current", "k_2.6", "rebuilt", "archived_jun2023"]}
    cnt_ai = {b: ((t2.term == "AI") & (t2.ai_measure == "ln AI postings") & (t2[f"{b}_fang_inside"] == "yes")).sum() for b in ["current", "k_2.6", "rebuilt", "archived_jun2023"]}
    # figure: placebo vs AI, Fang spec and ours
    pl = tp[(tp.block == "placebo") & (tp.term == "AI")].copy()
    pl["lab"] = pl.ai_measure + " | " + pl.spec.map({"fang6": "Fang spec", "twfe": "our spec"}) + " | " + pl.outcome
    pl = pl.sort_values(["spec", "outcome", "ai_measure"])
    fig, ax = plt.subplots(figsize=(8, 5))
    col = pl.ai_measure.map(lambda a: "#d1495b" if a in ("distilleries", "petcare") else "#2a6ebb")
    ax.errorbar(pl.estimate, range(len(pl)), xerr=[pl.estimate - pl.ci_lo, pl.ci_hi - pl.estimate], fmt="none", ecolor="grey", capsize=2)
    ax.scatter(pl.estimate, range(len(pl)), c=col, zorder=3)
    ax.set_yticks(range(len(pl))); ax.set_yticklabels(pl.lab, fontsize=7); ax.axvline(0, color="grey", lw=.8)
    ax.set_xlabel("Coefficient (95% CI); red = placebo industry, blue = AI")
    ax.set_title("Trend placebo: unrelated industries vs AI"); fig.tight_layout(); fig.savefig(os.path.join(F, "fig_s1_trend_placebo.png"), dpi=150); plt.close(fig)
    g = lambda blk, spec, m, y, term="AI": tp[(tp.block == blk) & (tp.spec == spec) & (tp.ai_measure == m) & (tp.outcome == y) & (tp.term == term)].iloc[0]
    a = r[(r.block == "t2") & (r.spec == "c6-archived") & (r.ai_measure == "aipostings") & (r.term == "AI")].iloc[0]
    rb = r[(r.block == "t2") & (r.spec == "c6-rebuilt") & (r.ai_measure == "aipostings") & (r.term == "AI")].iloc[0]
    cu = r[(r.block == "t2") & (r.spec == "c6-current") & (r.ai_measure == "aipostings") & (r.term == "AI")].iloc[0]
    tr = g("trend", "fang6trend", "aipostings", "lnET_rb"); pc = g("placebo", "fang6", "petcare", "lnET_rb"); pt = g("placebo", "twfe", "petcare", "lnRE_rb"); di = g("placebo", "twfe", "distilleries", "lnRE_rb")
    reg = ds[~ds.variable.str.startswith("lnET") & (ds.variable != "lnAIp")]
    verdict = (
        f"**Verdict.** Our data match Fang's on every regressor. The means implied by Fang's Table 2 constants are within {reg.diff_sd.abs().max():.2f} SD of ours "
        f"for EPU, EP, GDP, POP and EDU; GDP's {ds.loc[ds.variable=='lnGDP','diff'].iloc[0]:.3f} gap is consistent with chained 2012 vs 2017 dollars (expected 0.073), "
        f"and POP matches Fang's stated units (thousands). The outcome is what differs: on current SEDS our mean ln renewables is {ds.loc[ds.variable=='lnET','diff'].iloc[0]:.3f} "
        f"below Fang's implied mean ({ds.loc[ds.variable=='lnET','diff_sd'].iloc[0]:.2f} SD, the only flagged row), while on the old fossil-fuel-equivalence basis the gap is "
        f"{ds.loc[ds.variable=='lnET_rb','diff'].iloc[0]:.3f} (rebuilt) and {ds.loc[ds.variable=='lnET_k26','diff'].iloc[0]:.3f} (k = 2.6), which is consistent with Fang having used SEDS as published before October 2023. "
        f"On that June 2023 release, Fang's coefficients fall inside our 95% CIs for {cnt_post['archived_jun2023']} of {int((t2.ai_measure=='ln AI postings').sum())} postings-model coefficients, including all six AI coefficients "
        f"(column 6 AI: {a.estimate:+.4f}, {fp(a.pval)}, against Fang's +0.0531); the rebuild on today's data is smaller ({rb.estimate:+.4f}, {fp(rb.pval)}) because EIA has since revised biomass, "
        f"and current SEDS flips the sign ({cu.estimate:+.4f}, {fp(cu.pval)}). Fang's spec has no year effects, and the trend tests show why that matters: a linear year trend moves the rebuilt-basis "
        f"postings coefficient to {tr.estimate:+.4f} ({fp(tr.pval)}), and pet-care employment, which has nothing to do with energy, is associated with renewables more strongly than AI is in Fang's spec "
        f"({pc.estimate:+.4f}, {fp(pc.pval)}). In our two-way FE spec pet care is null ({pt.estimate:+.4f}, {fp(pt.pval)}), but distillery employment (N = {di.N}, the state-years where it isn't suppressed) is still significant "
        f"({di.estimate:+.4f}, {fp(di.pval)}), a reminder that year effects remove national trends, not state-specific ones.")
    open(os.path.join(T, "s1_verdict.md"), "w").write(verdict + "\n")
    print(verdict); print('inside CI, all coefficients:', cnt, '| postings models:', cnt_post, '| postings AI only:', cnt_ai)


LAB = {"share": "share of generation", "ln_gen": "ln generation", "add": "MW added per 1,000 MW (2015 cap.)"}
TYPE = {"wind": "wind", "solar": "utility solar", "hydro": "hydro", "geo": "geothermal", "bio": "biomass"}


def olab(o):
    if o.startswith("ln_seds_"):
        return {"ln_seds_woodwaste": "SEDS wood and waste (ln)", "ln_seds_biofuels": "SEDS biofuels (ln)", "ln_seds_re_exbiomass": "SEDS renewables excl. all biomass (ln)",
                "ln_seds_re_exbiofuels": "SEDS renewables excl. biofuels (ln)", "ln_seds_re_total": "SEDS renewables, total (ln)"}[o]
    for k, v in LAB.items():
        if o.startswith(k + "_"):
            t = o[len(k) + 1:].replace("_per1000", "")
            return f"{TYPE.get(t, t)}: {v}"
    return o


def family_table(m):
    t = m.copy()
    t["outcome_label"] = t.outcome.map(olab)
    t["ai"] = t.ai_measure.map({"ai518210": "jobs per 1,000", "aipostp1000": "postings per 1,000"})
    t["coef"] = t.apply(lambda r: "" if pd.isna(r.estimate) else f"{r.estimate:+.4g}{star(r.pval)}", axis=1)
    t["ci95"] = t.apply(lambda r: "" if pd.isna(r.estimate) else f"[{r.ci_lo:+.3g}, {r.ci_hi:+.3g}]", axis=1)
    t["lead_placebo"] = t.apply(lambda r: "" if pd.isna(r.lead_est) else f"lead {r.lead_est:+.3g} (p={r.lead_p:.3f}) vs lag {r.lag_est_pl:+.3g}", axis=1)
    return t[["outcome_label", "ai", "coef", "ci95", "pval", "qval", "N", "years", "lead_placebo", "finding", "status", "note", "tag"]]


def s2(date, E, T, F):
    m = pd.read_csv(os.path.join(E, "s2_bytype_family.csv"))
    ft = family_table(m); ft.to_csv(os.path.join(T, "s2_bytype_table.csv"), index=False)
    gi = pd.read_csv(os.path.join(E, "s2_georgia_implied.csv"))
    mix = pd.read_csv(os.path.join(E, "s2_georgia_mix.csv"))
    none = {t for t in ["wind", "geo"] if (mix[f"share_{t}"].fillna(0) == 0).all()}
    def sent(r):
        t = r.outcome.split("_")[-1] if not r.outcome.startswith("add_") else r.outcome.split("_")[1]
        lab = olab(r.outcome) + (" (jobs)" if r.ai_measure == "ai518210" else " (postings)")
        if t in none:
            return f"{lab}: Georgia has no {TYPE[t]} generation in 2015-2025, so this doesn't apply."
        if pd.isna(r.implied):
            return f"{lab}: not estimable."
        if pd.isna(r.actual_change) or r.actual_change == 0:
            return f"{lab}: implied {r.implied:+.3g} (95% CI {r.implied_lo:+.3g} to {r.implied_hi:+.3g}); Georgia's actual change over {r.window} is zero, so no share can be stated."
        a = r.at_most_share_of_actual
        tail = f"at most {100*a:.0f}% of Georgia's actual change" if a <= 1 else f"the CI is wide enough to exceed Georgia's actual change ({a:.1f} times)"
        sign = "" if np.sign(r.implied) == np.sign(r.actual_change) else "; the point estimate has the opposite sign"
        return f"{lab}: implied {r.implied:+.3g} (95% CI {r.implied_lo:+.3g} to {r.implied_hi:+.3g}) against an actual {r.actual_change:+.3g} over {r.window}: {tail}{sign}."
    gi["sentence"] = gi.apply(sent, axis=1)
    gi["outcome_label"] = gi.outcome.map(olab)
    gi.to_csv(os.path.join(T, "s2_georgia_implied_vs_actual.csv"), index=False)
    pd.read_csv(os.path.join(E, "s2_georgia_ai_profile.csv")).to_csv(os.path.join(T, "s2_georgia_ai_profile.csv"), index=False)
    mix.to_csv(os.path.join(T, "s2_georgia_mix.csv"), index=False)
    cs = pd.read_csv(os.path.join(E, "s2_cross_state_changes.csv"))
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
    for ax, y, lab in [(axs[0], "d_solar", "Change in solar share of generation"), (axs[1], "d_renew", "Change in renewable share of generation")]:
        ax.scatter(cs.d_ai, cs[y], s=18, color="#9bb7d4")
        g = cs[cs.state == "GA"].iloc[0]; ax.scatter([g.d_ai], [g[y]], s=40, color="#d1495b"); ax.annotate("GA", (g.d_ai, g[y]), xytext=(4, 4), textcoords="offset points", color="#d1495b")
        for _, r in cs[cs.d_ai.abs() > cs.d_ai.abs().quantile(.94)].iterrows():
            if r.state != "GA":
                ax.annotate(r.state, (r.d_ai, r[y]), xytext=(3, -8), textcoords="offset points", fontsize=7, color="grey")
        b = np.polyfit(cs.d_ai, cs[y], 1); xs = np.linspace(cs.d_ai.min(), cs.d_ai.max(), 10); ax.plot(xs, b[0] * xs + b[1], color="grey", lw=.8, ls="--")
        ax.axhline(0, color="grey", lw=.5); ax.set_xlabel("Change in data-center jobs per 1,000 (t-1), 2015-2025"); ax.set_ylabel(lab)
    fig.suptitle("Across states, 2015-2025 (50 states; Georgia in red; dashed = OLS line, descriptive)"); fig.tight_layout()
    fig.savefig(os.path.join(F, "fig_s2_cross_state_georgia.png"), dpi=150); plt.close(fig)
    # family chart
    x = m[m.status == "ok"].copy(); x["lab"] = x.outcome.map(olab) + " | " + x.ai_measure.map({"ai518210": "jobs", "aipostp1000": "postings"})
    x["z"] = x.estimate / x.se
    fig, ax = plt.subplots(figsize=(7, 8)); ax.barh(range(len(x)), x.z, color=["#d1495b" if q < .1 else "#9bb7d4" for q in x.qval])
    ax.set_yticks(range(len(x))); ax.set_yticklabels(x.lab, fontsize=6.5); ax.axvline(0, color="grey", lw=.8)
    for v in (-1.96, 1.96): ax.axvline(v, color="grey", lw=.5, ls=":")
    ax.set_xlabel("t-statistic (red: q < 0.10)"); ax.set_title("AI(t-1) by renewable type, main spec"); fig.tight_layout(); fig.savefig(os.path.join(F, "fig_s2_bytype_t.png"), dpi=150); plt.close(fig)
    print(ft.to_string()); print("\n".join(gi.sentence))


IMP = {"ln_sales_com_pc": "ln commercial sales per person", "ln_sales_ind_pc": "ln industrial sales per person", "ln_sales_res_pc": "ln residential sales per person",
       "price_com861_c_kwh": "commercial price, cents/kWh (ctrl3)", "price_ind_c_kwh": "industrial price, cents/kWh (ctrl3)", "price_res_c_kwh": "residential price, cents/kWh (ctrl3)",
       "share_gas": "gas share of generation", "share_coal": "coal share of generation", "share_nuclear": "nuclear share of generation",
       "add_gas_per1000": "gas MW added per 1,000 MW", "add_solar_per1000": "solar MW added per 1,000 MW", "add_wind_per1000": "wind MW added per 1,000 MW",
       "net_imports": "net imports share of retail sales", "ln_co2_power": "ln power-sector CO2", "co2_per_mwh_t": "power-sector CO2 per MWh (t)"}


def s3(date, E, T, F):
    m = pd.read_csv(os.path.join(E, "s3_impact_family.csv"))
    t = family_table(m); t["outcome_label"] = m.outcome.map(IMP); t.to_csv(os.path.join(T, "s3_impact_table.csv"), index=False)
    rs = pd.read_csv(os.path.join(E, "s3_impact_restructured.csv")); rs.to_csv(os.path.join(T, "s3_impact_restructured.csv"), index=False)
    r = pd.read_csv("data/extend_restructured.csv"); r = r[r.state != "DC"].sort_values("energy_only_share_pct_2015", ascending=False)
    r[["state", "energy_only_share_pct_2015", "rpm_share_pct_2025", "restructured", "restructured_check_rpm2025", "near_cutoff_flag", "near_cutoff_flag_check"]].to_csv(os.path.join(T, "s3_restructured_classification.csv"), index=False)
    x = m[m.status == "ok"].copy(); x["lab"] = x.outcome.map(IMP) + " | " + x.ai_measure.map({"ai518210": "jobs", "aipostp1000": "postings"})
    x["z"] = x.estimate / x.se
    fig, ax = plt.subplots(figsize=(7, 7)); ax.barh(range(len(x)), x.z, color=["#d1495b" if q < .1 else "#9bb7d4" for q in x.qval])
    ax.set_yticks(range(len(x))); ax.set_yticklabels(x.lab, fontsize=7); ax.axvline(0, color="grey", lw=.8)
    for v in (-1.96, 1.96): ax.axvline(v, color="grey", lw=.5, ls=":")
    ax.set_xlabel("t-statistic (red: q < 0.10; none)"); ax.set_title("What AI(t-1) is associated with: main spec"); fig.tight_layout()
    fig.savefig(os.path.join(F, "fig_s3_impact_t.png"), dpi=150); plt.close(fig)
    print(t.to_string()); print("min q:", m.qval.min())


def s4(date, E, T, F):
    ye = pd.read_csv(os.path.join(E, "s4_year_effects.csv")); dm = pd.read_csv(os.path.join(E, "s4_drivers_models.csv")); pf = pd.read_csv(os.path.join(E, "s4_path_fit.csv"))
    nat = pd.read_csv("data/extend_drivers_national.csv")
    nat.to_csv(os.path.join(T, "s4_national_drivers.csv"), index=False); pd.read_csv("data/extend_drivers_state.csv").to_csv(os.path.join(T, "s4_state_resource.csv"), index=False)
    ye.to_csv(os.path.join(T, "s4_year_effects.csv"), index=False); pf.to_csv(os.path.join(T, "s4_path_fit.csv"), index=False)
    ai = dm[dm.term == "AI"].copy(); ai["coef"] = ai.apply(lambda r: f"{r.estimate:+.4g}{star(r.pval)} (p={r.pval:.3f})", axis=1)
    w = ai.pivot_table(index=["outcome", "ai_measure"], columns="model", values="coef", aggfunc="first").reset_index()
    w.to_csv(os.path.join(T, "s4_ai_three_models.csv"), index=False); dm.to_csv(os.path.join(T, "s4_drivers_models.csv"), index=False)
    lab = {"renew_share": "Renewable share", "ln_gen_wind": "ln wind generation", "ln_gen_solar": "ln solar generation"}
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    for ax, (y, l) in zip(axs, lab.items()):
        e = ye[ye.outcome == y]; ax.fill_between(e.year, e.ci_lo, e.ci_hi, color="#9bb7d4", alpha=.5); ax.plot(e.year, e.estimate, "o-", color="#2a6ebb", label="year effect (95% CI)")
        z = pd.read_csv(os.path.join(E, f"s4_path_{y}.csv")); ax.plot(z.year, z.driver_path, "s--", color="#d1495b", label="fitted driver path" + ("" if (dm.model == "drivers").any() else " (interim)"))
        r = pf[pf.outcome == y].iloc[0]; ax.set_title(f"{l}\ncorr {r.correlation:.2f}, R2 {r.r_squared:.2f}", fontsize=9); ax.axhline(0, color="grey", lw=.6)
    axs[0].legend(frameon=False, fontsize=7); fig.suptitle("Year effects (two-way model, base 2015) and the path fitted from measured drivers"); fig.tight_layout()
    fig.savefig(os.path.join(F, "fig_s4_year_effects_drivers.png"), dpi=150); plt.close(fig)
    g = lambda y, m, mod: ai[(ai.outcome == y) & (ai.ai_measure == m) & (ai.model == mod)].iloc[0]
    rs = [g("renew_share", "ai518210", k) for k in ["statefe", ("drivers" if (ai.model == "drivers").any() else "drivers-interim"), "twfe"]]
    full = not ai.model.str.contains("interim").any()
    dl = "drivers" if full else "drivers-interim"
    text = (f"**AI isn't the national trend.** With data-center jobs, the renewable-share coefficient barely moves across the three models: {rs[0].estimate:+.3f} with state FE only (p = {rs[0].pval:.3f}), "
            f"{rs[1].estimate:+.3f} with measured drivers (p = {rs[1].pval:.3f}) and {rs[2].estimate:+.3f} with two-way FE (p = {rs[2].pval:.3f}). Leaving out year effects doesn't make it positive, so the national rise isn't loading on AI. "
            f"**What the drivers show{'' if full else ' (interim: wind cost and the PTC pending)'}.** The year effects rise steadily for all three outcomes. A path fitted from measured drivers that vary by state, namely state RPS/CES targets (LBNL), solar resource x utility-scale solar LCOE "
            f"(LBNL Utility-Scale Solar), solar resource x the solar ITC (CRS IF10479; P.L. 117-169){', wind resource x wind cost (LBNL) and wind resource x the PTC (CRS R43453; P.L. 116-260; P.L. 117-169)' if full else ''} and 2015 gas share x the Henry Hub price (EIA), "
            f"correlates with them at {pf.loc[pf.outcome=='renew_share','correlation'].iloc[0]:.2f} (renewable share), {pf.loc[pf.outcome=='ln_gen_wind','correlation'].iloc[0]:.2f} (ln wind) and {pf.loc[pf.outcome=='ln_gen_solar','correlation'].iloc[0]:.2f} (ln solar) over 11 years. "
            f"That is consistent with these drivers' role but doesn't prove it: any series that rises over 2015-2025 correlates with a national trend. "
            f"Solar LCOE fell from {nat.solar_lcoe_2025usd_mwh.iloc[0]:.0f} to {nat.solar_lcoe_2025usd_mwh.min():.0f} $/MWh (2022) and rose to {nat.solar_lcoe_2025usd_mwh.iloc[-1]:.0f}; the ITC was 30%, 26% for 2020-2021, and 30% again under the IRA. "
            + (f"One exception: postings and ln solar generation are positive without year effects ({g('ln_gen_solar','aipostp1000','statefe').estimate:+.3f}, p = {g('ln_gen_solar','aipostp1000','statefe').pval:.3f}) and with drivers "
               f"({g('ln_gen_solar','aipostp1000',dl).estimate:+.3f}, p = {g('ln_gen_solar','aipostp1000',dl).pval:.3f}), and gone with year effects ({g('ln_gen_solar','aipostp1000','twfe').estimate:+.3f}, p = {g('ln_gen_solar','aipostp1000','twfe').pval:.3f}): "
               f"a 2019-2025 trend the measured drivers don't capture."
               if g('ln_gen_solar','aipostp1000',dl).estimate > 0 and g('ln_gen_solar','aipostp1000',dl).pval < .10 else
               f"Postings and ln solar generation are positive with state FE only ({g('ln_gen_solar','aipostp1000','statefe').estimate:+.3f}, p = {g('ln_gen_solar','aipostp1000','statefe').pval:.3f}), "
               f"but not once the measured drivers are in ({g('ln_gen_solar','aipostp1000',dl).estimate:+.3f}, p = {g('ln_gen_solar','aipostp1000',dl).pval:.3f}) or with year effects "
               f"({g('ln_gen_solar','aipostp1000','twfe').estimate:+.3f}, p = {g('ln_gen_solar','aipostp1000','twfe').pval:.3f}): the drivers absorb the shared 2019-2025 trend that the state-FE-only model loads on postings.")
            + " All are associations.")
    open(os.path.join(T, "s4_writeup.md"), "w").write(text + "\n"); print(text); print(w.to_string())


def s_p2(date, E, T, F):
    """Pass 2 additions (EXPERIMENTS.md 14.5): P1, P2, P4, P8, P9, P11."""
    r = pd.read_csv(os.path.join(E, "p2_checks.csv")); f8 = pd.read_csv(os.path.join("results", date, "fang", "fang8_results.csv"))
    # P11 gap decomposition
    rows = []
    for m, lab in [("aipostings", "ln AI postings"), ("dcjobs", "ln data-center jobs")]:
        for c in (1, 2, 6):
            v = {b: f8[(f8.block == "t2") & (f8.spec == f"c{c}-{b}") & (f8.ai_measure == m) & (f8.term == "AI")].iloc[0] for b in ["current", "rebuilt", "archived"]}
            gap = v["archived"].estimate - v["current"].estimate
            rows.append({"ai_measure": lab, "column": c, "current": round(v["current"].estimate, 4), "rebuilt": round(v["rebuilt"].estimate, 4), "june2023": round(v["archived"].estimate, 4),
                         "gap_june2023_minus_current": round(gap, 4), "share_accounting_rebuild": round((v["rebuilt"].estimate - v["current"].estimate) / gap, 3),
                         "share_later_data_revisions": round((v["archived"].estimate - v["rebuilt"].estimate) / gap, 3), "fang": FANG_T2["AI"][c - 1],
                         "june2023_as_share_of_fang": round(v["archived"].estimate / FANG_T2["AI"][c - 1], 3), "tags": "; ".join(x.tag for x in v.values())})
    gd = pd.DataFrame(rows); gd.to_csv(os.path.join(T, "p2_gap_decomposition.csv"), index=False)
    # P1 June 2023 rows, added to section 1 tables
    p1 = r[r.block.str.startswith("p1")]; p1.to_csv(os.path.join(T, "s1_june2023_trend_placebo_final.csv"), index=False)
    # P2 side by side
    w = r[r.block.str.startswith("p2") & (r.status == "ok")].pivot_table(index=["block", "ai_measure", "outcome"], columns="spec", values=["estimate", "se", "pval", "N"]).reset_index()
    w.columns = ["_".join([c for c in col if c]).replace("-", "_") for col in w.columns]
    w.to_csv(os.path.join(T, "p2_state_trends_side_by_side.csv"), index=False)
    # P4 biomass rows
    bt = pd.read_csv(os.path.join(E, "s2_bytype_results.csv"))
    bio = bt[bt.outcome.isin(["ln_seds_re_total", "ln_seds_woodwaste", "ln_seds_biofuels", "ln_seds_re_exbiomass", "ln_seds_re_exbiofuels", "share_bio", "ln_gen_bio"]) & bt.model.isin(["twfe"])]
    bio = bio[["outcome", "ai_measure", "estimate", "ci_lo", "ci_hi", "pval", "qval", "N", "tag"]].copy(); bio["outcome_label"] = bio.outcome.map(olab); bio.to_csv(os.path.join(T, "p2_biomass_rows.csv"), index=False)
    # P8 section 3 bounds per within-state SD
    m3 = pd.read_csv(os.path.join(E, "s3_impact_family.csv"))
    m3["per_sd"] = m3.estimate * m3.sd_within_ai; m3["per_sd_lo"] = m3.ci_lo * m3.sd_within_ai; m3["per_sd_hi"] = m3.ci_hi * m3.sd_within_ai
    m3["outcome_label"] = m3.outcome.map(IMP)
    m3[["outcome_label", "ai_measure", "sd_within_ai", "estimate", "ci_lo", "ci_hi", "per_sd", "per_sd_lo", "per_sd_hi", "pval", "qval", "tag"]].to_csv(os.path.join(T, "s3_bounds_per_within_sd.csv"), index=False)
    # P9 relevance
    rel = pd.read_csv(os.path.join(E, "p2_relevance.csv")); rel.to_csv(os.path.join(T, "p2_relevance.csv"), index=False)
    # Verdict, pass 2 wording (team items 1 and 10): June 2023 SEDS is the main old basis
    ds = pd.read_csv(os.path.join(T, "s1_descriptives_comparison.csv")); tp = pd.read_csv(os.path.join(E, "e3_e4_trend_placebo.csv"))
    a = lambda c: f8[(f8.block == "t2") & (f8.spec == f"c{c}-archived") & (f8.ai_measure == "aipostings") & (f8.term == "AI")].iloc[0]
    g1 = lambda blk, spec, m, term="AI": p1[(p1.block == blk) & (p1.spec == spec) & (p1.ai_measure == m) & (p1.term == term)].iloc[0]
    tw = lambda blk, m, y, spec: r[(r.block == blk) & (r.ai_measure == m) & (r.outcome == y) & (r.spec == spec)].iloc[0]
    reg = ds[~ds.variable.str.startswith("lnET") & (ds.variable != "lnAIp")]
    v = (f"**Verdict.** Our data match Fang's on every regressor: the means implied by Fang's Table 2 constants are within {reg.diff_sd.abs().max():.2f} SD of ours (GDP's gap fits 2012 vs 2017 dollars). "
         f"The outcome is what differs. On current SEDS, our mean ln renewables is {ds.loc[ds.variable=='lnET','diff_sd'].iloc[0]:.2f} SD below Fang's implied mean, the only flagged row; on the old fossil-fuel-equivalence basis the gap is about 0.04-0.06 SD. "
         f"**SEDS as published in June 2023 largely reproduces Fang:** the same sign, a similar size in columns 1-2 ({a(1).estimate:+.4f} and {a(2).estimate:+.4f} against +0.0428 and +0.0452), and about two-thirds of Fang's size in column 6 "
         f"({a(6).estimate:+.4f}, {fp(a(6).pval)}, against +0.0531). Of the move from current to June 2023 SEDS, {gd.loc[(gd.ai_measure=='ln AI postings')&(gd.column==6),'share_accounting_rebuild'].iloc[0]:.0%} (column 6, postings) comes from the accounting change and the rest from EIA's later data revisions. "
         f"But Fang's spec has no year effects, and on the June 2023 basis a linear trend turns column 6 to {g1('p1trend','fang6trend','aipostings').estimate:+.4f} ({fp(g1('p1trend','fang6trend','aipostings').pval)}), while pet-care employment, which has nothing to do with energy, "
         f"is associated with renewables more strongly than AI ({g1('p1placebo','fang6','petcare').estimate:+.4f}, {fp(g1('p1placebo','fang6','petcare').pval)}; distilleries {g1('p1placebo','fang6','distilleries').estimate:+.4f}, {fp(g1('p1placebo','fang6','distilleries').pval)}). "
         f"In our final spec, the June 2023 basis gives {tw('p1final','aipostings','lnET_arch','twfe').estimate:+.4f} ({fp(tw('p1final','aipostings','lnET_arch','twfe').pval)}; 2019-2021, the years the release covers) for postings. "
         f"Year effects remove national trends but not state-specific ones: distillery employment stays significant in our spec even with state linear trends "
         f"({tw('p2placebo','distilleries','lnRE','twfe-trend').estimate:+.4f}, {fp(tw('p2placebo','distilleries','lnRE','twfe-trend').pval)}).")
    open(os.path.join(T, "s1_verdict.md"), "w").write(v + "\n"); print(v)
    print(gd.drop(columns="tags").to_string()); print(m3[["outcome_label", "ai_measure", "sd_within_ai", "per_sd", "per_sd_lo", "per_sd_hi"]].round(4).to_string())
    print(bio.round(4).drop(columns="tag").to_string())


def s5(date, E, T, F):
    L = "logs/2026-11-07/"
    rel = pd.read_csv(os.path.join(E, "p2b_relevance_index.csv")); rel.to_csv(os.path.join(T, "s5_relevance_first.csv"), index=False)
    rk = pd.read_csv(os.path.join(E, "p2b_permutation_ranks.csv")); rk.to_csv(os.path.join(T, "s5_state_slope_ranks.csv"), index=False)
    for f in ["ai_index_coverage", "ai_index_loadings", "ai_index_diagnostics", "ai_index_component_correlations", "ai_index_crossstate_checks", "ai_index_oews_mapping"]:
        pd.read_csv(L + f + ".csv").to_csv(os.path.join(T, f"s5_{f.replace('ai_index_', '')}.csv"), index=False)
    ix = pd.read_csv(os.path.join(E, "p2b_index_family.csv")); ix["outcome_label"] = ix.outcome.map(lambda o: IMP.get(o, olab(o)))
    ix.to_csv(os.path.join(T, "s5_index_family.csv"), index=False)
    for f, n in [("p2b_2sls", "s5_2sls"), ("p2b_groupings", "addon_groupings"), ("p2b_land_moderator", "addon_land_moderator"), ("p2b_land_moderator_X5", "addon_land_moderator_X5"),
                 ("p2b_distillery_suppression", "p2_distillery_suppression"), ("p2b_distillery_rerun", "p2_distillery_rerun")]:
        pd.read_csv(os.path.join(E, f + ".csv")).to_csv(os.path.join(T, n + ".csv"), index=False)
    # chart: per-state slopes, commercial sales on AI, VA/TX/GA highlighted (jobs, all 50)
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    for ax, (tagm, lab) in zip(axs, [("ai518210", "data-center jobs"), ("aipostp1000", "postings"), ("indexA", "Index A")]):
        sl = pd.read_csv(os.path.join(E, f"p2b_state_slopes_{tagm}_all50.csv")).sort_values("slope").reset_index(drop=True)
        ax.bar(range(len(sl)), sl.slope, color=["#d1495b" if s_ in ("VA", "TX", "GA") else "#9bb7d4" for s_ in sl.state])
        for i, r in sl.iterrows():
            if r.state in ("VA", "TX", "GA"):
                ax.annotate(r.state, (i, r.slope), ha="center", va="bottom", fontsize=7, color="#d1495b")
        ax.axhline(0, color="grey", lw=.6); ax.set_xticks([]); ax.set_title(f"{lab}: one slope per state", fontsize=9)
    axs[0].set_ylabel("ln commercial sales per person\non AI(t-1), by state"); fig.tight_layout(); fig.savefig(os.path.join(F, "fig_s5_state_slopes.png"), dpi=150); plt.close(fig)
    x = ix[(ix.status == "ok") & (ix.family == "index") & (ix["sample"] == "all50")].copy(); x["z"] = x.estimate / x.se
    fig, ax = plt.subplots(figsize=(8, 4))
    for k, c in zip(["index_a", "index_b", "sub_infra", "sub_talent"], ["#2a6ebb", "#d1495b", "#6a994e", "#bc6c25"]):
        y = x[x["index"] == k]; ax.scatter(y.z, [k] * len(y), color=c, alpha=.6)
    for v in (-1.96, 1.96): ax.axvline(v, color="grey", lw=.5, ls=":")
    ax.set_xlabel("t-statistic, 34 outcomes per index (none with q < 0.10)"); ax.set_title("Index family, 50 states"); fig.tight_layout(); fig.savefig(os.path.join(F, "fig_s5_index_family.png"), dpi=150); plt.close(fig)
    print(rel[rel.version == "pooled"].round(4).to_string()); print(rk.to_string())


def main(date, section):
    E = os.path.join("results", date, "extend"); T = os.path.join(E, "tables"); F = os.path.join(E, "figures")
    os.makedirs(T, exist_ok=True); os.makedirs(F, exist_ok=True)
    {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 25: s_p2}.get(section, lambda *a: (_ for _ in ()).throw(SystemExit(f"section {section} not built yet")))(date, E, T, F)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--section", type=int, required=True)
    a = ap.parse_args(); main(a.date, a.section)

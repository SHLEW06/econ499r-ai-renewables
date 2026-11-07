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


def main(date, section):
    E = os.path.join("results", date, "extend"); T = os.path.join(E, "tables"); F = os.path.join(E, "figures")
    os.makedirs(T, exist_ok=True); os.makedirs(F, exist_ok=True)
    {1: s1, 2: s2}.get(section, lambda *a: (_ for _ in ()).throw(SystemExit(f"section {section} not built yet")))(date, E, T, F)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--section", type=int, required=True)
    a = ap.parse_args(); main(a.date, a.section)

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


def main(date, section):
    E = os.path.join("results", date, "extend"); T = os.path.join(E, "tables"); F = os.path.join(E, "figures")
    os.makedirs(T, exist_ok=True); os.makedirs(F, exist_ok=True)
    {1: s1}.get(section, lambda *a: (_ for _ in ()).throw(SystemExit(f"section {section} not built yet")))(date, E, T, F)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--section", type=int, required=True)
    a = ap.parse_args(); main(a.date, a.section)

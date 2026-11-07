#!/usr/bin/env python3
"""Tables and figures for prompts/08_finalize.md section 1 (EXPERIMENTS.md section 9b, F20-F26).

Usage: python3 code/python/04h3_fang_finalize_tables.py --date YYYY-MM-DD
Reads results/<date>/fang/fang8_results.csv. Writes results/<date>/fang/tables/*.csv and figures/*.png.
Fang's published numbers are typed from the paper (Fang, Lee & Li 2025, Renewable Energy 246, 122969), with PDF pages.
"""
import argparse, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Fang's AI coefficient (SE, N) by group: Table 3 (PDF p. 5), Table 4 (PDF p. 6), Table 5 (PDF p. 6)
FANG_SPLIT = {
    "elec": ("Electricity consumption", "T3 p.5", ("high", -0.0025, 0.026, 104), ("low", 0.0730, 0.028, 100), "low"),
    "price": ("Electricity price", "T3 p.5", ("high", 0.0628, 0.030, 108), ("low", 0.0334, 0.026, 96), "high"),
    "net": ("Net producer (high = producer)", "T3 p.5", ("high", -0.0060, 0.034, 76), ("low", 0.0425, 0.024, 128), "low"),
    "rd": ("R&D funding", "T4 p.6", ("high", 0.0163, 0.028, 100), ("low", 0.0704, 0.028, 104), "low"),
    "income": ("Per capita income", "T4 p.6", ("high", 0.1236, 0.034, 96), ("low", 0.0005, 0.021, 108), "high"),
    "weather": ("Extreme weather", "T4 p.6", ("high", 0.0790, 0.030, 104), ("low", 0.0145, 0.026, 100), "high"),
}
FANG_REG = {"West": (0.1176, 0.050, 52), "South": (-0.0409, 0.028, 68), "Northeast": (0.0235, 0.083, 36), "Midwest": (0.0626, 0.030, 48)}
# Fang Table 2 (PDF p. 5): AI and controls, columns 1-6
FANG_T2 = {"AI": [0.0428, 0.0452, 0.0396, 0.0548, 0.0561, 0.0531], "lnEPU": [None, -0.0284, -0.0206, -0.0242, -0.0239, -0.0253],
           "lnEP": [None, None, 0.1533, 0.2645, 0.2622, 0.2907], "lnGDP": [None, None, None, -0.7016, -0.6911, -0.7302],
           "lnPOP": [None, None, None, None, -0.1049, -0.0148], "lnEDU": [None, None, None, None, None, 0.1143]}
FANG_T2_SE = {"AI": [0.015, 0.015, 0.015, 0.016, 0.019, 0.019]}
MEAS = {"aipostings": "ln AI postings", "dcjobs": "ln data-center jobs"}


def star(p):
    return "" if pd.isna(p) else "***" if p < .01 else "**" if p < .05 else "*" if p < .1 else ""


def fmt(e, p):
    return "" if pd.isna(e) else f"{e:+.4f}{star(p)} (p={p:.3f})"


def sig_pattern(hi, plo_hi, lo, plo_lo, fang_side):
    """Fang's pattern: positive and significant (p<0.10) on fang_side, not significant on the other side."""
    on, onp, off, offp = (hi, plo_hi, lo, plo_lo) if fang_side == "high" else (lo, plo_lo, hi, plo_hi)
    if on > 0 and onp < .10 and offp >= .10:
        return "matches"
    if on > 0 and onp < .10:
        return "partly (both sides significant)"
    if on > off:
        return "same ordering, not significant"
    return "does not match"


def main(date):
    base = os.path.join("results", date, "fang")
    r = pd.read_csv(os.path.join(base, "fang8_results.csv"))
    T, F = os.path.join(base, "tables"), os.path.join(base, "figures")
    os.makedirs(T, exist_ok=True); os.makedirs(F, exist_ok=True)
    g = lambda block, spec, m, term="AI": r[(r.block == block) & (r.spec == spec) & (r.ai_measure == m) & (r.term == term)].iloc[0]
    # ---------- splits table ----------
    def arch(sn, m, side):
        h, l_ = g("splitarch", f"{sn}-high", m), g("splitarch", f"{sn}-low", m)
        i = r[(r.block == "interarch") & (r.spec == f"fang-{sn}") & (r.ai_measure == m)].iloc[0]
        return {"archived_high": fmt(h.estimate, h.pval), "archived_low": fmt(l_.estimate, l_.pval), "archived_diff": fmt(i.estimate, i.pval),
                "matches_fang_pattern_archived": sig_pattern(h.estimate, h.pval, l_.estimate, l_.pval, side)}
    rows = []
    for key, (lab, src, (_, fh, fhs, fhn), (_, fl, fls, fln), side) in FANG_SPLIT.items():
        for m in MEAS:
            for split in (["mean", "median"] if key != "net" else ["binary"]):
                sn = "net_producer" if key == "net" else f"{key}_{split}"
                hi, lo = g("split", f"{sn}-high", m), g("split", f"{sn}-low", m)
                thi, tlo = g("splittw", f"{sn}-high", m), g("splittw", f"{sn}-low", m)
                fi = r[(r.block == "inter") & (r.spec == f"fang-{sn}") & (r.ai_measure == m)].iloc[0]
                ti = r[(r.block == "inter") & (r.spec == f"twfe-{sn}") & (r.ai_measure == m)].iloc[0]
                rows.append({"group": lab, "fang_source": src, "split": split, "ai_measure": MEAS[m],
                             "fang_high": f"{fh:+.4f} (SE {fhs}, N {fhn})", "fang_low": f"{fl:+.4f} (SE {fls}, N {fln})",
                             "fangspec_high": fmt(hi.estimate, hi.pval), "N_high": int(hi.N), "fangspec_low": fmt(lo.estimate, lo.pval), "N_low": int(lo.N),
                             "fangspec_diff": fmt(fi.estimate, fi.pval), "fangspec_diff_se": round(fi.se, 4),
                             "ourspec_high": fmt(thi.estimate, thi.pval), "ourspec_low": fmt(tlo.estimate, tlo.pval),
                             "ourspec_diff": fmt(ti.estimate, ti.pval), "ourspec_diff_se": round(ti.se, 4),
                             "matches_fang_pattern_fangspec": sig_pattern(hi.estimate, hi.pval, lo.estimate, lo.pval, side),
                             **arch(sn, m, side), "tag_high": hi.tag, "tag_diff_ourspec": ti.tag})
        if key == "weather":
            for m in MEAS:
                hi, lo = g("split", "weather_episodes_mean-high", m), g("split", "weather_episodes_mean-low", m)
                ti = r[(r.block == "inter") & (r.spec == "twfe-weather_episodes_mean") & (r.ai_measure == m)].iloc[0]
                fi = r[(r.block == "inter") & (r.spec == "fang-weather_episodes_mean") & (r.ai_measure == m)].iloc[0]
                rows.append({"group": "Extreme weather (episodes, check)", "fang_source": src, "split": "mean", "ai_measure": MEAS[m],
                             "fang_high": f"{fh:+.4f}", "fang_low": f"{fl:+.4f}", "fangspec_high": fmt(hi.estimate, hi.pval), "N_high": int(hi.N),
                             "fangspec_low": fmt(lo.estimate, lo.pval), "N_low": int(lo.N), "fangspec_diff": fmt(fi.estimate, fi.pval), "fangspec_diff_se": round(fi.se, 4),
                             "ourspec_high": fmt(g("splittw", "weather_episodes_mean-high", m).estimate, g("splittw", "weather_episodes_mean-high", m).pval),
                             "ourspec_low": fmt(g("splittw", "weather_episodes_mean-low", m).estimate, g("splittw", "weather_episodes_mean-low", m).pval),
                             "ourspec_diff": fmt(ti.estimate, ti.pval), "ourspec_diff_se": round(ti.se, 4),
                             "matches_fang_pattern_fangspec": sig_pattern(hi.estimate, hi.pval, lo.estimate, lo.pval, "high"), **arch("weather_episodes_mean", m, "high"), "tag_high": hi.tag, "tag_diff_ourspec": ti.tag})
    for reg, (fe_, fs_, fn_) in FANG_REG.items():
        for m in MEAS:
            a, b = g("split", f"region-{reg}", m), g("splittw", f"region-{reg}", m)
            fj = r[(r.block == "inter") & (r.spec == "fang-region") & (r.ai_measure == m)].iloc[0]
            tj = r[(r.block == "inter") & (r.spec == "twfe-region") & (r.ai_measure == m)].iloc[0]
            cat = lambda e, p: "sig+" if (e > 0 and p < .10) else "sig-" if (e < 0 and p < .10) else "null"
            pat = "matches" if cat(fe_, 2 * (1 - __import__("scipy.stats").stats.norm.cdf(abs(fe_ / fs_)))) == cat(a.estimate, a.pval) else "does not match"
            rows.append({"group": f"Region: {reg}", "fang_source": "T5 p.6", "split": "region", "ai_measure": MEAS[m],
                         "fang_high": f"{fe_:+.4f} (SE {fs_}, N {fn_})", "fang_low": "", "fangspec_high": fmt(a.estimate, a.pval), "N_high": int(a.N),
                         "fangspec_low": "", "N_low": np.nan, "fangspec_diff": f"joint F {fj.estimate:.2f} (p={fj.pval:.3f})", "fangspec_diff_se": np.nan,
                         "ourspec_high": fmt(b.estimate, b.pval), "ourspec_low": "", "ourspec_diff": f"joint F {tj.estimate:.2f} (p={tj.pval:.3f})", "ourspec_diff_se": np.nan,
                         "matches_fang_pattern_fangspec": pat + " (sign and significance on this region)",
                         "archived_high": fmt(g("splitarch", f"region-{reg}", m).estimate, g("splitarch", f"region-{reg}", m).pval), "archived_low": "", "archived_diff": "",
                         "matches_fang_pattern_archived": ("matches" if cat(fe_, 2 * (1 - __import__("scipy.stats").stats.norm.cdf(abs(fe_ / fs_)))) == cat(g("splitarch", f"region-{reg}", m).estimate, g("splitarch", f"region-{reg}", m).pval) else "does not match"),
                         "tag_high": a.tag, "tag_diff_ourspec": tj.tag})
    sp = pd.DataFrame(rows); sp.to_csv(os.path.join(T, "fang8_splits_table.csv"), index=False)
    # ---------- Table 2 by basis ----------
    t2 = []
    for m in MEAS:
        for term in ["AI", "lnEPU", "lnEP", "lnGDP", "lnPOP", "lnEDU"]:
            for c in range(1, 7):
                fv = FANG_T2[term][c - 1]
                if fv is None:
                    continue
                row = {"ai_measure": MEAS[m], "term": term, "column": c, "fang": fv}
                for b in ["current", "k26", "rebuilt", "archived"]:
                    x = r[(r.block == "t2") & (r.spec == f"c{c}-{b}") & (r.ai_measure == m) & (r.term == term)].iloc[0]
                    row[b] = round(x.estimate, 4); row[f"{b}_p"] = round(x.pval, 3); row[f"{b}_ci"] = f"[{x.ci_lo:.4f}, {x.ci_hi:.4f}]"
                    row[f"{b}_fang_in_ci"] = bool(x.ci_lo <= fv <= x.ci_hi); row[f"{b}_tag"] = x.tag
                t2.append(row)
    t2 = pd.DataFrame(t2); t2.to_csv(os.path.join(T, "fang8_table2_by_basis.csv"), index=False)
    # ---------- negative indicator, final spec, event study ----------
    r[r.block == "neg"][["tag", "spec", "ai_measure", "outcome", "estimate", "se", "pval", "ci_lo", "ci_hi", "N"]].to_csv(os.path.join(T, "fang8_negative_indicator.csv"), index=False)
    r[r.block == "final"][["tag", "spec", "ai_measure", "outcome", "estimate", "se", "pval", "ci_lo", "ci_hi", "N"]].to_csv(os.path.join(T, "fang8_final_by_basis.csv"), index=False)
    es = r[r.block == "es"].copy(); es.to_csv(os.path.join(T, "fang8_event_study.csv"), index=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    for b, col, off in [("current", "#2a6ebb", -0.08), ("rebuilt", "#d1495b", 0.08)]:
        e = es[(es.spec == b) & es.term.str.match(r"b\d{4}")].copy(); e["yr"] = e.term.str[1:].astype(int)
        e = pd.concat([e, pd.DataFrame({"yr": [2021], "estimate": [0.0], "ci_lo": [0.0], "ci_hi": [0.0]})]).sort_values("yr")
        ax.errorbar(e.yr + off, e.estimate, yerr=[e.estimate - e.ci_lo, e.ci_hi - e.estimate], fmt="o-", color=col, capsize=3, label=f"{b} SEDS basis")
    ax.axhline(0, color="grey", lw=.8); ax.axvline(2021.5, color="grey", ls=":", lw=.8)
    ax.set_xlabel("Year"); ax.set_ylabel("Effect on ln renewables per 1 pp\nof 2019 postings share (95% CI)")
    ax.set_title("Event study: 2019 AI-postings exposure x year (base 2021)"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(F, "fig_fang8_event_study.png"), dpi=150); plt.close(fig)
    # Table 2 chart: column 6 AI, four bases
    fig, ax = plt.subplots(figsize=(7, 3.6))
    labs = ["Fang", "current", "k = 2.6", "rebuilt", "archived"]
    for i, m in enumerate(MEAS):
        x = t2[(t2.ai_measure == MEAS[m]) & (t2.term == "AI") & (t2.column == 6)].iloc[0]
        vals = [x.fang, x.current, x.k26, x.rebuilt, x.archived]
        lo = [x.fang - 1.96 * .019] + [float(x[f"{b}_ci"].strip("[]").split(",")[0]) for b in ["current", "k26", "rebuilt", "archived"]]
        hi = [x.fang + 1.96 * .019] + [float(x[f"{b}_ci"].strip("[]").split(",")[1]) for b in ["current", "k26", "rebuilt", "archived"]]
        xs = np.arange(5) + (i - .5) * .3
        ax.errorbar(xs, vals, yerr=[np.array(vals) - lo, np.array(hi) - vals], fmt="o", capsize=3, label=MEAS[m])
    ax.set_xticks(range(5)); ax.set_xticklabels(labs); ax.axhline(0, color="grey", lw=.8)
    ax.set_ylabel("AI coefficient, col. 6 (95% CI)"); ax.set_title("Fang Table 2, column 6, by SEDS basis"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(F, "fig_fang8_table2_by_basis.png"), dpi=150); plt.close(fig)
    print(sp[["group", "split", "ai_measure", "fang_high", "fang_low", "fangspec_high", "fangspec_low", "ourspec_diff", "matches_fang_pattern_fangspec", "archived_high", "archived_low", "matches_fang_pattern_archived"]].to_string())
    print(t2[t2.term == "AI"][["ai_measure", "column", "fang", "current", "k26", "rebuilt", "rebuilt_p", "archived", "archived_p", "archived_fang_in_ci", "rebuilt_fang_in_ci"]].to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); main(ap.parse_args().date)

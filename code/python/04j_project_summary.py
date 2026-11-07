#!/usr/bin/env python3
"""Write docs/<date>/project-summary.md. Every number is read from a result file and traced to its tag in the appendix.
Usage: python3 code/python/04j_project_summary.py --date YYYY-MM-DD"""
import argparse, os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from results_lookup import Ledger
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); D = ap.parse_args().date
B = "2026-11-04"  # Nov 2-4 blocks stay in their folders
P = f"results/{D}/paper"; RB = f"results/{B}/robustness/robustness.csv"; F = f"results/{B}/fang/fang_results.csv"; SH = f"results/{B}/stretch/stretch.csv"; PI = f"results/{B}/h3_placebo/placebo_sdm_impacts.csv"; PS = f"results/{B}/h3_placebo/placebo_slx.csv"; G = f"results/{B}/georgia_solar/projection_long.csv"; BC = f"results/{B}/georgia_solar/base_cost.csv"
F8R = "results/2026-11-07/fang/fang8_results.csv"; EX = "results/2026-11-07/extend"; GD = f"{EX}/tables/p2_gap_decomposition.csv"; P2C = f"{EX}/p2_checks.csv"; ES = f"{P}/tables/ext_summary.csv"; DM = f"{EX}/s4_drivers_models.csv"; PF = f"{EX}/s4_path_fit.csv"; RL = f"{EX}/p2b_relevance_index.csv"; RK = f"{EX}/p2b_permutation_ranks.csv"; BT = f"{EX}/s2_bytype_family.csv"; GI = f"{EX}/s2_georgia_implied.csv"
t2 = lambda b_, c_: dict(block="t2", spec=f"c{c_}-{b_}", ai_measure="aipostings", term="AI"); dm = lambda mod: dict(outcome="renew_share", ai_measure="ai518210", model=mod, term="AI")
H1 = "results/2026-11-02/h1"; C = f"{H1}/h1_core.csv"; X = f"{H1}/h1_extras.csv"; H2 = "results/2026-11-03/h2/h2_results.csv"; MS = "results/2026-11-03/h3_mainspec/sdm_impacts.csv"; MC = "results/2026-11-03/h3_mainspec/sdm_core.csv"; RU = f"{P}/rule_out.csv"; MED = f"{P}/tables/mediation_summary.csv"; LR = f"results/{B}/georgia_solar/national_lcoe_lbnl_tab.csv"; WX = f"results/{B}/robustness/weather_check.csv"; NP = f"results/{B}/fang/net_producer_check.csv"
SEDSURL = "https://www.eia.gov/state/seds/seds-change/index.php"
L = Ledger("project-summary.md"); W = pd.read_csv(RU)
t = lambda y: f"h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_{y}_50s2015_2025"; xt = lambda s: f"h1x_{s}"
e = lambda path, fmt="{:.4f}", **k: L.n(path, "estimate", fmt, **k); pv = lambda path, **k: L.p(path, **k)
MW = xt("twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025"); PC = xt("rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per1000mw_50s2015_2025")
ci = lambda i, f="{:.2f}": f"{L.n(RU, 'ci_lo_per_sd', f, tag=W.tag[i])} to {L.n(RU, 'ci_hi_per_sd', f, tag=W.tag[i])}"
sdm = dict(outcome="renew_share", W_version="invdist50", estimator="ML", effect="indirect"); sdt = dict(outcome="renew_share", W_version="invdist50", estimator="ML", effect="total")
br = lambda m: dict(block="bridge", spec="s6-noDC", ai_measure=m); r6 = dict(block="rep", spec="c6", ai_measure="aipostings", term="AI", vcov="iid", sample="51s2018_2021")
tx = f"""# Project summary

ECON 499R, Emory University. Shunji Lewandowski (modeling) and Alexander Hendricks (data and finance). Advisor: Prof. Fohlin. As of {D}. All results are associations; nothing here shows that AI causes a change. Every number traces to a result tag in the appendix.

## The question

Is growth in AI-related activity associated with more or less electricity use, energy efficiency and renewable energy across U.S. states? We test two papers. Zhang et al. (2026), "Blessing or Peril?", argues AI shapes energy use through tech jobs and density and spills across borders. Fang, Lee and Li (2025) find a positive association between AI job postings and renewable energy use. We also add a Georgia case box, because Georgia is a large data-center market with a regulated utility.

## The data

- **Panel:** 50 states and DC, 2015-2025 (561 rows, 80 variables), from public sources: EIA, BLS, BEA and Census. CO2 and SEDS end in 2024.
- **AI measure:** private data-center jobs per 1,000 workers (NAICS 518210, BLS). It's a proxy for data-center activity, not AI use. BLS suppressed four states in 2025.
- **Fang's measure:** AI job postings from the Stanford AI Index, 2018-2025. Almost every year comes from a different report edition, so **data-center jobs are the more reliable measure** when we extend the sample.
- **Checks:** Part C validation: 0 red, 3 yellow, 17 green. A separate cell-by-cell audit, and cross-source checks that are green, except one reported gap: no net-producer rule reaches Fang's count. Everything is in the master workbook, with sources, ratings and limitations.

## What we ran

| Test | Model | Data | N |
|---|---|---|---|
| H1, Zhang | Two-way fixed effects, last year's AI, four controls, SEs clustered by state | 50 states, 2015-2025 | {L.n(C, "N", "{:.0f}", tag=t("ln_ec"))} |
| H2, mediation | Same design, Sobel tests and a cluster bootstrap, 9 pairs | Same | {L.n(H2, "N", "{:.0f}", tag="h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a")} |
| H3, spillovers | Spatial Durbin, inverse-distance weights (main), border (check) | Same; timing test 2015-2023 | {L.n(MC, "N", "{:.0f}", outcome="renew_share", W_version="invdist50", estimator="ML")}; timing {L.n(PI, "N", "{:.0f}", W_version="invdist50", outcome="renew_share", version="a_lag", effect="indirect")} |
| Robustness | Timing placebo, RPS control, all-ownership AI, drop-one-state, others | Same | Varies |
| Fang replication | State FE only, conventional SEs, Fang's controls | 50 states and DC, 2018-2021 | {L.n(F, "N", "{:.0f}", **r6)} |
| Fang bridge | One change at a time, to our design | Up to 2015-2024, no DC | Postings {L.n(F, "N", "{:.0f}", **br("aipostings"))}; jobs {L.n(F, "N", "{:.0f}", **br("dcjobs"))} |
| Stretch | Shift-share IV; broadband and R&D moderation | Varies | {L.n(SH, "N", "{:.0f}", spec="base2015", outcome="first_stage", term="KP_F")} |
| Georgia solar | Learning-curve arithmetic on IEA paths | LBNL projects, Georgia | {L.n(BC, "n_projects", "{:.0f}", area="Georgia")} projects |

## The results, and whether each holds up

- **H1, electricity use and efficiency: no association.** Coefficients {e(C, tag=t("ln_ec"))} ({pv(C, tag=t("ln_ec"))}) and {e(C, tag=t("ln_ee"))} ({pv(C, tag=t("ln_ee"))}). **Holds up** under clustered SEs. Driscoll-Kraay SEs, a sensitivity check only with 11 years, put ln_ee at {pv(RB, spec="dk", outcome="ln_ee", coef="ai_dc_per1000_lag1")}.
- **H1, renewable share: negative but not significant, and the timing fails.** {e(C, tag=t("renew_share"))} ({pv(C, tag=t("renew_share"))}; {pv(RB, spec="dk", outcome="renew_share", coef="ai_dc_per1000_lag1")} under Driscoll-Kraay, sensitivity only). Next year's AI predicts this year's share ({e(RB, spec="placebo", outcome="renew_share", coef="ai_lead1_w")}, {pv(RB, spec="placebo", outcome="renew_share", coef="ai_lead1_w")}). With both in one model the lag is about zero ({e(RB, spec="placebo-joint", outcome="renew_share", coef="ai_dc_per1000_lag1")}, {pv(RB, spec="placebo-joint", outcome="renew_share", coef="ai_dc_per1000_lag1")}). This reflects where and when data-center jobs grow (reverse timing or selection), not AI lowering the share.
- **H1, new renewable capacity: doesn't hold up.** {e(X, "{:.1f}", tag=MW)} MW ({pv(X, tag=MW)}) in raw MW, but {e(X, "{:.2f}", tag=PC)} ({pv(X, tag=PC)}) per 1,000 MW of 2015 capacity. Its lead is positive too ({e(RB, "{:.1f}", spec="placebo", outcome="new_renew_mw", coef="ai_lead1_w")}, {pv(RB, spec="placebo", outcome="new_renew_mw", coef="ai_lead1_w")}), and with both in one model neither is significant.
- **H2, mediation: no channel.** AI isn't associated with the tech-job share ({L.n(H2, "estimate", "{:.6f}", tag="h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a")}, {L.p(H2, tag="h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a")}). Sobel p-values run from {L.n(MED, "min_p", "{:.3f}", tag="h2_sobel_summary")} to {L.n(MED, "max_p", "{:.3f}", tag="h2_sobel_summary")}, and every bootstrap CI includes zero.
- **H3, spillovers: not supported.** On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate ({L.n(MS, "plugin", "{:.3f}", **sdm)}, {L.p(MS, "p", **sdm)}) can't be separated from this reverse timing. H3 is not supported.
- **Robustness: no change.** The RPS control (LBNL current RPS/CES schedule) and all-ownership AI change no result. Holding Gavins Point in Nebraska gives {L.n(RB, "estimate", "{:.1f}", spec="gavins-ne", outcome="new_renew_mw", coef="ai_dc_per1000_lag1")} MW. With NOAA heating and cooling degree days on the 48 contiguous states, ln_ec is {L.n(WX, "estimate", spec="weather-hddcdd", coef="ai_dc_per1000_lag1")} ({L.p(WX, spec="weather-hddcdd", coef="ai_dc_per1000_lag1")}), against {L.n(WX, "estimate", spec="weather-base48", coef="ai_dc_per1000_lag1")} ({L.p(WX, spec="weather-base48", coef="ai_dc_per1000_lag1")}) on the same states without them.
- **Fang: largely reproduces on the data Fang used, not on today's, and not in our design.** Fang's {L.typed("0.0531", "Fang et al. 2025, Table 2, col. 6")} is {e(F, **r6)} ({pv(F, **r6)}) on current SEDS. On SEDS as published in June 2023, before EIA's accounting change ([notice]({SEDSURL})), column 6 is {L.n(F8R, "estimate", **t2("archived", 6))} ({L.p(F8R, **t2("archived", 6))}), about two-thirds of Fang's, with similar sizes in columns 1-2; {L.n(GD, "share_accounting_rebuild", "{:.0%}", ai_measure="ln AI postings", column=6)} of the gap from current SEDS comes from the accounting change and the rest from later data revisions. Fang's spec has no year effects: a linear trend turns column 6 to {L.n(P2C, "estimate", block="p1trend", spec="fang6trend", ai_measure="aipostings", outcome="lnET_arch", term="AI")} ({L.p(P2C, block="p1trend", spec="fang6trend", ai_measure="aipostings", outcome="lnET_arch", term="AI")}), and pet-care employment "explains" renewables more strongly than AI. In our final spec, postings are {e(F, **br("aipostings"))} ({pv(F, **br("aipostings"))}) and data-center jobs {e(F, **br("dcjobs"))} ({pv(F, **br("dcjobs"))}): neither significant. Fang's headline subgroup splits (price, net producer) don't reproduce; the partial matches on the June 2023 basis are exploratory.
- **Extensions (Nov 7).** By renewable type, one row passes the multiple-testing rule (postings and wind generation, {L.n(BT, "estimate", outcome="ln_gen_wind", ai_measure="aipostp1000")}), but it runs against the expected sign and fails with state trends, so it's exploratory. None of 30 other AI-impact outcomes (sales by sector, prices, generation mix, imports, CO2) has q below 0.10. Georgia's solar share rose {L.n(GI, "actual_change", "{:.3f}", outcome="share_solar", ai_measure="ai518210")}; AI could account for at most {L.n(GI, "at_most_share_of_actual", "{:.0%}", outcome="share_solar", ai_measure="ai518210")} of it. The renewable-share coefficient barely moves without year effects or with measured drivers ({L.n(DM, "estimate", "{:.3f}", **dm("statefe"))}, {L.n(DM, "estimate", "{:.3f}", **dm("drivers"))}, {L.n(DM, "estimate", "{:.3f}", **dm("twfe"))}), so the national trend isn't AI; costs, tax credits and mandates track it (correlation {L.n(PF, "correlation", "{:.2f}", outcome="renew_share")}, consistent with but not proof of their role). Pooled, data-center jobs don't predict commercial electricity sales ({L.p(RL, sample="all50", ai_measure="ai518210", version="pooled")}); Virginia's state slope ranks {L.n(RK, "rank_desc", "{:.0f}", sample="all50", ai_measure="ai518210", state="VA")} of 50. A broader "infrastructure + talent" AI index finds nothing either (smallest q {L.n(ES, "value", "{:.2f}", tag="ext_index_min_q_all50")}).
- **EPU moderation: only in Fang's spec.** AI x state EPU is {e(F, block="mod", spec="fang-lnEPUS", ai_measure="aipostings", term="AI_x_EPU")} ({pv(F, block="mod", spec="fang-lnEPUS", ai_measure="aipostings", term="AI_x_EPU")}) there and not significant under two-way FE ({pv(F, block="mod", spec="twfe-lnEPUS", ai_measure="aipostings", term="AI_x_EPU")}).
- **Net-producer split: depends on the definition.** Our rule gives {L.n(NP, "net_producer_state_years", "{:.0f}", definition="gen_gt_sales", ai_measure="aipostings", group="difference")} net-producer state-years against Fang's 76; SEDS total energy gives {L.n(NP, "net_producer_state_years", "{:.0f}", definition="teprb_gt_tetcb", ai_measure="aipostings", group="difference")} and SEDS net interstate flow {L.n(NP, "net_producer_state_years", "{:.0f}", definition="elisb_negative", ai_measure="aipostings", group="difference")}. The gap between groups in Fang's spec is significant only on our rule ({L.p(NP, definition="gen_gt_sales", ai_measure="aipostings", group="difference")}). Exploratory.
- **Shift-share IV: uninformative.** KP F = {e(SH, "{:.2f}", spec="base2015", outcome="first_stage", term="KP_F")}, below 10. **Broadband and R&D:** no interaction is significant. **Hansen threshold:** not run, dropped by the team.
- **Georgia solar.** At a 24% learning rate on IEA's Stated Policies path (*World Energy Outlook 2025*, Table A.3b, p. 423), the arithmetic implies ${L.n(G, "lcoe_2025usd_mwh", "{:.2f}", path="Central", learning_rate=.24, year=2035)}/MWh in 2035, with a range across cases, also using Current Policies (Table A.3a, p. 417) and Net Zero Emissions by 2050 (Table A.3c, p. 429), of ${L.n(G, "lcoe_2025usd_mwh", "{:.2f}", path="High", learning_rate=.45, year=2035)} to ${L.n(G, "lcoe_2025usd_mwh", "{:.2f}", path="Low", learning_rate=.12, year=2035)}. It starts from ${L.n(BC, "lcoe_capacity_weighted", "{:.2f}", area="Georgia")}/MWh. These aren't forecasts of ours, and national LCOE has risen since 2022 ({L.n(LR, "lcoe", "{:.1f}", year=2022)} to {L.n(LR, "lcoe", "{:.1f}", year=2025)}), so the curve assumes costs resume falling.

## What we can rule out

95% CI per one within-state SD of AI. **The SD is {L.n(RU, "sd_ai", tag=W.tag[0])}: winsorized lagged AI after removing state and year effects, 50 states, N = {L.n(C, "N", "{:.0f}", tag=t("ln_ee"))}.** That's the variation the Zhang models use. The Fang rows use the SD of each log AI measure the same way.

| Outcome | 95% CI per SD | Unit |
|---|---|---|
| Electricity use per person | {ci(0)} | percent |
| GDP per MWh | {ci(1)} | percent |
| Renewable share of generation | {ci(2)} | percentage points |
| Change in renewable capacity | {ci(3)} | MW; not robust to scaling |
| Same, per 1,000 MW of 2015 capacity | {ci(4)} | MW per 1,000 MW |
| Renewable consumption, per SD of ln(AI postings), SD {L.n(RU, "sd_ai", tag=W.tag[5])} | {ci(5)} | percent |
| Renewable consumption, per SD of ln(data-center jobs), SD {L.n(RU, "sd_ai", tag=W.tag[6])} | {ci(6)} | percent |

So a typical within-state swing in data-center jobs isn't associated with a fall in electricity use of more than {L.n(RU, "ci_lo_per_sd", "{:.2f}", scale=-1, tag=W.tag[0])} percent or a rise of more than {L.n(RU, "ci_hi_per_sd", "{:.2f}", tag=W.tag[0])} percent, or with a fall in renewable share of more than {L.n(RU, "ci_lo_per_sd", "{:.2f}", scale=-1, tag=W.tag[2])} points. These limits apply to data-center jobs over this period. They don't cover a much larger future build-out, and jobs aren't MW.

## What it means

At the state level over 2015-2025, we don't find that data-center job growth is associated with lower efficiency, higher electricity use or a lower renewable share once timing is taken into account. Neither the "blessing" nor the "peril" holds up in this data. The most useful result is the placebo: associations that look real in a standard panel are explained as well or better by next year's AI, so they're likely about where data-center jobs go. Our main limits are that jobs are a rough proxy for AI power use, states have little within-state variation, and we have no strong instrument. Georgia Power reports commitments from large-load customers of {L.typed("15,600", "Georgia Power Q2 2026 Large Load Economic Development Report, PSC Docket 55378, p. 4 [PDF p. 8]")} MW as of June 2026, up from {L.typed("3,600", "Georgia Power Q2 2026 Large Load Economic Development Report, PSC Docket 55378, p. 4 [PDF p. 8]")} MW at its October 2023 filing (Q2 2026 Large Load Economic Development Report, filed Aug. 17, 2026, Georgia PSC Docket 55378, p. 4 [PDF p. 8]). That's the utility's own reporting, and most of that load is scheduled after our sample ends, so these results describe the past, not that build-out.

## Status and next steps

- **Done:** data, validation, H1-H3, robustness, Fang test (incl. the completed method set, Nov 7), extensions (by type, AI impact, national drivers, AI index, add-on), stretch, Georgia solar, results pack, master workbook.
- **Pending, needs a person:** Q1-Q4 2024 Georgia large-load reports (browser download from PSC Docket 55378); LBNL Queued Up (refuses scripted download); Fang's supplementary material (Table A1, Supplement B); PatentsView inventor locations, if the innovation dimension is wanted.
- **Next:** team review of the results by Nov 17; draft by Nov 24 from `methods_section.tex` and `findings.md`; turn-in Dec 1. `methods_section.tex` hasn't been compiled here, since no LaTeX is installed.

## Where things are

| Looking for | Where |
|---|---|
| All data, variables, ratings and limitations | `outputs/ECON499R_Master_Data_{D}.xlsx`; `data/variable_registry.csv` |
| Results tables, figures and findings | `results/{D}/paper/` |
| Readable report | `outputs/ECON499R_Results_{D}.pdf` |
| Methods draft and memo differences | `docs/{D}/methods_section.tex`; `docs/{D}/memo-to-paper.md`; `EXPERIMENTS.md` |
| Notebooks | `notebooks/` |
| Rebuild steps and sources | `data/receipts/README.md` |
| Packages | `release/results_and_data_{D}/` (local); `release/github/econ499r-ai-renewables/` (clean copy to push) |
"""
ck = L.check(tx); ck.to_csv(f"{P}/number_check_summary.csv", index=False)
if (ck.match.isin(["NO"])).any() or (ck.in_document == "no").any(): print(ck[(ck.match == "NO") | (ck.in_document == "no")].to_string()); sys.exit("number check failed")
un = ck[ck.match == "UNLOGGED"]; print("unlogged:", un.number.tolist())
ap_ = "\n\n## Appendix: every number and its result tag\n\n| Number | Source file | Tag | Column |\n|---|---|---|---|\n"
seen = set()
for r in ck[ck.match != "UNLOGGED"].itertuples():
    k = (r.number, r.source_tag, r.column)
    if k in seen: continue
    seen.add(k); ap_ += f"| {r.number} | `{r.source_file}` | `{r.source_tag}` | {r.column} |\n"
if len(un): sys.exit("unlogged numbers: " + ", ".join(un.number))
open(f"docs/{D}/project-summary.md", "w").write(tx + ap_); print(ck.match.value_counts().to_dict(), "words", len(tx.split()))

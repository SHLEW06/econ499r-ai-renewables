#!/usr/bin/env python3
"""Readable results report: self-contained HTML first, then PDF with headless Chrome. No new estimation.
Tables are read verbatim from results/<date>/paper/tables/. Every number in the text comes through a Ledger and is listed in the appendix.
Usage: python3 code/python/04k_results_report.py --date YYYY-MM-DD"""
import argparse, base64, html, os, re, subprocess, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from results_lookup import Ledger
ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); D = ap.parse_args().date
B = "2026-11-04"  # Nov 2-4 blocks stay in their folders
P = f"results/{D}/paper"; TB = f"{P}/tables"; FG = f"{P}/figures"; RB = f"results/{B}/robustness/robustness.csv"; F = f"results/{B}/fang/fang_results.csv"; SH = f"results/{B}/stretch/stretch.csv"; PI = f"results/{B}/h3_placebo/placebo_sdm_impacts.csv"; PS = f"results/{B}/h3_placebo/placebo_slx.csv"; G = f"results/{B}/georgia_solar/projection_long.csv"; BC = f"results/{B}/georgia_solar/base_cost.csv"; LR = f"results/{B}/georgia_solar/national_lcoe_lbnl_tab.csv"; WX = f"results/{B}/robustness/weather_check.csv"; NP = f"results/{B}/fang/net_producer_check.csv"; LV = f"results/{B}/fang/seds_basis_level_check.csv"
F8R = "results/2026-11-07/fang/fang8_results.csv"; EX = "results/2026-11-07/extend"; GD = f"{EX}/tables/p2_gap_decomposition.csv"; P2C = f"{EX}/p2_checks.csv"; DM = f"{EX}/s4_drivers_models.csv"; PF = f"{EX}/s4_path_fit.csv"; RL = f"{EX}/p2b_relevance_index.csv"; RK = f"{EX}/p2b_permutation_ranks.csv"; BT = f"{EX}/s2_bytype_family.csv"; GI = f"{EX}/s2_georgia_implied.csv"; B3 = f"{EX}/tables/s3_bounds_per_within_sd.csv"; DG = "logs/2026-11-07/ai_index_diagnostics.csv"; CK = "logs/2026-11-07/ai_index_crossstate_checks.csv"; DI = f"{EX}/p2b_distillery_rerun.csv"; A1T = f"{EX}/e1_descriptives_vs_tableA1.csv"
t2 = lambda b_, c_, m_="aipostings": dict(block="t2", spec=f"c{c_}-{b_}", ai_measure=m_, term="AI"); dmf = lambda mod: dict(outcome="renew_share", ai_measure="ai518210", model=mod, term="AI"); pc2 = lambda blk, spec, m_, y, term="AI": dict(block=blk, spec=spec, ai_measure=m_, outcome=y, term=term)
VC = f"{P}/validation_counts.csv"; H1 = "results/2026-11-02/h1"; C = f"{H1}/h1_core.csv"; X = f"{H1}/h1_extras.csv"; H2 = "results/2026-11-03/h2/h2_results.csv"; MS = "results/2026-11-03/h3_mainspec/sdm_impacts.csv"; MC = "results/2026-11-03/h3_mainspec/sdm_core.csv"; RU = f"{P}/rule_out.csv"; MED = f"{TB}/mediation_summary.csv"; MO = "results/2026-11-03/h3/h3_moran.csv"; GL = "data/georgia_large_load_table2.csv"
for f in (VC, C, X, H2, MS, RB, F, SH, PI, PS, G, BC, RU, MED, MO, GL, WX, NP, LV):
    if not os.path.exists(f): sys.exit(f"missing input: {f}")
L = Ledger(f"ECON499R_Results_{D}.pdf"); W = pd.read_csv(RU)
t = lambda y: f"h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_{y}_50s2015_2025"; xt = lambda s: f"h1x_{s}"
e = lambda path, fmt="{:.4f}", **k: L.n(path, "estimate", fmt, **k); pv = lambda path, **k: L.p(path, **k)
MW = xt("twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025"); PC = xt("rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per1000mw_50s2015_2025")
sdm = lambda eff: dict(outcome="renew_share", W_version="invdist50", estimator="ML", effect=eff)
br = lambda m: dict(block="bridge", spec="s6-noDC", ai_measure=m); r6 = dict(block="rep", spec="c6", ai_measure="aipostings", term="AI", vcov="iid", sample="51s2018_2021")
TA = "h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a"
ci = lambda i, f="{:.2f}": f"{L.n(RU, 'ci_lo_per_sd', f, tag=W.tag[i])} to {L.n(RU, 'ci_hi_per_sd', f, tag=W.tag[i])}"
gl = lambda row, col: L.n(GL, col, "{:,.0f}", row=row)
mor = pd.read_csv(MO); mor = mor[(mor.variable == "renew_share") & (mor.W_version == "invdist50") & (mor.type == "raw")]; ymin, ymax = int(mor.loc[mor.moran_I.idxmin(), "year"]), int(mor.loc[mor.moran_I.idxmax(), "year"])
mi = lambda y: L.n(MO, "moran_I", "{:.3f}", variable="renew_share", W_version="invdist50", type="raw", year=y)
slxb = lambda w, y: f"{L.n(PS, 'estimate', W_version=w, outcome=y, version='d_both', term='theta_lag')}, {L.p(PS, W_version=w, outcome=y, version='d_both', term='theta_lag')}"
gproj = lambda path, lr, yr=2035: L.n(G, "lcoe_2025usd_mwh", "{:.2f}", path=path, learning_rate=lr, year=yr)
SEDSLINK = '<a href="https://www.eia.gov/state/seds/seds-change/index.php">eia.gov/state/seds/seds-change</a>'
vc = lambda sc, ra: L.n(VC, "n", "{:.0f}", scope=sc, rating=ra)
K23 = L.typed("2.3", "our approximation, EXPERIMENTS.md F18"); K29 = L.typed("2.9", "our approximation, EXPERIMENTS.md F18")
wxe = lambda sp_: L.n(WX, "estimate", spec=sp_, coef="ai_dc_per1000_lag1"); wxp = lambda sp_, c_="ai_dc_per1000_lag1": L.p(WX, spec=sp_, coef=c_)
npd = lambda dn: dict(definition=dn, ai_measure="aipostings", group="difference"); nps = lambda dn: L.n(NP, "net_producer_state_years", "{:.0f}", **npd(dn)); lvn = lambda r_: L.n(LV, "mean_lnET", "{:.2f}", row=r_)

# ---- tables: read verbatim; NaN prints as a dash ----
TN = [0]; TSRC = []
def T(name, caption, rows=None, cols=None, src="", cls="", rename=None, dec2=None):
    d = pd.read_csv(f"{TB}/{name}.csv", dtype=str)  # text, so cells print exactly as in the file
    if rows is not None: d = d.iloc[rows] if isinstance(rows, list) else d[rows(d)]
    if cols is not None: d = d[cols]
    for c in (dec2 or []): d[c] = d[c].astype(float).map("{:.2f}".format)  # the file drops trailing zeros (50.4 for 50.40)
    if rename: d = d.rename(columns=rename)
    TN[0] += 1; n = TN[0]; TSRC.append((f"Table {n}", f"{TB}/{name}.csv", src))
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in d.columns)
    body = ""
    for rec in d.itertuples(index=False):
        body += "<tr>" + "".join(f"<td>{'–' if pd.isna(v) else html.escape(str(v))}</td>" for v in rec) + "</tr>"
    return f'<figure class="tbl {cls}"><figcaption><b>Table {n}.</b> {caption}</figcaption><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></figure>'
def spill():  # the two renew_share rows of the spillover timing table, turned on their side
    d = pd.read_csv(f"{TB}/table5c_spillover_placebo.csv", dtype=str); d = d[d.Outcome == "renew_share"].set_index("W").drop(columns="Outcome").T
    TN[0] += 1; n = TN[0]; TSRC.append((f"Table {n}", f"{TB}/table5c_spillover_placebo.csv", "results/2026-11-04/h3_placebo/placebo_slx.csv; placebo_sdm_core.csv; placebo_sdm_impacts.csv"))
    body = "".join(f"<tr><td>{html.escape(i)}</td><td>{html.escape(str(r['Inverse distance']))}</td><td>{html.escape(str(r['Border']))}</td></tr>" for i, r in d.iterrows())
    return f'<figure class="tbl"><figcaption><b>Table {n}.</b> Timing test for the renew_share spillover, 2015-2023 (N = {L.n(PI, "N", "{:.0f}", W_version="invdist50", outcome="renew_share", version="a_lag", effect="indirect")} inverse distance; border weights use 48 states). SLX: coefficient (clustered SE). SDM: indirect estimate [95% CI].</figcaption><table><thead><tr><th>Model and term</th><th>Inverse distance</th><th>Border</th></tr></thead><tbody>{body}</tbody></table></figure>'
caps = dict(re.findall(r"\*\*`([^`]+)`\.\*\* (.+)", open(f"{FG}/CAPTIONS.md").read()))
FN = [0]
def FIG(names, cls=""):
    out = ""
    for nm in names:
        FN[0] += 1; b = base64.b64encode(open(f"{FG}/{nm}", "rb").read()).decode()
        out += f'<figure class="fig"><img alt="{html.escape(caps[nm])}" src="data:image/png;base64,{b}"><figcaption><b>Figure {FN[0]}.</b> {html.escape(caps[nm])}</figcaption></figure>'
    return f'<div class="figs {cls}">{out}</div>'

prose = {}
prose["summary"] = f"""
<h1>AI and Renewable Energy across U.S. States, 2015-2025</h1>
<p class="by">Results report, as of {D}. ECON 499R, Emory University. Shunji Lewandowski and Alexander Hendricks. Advisor: Prof. Fohlin.</p>
<h2 class="first">Summary</h2>
<p class="lead">We tested two papers on the same state panel. <b>Once timing is taken into account, data-center job growth isn't associated with electricity use, efficiency or the renewable share across states.</b> Neither Zhang et al.'s (2026) "blessing or peril" channels nor Fang et al.'s (2025) positive association holds up in our design. All results are associations.</p>
<table class="verdict"><thead><tr><th>Test</th><th>Main number</th><th>Holds up?</th></tr></thead><tbody>
<tr><td>H1: electricity use, efficiency</td><td>{e(C, tag=t("ln_ec"))} ({pv(C, tag=t("ln_ec"))}); {e(C, tag=t("ln_ee"))} ({pv(C, tag=t("ln_ee"))})</td><td>No association under clustered SEs</td></tr>
<tr><td>H1: renewable share</td><td>{e(C, tag=t("renew_share"))} ({pv(C, tag=t("renew_share"))})</td><td>No. Next year's AI carries it: lead {e(RB, spec="placebo-joint", outcome="renew_share", coef="ai_lead1_w")} ({pv(RB, spec="placebo-joint", outcome="renew_share", coef="ai_lead1_w")}), lag {e(RB, spec="placebo-joint", outcome="renew_share", coef="ai_dc_per1000_lag1")} ({pv(RB, spec="placebo-joint", outcome="renew_share", coef="ai_dc_per1000_lag1")})</td></tr>
<tr><td>H1: new renewable capacity</td><td>{e(X, "{:.1f}", tag=MW)} MW ({pv(X, tag=MW)})</td><td>No. {e(X, "{:.2f}", tag=PC)} ({pv(X, tag=PC)}) per 1,000 MW of 2015 capacity; its lead is positive too</td></tr>
<tr><td>H2: mediation</td><td>Tech-share first stage {L.n(H2, "estimate", "{:.6f}", tag=TA)} ({L.p(H2, tag=TA)})</td><td>No channel. Sobel p from {L.n(MED, "min_p", "{:.3f}", tag="h2_sobel_summary")} to {L.n(MED, "max_p", "{:.3f}", tag="h2_sobel_summary")}</td></tr>
<tr><td>H3: spillovers</td><td>{L.n(MS, "plugin", "{:.3f}", **sdm("indirect"))} ({L.p(MS, "p", **sdm("indirect"))}), full sample</td><td>Not supported: can't be separated from reverse timing</td></tr>
<tr><td>Fang replication</td><td>{L.typed("0.0531", "Fang et al. 2025, Table 2, col. 6")} published; {e(F, **r6)} ({pv(F, **r6)}) on current SEDS; {L.n(F8R, "estimate", **t2("archived", 6))} ({L.p(F8R, **t2("archived", 6))}) on SEDS as published in June 2023</td><td>Largely reproduces on the June 2023 release (same sign; about two-thirds of Fang's size in col. 6), not on current SEDS ({SEDSLINK}); gone with a linear trend</td></tr>
<tr><td>Fang, our design</td><td>Postings {e(F, **br("aipostings"))} ({pv(F, **br("aipostings"))}); data-center jobs {e(F, **br("dcjobs"))} ({pv(F, **br("dcjobs"))})</td><td>Neither significant. Data-center jobs are the more reliable measure</td></tr>
<tr><td>Extensions: by type, other outcomes, index</td><td>One by-type row with q &lt; 0.10 (postings, wind generation, {L.n(BT, "estimate", outcome="ln_gen_wind", ai_measure="aipostp1000")}); no row among 30 other outcomes or the index</td><td>No. The wind row is exploratory: wrong sign, fails with state trends and with jobs</td></tr>
<tr><td>National trend</td><td>AI on renewable share: {L.n(DM, "estimate", "{:.3f}", **dmf("statefe"))} / {L.n(DM, "estimate", "{:.3f}", **dmf("drivers"))} / {L.n(DM, "estimate", "{:.3f}", **dmf("twfe"))} (state FE / drivers / two-way)</td><td>The national rise isn't AI; measured drivers track it (consistent with, not proof)</td></tr>
<tr><td>Shift-share IV</td><td>KP F = {e(SH, "{:.2f}", spec="base2015", outcome="first_stage", term="KP_F")}</td><td>Uninformative: F is below 10</td></tr>
<tr><td>Georgia solar, 2035</td><td>${gproj("Central", .24)}/MWh; range ${gproj("High", .45)} to ${gproj("Low", .12)}</td><td>Arithmetic on cited IEA paths, not a forecast of ours</td></tr>
</tbody></table>
<h3>What we can rule out</h3>
<p>Per one within-state SD of AI ({L.n(RU, "sd_ai", tag=W.tag[0])}: winsorized lagged AI after removing state and year effects), the 95% CIs are {ci(0)} percent for electricity use per person, {ci(1)} percent for GDP per MWh, and {ci(2)} percentage points for the renewable share.</p>
<h3>Why the timing test matters</h3>
<p>A standard panel shows a negative association between data-center jobs and the renewable share, and a positive one with new capacity. But next year's AI predicts this year's outcome as well or better. Apart from anticipation, jobs that don't exist yet can't explain what's happening today, so these associations are likely about where and when data-center jobs grow.</p>
<h3>What this doesn't cover</h3>
<p>Jobs aren't MW, and our sample ends in 2025. Georgia Power reports {gl("Commitments", "q2_2026_mid2030s")} MW of large-load commitments through the mid-2030s as of June 2026, up from {gl("Commitments", "ifiling_mid2030s")} MW at its October 2023 filing (Q2 2026 Large Load Economic Development Report, filed Aug. 17, 2026, in Georgia PSC Docket 55378, page headers Docket 56002, p. 4 [PDF p. 8]). That's the utility's own reporting, and most of that load is scheduled after our sample ends. Our results describe the past, not that build-out.</p>
"""
prose["data"] = f"""
<h2>1. The question and the data</h2>
<p>Is growth in AI-related activity associated with more or less electricity use, energy efficiency and renewable energy? Zhang et al. (2026) argue AI works through tech jobs and density and spills across borders. Fang, Lee and Li (2025) find that AI job postings go with more renewable consumption across states in 2018-2021. We test both, then look at Georgia, a large data-center market with a regulated utility.</p>
<p><b>Panel:</b> 50 states and DC, 2015-2025, 561 rows. All sources are public: EIA (generation, capacity, sales, SEDS), BLS QCEW (jobs), BEA (GDP, population), Census (land, borders). The Zhang models use the 50 states (N = {L.n(C, "N", "{:.0f}", tag=t("ln_ec"))}). The workbook's Validation tab has {vc("all", "total")} checks: {vc("all", "green")} green, {vc("all", "yellow")} yellow, {vc("all", "red")} red and {vc("all", "not run")} not run. The red is the team's NSF file with no state rows, which isn't used. The {vc("model_variables", "total")} model variables rate {vc("model_variables", "green")} green, {vc("model_variables", "yellow")} yellow and {vc("model_variables", "red")} red. Cross-source checks are green, except one reported gap: no net-producer rule reaches Fang's count. The master workbook has every check, source and limitation.</p>
<p><b>Two AI measures:</b> <i>private data-center jobs per 1,000 workers</i> (NAICS 518210), one consistent series, but a proxy for data-center activity rather than AI use; and <i>AI job postings</i> (Stanford AI Index), Fang's measure, where almost every year comes from a different report edition. <b>Data-center jobs are the more reliable measure when we extend the sample.</b></p>
"""
prose["methods"] = f"""
<h2>2. Methods, in plain English</h2>
<div class="eq"><b>H1, two-way fixed effects.</b> <code>Y<sub>st</sub> = &alpha;<sub>s</sub> + &gamma;<sub>t</sub> + &beta; AI<sub>s,t-1</sub> + controls + e<sub>st</sub></code><br>Compares each state with itself over time, after removing anything that hit all states in a year. &beta; says how much the outcome differs when a state has more data-center jobs the year before. Controls: log GDP per person, manufacturing share, electricity price, population growth. SEs are clustered by state; Driscoll-Kraay is a sensitivity check only, since there are just 11 years. AI and outcomes are winsorized at the 1st and 99th percentiles.</div>
<div class="eq"><b>Timing test.</b> Replace AI<sub>t-1</sub> with AI<sub>t+1</sub>, then put both in one model. Apart from anticipation, future jobs can't produce today's outcome, so if the lead carries the association, it reflects where and when jobs grow (reverse timing or selection).</div>
<div class="eq"><b>H2, mediation.</b> <code>M = a AI + &hellip;</code> and <code>Y = b M + c AI + &hellip;</code>, indirect path = a &times; b. Does AI go with the mediator, and does the mediator go with the outcome? Mediators: tech-job share (main), HMA (the memo's version, positive by construction) and economic density. Sobel tests and a cluster bootstrap.</div>
<div class="eq"><b>H3, spatial Durbin.</b> <code>Y<sub>st</sub> = &rho; W Y<sub>st</sub> + &beta; AI<sub>s,t-1</sub> + &theta; W AI<sub>s,t-1</sub> + controls + FE + e<sub>st</sub></code><br>W averages over neighbors, weighted by inverse distance (main) or shared border (check). Because outcomes feed back through &rho;, we report direct (own state), indirect (neighbors, the spillover) and total. Plug-in estimates with simulated CIs.</div>
<div class="eq"><b>Fang test.</b> <code>ln RE<sub>st</sub> = &alpha;<sub>s</sub> + &beta; ln AI<sub>st</sub> + &phi; (ln AI<sub>st</sub> &times; EPU<sub>st</sub>) + controls + e<sub>st</sub></code><br>RE is SEDS renewable consumption. State effects only and conventional SEs, as in Fang. The bridge changes one thing at a time: year effects, lag, clustering, longer sample, no DC. That shows which step changes the answer.</div>
<div class="eq"><b>Shift-share IV.</b> Instrument = a state's 2015 share of national data-center jobs &times; national jobs outside that state. It's useful only if it predicts AI: a KP F below 10 means uninformative.</div>
<div class="eq"><b>Georgia learning curve.</b> <code>C<sub>t</sub> = C<sub>base</sub> (X<sub>t</sub> / X<sub>base</sub>)<sup>b</sup>, b = ln(1 - LR) / ln 2</code><br>Cost falls by the learning rate LR each time global capacity X doubles. X follows IEA's scenario paths. It's arithmetic: it has no AI variable, and learning curves are correlations.</div>
"""
prose["r_h1"] = f"""
<h2>3. Results: the Zhang test</h2>
<p><b>H1.</b> Electricity use and efficiency show no association under clustered SEs. The renewable share is negative but not significant ({pv(C, tag=t("renew_share"))}; {pv(RB, spec="dk", outcome="renew_share", coef="ai_dc_per1000_lag1")} under Driscoll-Kraay, sensitivity only). New capacity is positive in raw MW, driven by large-grid states, and not robust to scaling. No AI-squared curve passes the Lind-Mehlum test.</p>
"""
prose["r_h2"] = f"""<p><b>H2.</b> No channel is supported. AI isn't associated with the tech-job share or density, and HMA's first stage is positive by construction. All bootstrap CIs include zero.</p>"""
prose["r_h3"] = f"""
<p><b>H3.</b> Renewable share is clustered across states (Moran's I from {mi(ymin)} to {mi(ymax)}). On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate ({L.n(MS, "plugin", "{:.3f}", **sdm("indirect"))}, {L.p(MS, "p", **sdm("indirect"))}) can't be separated from this reverse timing. H3 is not supported. On inverse-distance weights, the test can't tell lag from lead: both CIs are wide. For ln_ec and ln_ee, the main-spec spillover CIs include zero. <b>Exploratory note:</b> with lead and lag in one model, the SLX shows neighbors' past AI as significant for ln_ec ({slxb("invdist50", "ln_ec")} inverse distance; {slxb("border48", "ln_ec")} border) and for border-weights ln_ee ({slxb("border48", "ln_ee")}). The SDM doesn't confirm it: those indirect CIs include zero. With this many tests, a few p &lt; 0.05 are expected by chance, so we don't read these as spillovers.</p>
"""
prose["r_rob"] = f"""
<p><b>Robustness and placebo.</b> The RPS control (the LBNL current RPS/CES schedule), all-ownership AI and holding Gavins Point in Nebraska change no result. For renew_share, next year's AI is {e(RB, spec="placebo", outcome="renew_share", coef="ai_lead1_w")} ({pv(RB, spec="placebo", outcome="renew_share", coef="ai_lead1_w")}); in one model, the lead is {e(RB, spec="placebo-joint", outcome="renew_share", coef="ai_lead1_w")} ({pv(RB, spec="placebo-joint", outcome="renew_share", coef="ai_lead1_w")}) and the lag {e(RB, spec="placebo-joint", outcome="renew_share", coef="ai_dc_per1000_lag1")} ({pv(RB, spec="placebo-joint", outcome="renew_share", coef="ai_dc_per1000_lag1")}). For new_renew_mw, the lead is {e(RB, "{:.1f}", spec="placebo", outcome="new_renew_mw", coef="ai_lead1_w")} ({pv(RB, spec="placebo", outcome="new_renew_mw", coef="ai_lead1_w")}); in one model, {e(RB, "{:.1f}", spec="placebo-joint", outcome="new_renew_mw", coef="ai_lead1_w")} ({pv(RB, spec="placebo-joint", outcome="new_renew_mw", coef="ai_lead1_w")}) and {e(RB, "{:.1f}", spec="placebo-joint", outcome="new_renew_mw", coef="ai_dc_per1000_lag1")} ({pv(RB, spec="placebo-joint", outcome="new_renew_mw", coef="ai_dc_per1000_lag1")}): neither significant.</p>
<p><b>Weather check.</b> With NOAA heating and cooling degree days on the 48 contiguous states, the ln_ec coefficient is {wxe("weather-hddcdd")} ({wxp("weather-hddcdd")}), against {wxe("weather-base48")} ({wxp("weather-base48")}) on the same states without them. Both degree-day terms are significant ({wxp("weather-hddcdd", "hdd_k")}), but the AI coefficient doesn't change.</p>
"""
prose["r_fang"] = f"""
<h2>4. Results: the Fang test</h2>
<p><b>Replication.</b> Fang's positive coefficient doesn't reproduce on current SEDS. In October 2023, starting with the 2022 data cycle and for all years, EIA moved wind, solar, hydro and geothermal from fossil fuel equivalency to captured energy at {L.typed("3,412", "EIA SEDS change notice")} Btu/kWh (EIA notice: {SEDSLINK}). <b>SEDS as published in June 2023, the archived release and our main old-basis series, largely reproduces Fang:</b> the same sign, a similar size in columns 1-2 ({L.n(F8R, "estimate", **t2("archived", 1))} and {L.n(F8R, "estimate", **t2("archived", 2))}), and about two-thirds of Fang's size in column 6 ({L.n(F8R, "estimate", **t2("archived", 6))}, {L.p(F8R, **t2("archived", 6))}). Our year-by-year rebuild of the old accounting on today's data gives {L.n(F8R, "estimate", **t2("rebuilt", 6))} ({L.p(F8R, **t2("rebuilt", 6))}): {L.n(GD, "share_accounting_rebuild", "{:.0%}", ai_measure="ln AI postings", column=6)} of the column-6 gap comes from the accounting change and the rest from EIA's later data revisions. k = {K23}-{K29}, our first approximation, is kept as a check. Fang's paper says EIA's renewable data ended in 2021 (PDF p. 3), and its Table 2 constants imply a mean log outcome of {lvn("Fang Table 2 col. 1: constant + 0.0428 x mean ln(AI)")}, which is consistent with the old basis ({lvn("Approximate old basis, k = 2.3")}-{lvn("Approximate old basis, k = 2.9")}), not the current one ({lvn("Current SEDS (captured energy)")}), assuming the usual fixed-effects constant. But Fang's spec has no year effects: on the June 2023 basis a linear trend turns column 6 to {L.n(P2C, "estimate", **pc2("p1trend", "fang6trend", "aipostings", "lnET_arch"))} ({L.p(P2C, **pc2("p1trend", "fang6trend", "aipostings", "lnET_arch"))}), and pet-care employment is associated with renewables more strongly than AI ({L.n(P2C, "estimate", **pc2("p1placebo", "fang6", "petcare", "lnET_arch"))}, {L.p(P2C, **pc2("p1placebo", "fang6", "petcare", "lnET_arch"))}).</p>
<p><b>Fang's supplement.</b> Against Fang's Table A1, our ln AI postings, EP, POP and EDU match, GDP differs by the 2012-vs-2017 dollar base, and ln EPU is {L.n(A1T, "diff", "{:.3f}", scale=-1, variable="lnEPU")} lower, close to ln 2 (consistent with a doubled index, which state FE in logs absorb). Supplement B1's coal and gas coefficients fall inside our CIs; petroleum doesn't.</p>
<p><b>Splits, negative indicator, weather, event study.</b> On current SEDS none of Fang's subgroup splits reproduces. On the June 2023 basis (added after seeing Table 2, so exploratory), low-consumption, low-R&amp;D, high-income and Midwest states match Fang's side, but <b>Fang's headline splits, electricity price and net producer, don't reproduce</b>, nor does the extreme-weather split (NOAA Storm Events, our counting rule). Fossil-fuel consumption is never negative and significant. In the event study on 2019 postings exposure, the pre-2021 coefficients are jointly significant on current SEDS ({L.p(F8R, block="es", spec="current", term="joint_pre_2015_2020")}), so the post-2021 gap looks like a trend already under way.</p>
"""
prose["r_bridge"] = f"""
<p><b>Bridge.</b> Neither measure is significant in the final spec. <b>Data-center jobs are the more reliable measure:</b> the postings extension mixes real change with edition changes. The share-of-national column isn't an independent test: with year effects, it equals the postings column by construction.</p>
"""
prose["r_mod"] = f"""
<p><b>EPU moderation, by type and placebo.</b> AI &times; EPU is positive in Fang's spec, and not significant under two-way FE, for either measure. By type, Fang's spec shows solar positive and biomass negative with postings, partly like Fang's pattern. Under two-way FE only biomass with postings stands out. The placebo isn't informative here: AI(t-1) isn't significant either.</p>
<p><b>Net-producer split (exploratory).</b> Fang's rule is electricity production above consumption from EIA, series not stated (PDF p. 4), with 76 net-producer state-years (Table 3). Our rule, generation above retail sales on each state's 2018-2021 average, gives {nps("gen_gt_sales")}. SEDS total energy production above consumption gives {nps("teprb_gt_tetcb")}, closer by count but not Fang's concept; SEDS net interstate electricity flow below zero gives {nps("elisb_negative")}. None reaches 76. In Fang's spec with postings, the producer-minus-consumer gap is {e(F, block="inter", spec="fang-net_producer", ai_measure="aipostings", term="difference_high_minus_low")} ({pv(F, block="inter", spec="fang-net_producer", ai_measure="aipostings", term="difference_high_minus_low")}) on our rule, and isn't significant on the other two ({pv(NP, **npd("teprb_gt_tetcb"))}; {pv(NP, **npd("elisb_negative"))}).</p>
"""
prose["r_ext"] = f"""
<h2>5. Results: extensions (Nov 7)</h2>
<p>Every model was pre-registered in <code>EXPERIMENTS.md</code> section 14 before it ran; deviations X1-X5 and F27 are logged there. Main spec: two-way FE, AI(t-1), ctrl4, clustered by state, winsorized; both data-center jobs and postings per 1,000 workers. A finding needs BH q &lt; 0.10 within its family and a clearly smaller lead.</p>
<p><b>Which renewable?</b> One by-type row passes: postings and ln wind generation ({L.n(BT, "estimate", outcome="ln_gen_wind", ai_measure="aipostp1000")}, q = {L.n(BT, "qval", "{:.3f}", outcome="ln_gen_wind", ai_measure="aipostp1000")}). It is exploratory: it runs against the expected sign, loses significance with state trends ({L.p(P2C, block="p2bytype", spec="twfe-trend", ai_measure="aipostp1000", outcome="ln_gen_wind", term="AI")}), and the jobs version fails the lead test. Biofuels are null, so the negative SEDS total isn't transport fuel. <b>Georgia:</b> its solar share rose {L.n(GI, "actual_change", "{:.3f}", outcome="share_solar", ai_measure="ai518210")} in 2015-2025; the AI association could account for at most {L.n(GI, "at_most_share_of_actual", "{:.0%}", outcome="share_solar", ai_measure="ai518210")} with jobs. Georgia Power's 2025 IRP (Docket 56002) plans for about {L.typed("8,200", "2025 IRP, p. 1 [PDF p. 8]")} MW of load growth through winter 2030/2031, with RFPs for up to {L.typed("9,500", "2025 IRP, p. 3 [PDF p. 10]")} MW of capacity that the IRP doesn't split by fuel, {L.typed("1,323", "2025 IRP, p. 126 [PDF p. 133]")} MW of new combustion turbines, about 780 MW of batteries (p. 128 [PDF p. 135]) and coal extensions.</p>
<p><b>What AI is associated with.</b> None of 30 rows (sales by sector, prices, generation mix, additions, imports, CO2) has q &lt; 0.10. Per one within-state SD of data-center jobs, commercial sales per person move between {L.n(B3, "per_sd_lo", "{:.1%}", outcome_label="ln commercial sales per person", ai_measure="ai518210")} and {L.n(B3, "per_sd_hi", "{:.1%}", outcome_label="ln commercial sales per person", ai_measure="ai518210")}.</p>
<p><b>The national trend.</b> The renewable-share coefficient barely moves across state FE only ({L.n(DM, "estimate", "{:.3f}", **dmf("statefe"))}), measured drivers ({L.n(DM, "estimate", "{:.3f}", **dmf("drivers"))}) and two-way FE ({L.n(DM, "estimate", "{:.3f}", **dmf("twfe"))}). Drivers (RPS targets; solar and wind LCOE from LBNL; the ITC and PTC from CRS IF10479 and R43453 and P.L. 116-260 and 117-169; Henry Hub) give a path that correlates with the year effects at {L.n(PF, "correlation", "{:.2f}", outcome="renew_share")}, consistent with their role but not proof, since any rising series tracks a national trend.</p>
<p><b>Relevance and a broader measure.</b> Pooled, data-center jobs don't predict commercial sales per person ({L.p(RL, sample="all50", ai_measure="ai518210", version="pooled")}); Virginia's per-state slope ranks {L.n(RK, "rank_desc", "{:.0f}", sample="all50", ai_measure="ai518210", state="VA")} of 50 and Texas {L.n(RK, "rank_desc", "{:.0f}", sample="all50", ai_measure="ai518210", state="TX")}. An "infrastructure + talent" index (2018-2023, 43 states; alpha {L.n(DG, "value", "{:.2f}", statistic="Cronbach alpha, 5 components")}; correlation with BTOS AI use {L.n(CK, "pearson_index_a_2024", "{:.2f}", check="BTOS 2024 average share of firms using AI")}) doesn't predict commercial sales either ({L.p(RL, sample="all50", ai_measure="indexA", version="pooled")}), and no index row has q &lt; 0.10, on all 50 states or without CA, CO and DE. Groupings by AI investment and a land moderator find nothing that survives BH, except an Alaska-driven land result we read as fragile. The distillery placebo stays significant with state trends ({L.p(DI, spec="our main spec", trend=True, states="never_suppressed_states")}), so state-specific trends remain a live problem. <b>Not run:</b> the Queued Up outcome (no scripted download), the innovation dimension (no inventor locations).</p>
"""
prose["r_stretch"] = f"""
<h2>6. Results: stretch goals and Georgia</h2>
<p><b>Shift-share IV.</b> The first stage is too weak (KP F = {e(SH, "{:.2f}", spec="base2015", outcome="first_stage", term="KP_F")}), so the IV is uninformative and can't settle the timing question. KP rank LM is computed directly, because the package's version errors with clustering. <b>Moderators.</b> No broadband or R&amp;D interaction is significant. The Hansen threshold wasn't run: the team dropped it.</p>
"""
prose["r_ga"] = f"""
<p><b>Georgia solar.</b> The base is Georgia's capacity-weighted LCOE without tax credits, ${L.n(BC, "lcoe_capacity_weighted", "{:.2f}", area="Georgia")}/MWh, for {L.n(BC, "n_projects", "{:.0f}", area="Georgia")} projects in service in 2023-2025 (LBNL). Capacity paths use IEA's <i>World Energy Outlook 2025</i>, Annex A, solar PV capacity: Low is Current Policies (Table A.3a, p. 417), Central is Stated Policies (Table A.3b, p. 423), High is Net Zero Emissions by 2050 (Table A.3c, p. 429). <b>These aren't forecasts of ours.</b> National LCOE rose from ${L.n(LR, "lcoe", "{:.1f}", year=2022)} in 2022 to ${L.n(LR, "lcoe", "{:.1f}", year=2025)} in 2025 while global capacity more than doubled, so the curve assumes costs resume falling. Georgia Power's 2025 IRP plans RFPs for up to {L.typed("4,000", "Georgia Power 2025 IRP, Main Document, p. 60 [PDF p. 67]")} MW of renewable resources by 2035, which is the utility's own plan.</p>
"""
prose["rule"] = f"""
<h2>8. What we can rule out</h2>
<p>95% CI per one within-state SD of AI. <b>The SD used is {L.n(RU, "sd_ai", tag=W.tag[0])}: winsorized lagged AI after removing both state and year effects, 50 states, N = {L.n(C, "N", "{:.0f}", tag=t("ln_ee"))}.</b> That's the variation the Zhang models use. The Fang rows use the SD of each log AI measure the same way. A typical swing in data-center jobs isn't associated with a fall in the renewable share of more than {L.n(RU, "ci_lo_per_sd", "{:.2f}", scale=-1, tag=W.tag[2])} points. The capacity row's range excludes zero, but that result isn't robust to scaling and fails the timing test. These limits apply to job swings seen in this period, not to a much larger future build-out.</p>
"""
prose["limits"] = f"""
<h2>9. Limitations</h2>
<ul class="tight">
<li><b>The AI measure.</b> Private NAICS 518210 jobs are a proxy for data-center activity, not AI use, and include general data processing and hosting. Jobs aren't MW. Georgia ranks above Virginia, likely from colocation and cloud hosting. BLS suppressed AK, ND, SD and WY in 2025.</li>
<li><b>Postings.</b> Postings aren't jobs. The vendor and counting changed across editions, and only 2019-2021 come from one edition.</li>
<li><b>Generation.</b> Utility-scale only, so no rooftop solar. Capacity is nameplate, and new capacity is a net change.</li>
<li><b>SEDS.</b> Ends in 2024. Renewable consumption includes non-electric uses, and EIA's 2023 accounting change ({SEDSLINK}) affects the Fang outcome.</li>
<li><b>RPS.</b> LBNL's current schedule, not the targets in force; LBNL revised past years.</li>
<li><b>Inference.</b> Little within-state AI variation over 11 years. Residual spatial dependence after two-way FE means clustered SEs may be too small. There's no strong instrument, so nothing here supports a causal reading.</li>
<li><b>Georgia.</b> Filings are the utility's own numbers, with project names redacted. The Q1-Q4 2024 large-load reports are pending: the PSC's list returns 404 to scripts. Georgia's regulated setting may not generalize.</li>
<li><b>Weather.</b> NOAA degree days cover the 48 contiguous states and enter one check only. Fang's extreme-weather split uses our count of NOAA Storm Events heat and cold records, since Fang's rule isn't stated.</li>
<li><b>Extensions.</b> No innovation dimension in the AI index; talent rests on two components; AI investment by state covers one year; NREL resource data weren't reachable, so capacity factors stand in.</li>
</ul>
<h2>10. What's next</h2>
<ul class="tight">
<li><b>Team review.</b> Read the readings and flags, by the Nov 17 core-results date.</li>
<li><b>By hand:</b> the Q1-Q4 2024 large-load reports (PSC Docket 55378), LBNL Queued Up (for the queue outcome), then rerun the affected steps.</li>
<li><b>Draft by Nov 24.</b> Start from <code>docs/{D}/methods_section.tex</code>, which hasn't been compiled here, and <code>results/{D}/paper/findings.md</code>. Turn-in is Dec 1.</li>
<li><b>GitHub.</b> Review <code>release/github/CHECKLIST.md</code> before pushing the clean copy. Don't push the working repo.</li>
</ul>
"""
for k in list(prose): prose[k] = prose[k].strip()

# ---- layout ----
nostar = "* p&lt;0.1, ** p&lt;0.05, *** p&lt;0.01. "
body = prose["summary"] + '<div class="brk"></div>'
body += prose["data"] + T("table1_descriptives", "Main variables, before winsorizing. 50 states.", rows=[0, 1, 2, 3, 4, 10, 11, 12, 13], cols=["Variable", "Mean", "SD", "Min", "Max", "N", "Source"], src="data/out/state_panel_2015_2025.csv")
body += prose["methods"]
body += prose["r_h1"] + FIG(["fig_h1_coefficients.png"]) + T("table2_h1", f"H1: AI(t-1), two-way FE, four controls, clustered by state. Coefficient (SE). {nostar}", rows=[0, 1, 2, 8, 9, 10], src=f"{C}; {X}")
body += prose["r_h2"] + T("table4_mediation", "H2: mediation. Coefficient (SE), Sobel p and bootstrap CI.", src=H2, rename={"AI_to_M": "AI to mediator", "M_to_Y": "Mediator to outcome", "Sobel_p": "Sobel p", "Bootstrap_95_CI": "Bootstrap 95% CI"})
body += prose["r_h3"] + T("table5b_sdm", "H3: spatial Durbin, full sample. Estimate [95% CI].", src="results/2026-11-03/h3_mainspec/sdm_core.csv; sdm_impacts.csv") + spill()
body += prose["r_rob"] + T("table6_robustness", f"Robustness: AI coefficient (SE) by specification. {nostar}Last row: the placebo.", rows=[0, 1, 2, 3, 6, 8, 9, 11, 14, 15, 16, 17, 18, 20], src=RB, cls="small", rename={"new_renew_per_1000mw": "per 1,000 MW"})
body += prose["r_fang"] + T("table7_fang_replication", f"Fang's Table 2 and our replication: AI coefficient (SE), state FE, conventional SEs. k is our approximation of the old SEDS accounting. {nostar}", src=F, cls="small")
body += prose["r_bridge"] + T("table8_fang_bridge", f"Bridge from Fang's spec to ours, one change at a time. Coefficient (SE) [N]. {nostar}", src=F, cls="small")
body += prose["r_mod"] + T("table9_fang_moderation", f"AI &times; EPU (centered), with the AI slope at the 25th and 75th percentiles of EPU. {nostar}", src=F, cls="small") + T("table10_fang_by_type", f"By renewable type: coefficient (SE) [N]. {nostar}", src=F, cls="small") + T("table13_fang_placebo", "Fang placebo, final spec: coefficient (SE).", src=F, cls="small")
body += prose["r_ext"] + T("table22_fang_table2_by_basis", "Fang Table 2 AI and control coefficients by SEDS basis, Fang spec. June 2023 is the main old basis; k = 2.6 is a check.", rows=lambda d: d.term == "AI", cols=["ai_measure", "column", "fang", "current", "k26", "rebuilt", "archived", "archived_fang_in_ci"], src=F8R, cls="small") + T("table23_gap_decomposition", "Gap from current to June 2023 SEDS: accounting change vs later data revisions.", cols=["ai_measure", "column", "current", "rebuilt", "june2023", "share_accounting_rebuild", "share_later_data_revisions", "june2023_as_share_of_fang"], src=F8R, cls="small") + FIG(["fig_fang_table2_by_basis.png", "fig_fang_event_study.png"], "two")
body += T("table33_ext_drivers_ai", "AI coefficient: state FE only, full measured-drivers model, two-way FE.", src=DM, cls="small") + T("table36_ext_slope_ranks", "Ranks of VA, TX and GA among per-state slopes of commercial sales on AI(t-1) (1 = largest).", cols=["sample", "ai_measure", "state", "slope", "rank_desc", "rank_of"], src=RK, cls="small") + T("table39_ext_index_family_summary", "AI index family: rows, smallest q and rows with q below 0.10, by sample and index.", src=f"{EX}/p2b_index_family.csv", cls="small") + FIG(["fig_ext_drivers.png"], "stack")
body += prose["r_stretch"] + T("table15_iv_first_stage", f"Shift-share IV first stage. {nostar}", src=SH) + T("table16_iv", f"OLS, reduced form and IV, coefficient (SE). {nostar}The IV column is uninformative.", src=SH) + T("table17_moderation", f"Broadband and R&amp;D moderation, each with its main effect. {nostar}", src=SH, cls="small")
body += prose["r_ga"] + T("table18_georgia", "Georgia solar LCOE, 2025 $/MWh, by learning rate and IEA path. Not forecasts of ours. Paths: IEA WEO 2025, Tables A.3a, A.3b and A.3c.", src=G, dec2=["2025", "2030", "2035"], rename={"lr_label": "Learning rate", "path": "IEA path", "change_2025_2035_pct": "Change 2025-2035, %"})
body += '<h2>7. Key figures</h2>' + FIG(["fig_georgia_trends.png", "fig_map_ai_2025.png"], "two") + FIG(["fig_spec_curve.png", "fig_spillover_placebo.png", "fig_fang_bridge.png", "fig_moderation.png", "fig_georgia_fan.png"], "stack")
body += prose["rule"] + T("table19_rule_out", "Per one within-state SD of AI. Estimate and 95% CI.", src=RU)
body += prose["limits"]
# ---- number check on the words only; tables are verbatim copies of result files ----
words = "\n".join(prose.values()) + "\n" + "\n".join(caps.values())
words = re.sub(r"\$(?=\d)", "", words)
ck = L.check(words); ck.to_csv(f"{P}/number_check_report.csv", index=False)
bad = ck[(ck.match == "NO") | (ck.in_document == "no") | (ck.match == "UNLOGGED")]
if len(bad): print(bad.to_string()); sys.exit("number check failed")
txt = re.sub(r"<[^>]+>", " ", words)
CAUS = re.findall(r"\b(causes?|caused|causal effect|leads? to|impacts?|because of AI|effect of AI)\b", txt, re.I); print("causal-word check:", CAUS)
# ---- appendix ----
ap_t = "".join(f"<tr><td>{a}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>" for a, b, c in TSRC)
seen = set(); ap_n = ""
for r in ck.itertuples():
    k = (r.number, r.source_tag, r.column)
    if k in seen: continue
    seen.add(k); ap_n += f"<tr><td>{html.escape(str(r.number))}</td><td>{html.escape(str(r.source_file).replace('results/', ''))}</td><td>{html.escape(str(r.source_tag))}</td><td>{html.escape(str(r.column))}</td></tr>"
body += f"""<div class="brk"></div><div class="appx"><h2>Appendix: where every number comes from</h2>
<p>Built by <code>code/python/04k_results_report.py</code> with no new estimation. Tables are verbatim copies of <code>results/{D}/paper/tables/</code>, built by <code>code/python/04g_results_pack.py</code> from the result files below, and each result row carries a parseable tag. Numbers in the text are read from result files as the report is built, then re-read and checked ({int((ck.match == 'yes').sum())} of {int((ck.match == 'yes').sum())} match; {int(ck.match.str.startswith('published').sum())} published figures are cited with their location). Log: <code>results/{D}/paper/number_check_report.csv</code>.</p>
<h3>A. Tables</h3><table><thead><tr><th>Table</th><th>Table file</th><th>Result files</th></tr></thead><tbody>{ap_t}</tbody></table>
<h3>B. Numbers in the text</h3><table class="tags"><thead><tr><th>Number</th><th>File (under results/ unless shown)</th><th>Result tag or location</th><th>Column</th></tr></thead><tbody>{ap_n}</tbody></table></div>"""
css = """
:root{--ink:#111827;--mute:#4b5563;--line:#d1d5db;--head:#1f3864;--tint:#f3f5f9}
@page{size:letter;margin:.62in .68in .68in;@bottom-center{content:counter(page) " of " counter(pages);font:8pt Arial,Helvetica,sans-serif;color:#4b5563}@bottom-left{content:"ECON 499R results report";font:8pt Arial,Helvetica,sans-serif;color:#4b5563}}
*{box-sizing:border-box}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font:10pt/1.36 Arial,Helvetica,sans-serif;color:var(--ink);background:#fff;margin:0}
h1{font-size:19pt;line-height:1.15;margin:0 0 3pt;color:var(--head)}.by{color:var(--mute);margin:0 0 10pt;font-size:9pt}
h2{font-size:12.5pt;margin:13pt 0 4pt;color:var(--head);border-bottom:1pt solid var(--head);padding-bottom:2pt;break-after:avoid}h2.first{margin-top:4pt}
h3{font-size:10pt;margin:9pt 0 2pt;break-after:avoid}p{margin:0 0 6pt}.lead{font-size:10.6pt;line-height:1.38}
code{font:8.6pt Menlo,Consolas,monospace}.brk{break-after:page}
table{border-collapse:collapse;width:100%;font-size:8pt;line-height:1.22}th{background:var(--head);color:#fff;text-align:left;font-weight:bold;padding:2.5pt 4pt;vertical-align:bottom}td{padding:2.2pt 4pt;border-bottom:.5pt solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:var(--tint)}tr{break-inside:avoid}thead{display:table-header-group}
figure{margin:0}.tbl{margin:4pt 0 9pt;break-inside:avoid}.tbl figcaption,.fig figcaption{font-size:8.2pt;color:var(--ink);margin-bottom:2.5pt;line-height:1.28}.tbl.small table{font-size:8pt}.tbl.small td,.tbl.small th{padding:1.8pt 3pt}
.verdict{margin:6pt 0 8pt;font-size:8.7pt}.verdict td:first-child{font-weight:bold;width:23%}.verdict td:nth-child(2){width:37%}
.eq{margin:0 0 5pt;padding:4pt 7pt;border-left:2.5pt solid var(--head);background:var(--tint);font-size:9pt;line-height:1.3;break-inside:avoid}
.figs{margin:3pt 0 6pt}.fig{break-inside:avoid;margin-bottom:7pt}.fig img{width:100%;display:block}.figs.stack .fig img{width:80%;margin:0 auto}.fig figcaption{margin:2pt 0 0}.figs.two{display:grid;grid-template-columns:1fr 1fr;gap:10pt}
ul.tight{margin:0 0 6pt;padding-left:13pt}ul.tight li{margin-bottom:2.5pt}
.appx{font-size:8pt}.appx p{margin-bottom:4pt}.appx table{font-size:8pt;line-height:1.15}.appx td,.appx th{padding:.8pt 2.5pt;word-break:break-word}.appx code{font-size:8pt}.tags td:nth-child(1){width:6%;white-space:nowrap}.tags td:nth-child(2){width:24%}.tags td:nth-child(4){width:11%;word-break:normal}
"""
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ECON 499R Results Report</title><style>{css}</style></head><body>{body}</body></html>'
HT = f"outputs/ECON499R_Results_{D}.html"; PDF = f"outputs/ECON499R_Results_{D}.pdf"; open(HT, "w").write(doc)
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files", f"--print-to-pdf={os.path.abspath(PDF)}", "file://" + os.path.abspath(HT)], check=True, capture_output=True, timeout=180)
print(ck.match.value_counts().to_dict(), "tables", TN[0], "figures", FN[0], "pdf MB", round(os.path.getsize(PDF) / 1e6, 2))
print(subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout)

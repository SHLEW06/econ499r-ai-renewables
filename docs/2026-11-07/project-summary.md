# Project summary

ECON 499R, Emory University. Shunji Lewandowski (modeling) and Alexander Hendricks (data and finance). Advisor: Prof. Fohlin. As of 2026-11-07. All results are associations; nothing here shows that AI causes a change. Every number traces to a result tag in the appendix.

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
| H1, Zhang | Two-way fixed effects, last year's AI, four controls, SEs clustered by state | 50 states, 2015-2025 | 550 |
| H2, mediation | Same design, Sobel tests and a cluster bootstrap, 9 pairs | Same | 550 |
| H3, spillovers | Spatial Durbin, inverse-distance weights (main), border (check) | Same; timing test 2015-2023 | 550; timing 450 |
| Robustness | Timing placebo, RPS control, all-ownership AI, drop-one-state, others | Same | Varies |
| Fang replication | State FE only, conventional SEs, Fang's controls | 50 states and DC, 2018-2021 | 204 |
| Fang bridge | One change at a time, to our design | Up to 2015-2024, no DC | Postings 300; jobs 500 |
| Stretch | Shift-share IV; broadband and R&D moderation | Varies | 550 |
| Georgia solar | Learning-curve arithmetic on IEA paths | LBNL projects, Georgia | 17 projects |

## The results, and whether each holds up

- **H1, electricity use and efficiency: no association.** Coefficients -0.0016 (p = 0.795) and 0.0022 (p = 0.707). **Holds up** under clustered SEs. Driscoll-Kraay SEs, a sensitivity check only with 11 years, put ln_ee at p = 0.036.
- **H1, renewable share: negative but not significant, and the timing fails.** -0.0101 (p = 0.100; p = 0.001 under Driscoll-Kraay, sensitivity only). Next year's AI predicts this year's share (-0.0197, p = 0.006). With both in one model the lag is about zero (0.0015, p = 0.827). This reflects where and when data-center jobs grow (reverse timing or selection), not AI lowering the share.
- **H1, new renewable capacity: doesn't hold up.** 70.8 MW (p = 0.033) in raw MW, but 1.00 (p = 0.616) per 1,000 MW of 2015 capacity. Its lead is positive too (86.8, p = 0.028), and with both in one model neither is significant.
- **H2, mediation: no channel.** AI isn't associated with the tech-job share (-0.000157, p = 0.454). Sobel p-values run from 0.322 to 0.991, and every bootstrap CI includes zero.
- **H3, spillovers: not supported.** On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate (-0.161, p = 0.035) can't be separated from this reverse timing. H3 is not supported.
- **Robustness: no change.** The RPS control (LBNL current RPS/CES schedule) and all-ownership AI change no result. Holding Gavins Point in Nebraska gives 71.0 MW. With NOAA heating and cooling degree days on the 48 contiguous states, ln_ec is -0.0021 (p = 0.711), against -0.0009 (p = 0.880) on the same states without them.
- **Fang: largely reproduces on the data Fang used, not on today's, and not in our design.** Fang's 0.0531 is -0.0188 (p = 0.317) on current SEDS. On SEDS as published in June 2023, before EIA's accounting change ([notice](https://www.eia.gov/state/seds/seds-change/index.php)), column 6 is 0.0348 (p = 0.057), about two-thirds of Fang's, with similar sizes in columns 1-2; 61% of the gap from current SEDS comes from the accounting change and the rest from later data revisions. Fang's spec has no year effects: a linear trend turns column 6 to -0.0419 (p = 0.121), and pet-care employment "explains" renewables more strongly than AI. In our final spec, postings are -0.0479 (p = 0.109) and data-center jobs -0.0567 (p = 0.208): neither significant. Fang's headline subgroup splits (price, net producer) don't reproduce; the partial matches on the June 2023 basis are exploratory.
- **Extensions (Nov 7).** By renewable type, one row passes the multiple-testing rule (postings and wind generation, -0.0477), but it runs against the expected sign and fails with state trends, so it's exploratory. None of 30 other AI-impact outcomes (sales by sector, prices, generation mix, imports, CO2) has q below 0.10. Georgia's solar share rose 0.076; AI could account for at most 25% of it. The renewable-share coefficient barely moves without year effects or with measured drivers (-0.012, -0.011, -0.010), so the national trend isn't AI; costs, tax credits and mandates track it (correlation 0.95, consistent with but not proof of their role). Pooled, data-center jobs don't predict commercial electricity sales (p = 0.764); Virginia's state slope ranks 3 of 50. A broader "infrastructure + talent" AI index finds nothing either (smallest q 0.86).
- **EPU moderation: only in Fang's spec.** AI x state EPU is 0.0193 (p = 0.002) there and not significant under two-way FE (p = 0.163).
- **Net-producer split: depends on the definition.** Our rule gives 120 net-producer state-years against Fang's 76; SEDS total energy gives 40 and SEDS net interstate flow 104. The gap between groups in Fang's spec is significant only on our rule (p = 0.003). Exploratory.
- **Shift-share IV: uninformative.** KP F = 2.81, below 10. **Broadband and R&D:** no interaction is significant. **Hansen threshold:** not run, dropped by the team.
- **Georgia solar.** At a 24% learning rate on IEA's Stated Policies path (*World Energy Outlook 2025*, Table A.3b, p. 423), the arithmetic implies $37.06/MWh in 2035, with a range across cases, also using Current Policies (Table A.3a, p. 417) and Net Zero Emissions by 2050 (Table A.3c, p. 429), of $14.51 to $50.40. It starts from $63.81/MWh. These aren't forecasts of ours, and national LCOE has risen since 2022 (49.0 to 61.0), so the curve assumes costs resume falling.

## What we can rule out

95% CI per one within-state SD of AI. **The SD is 0.5212: winsorized lagged AI after removing state and year effects, 50 states, N = 550.** That's the variation the Zhang models use. The Fang rows use the SD of each log AI measure the same way.

| Outcome | 95% CI per SD | Unit |
|---|---|---|
| Electricity use per person | -0.71 to 0.54 | percent |
| GDP per MWh | -0.50 to 0.73 | percent |
| Renewable share of generation | -1.16 to 0.11 | percentage points |
| Change in renewable capacity | 3.05 to 70.79 | MW; not robust to scaling |
| Same, per 1,000 MW of 2015 capacity | -1.55 to 2.59 | MW per 1,000 MW |
| Renewable consumption, per SD of ln(AI postings), SD 0.2457 | -2.62 to 0.27 | percent |
| Renewable consumption, per SD of ln(data-center jobs), SD 0.2163 | -3.16 to 0.70 | percent |

So a typical within-state swing in data-center jobs isn't associated with a fall in electricity use of more than 0.71 percent or a rise of more than 0.54 percent, or with a fall in renewable share of more than 1.16 points. These limits apply to data-center jobs over this period. They don't cover a much larger future build-out, and jobs aren't MW.

## What it means

At the state level over 2015-2025, we don't find that data-center job growth is associated with lower efficiency, higher electricity use or a lower renewable share once timing is taken into account. Neither the "blessing" nor the "peril" holds up in this data. The most useful result is the placebo: associations that look real in a standard panel are explained as well or better by next year's AI, so they're likely about where data-center jobs go. Our main limits are that jobs are a rough proxy for AI power use, states have little within-state variation, and we have no strong instrument. Georgia Power reports commitments from large-load customers of 15,600 MW as of June 2026, up from 3,600 MW at its October 2023 filing (Q2 2026 Large Load Economic Development Report, filed Aug. 17, 2026, Georgia PSC Docket 55378, p. 4 [PDF p. 8]). That's the utility's own reporting, and most of that load is scheduled after our sample ends, so these results describe the past, not that build-out.

## Status and next steps

- **Done:** data, validation, H1-H3, robustness, Fang test (incl. the completed method set, Nov 7), extensions (by type, AI impact, national drivers, AI index, add-on), stretch, Georgia solar, results pack, master workbook.
- **Pending, needs a person:** Q1-Q4 2024 Georgia large-load reports (browser download from PSC Docket 55378); LBNL Queued Up (refuses scripted download); PatentsView inventor locations, if the innovation dimension is wanted.
- **Next:** team review of the results by Nov 17; draft by Nov 24 from `methods_section.tex` and `findings.md`; turn-in Dec 1. `methods_section.tex` hasn't been compiled here, since no LaTeX is installed.

## Where things are

| Looking for | Where |
|---|---|
| All data, variables, ratings and limitations | `outputs/ECON499R_Master_Data_2026-11-07.xlsx`; `data/variable_registry.csv` |
| Results tables, figures and findings | `results/2026-11-07/paper/` |
| Readable report | `outputs/ECON499R_Results_2026-11-07.pdf` |
| Methods draft and memo differences | `docs/2026-11-07/methods_section.tex`; `docs/2026-11-07/memo-to-paper.md`; `EXPERIMENTS.md` |
| Notebooks | `notebooks/` |
| Rebuild steps and sources | `data/receipts/README.md` |
| Packages | `release/results_and_data_2026-11-07/` (local); `release/github/econ499r-ai-renewables/` (clean copy to push) |


## Appendix: every number and its result tag

| Number | Source file | Tag | Column |
|---|---|---|---|
| 550 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | N |
| 550 | `results/2026-11-03/h2/h2_results.csv` | `h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a` | N |
| 550 | `results/2026-11-03/h3_mainspec/sdm_core.csv` | `h3_sdm-ML_ai518210_lag1_ctrl4_w9901_ml_renew_share_50s2015_2025_invdist50` | N |
| 450 | `results/2026-11-04/h3_placebo/placebo_sdm_impacts.csv` | `h3_sdm-ML-placebo-a_lag_ai518210_lead1lag1_ctrl4_w9901_ml_renew_share_50s2015_2023_invdist50` | N |
| 204 | `results/2026-11-04/fang/fang_results.csv` | `fang_rep_c6_aipostings_contemp_state_iid_lnET_51s2018_2021_AI` | N |
| 300 | `results/2026-11-04/fang/fang_results.csv` | `fang_bridge_s6-noDC_aipostings_lag1_state-year_cl-state_lnET_50s2019_2024_AI` | N |
| 500 | `results/2026-11-04/fang/fang_results.csv` | `fang_bridge_s6-noDC_dcjobs_lag1_state-year_cl-state_lnET_50s2015_2024_AI` | N |
| 550 | `results/2026-11-04/stretch/stretch.csv` | `stretch_iv_base2015_ai518210_lag1_ctrl4_w9901_cl-state_first_stage_50s2015_2025_KP_F` | N |
| 17 | `results/2026-11-04/georgia_solar/base_cost.csv` | `{'area': 'Georgia'}` | n_projects |
| -0.0016 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | estimate |
| 0.795 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | pval |
| 0.0022 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_ln_ee_50s2015_2025` | estimate |
| 0.707 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_ln_ee_50s2015_2025` | pval |
| 0.036 | `results/2026-11-04/robustness/robustness.csv` | `rob_dk_ai518210_lag1_ctrl4_w9901_dk_ln_ee_50s2015_2025` | pval |
| -0.0101 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2025` | estimate |
| 0.100 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2025` | pval |
| 0.001 | `results/2026-11-04/robustness/robustness.csv` | `rob_dk_ai518210_lag1_ctrl4_w9901_dk_renew_share_50s2015_2025` | pval |
| -0.0197 | `results/2026-11-04/robustness/robustness.csv` | `rob_placebo_ai518210_lead1_ctrl4_w9901_cl-state_renew_share_50s2015_2024` | estimate |
| 0.006 | `results/2026-11-04/robustness/robustness.csv` | `rob_placebo_ai518210_lead1_ctrl4_w9901_cl-state_renew_share_50s2015_2024` | pval |
| 0.0015 | `results/2026-11-04/robustness/robustness.csv` | `rob_placebo-joint-lag_ai518210_lead1lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2024` | estimate |
| 0.827 | `results/2026-11-04/robustness/robustness.csv` | `rob_placebo-joint-lag_ai518210_lead1lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2024` | pval |
| 70.8 | `results/2026-11-02/h1/h1_extras.csv` | `h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025` | estimate |
| 0.033 | `results/2026-11-02/h1/h1_extras.csv` | `h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025` | pval |
| 1.00 | `results/2026-11-02/h1/h1_extras.csv` | `h1x_rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per1000mw_50s2015_2025` | estimate |
| 0.616 | `results/2026-11-02/h1/h1_extras.csv` | `h1x_rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per1000mw_50s2015_2025` | pval |
| 86.8 | `results/2026-11-04/robustness/robustness.csv` | `rob_placebo_ai518210_lead1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2024` | estimate |
| 0.028 | `results/2026-11-04/robustness/robustness.csv` | `rob_placebo_ai518210_lead1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2024` | pval |
| -0.000157 | `results/2026-11-03/h2/h2_results.csv` | `h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a` | estimate |
| 0.454 | `results/2026-11-03/h2/h2_results.csv` | `h2a_med_ai518210_lag1_M-techshare_ctrl4_w9901_cl-state_renew_share_50s2015_2025_eq-a` | pval |
| 0.322 | `results/2026-11-07/paper/tables/mediation_summary.csv` | `h2_sobel_summary` | min_p |
| 0.991 | `results/2026-11-07/paper/tables/mediation_summary.csv` | `h2_sobel_summary` | max_p |
| -0.161 | `results/2026-11-03/h3_mainspec/sdm_impacts.csv` | `h3_sdm-ML_ai518210_lag1_ctrl4_w9901_ml_renew_share_50s2015_2025_invdist50` | plugin |
| 0.035 | `results/2026-11-03/h3_mainspec/sdm_impacts.csv` | `h3_sdm-ML_ai518210_lag1_ctrl4_w9901_ml_renew_share_50s2015_2025_invdist50` | p |
| 71.0 | `results/2026-11-04/robustness/robustness.csv` | `rob_gavins-ne_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025` | estimate |
| -0.0021 | `results/2026-11-04/robustness/weather_check.csv` | `rob_weather-hddcdd_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_48s2015_2025_ai_dc_per1000_lag1` | estimate |
| 0.711 | `results/2026-11-04/robustness/weather_check.csv` | `rob_weather-hddcdd_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_48s2015_2025_ai_dc_per1000_lag1` | pval |
| -0.0009 | `results/2026-11-04/robustness/weather_check.csv` | `rob_weather-base48_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_48s2015_2025_ai_dc_per1000_lag1` | estimate |
| 0.880 | `results/2026-11-04/robustness/weather_check.csv` | `rob_weather-base48_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_48s2015_2025_ai_dc_per1000_lag1` | pval |
| 0.0531 | `Fang et al. 2025, Table 2, col. 6` | `published` |  |
| -0.0188 | `results/2026-11-04/fang/fang_results.csv` | `fang_rep_c6_aipostings_contemp_state_iid_lnET_51s2018_2021_AI` | estimate |
| 0.317 | `results/2026-11-04/fang/fang_results.csv` | `fang_rep_c6_aipostings_contemp_state_iid_lnET_51s2018_2021_AI` | pval |
| 0.0348 | `results/2026-11-07/fang/fang8_results.csv` | `fang8_t2_c6-archived_aipostings_contemp_state_iid_lnET_arch_51s2018_2021_AI` | estimate |
| 0.057 | `results/2026-11-07/fang/fang8_results.csv` | `fang8_t2_c6-archived_aipostings_contemp_state_iid_lnET_arch_51s2018_2021_AI` | pval |
| 61% | `results/2026-11-07/extend/tables/p2_gap_decomposition.csv` | `{'ai_measure': 'ln AI postings', 'column': 6}` | share_accounting_rebuild |
| -0.0419 | `results/2026-11-07/extend/p2_checks.csv` | `ext_p2_p1trend_fang6trend_aipostings_lnET_arch_51s2018_2021_AI` | estimate |
| 0.121 | `results/2026-11-07/extend/p2_checks.csv` | `ext_p2_p1trend_fang6trend_aipostings_lnET_arch_51s2018_2021_AI` | pval |
| -0.0479 | `results/2026-11-04/fang/fang_results.csv` | `fang_bridge_s6-noDC_aipostings_lag1_state-year_cl-state_lnET_50s2019_2024_AI` | estimate |
| 0.109 | `results/2026-11-04/fang/fang_results.csv` | `fang_bridge_s6-noDC_aipostings_lag1_state-year_cl-state_lnET_50s2019_2024_AI` | pval |
| -0.0567 | `results/2026-11-04/fang/fang_results.csv` | `fang_bridge_s6-noDC_dcjobs_lag1_state-year_cl-state_lnET_50s2015_2024_AI` | estimate |
| 0.208 | `results/2026-11-04/fang/fang_results.csv` | `fang_bridge_s6-noDC_dcjobs_lag1_state-year_cl-state_lnET_50s2015_2024_AI` | pval |
| -0.0477 | `results/2026-11-07/extend/s2_bytype_family.csv` | `ext_bytype_twfe_aipostp1000_lag1_ctrl4_w9901_cl-state_ln_gen_wind_50s` | estimate |
| 0.076 | `results/2026-11-07/extend/s2_georgia_implied.csv` | `ext_bytype_twfe_ai518210_lag1_ctrl4_w9901_cl-state_share_solar_50s` | actual_change |
| 25% | `results/2026-11-07/extend/s2_georgia_implied.csv` | `ext_bytype_twfe_ai518210_lag1_ctrl4_w9901_cl-state_share_solar_50s` | at_most_share_of_actual |
| -0.012 | `results/2026-11-07/extend/s4_drivers_models.csv` | `ext_natl_statefe_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s` | estimate |
| -0.011 | `results/2026-11-07/extend/s4_drivers_models.csv` | `ext_natl_drivers_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s` | estimate |
| -0.010 | `results/2026-11-07/extend/s4_drivers_models.csv` | `ext_natl_twfe_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s` | estimate |
| 0.95 | `results/2026-11-07/extend/s4_path_fit.csv` | `ext_natl_pathfit_ai518210_drivers_renew_share` | correlation |
| 0.764 | `results/2026-11-07/extend/p2b_relevance_index.csv` | `ext_p2b_relevance_ai518210_ln_sales_com_pc_all50_pooled` | pval |
| 3 | `results/2026-11-07/extend/p2b_permutation_ranks.csv` | `ext_p2b_permrank_ai518210_all50_VA` | rank_desc |
| 0.86 | `results/2026-11-07/paper/tables/ext_summary.csv` | `ext_index_min_q_all50` | value |
| 0.0193 | `results/2026-11-04/fang/fang_results.csv` | `fang_mod_fang-lnEPUS_aipostings_contemp_state_iid_lnET_51s2018_2021_AI_x_EPU` | estimate |
| 0.002 | `results/2026-11-04/fang/fang_results.csv` | `fang_mod_fang-lnEPUS_aipostings_contemp_state_iid_lnET_51s2018_2021_AI_x_EPU` | pval |
| 0.163 | `results/2026-11-04/fang/fang_results.csv` | `fang_mod_twfe-lnEPUS_aipostings_lag1_state-year_cl_lnET_50s2019_2024_AI_x_EPU` | pval |
| 120 | `results/2026-11-04/fang/net_producer_check.csv` | `fang_netdef_gen_gt_sales_difference_aipostings_producer_minus_consumer` | net_producer_state_years |
| 40 | `results/2026-11-04/fang/net_producer_check.csv` | `fang_netdef_teprb_gt_tetcb_difference_aipostings_producer_minus_consumer` | net_producer_state_years |
| 104 | `results/2026-11-04/fang/net_producer_check.csv` | `fang_netdef_elisb_negative_difference_aipostings_producer_minus_consumer` | net_producer_state_years |
| 0.003 | `results/2026-11-04/fang/net_producer_check.csv` | `fang_netdef_gen_gt_sales_difference_aipostings_producer_minus_consumer` | pval |
| 2.81 | `results/2026-11-04/stretch/stretch.csv` | `stretch_iv_base2015_ai518210_lag1_ctrl4_w9901_cl-state_first_stage_50s2015_2025_KP_F` | estimate |
| 37.06 | `results/2026-11-04/georgia_solar/projection_long.csv` | `ga_solar_lc_lr24_cap-central_2035` | lcoe_2025usd_mwh |
| 14.51 | `results/2026-11-04/georgia_solar/projection_long.csv` | `ga_solar_lc_lr45_cap-high_2035` | lcoe_2025usd_mwh |
| 50.40 | `results/2026-11-04/georgia_solar/projection_long.csv` | `ga_solar_lc_lr12_cap-low_2035` | lcoe_2025usd_mwh |
| 63.81 | `results/2026-11-04/georgia_solar/base_cost.csv` | `{'area': 'Georgia'}` | lcoe_capacity_weighted |
| 49.0 | `results/2026-11-04/georgia_solar/national_lcoe_lbnl_tab.csv` | `{'year': 2022}` | lcoe |
| 61.0 | `results/2026-11-04/georgia_solar/national_lcoe_lbnl_tab.csv` | `{'year': 2025}` | lcoe |
| 0.5212 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | sd_ai |
| 550 | `results/2026-11-02/h1/h1_core.csv` | `h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_ln_ee_50s2015_2025` | N |
| -0.71 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | ci_lo_per_sd |
| 0.54 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | ci_hi_per_sd |
| -0.50 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_ln_ee_50s2015_2025` | ci_lo_per_sd |
| 0.73 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_ln_ee_50s2015_2025` | ci_hi_per_sd |
| -1.16 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2025` | ci_lo_per_sd |
| 0.11 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2025` | ci_hi_per_sd |
| 3.05 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025` | ci_lo_per_sd |
| 70.79 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025` | ci_hi_per_sd |
| -1.55 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per_1000mw_50s2015_2025` | ci_lo_per_sd |
| 2.59 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per_1000mw_50s2015_2025` | ci_hi_per_sd |
| 0.2457 | `results/2026-11-07/paper/rule_out.csv` | `fang_bridge_s6-noDC_aipostings_lag1_state-year_cl-state_lnET_50s2019_2024_AI` | sd_ai |
| -2.62 | `results/2026-11-07/paper/rule_out.csv` | `fang_bridge_s6-noDC_aipostings_lag1_state-year_cl-state_lnET_50s2019_2024_AI` | ci_lo_per_sd |
| 0.27 | `results/2026-11-07/paper/rule_out.csv` | `fang_bridge_s6-noDC_aipostings_lag1_state-year_cl-state_lnET_50s2019_2024_AI` | ci_hi_per_sd |
| 0.2163 | `results/2026-11-07/paper/rule_out.csv` | `fang_bridge_s6-noDC_dcjobs_lag1_state-year_cl-state_lnET_50s2015_2024_AI` | sd_ai |
| -3.16 | `results/2026-11-07/paper/rule_out.csv` | `fang_bridge_s6-noDC_dcjobs_lag1_state-year_cl-state_lnET_50s2015_2024_AI` | ci_lo_per_sd |
| 0.70 | `results/2026-11-07/paper/rule_out.csv` | `fang_bridge_s6-noDC_dcjobs_lag1_state-year_cl-state_lnET_50s2015_2024_AI` | ci_hi_per_sd |
| 0.71 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_50s2015_2025` | ci_lo_per_sd |
| 1.16 | `results/2026-11-07/paper/rule_out.csv` | `rob_base_ai518210_lag1_ctrl4_w9901_cl-state_renew_share_50s2015_2025` | ci_lo_per_sd |
| 15,600 | `Georgia Power Q2 2026 Large Load Economic Development Report, PSC Docket 55378, p. 4 [PDF p. 8]` | `published` |  |
| 3,600 | `Georgia Power Q2 2026 Large Load Economic Development Report, PSC Docket 55378, p. 4 [PDF p. 8]` | `published` |  |

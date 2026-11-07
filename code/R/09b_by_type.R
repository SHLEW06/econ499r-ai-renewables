#!/usr/bin/env Rscript
# 09b_by_type.R: prompts/09_extend.md section 2 (EXPERIMENTS.md section 14.2). Family "bytype".
# Main spec for 19 by-type outcomes x 2 AI measures, BH q-values, lead placebo for p < 0.10, Georgia implied vs actual changes.
# Usage: Rscript code/R/09b_by_type.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date()
need(c("data/extend_outcomes.csv"))
OUT <- file.path("results", date_arg, "extend"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
P <- main_panel()
eo <- fread("data/extend_outcomes.csv")[is_dc==0]
FAM <- c("share_wind","ln_gen_wind","add_wind_per1000","share_solar","ln_gen_solar","add_solar_per1000","share_hydro","ln_gen_hydro","add_hydro_per1000",
         "share_geo","ln_gen_geo","add_geo_per1000","share_bio","ln_gen_bio","add_bio_per1000","ln_seds_woodwaste","ln_seds_biofuels","ln_seds_re_exbiomass","ln_seds_re_exbiofuels")
REF <- "ln_seds_re_total"
raw <- copy(eo[, c("state","year",FAM,REF), with=FALSE]); setnames(raw, c(FAM,REF), paste0(c(FAM,REF), "_raw"))
P <- merge(P, eo[, c("state","year",FAM,REF), with=FALSE], by=c("state","year"))
P <- merge(P, raw, by=c("state","year")); setorder(P, state, year)
for (v in c(FAM, REF)) P[, (v) := wz(get(v))]
stopifnot(nrow(P)==550)

for (y in FAM) for (mn in names(AIM)) run_main("bytype", y, P, AIM[[mn]], "bytype", "50s")
for (mn in names(AIM)) run_main("bytype", REF, P, AIM[[mn]], "reference", "50s", note="reference row outside the family")
res <- rbindlist(ROWS$r, fill=TRUE); res <- add_bh(res, "bytype")
# lead placebo for p < 0.10
pl <- res[family=="bytype" & status=="ok" & pval < 0.10]
for (i in seq_len(nrow(pl))) { m <- AIM[[if (pl$ai_measure[i]=="ai518210") "jobs" else "post"]]; run_lead("bytype", pl$outcome[i], P, m, "bytype", "50s") }
res <- rbindlist(ROWS$r, fill=TRUE); res <- add_bh(res, "bytype")
# finding rule
pp <- res[model=="placebo"]; main <- res[model=="twfe" & family=="bytype"]
main[, `:=`(lead_est=NA_real_, lead_p=NA_real_, lag_est_pl=NA_real_, finding=FALSE)]
for (i in which(main$pval < 0.10)) { a <- pp[outcome==main$outcome[i] & ai_measure==main$ai_measure[i]]
  la <- a[lag=="lag1"]; le <- a[lag=="lead1"]; main[i, `:=`(lead_est=le$estimate, lead_p=le$pval, lag_est_pl=la$estimate,
                                                         finding = qval < 0.10 & clearly_smaller(la$estimate, le$estimate, le$pval))] }
fwrite(res, file.path(OUT, "s2_bytype_results.csv"))
fwrite(main, file.path(OUT, "s2_bytype_family.csv"))
print(main[, .(outcome, ai_measure, estimate=signif(estimate,3), p=round(pval,3), q=round(qval,3), N, lead_est=signif(lead_est,3), lead_p=round(lead_p,3), finding)])

# ================ Georgia ================
G <- P[state=="GA"]; setorder(G, year)
P[, jobs_lag_raw := ai_dc_per1000_lag1]  # winsorized in load_panel; recover raw from the unwinsorized series
pr <- fread("data/out/state_panel_2015_2025.csv")[is_dc==0, .(state, year, ai_raw=ai_dc_per1000, ai_lag_raw=ai_dc_per1000_lag1, total_jobs, renew_share, solar_share)]
fp <- fread("data/fang_panel.csv")[, .(state, year, ai_postings)]
pr <- merge(pr, fp, by=c("state","year")); pr[, post_raw := ai_postings/total_jobs*1000]
ga <- pr[state=="GA"]
dJ <- ga[year==2025, ai_lag_raw] - ga[year==2015, ai_lag_raw]
dP <- ga[year==2024, post_raw] - ga[year==2018, post_raw]
capJ <- max(P$jobs_lag1, na.rm=TRUE); capP <- max(P$post_lag1, na.rm=TRUE)
win <- list(ai518210=list(d=dJ, s=2015, e=2025, cap=ga[year==2024, ai_raw] > capJ), aipostp1000=list(d=dP, s=2019, e=2025, cap=ga[year==2024, post_raw] > capP))
gi <- main[, {w <- win[[ai_measure]]; yr <- if (outcome %like% "seds") min(w$e, 2024) else w$e
  a0 <- P[state=="GA" & year==w$s][[paste0(outcome,"_raw")]]; a1 <- P[state=="GA" & year==yr][[paste0(outcome,"_raw")]]
  .(window=sprintf("%d-%d", w$s, yr), ga_delta_ai=w$d, implied=estimate*w$d, implied_lo=min(ci_lo*w$d, ci_hi*w$d), implied_hi=max(ci_lo*w$d, ci_hi*w$d),
    actual_start=a0, actual_end=a1, actual_change=a1-a0, ga_ai_above_winsor_cap=w$cap) }, by=.(outcome, ai_measure, tag, estimate, pval, qval)]
gi[, at_most_share_of_actual := pmax(abs(implied_lo), abs(implied_hi)) / abs(actual_change)]
gi[, sentence := sprintf("%s, %s: the association implies %+.3g (95%% CI %+.3g to %+.3g) against Georgia's actual change of %+.3g over %s; at most %s of the actual change.",
                         outcome, ai_measure, implied, implied_lo, implied_hi, actual_change, window,
                         fifelse(is.finite(at_most_share_of_actual), sprintf("%.0f%%", 100*at_most_share_of_actual), "an undefined share (no actual change)"))]
fwrite(gi, file.path(OUT, "s2_georgia_implied.csv"))
cat(sprintf("Georgia: change in AI(t-1), jobs 2015-2025 = %.3f per 1,000 (GA 2024 above the winsor cap: %s); postings 2019-2025 = %.3f per 1,000 (above cap: %s)\n", dJ, win$ai518210$cap, dP, win$aipostp1000$cap))

# profile
ranks <- pr[year %in% c(2015, 2024, 2025), .(state, year, ai_raw, post_raw)]
rk <- function(x) frank(-x, na.last="keep", ties.method="min")
ranks[, `:=`(rank_jobs=rk(ai_raw), rank_post=rk(post_raw)), by=year]
chg <- dcast(pr[year %in% c(2015, 2024)], state ~ year, value.var="ai_raw"); chg[, d := `2024` - `2015`]; chg[, rank_change := rk(d)]
chgp <- dcast(pr[year %in% c(2018, 2024)], state ~ year, value.var="post_raw"); chgp[, d := `2024` - `2018`]; chgp[, rank_change := rk(d)]
prof <- rbind(ranks[state=="GA", .(item=paste0("AI level, ", year), jobs_per1000=ai_raw, jobs_rank_of_50=rank_jobs, postings_per1000=post_raw, postings_rank_of_50=rank_post)],
              data.table(item="AI change (jobs 2015-2024; postings 2018-2024)", jobs_per1000=chg[state=="GA", d], jobs_rank_of_50=chg[state=="GA", rank_change],
                         postings_per1000=chgp[state=="GA", d], postings_rank_of_50=chgp[state=="GA", rank_change]))
fwrite(prof, file.path(OUT, "s2_georgia_ai_profile.csv"))
mix <- merge(eo[state=="GA", .(year, share_wind, share_solar, share_hydro, share_geo, share_bio, share_gas, share_coal, share_nuclear, add_solar_per1000, add_wind_per1000, add_gas_per1000, add_hydro_per1000, add_bio_per1000)],
             fread("data/out/state_panel_2015_2025.csv")[state=="GA", .(year, renew_share, cap_total_mw, new_solar_mw, new_wind_mw, new_renew_mw)], by="year")
fwrite(mix, file.path(OUT, "s2_georgia_mix.csv"))
# cross-state changes for the chart
cs <- merge(pr[year==2015, .(state, ai15=ai_lag_raw, sol15=solar_share, ren15=renew_share)], pr[year==2025, .(state, ai25=ai_lag_raw, sol25=solar_share, ren25=renew_share)], by="state")
cs[, `:=`(d_ai=ai25-ai15, d_solar=sol25-sol15, d_renew=ren25-ren15)]
csp <- merge(pr[year==2019, .(state, p19=shift(0))], pr[, .(state, year)], by="state")[0]
cs2 <- merge(pr[year==2018, .(state, p18=post_raw)], pr[year==2024, .(state, p24=post_raw)], by="state"); cs <- merge(cs, cs2, by="state"); cs[, d_post := p24 - p18]
fwrite(cs, file.path(OUT, "s2_cross_state_changes.csv"))
print(prof); print(gi[, .(outcome, ai_measure, implied=signif(implied,3), lo=signif(implied_lo,3), hi=signif(implied_hi,3), actual=signif(actual_change,3), at_most=round(at_most_share_of_actual,2))])
cat("DONE\n")

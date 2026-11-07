#!/usr/bin/env Rscript
# 09g_land_sensitivity.R: deviation X5 (EXPERIMENTS.md 14.6): land moderator in logs, and in levels without AK. Post hoc, labeled.
# Usage: Rscript code/R/09g_land_sensitivity.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date(); OUT <- file.path("results", date_arg, "extend")
P <- main_panel(); eo <- fread("data/extend_outcomes.csv")[is_dc==0]; cs <- fread("data/ai_index_crossstate.csv")
BYT <- c("share_wind","ln_gen_wind","add_wind_per1000","share_solar","ln_gen_solar","add_solar_per1000","share_hydro","ln_gen_hydro","add_hydro_per1000",
         "share_geo","ln_gen_geo","add_geo_per1000","share_bio","ln_gen_bio","add_bio_per1000","ln_seds_woodwaste","ln_seds_biofuels","ln_seds_re_exbiomass","ln_seds_re_exbiofuels")
P <- merge(P, eo[, c("state","year",BYT), with=FALSE], by=c("state","year")); for (v in BYT) P[, (v) := wz(get(v))]
P <- merge(P, cs[, .(state, room=land_sqmi_per_twh_2015)], by="state")
L <- list()
for (sn in c("all50","noCACODE")) for (ver in c("log_room","level_noAK")) { S <- P[if (sn=="all50") TRUE else !state %in% c("CA","CO","DE")]; if (ver=="level_noAK") S <- S[state!="AK"]
  st <- unique(S[, .(state, room)]); mu <- if (ver=="log_room") mean(log(st$room)) else mean(st$room)
  S[, room_c := (if (ver=="log_room") log(room) else room) - mu]
  for (mn in names(AIM)) { x <- AIM[[mn]]$lag; for (y in c("ln_ec","ln_ee","renew_share", BYT)) { d0 <- S[!is.na(get(y)) & !is.na(get(x))]; d0[, x_room := get(x) * room_c]
    m <- tryCatch(fit_main(y, c(x, "x_room"), d0), error=function(e) NULL); if (is.null(m) || !"x_room" %in% names(coef(m))) next
    L[[length(L)+1]] <- data.table(tag=sprintf("ext_p2b_landX5_%s_%s_%s_%s", ver, AIM[[mn]]$tag, y, sn), sample=sn, version=ver, ai_measure=AIM[[mn]]$tag, outcome=y,
      interaction=coef(m)["x_room"], interaction_p=pvalue(m)["x_room"], N=m$nobs) } } }
L <- rbindlist(L); L[, interaction_q := p.adjust(interaction_p, "BH"), by=.(sample, version)]; fwrite(L, file.path(OUT, "p2b_land_moderator_X5.csv"))
print(L[, .(n=.N, n_q10=sum(interaction_q<0.10), min_q=min(interaction_q)), by=.(sample, version)]); print(L[interaction_q<0.10, .(sample, version, ai_measure, outcome, interaction=signif(interaction,3), q=round(interaction_q,3))])

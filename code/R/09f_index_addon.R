#!/usr/bin/env Rscript
# 09f_index_addon.R: section 5 index use, B4 per-state slope ranks, B6 distillery rerun, add-on A2 groupings, A3 land moderator
# (EXPERIMENTS.md section 14.6). Every section 5 and add-on result runs on 50 states and without CA, CO and DE (A5).
# Usage: Rscript code/R/09f_index_addon.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date()
need(c("data/ai_index_state.csv","data/ai_index_crossstate.csv","data/extend_outcomes.csv","data/seds_old_basis.csv"))
OUT <- file.path("results", date_arg, "extend"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
P <- main_panel()
eo <- fread("data/extend_outcomes.csv")[is_dc==0]
BYT <- c("share_wind","ln_gen_wind","add_wind_per1000","share_solar","ln_gen_solar","add_solar_per1000","share_hydro","ln_gen_hydro","add_hydro_per1000",
         "share_geo","ln_gen_geo","add_geo_per1000","share_bio","ln_gen_bio","add_bio_per1000","ln_seds_woodwaste","ln_seds_biofuels","ln_seds_re_exbiomass","ln_seds_re_exbiofuels")
IMP <- c("ln_sales_com_pc","ln_sales_ind_pc","ln_sales_res_pc","price_com861_c_kwh","price_ind_c_kwh","price_res_c_kwh","share_gas","share_coal","share_nuclear",
         "add_gas_per1000","add_solar_per1000","add_wind_per1000","net_imports","ln_co2_power","co2_per_mwh_t")
H1 <- c("ln_ec","ln_ee","renew_share"); PRICE <- c("price_com861_c_kwh","price_ind_c_kwh","price_res_c_kwh"); CTRL3 <- setdiff(CTRL4, "price_c_kwh")
newv <- setdiff(unique(c(BYT, IMP)), c("co2_per_mwh_t"))
P <- merge(P, eo[, c("state","year",newv), with=FALSE], by=c("state","year")); for (v in newv) P[, (v) := wz(get(v))]
ix <- fread("data/ai_index_state.csv"); cs <- fread("data/ai_index_crossstate.csv")
mi <- ix[version=="main_2018_2023"]; ck <- ix[version=="check_2015_2023_no_postings", .(state, year, chk_a=index_a)]
IXV <- c("index_a","index_b","sub_infra","sub_talent")
lagit <- function(d, vars) { d <- copy(d); d[, year := year + 1L]; setnames(d, vars, paste0(vars, "_lag1")); d }
P <- merge(P, lagit(mi[, c("state","year",IXV), with=FALSE], IXV), by=c("state","year"), all.x=TRUE)
P <- merge(P, lagit(ck, "chk_a"), by=c("state","year"), all.x=TRUE); setorder(P, state, year)
for (v in c(paste0(IXV, "_lag1"), "chk_a_lag1")) P[, (v) := wz(get(v))]
P <- merge(P, cs[, .(state, grp_invest, grp_invest_per_twh, grp_jobs_per_twh, land_sqmi_per_twh_2015)], by="state"); setorder(P, state, year)
stopifnot(nrow(P)==550)
XI <- list(index_a=list(lag="index_a_lag1", tag="indexA"), index_b=list(lag="index_b_lag1", tag="indexB"), sub_infra=list(lag="sub_infra_lag1", tag="subInfra"),
           sub_talent=list(lag="sub_talent_lag1", tag="subTalent"), chk_a=list(lag="chk_a_lag1", tag="indexAcheck1523"))
SAMPLES <- list(all50=P, noCACODE=P[!state %in% c("CA","CO","DE")])
sdw <- function(d, x) sd(d[[x]] - ave(d[[x]], d$state) - ave(d[[x]], d$year) + mean(d[[x]]))
fitc <- function(y, xs, d, extra=character(0), fe="state + year") feols(as.formula(paste(y, "~", paste(c(xs, extra, if (y %in% PRICE) CTRL3 else CTRL4), collapse=" + "), "|", fe)), data=d, vcov=~state)
R <- list(); rec <- function(...) R[[length(R)+1]] <<- data.table(...)
tg <- function(...) paste("ext_p2b", ..., sep="_")

# ================ 1. Relevance (reported first) and B4 per-state slope ranks ================
REL <- list(); RANK <- list()
for (sn in names(SAMPLES)) { S <- SAMPLES[[sn]]
  ms <- c(list(jobs=list(lag="jobs_lag1", tag="ai518210"), post=list(lag="post_lag1", tag="aipostp1000")), XI)
  for (mn in names(ms)) { x <- ms[[mn]]$lag; d0 <- copy(S[!is.na(ln_sales_com_pc) & !is.na(get(x))]); s_ <- sdw(d0, x)
    a <- fitc("ln_sales_com_pc", x, d0); ct <- coeftable(a); ci <- confint(a)
    REL[[length(REL)+1]] <- data.table(tag=tg("relevance", ms[[mn]]$tag, "ln_sales_com_pc", sn, "pooled"), sample=sn, ai_measure=ms[[mn]]$tag, version="pooled", slope=ct[x,1], se=ct[x,2], pval=ct[x,4],
                                       ci_lo=ci[x,1], ci_hi=ci[x,2], per_within_sd=ct[x,1]*s_, sd_within=s_, N=a$nobs, n_states=uniqueN(d0$state))
    keep <- intersect(c("VA","TX","GA"), unique(d0$state))
    for (s in keep) d0[, (paste0("x_", s)) := get(x) * (state==s)]
    b <- fitc("ln_sales_com_pc", c(x, paste0("x_", keep)), d0); V <- vcov(b)
    REL[[length(REL)+1]] <- data.table(tag=tg("relevance", ms[[mn]]$tag, "ln_sales_com_pc", sn, "rest"), sample=sn, ai_measure=ms[[mn]]$tag, version="rest of states", slope=coef(b)[x], se=se(b)[x],
                                       pval=pvalue(b)[x], ci_lo=NA, ci_hi=NA, per_within_sd=coef(b)[x]*s_, sd_within=s_, N=b$nobs, n_states=uniqueN(d0$state))
    for (s in keep) { n <- c(x, paste0("x_", s)); REL[[length(REL)+1]] <- data.table(tag=tg("relevance", ms[[mn]]$tag, "ln_sales_com_pc", sn, s), sample=sn, ai_measure=ms[[mn]]$tag, version=s,
      slope=sum(coef(b)[n]), se=sqrt(sum(V[n,n])), pval=NA_real_, ci_lo=NA, ci_hi=NA, per_within_sd=sum(coef(b)[n])*s_, sd_within=s_, N=b$nobs, n_states=uniqueN(d0$state)) }
    # B4: one slope per state (main spec), ranks of VA, TX, GA
    if (mn %in% c("jobs","post","index_a")) {
      pm <- feols(as.formula(paste("ln_sales_com_pc ~", x, ":i(state) +", paste(CTRL4, collapse=" + "), "| state + year")), data=d0, vcov=~state)
      cf <- coef(pm); cf <- cf[grepl("state::", names(cf))]; st <- sub(".*state::([A-Z]{2}).*", "\\1", names(cf))
      sl <- data.table(state=st, slope=as.numeric(cf))[!is.na(slope)]; sl[, rank_desc := frank(-slope, ties.method="min")]
      for (s in c("VA","TX","GA")) if (s %in% sl$state) RANK[[length(RANK)+1]] <- data.table(tag=tg("permrank", ms[[mn]]$tag, sn, s), sample=sn, ai_measure=ms[[mn]]$tag, state=s,
        slope=sl[state==s, slope], rank_of=nrow(sl), rank_desc=sl[state==s, rank_desc], share_states_larger=(sl[state==s, rank_desc]-1)/nrow(sl), median_slope=median(sl$slope))
      fwrite(sl, file.path(OUT, sprintf("p2b_state_slopes_%s_%s.csv", ms[[mn]]$tag, sn))) } } }
fwrite(rbindlist(REL), file.path(OUT, "p2b_relevance_index.csv")); fwrite(rbindlist(RANK), file.path(OUT, "p2b_permutation_ranks.csv"))

# ================ 2. Index family: H1 core + by-type + section 3 outcomes on each index ================
for (sn in names(SAMPLES)) { S <- SAMPLES[[sn]]
  for (k in names(XI)) { x <- XI[[k]]$lag
    for (y in unique(c(H1, BYT, IMP))) { d0 <- S[!is.na(get(y)) & !is.na(get(x))]
      fam <- if (k=="chk_a") "index_check" else "index"
      if (nrow(d0) < 60 || uniqueN(d0$state) < 10 || sd(d0[[y]])==0) { rec(tag=tg("index", XI[[k]]$tag, y, sn), sample=sn, family=fam, index=k, outcome=y, status="FAILED", note="too few observations or states"); next }
      a <- fitc(y, x, d0); ct <- coeftable(a); ci <- confint(a); s_ <- sdw(d0, x)
      rec(tag=tg("index", XI[[k]]$tag, y, sn), sample=sn, family=fam, index=k, outcome=y, estimate=ct[x,1], se=ct[x,2], pval=ct[x,4], ci_lo=ci[x,1], ci_hi=ci[x,2],
          sd_within=s_, per_sd=ct[x,1]*s_, per_sd_lo=ci[x,1]*s_, per_sd_hi=ci[x,2]*s_, N=a$nobs, n_states=uniqueN(d0$state), years=paste(range(d0$year), collapse="-"), status="ok", note=if (y %in% PRICE) "ctrl3 (X2)" else "") } } }
IXR <- rbindlist(R, fill=TRUE); R <- list()
IXR[status=="ok" & family=="index", qval := p.adjust(pval, "BH"), by=sample]
# lead placebo for q < 0.10 (index lead = index at t+1)
P2 <- merge(P, { d <- copy(mi[, c("state","year",IXV), with=FALSE]); d[, year := year - 1L]; setnames(d, IXV, paste0(IXV, "_lead1")); d }, by=c("state","year"), all.x=TRUE)
for (v in paste0(IXV, "_lead1")) P2[, (v) := wz(get(v))]
IXR[, `:=`(lead_est=NA_real_, lead_p=NA_real_, lag_est_pl=NA_real_, finding=FALSE)]
for (i in which(IXR$qval < 0.10)) { k <- IXR$index[i]; y <- IXR$outcome[i]; S <- if (IXR$sample[i]=="all50") P2 else P2[!state %in% c("CA","CO","DE")]
  d0 <- S[!is.na(get(y)) & !is.na(get(paste0(k,"_lag1"))) & !is.na(get(paste0(k,"_lead1")))]
  la <- fitc(y, paste0(k,"_lag1"), d0); le <- fitc(y, paste0(k,"_lead1"), d0)
  IXR[i, `:=`(lag_est_pl=coef(la)[1], lead_est=coef(le)[1], lead_p=pvalue(le)[1])]; IXR[i, finding := clearly_smaller(lag_est_pl, lead_est, lead_p)] }
fwrite(IXR, file.path(OUT, "p2b_index_family.csv"))

# ================ 3. Measurement-error check: 2SLS ================
IV <- list()
for (sn in names(SAMPLES)) { S <- SAMPLES[[sn]][!is.na(post_lag1) & !is.na(jobs_lag1)]
  for (y in H1) for (dir in list(c("post_lag1","jobs_lag1","postings instrumented by jobs"), c("jobs_lag1","post_lag1","jobs instrumented by postings"))) {
    d0 <- S[!is.na(get(y))]
    m <- feols(as.formula(paste(y, "~", paste(CTRL4, collapse=" + "), "| state + year |", dir[1], "~", dir[2])), data=d0, vcov=~state)
    f1 <- fitstat(m, "ivwald1")[[1]]$stat; ct <- coeftable(m); nm <- paste0("fit_", dir[1])
    IV[[length(IV)+1]] <- data.table(tag=tg("2sls", dir[1], y, sn), sample=sn, outcome=y, direction=dir[3], estimate=ct[nm,1], se=ct[nm,2], pval=ct[nm,4], first_stage_F=f1,
                                     informative=f1 >= 10, N=m$nobs) } }
fwrite(rbindlist(IV), file.path(OUT, "p2b_2sls.csv"))

# ================ 4. Add-on A2 groupings and A3 land moderator ================
GR <- list(); LM <- list()
GRPS <- list(grp_invest=c("lt_100M","100M_1B","ge_1B"), grp_invest_per_twh=c("low","mid","high"), grp_jobs_per_twh=c("low","mid","high"))
for (sn in names(SAMPLES)) { S <- SAMPLES[[sn]]
  for (g in names(GRPS)) for (mn in names(AIM)) { x <- AIM[[mn]]$lag; lv <- GRPS[[g]]
    for (y in c(H1, BYT)) { d0 <- copy(S[!is.na(get(y)) & !is.na(get(x)) & !is.na(get(g)) & get(g) != ""])
      for (l in lv[-1]) d0[, (paste0("x_", l)) := get(x) * (get(g)==l)]
      ok <- sapply(paste0("x_", lv[-1]), function(v) sd(d0[[v]]) > 0)
      m <- tryCatch(fitc(y, c(x, paste0("x_", lv[-1])[ok]), d0), error=function(e) NULL)
      if (is.null(m) || !all(paste0("x_", lv[-1])[ok] %in% names(coef(m)))) { GR[[length(GR)+1]] <- data.table(tag=tg("group", g, AIM[[mn]]$tag, y, sn), sample=sn, grouping=g, ai_measure=AIM[[mn]]$tag, outcome=y, status="FAILED"); next }
      w <- wald(m, paste0("^x_(", paste(lv[-1], collapse="|"), ")$"), print=FALSE); V <- vcov(m)
      sl <- sapply(lv, function(l) if (l==lv[1]) coef(m)[x] else if (paste0("x_",l) %in% names(coef(m))) sum(coef(m)[c(x, paste0("x_",l))]) else NA)
      GR[[length(GR)+1]] <- data.table(tag=tg("group", g, AIM[[mn]]$tag, y, sn), sample=sn, grouping=g, ai_measure=AIM[[mn]]$tag, outcome=y, joint_F=w$stat, joint_p=w$p,
        slope_g1=sl[1], slope_g2=sl[2], slope_g3=sl[3], groups=paste(lv, collapse="/"), n_states=paste(sapply(lv, function(l) uniqueN(d0[get(g)==l, state])), collapse="/"), N=m$nobs, status="ok") } }
  for (mn in names(AIM)) { x <- AIM[[mn]]$lag
    for (y in c(H1, BYT)) { d0 <- copy(S[!is.na(get(y)) & !is.na(get(x))]); d0[, room_c := land_sqmi_per_twh_2015 - mean(unique(d0[, .(state, land_sqmi_per_twh_2015)])$land_sqmi_per_twh_2015)]
      d0[, x_room := get(x) * room_c]; m <- tryCatch(fitc(y, c(x, "x_room"), d0), error=function(e) NULL)
      if (is.null(m) || !"x_room" %in% names(coef(m))) { LM[[length(LM)+1]] <- data.table(tag=tg("land", AIM[[mn]]$tag, y, sn), sample=sn, ai_measure=AIM[[mn]]$tag, outcome=y, status="FAILED"); next }
      ct <- coeftable(m); LM[[length(LM)+1]] <- data.table(tag=tg("land", AIM[[mn]]$tag, y, sn), sample=sn, ai_measure=AIM[[mn]]$tag, outcome=y, ai_at_mean_room=ct[x,1], ai_p=ct[x,4],
        interaction=ct["x_room",1], interaction_se=ct["x_room",2], interaction_p=ct["x_room",4], room_sd=sd(unique(d0[, .(state, room_c)])$room_c), N=m$nobs, status="ok") } } }
GR <- rbindlist(GR, fill=TRUE); GR[status=="ok", joint_q := p.adjust(joint_p, "BH"), by=.(sample, grouping)]; fwrite(GR, file.path(OUT, "p2b_groupings.csv"))
LM <- rbindlist(LM, fill=TRUE); LM[status=="ok", interaction_q := p.adjust(interaction_p, "BH"), by=sample]; fwrite(LM, file.path(OUT, "p2b_land_moderator.csv"))

# ================ 5. B6 distillery placebo on never-suppressed states ================
fp <- data.table(fips=sprintf("%02d", c(1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56)),
                 state=c("AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"))
q <- rbindlist(lapply(2014:2024, function(y) { x <- fread(sprintf("data/raw/bls/placebo/qcew_%d_312140.csv", y), colClasses=list(character="area_fips"))
  x[agglvl_code==58 & own_code==5 & grepl("000$", area_fips) & area_fips!="US000", .(fips=substr(area_fips,1,2), year=y, emp=annual_avg_emplvl)] }))
q <- merge(q, fp, by="fips"); full <- CJ(state=fp$state, year=2014:2024); q <- merge(full, q[, .(state, year, emp)], by=c("state","year"), all.x=TRUE)
q[, supp := is.na(emp) | emp <= 0]; sup <- q[, .(years_suppressed=sum(supp), years=paste(year[supp], collapse=";")), by=state]
clean <- sup[years_suppressed==0, state]; fwrite(sup[order(-years_suppressed)], file.path(OUT, "p2b_distillery_suppression.csv"))
d <- fread("data/fang_panel.csv"); sb <- fread("data/seds_old_basis.csv"); d <- merge(d, sb[,.(state,year,re_bbtu_rebuilt,RETCB_arch2021)], by=c("state","year"), all.x=TRUE)
d <- merge(d, q[, .(state, year, emp)], by=c("state","year"), all.x=TRUE); setorder(d, state, year)
d[, `:=`(lnET=log(re_bbtu), lnET_arch=log(RETCB_arch2021), lnEPU=log(epu_composite), lnEP=log(ep_tetcd), lnGDP=log(gdp_real_musd2017), lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000), lnDist=log(emp), trend=year-2018)]
CF <- c("lnEPU","lnEP","lnGDP","lnPOP","lnEDU"); DI <- list()
for (cl in list(list("all_nonsuppressed_obs", unique(d$state)), list("never_suppressed_states", clean))) { S18 <- d[year %between% c(2018,2021) & state %in% cl[[2]] & !is.na(lnDist)]
  for (y in c("lnET","lnET_arch")) for (tr in c(FALSE, TRUE)) { m <- feols(as.formula(paste(y, "~ lnDist +", paste(c(CF, if (tr) "trend"), collapse=" + "), "| state")), data=S18, vcov="iid")
    DI[[length(DI)+1]] <- data.table(tag=tg("distill", "fang6", if (tr) "trend" else "notrend", y, cl[[1]]), spec="Fang col. 6", trend=tr, outcome=y, states=cl[[1]], estimate=coef(m)["lnDist"], pval=pvalue(m)["lnDist"], N=m$nobs, n_states=uniqueN(S18$state)) } }
q[, lnDist_l1 := shift(log(emp)), by=state]; PP <- merge(P, q[, .(state, year, lnDist_l1)], by=c("state","year"), all.x=TRUE)
PP <- merge(PP, sb[, .(state, year, re_bbtu_current)], by=c("state","year")); PP[, `:=`(lnRE=wz(log(re_bbtu_current)), lnDist_l1=wz(lnDist_l1), t=year-2015)]
for (cl in list(list("all_nonsuppressed_obs", unique(PP$state)), list("never_suppressed_states", clean))) for (tr in c(FALSE, TRUE)) {
  d0 <- PP[year %between% c(2015,2024) & state %in% cl[[2]] & !is.na(lnDist_l1) & !is.na(lnRE)]
  m <- feols(as.formula(paste("lnRE ~ lnDist_l1 +", paste(CTRL4, collapse=" + "), "|", if (tr) "state[t] + year" else "state + year")), data=d0, vcov=~state)
  DI[[length(DI)+1]] <- data.table(tag=tg("distill", "twfe", if (tr) "trend" else "notrend", "lnRE", cl[[1]]), spec="our main spec", trend=tr, outcome="lnRE", states=cl[[1]], estimate=coef(m)["lnDist_l1"], pval=pvalue(m)["lnDist_l1"], N=m$nobs, n_states=uniqueN(d0$state)) }
fwrite(rbindlist(DI), file.path(OUT, "p2b_distillery_rerun.csv"))
cat("Never-suppressed distillery states:", length(clean), paste(clean, collapse=","), "\n")
print(rbindlist(REL)[version=="pooled", .(sample, ai_measure, slope=signif(slope,3), p=round(pval,3), per_sd=signif(per_within_sd,3), N)])
print(rbindlist(RANK)[, .(sample, ai_measure, state, rank_desc, rank_of, slope=signif(slope,3))])
print(IXR[status=="ok" & family=="index", .(n=.N, min_q=min(qval, na.rm=TRUE), n_q10=sum(qval<0.10, na.rm=TRUE), n_find=sum(finding)), by=sample])
print(IXR[qval<0.10, .(sample, index, outcome, est=signif(estimate,3), p=signif(pval,3), q=round(qval,3), lead=signif(lead_est,3), lead_p=round(lead_p,3), finding)])
print(rbindlist(IV)[, .(sample, outcome, direction, est=signif(estimate,3), p=round(pval,3), F=round(first_stage_F,1))])
print(GR[status=="ok", .(n=.N, min_q=min(joint_q), n_q10=sum(joint_q<0.10)), by=.(sample, grouping)]); print(GR[joint_q<0.10, .(sample, grouping, ai_measure, outcome, joint_p=signif(joint_p,3), joint_q=round(joint_q,3), slope_g1=signif(slope_g1,3), slope_g2=signif(slope_g2,3), slope_g3=signif(slope_g3,3))])
print(LM[status=="ok", .(n=.N, min_q=min(interaction_q), n_q10=sum(interaction_q<0.10)), by=sample])
print(rbindlist(DI))
cat("DONE\n")

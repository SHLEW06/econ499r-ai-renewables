#!/usr/bin/env Rscript
# 09e_pass2_checks.R: pass 2 additions (EXPERIMENTS.md section 14.5): P1 June 2023 SEDS as main old basis,
# P2 state-specific linear trends, P9 relevance test (commercial sales) with separate VA, TX, GA slopes.
# Usage: Rscript code/R/09e_pass2_checks.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date()
need(c("data/fang_panel.csv","data/seds_old_basis.csv","data/extend_outcomes.csv", sprintf("data/raw/bls/placebo/qcew_%d_%s.csv", rep(2014:2024, 2), rep(c("312140","812910"), each=11))))
OUT <- file.path("results", date_arg, "extend"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
rows <- list()
rec <- function(block, spec, meas, y, x, mod, sample, note="", term="AI") { ct <- coeftable(mod); ci <- confint(mod)
  rows[[length(rows)+1]] <<- data.table(tag=sprintf("ext_p2_%s_%s_%s_%s_%s_%s", block, spec, meas, y, sample, term), block=block, spec=spec, ai_measure=meas, outcome=y, term=term, variable=x,
    estimate=ct[x,1], se=ct[x,2], pval=ct[x,4], ci_lo=ci[x,1], ci_hi=ci[x,2], N=mod$nobs, status="ok", note=note) }

# ---------------- Fang panel with all bases and the placebo industries ----------------
d <- fread("data/fang_panel.csv"); sb <- fread("data/seds_old_basis.csv")
d <- merge(d, sb[,.(state,year,re_bbtu_rebuilt,RETCB_arch2021)], by=c("state","year"), all.x=TRUE); setorder(d, state, year)
d[, `:=`(lnET=log(re_bbtu), lnET_rb=log(re_bbtu_rebuilt), lnET_arch=log(RETCB_arch2021), lnEPU=log(epu_composite), lnEP=log(ep_tetcd), lnGDP=log(gdp_real_musd2017),
         lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000), lnAIp=log(ai_postings), lnAIj=log(dc_jobs), trend=year-2018, t=year-2015)]
d[, lnAIp_l1 := shift(lnAIp), by=state]; d[, lnAIj_l1 := log(dc_jobs_lag1)]
fp <- data.table(fips=sprintf("%02d", c(1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56)),
                 state=c("AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"))
q <- rbindlist(lapply(c("312140","812910"), function(c) rbindlist(lapply(2014:2024, function(y) {
  x <- fread(sprintf("data/raw/bls/placebo/qcew_%d_%s.csv", y, c), colClasses=list(character="area_fips"))
  x[agglvl_code==58 & own_code==5 & grepl("000$", area_fips) & area_fips!="US000", .(fips=substr(area_fips,1,2), year=y, naics=c, emp=annual_avg_emplvl)] }))))
q <- merge(q, fp, by="fips")[, emp := fifelse(emp > 0, emp, NA_real_)]
q <- dcast(q, state + year ~ naics, value.var="emp"); setnames(q, c("312140","812910"), c("emp_distill","emp_petcare")); setorder(q, state, year)
q[, `:=`(lnDist=log(emp_distill), lnPet=log(emp_petcare))]; q[, `:=`(lnDist_l1=shift(lnDist), lnPet_l1=shift(lnPet)), by=state]
d <- merge(d, q[, .(state, year, lnDist, lnPet)], by=c("state","year"), all.x=TRUE); setorder(d, state, year)
CF <- c("lnEPU","lnEP","lnGDP","lnPOP","lnEDU"); S18 <- d[year %between% c(2018,2021)]
fang6 <- function(y, x, dd, extra=character(0)) feols(as.formula(paste(y, "~", paste(c(x, CF, extra), collapse=" + "), "| state")), data=dd, vcov="iid")

# ================ P1. June 2023 SEDS as the main old basis ================
for (mm in list(c("aipostings","lnAIp"), c("dcjobs","lnAIj"))) { a <- fang6("lnET_arch", mm[2], S18); rec("p1trend", "fang6", mm[1], "lnET_arch", mm[2], a, "51s2018_2021", "Fang col. 6, June 2023 SEDS")
  b <- fang6("lnET_arch", mm[2], S18, "trend"); rec("p1trend", "fang6trend", mm[1], "lnET_arch", mm[2], b, "51s2018_2021", "Fang col. 6 + linear trend, June 2023 SEDS"); rec("p1trend", "fang6trend", mm[1], "lnET_arch", "trend", b, "51s2018_2021", term="trend") }
for (pp in list(c("distilleries","lnDist"), c("petcare","lnPet"))) { dd <- S18[!is.na(get(pp[2]))]
  rec("p1placebo", "fang6", pp[1], "lnET_arch", pp[2], fang6("lnET_arch", pp[2], dd), sprintf("%ds2018_2021", uniqueN(dd$state)), "Fang col. 6, industry in place of AI, June 2023 SEDS")
  rec("p1placebo", "fang6trend", pp[1], "lnET_arch", pp[2], fang6("lnET_arch", pp[2], dd, "trend"), sprintf("%ds2018_2021", uniqueN(dd$state)), "same + linear trend") }
FE2 <- "state + year"; finfit <- function(y, x, dd, fe=FE2) feols(as.formula(paste(y, "~", paste(c(x, CF), collapse=" + "), "|", fe)), data=dd, vcov=~state)
for (mm in list(list("aipostings","lnAIp_l1",c(2019,2021)), list("dcjobs","lnAIj_l1",c(2015,2021)))) { dd <- d[year %between% mm[[3]] & is_dc==0]
  for (y in c("lnET","lnET_rb","lnET_arch")) rec("p1final", "twfe", mm[[1]], y, mm[[2]], finfit(y, mm[[2]], dd), sprintf("50s%d_%d", mm[[3]][1], mm[[3]][2]), "final bridge spec on the years the June 2023 release covers") }

# ================ P2. State-specific linear trends ================
TR <- "state[t] + year"
# (a) final bridge spec, full samples, current and rebuilt; archived on its short sample
for (mm in list(list("aipostings","lnAIp_l1",c(2019,2024)), list("dcjobs","lnAIj_l1",c(2015,2024)))) for (y in c("lnET","lnET_rb","lnET_arch")) {
  yr <- if (y=="lnET_arch") c(mm[[3]][1], 2021) else mm[[3]]; dd <- d[year %between% yr & is_dc==0 & !is.na(get(y)) & !is.na(get(mm[[2]]))]; sm <- sprintf("50s%d_%d", yr[1], yr[2])
  rec("p2bridge", "twfe", mm[[1]], y, mm[[2]], finfit(y, mm[[2]], dd), sm, "final bridge spec"); rec("p2bridge", "twfe-trend", mm[[1]], y, mm[[2]], finfit(y, mm[[2]], dd, TR), sm, "final bridge spec + state linear trends") }
# (b) main-spec panel: H1 core, by-type family, placebo industries
P <- main_panel(); P[, t := year - 2015]
eo <- fread("data/extend_outcomes.csv")[is_dc==0]
FAM <- c("share_wind","ln_gen_wind","add_wind_per1000","share_solar","ln_gen_solar","add_solar_per1000","share_hydro","ln_gen_hydro","add_hydro_per1000",
         "share_geo","add_geo_per1000","share_bio","ln_gen_bio","add_bio_per1000","ln_seds_woodwaste","ln_seds_biofuels","ln_seds_re_exbiomass","ln_seds_re_exbiofuels","ln_seds_re_total","ln_sales_com_pc")
P <- merge(P, eo[, c("state","year",FAM), with=FALSE], by=c("state","year")); for (v in FAM) P[, (v) := wz(get(v))]
P <- merge(P, sb[,.(state,year,re_bbtu_current,re_bbtu_rebuilt)], by=c("state","year"), all.x=TRUE)
P <- merge(P, q[, .(state, year, lnDist_l1, lnPet_l1)], by=c("state","year"), all.x=TRUE); setorder(P, state, year)
P[, `:=`(lnRE=wz(log(re_bbtu_current)), lnRE_rb=wz(log(re_bbtu_rebuilt)), lnDist_l1=wz(lnDist_l1), lnPet_l1=wz(lnPet_l1))]
mfit <- function(y, x, dd, fe) feols(as.formula(paste(y, "~", paste(c(x, CTRL4), collapse=" + "), "|", fe)), data=dd, vcov=~state)
for (y in c("ln_ec","ln_ee","renew_share", setdiff(FAM, "ln_sales_com_pc"))) for (mn in names(AIM)) { m <- AIM[[mn]]; dd <- P[!is.na(get(y)) & !is.na(get(m$lag))]
  blk <- if (y %in% c("ln_ec","ln_ee","renew_share")) "p2h1" else "p2bytype"
  rec(blk, "twfe", m$tag, y, m$lag, mfit(y, m$lag, dd, FE2), "50s", "main spec")
  r2 <- tryCatch(mfit(y, m$lag, dd, TR), error=function(e) NULL)
  if (!is.null(r2) && m$lag %in% names(coef(r2))) rec(blk, "twfe-trend", m$tag, y, m$lag, r2, "50s", "main spec + state linear trends") else
    rows[[length(rows)+1]] <- data.table(tag=sprintf("ext_p2_%s_twfe-trend_%s_%s_50s_AI", blk, m$tag, y), block=blk, spec="twfe-trend", ai_measure=m$tag, outcome=y, term="AI", status="FAILED", note="not estimable with state trends") }
PS <- P[year %between% c(2015,2024)]
for (y in c("lnRE","lnRE_rb")) for (pp in list(c("distilleries","lnDist_l1"), c("petcare","lnPet_l1"))) { dd <- PS[!is.na(get(pp[2])) & !is.na(get(y))]; sm <- sprintf("%ds2015_2024", uniqueN(dd$state))
  rec("p2placebo", "twfe", pp[1], y, pp[2], mfit(y, pp[2], dd, FE2), sm, "main spec, industry in place of AI")
  rec("p2placebo", "twfe-trend", pp[1], y, pp[2], mfit(y, pp[2], dd, TR), sm, "main spec + state linear trends, industry in place of AI") }

# ================ P9. Relevance: commercial sales per person ================
REL <- list()
relevance <- function(lab, x, dd) { d0 <- copy(dd[!is.na(ln_sales_com_pc) & !is.na(get(x))])
  a <- mfit("ln_sales_com_pc", x, d0, FE2); sdw <- sd(d0[[x]] - ave(d0[[x]], d0$state) - ave(d0[[x]], d0$year) + mean(d0[[x]]))
  ct <- coeftable(a); ci <- confint(a)
  out <- data.table(ai_measure=lab, version="pooled", slope=ct[x,1], se=ct[x,2], pval=ct[x,4], ci_lo=ci[x,1], ci_hi=ci[x,2], per_within_sd=ct[x,1]*sdw, sd_within=sdw, N=a$nobs)
  for (s in c("VA","TX","GA")) d0[, (paste0("x_", s)) := get(x) * (state==s)]
  b <- feols(as.formula(paste("ln_sales_com_pc ~", x, "+ x_VA + x_TX + x_GA +", paste(CTRL4, collapse=" + "), "| state + year")), data=d0, vcov=~state)
  cb <- coeftable(b); V <- vcov(b); df <- degrees_freedom(b, "t")
  out <- rbind(out, data.table(ai_measure=lab, version="rest of states", slope=cb[x,1], se=cb[x,2], pval=cb[x,4], ci_lo=cb[x,1]-qt(.975,df)*cb[x,2], ci_hi=cb[x,1]+qt(.975,df)*cb[x,2], per_within_sd=cb[x,1]*sdw, sd_within=sdw, N=b$nobs))
  for (s in c("VA","TX","GA")) { n <- c(x, paste0("x_", s)); e <- sum(coef(b)[n]); se_ <- sqrt(sum(V[n,n])); p <- 2*pt(-abs(e/se_), df)
    out <- rbind(out, data.table(ai_measure=lab, version=s, slope=e, se=se_, pval=p, ci_lo=e-qt(.975,df)*se_, ci_hi=e+qt(.975,df)*se_, per_within_sd=e*sdw, sd_within=sdw, N=b$nobs)) }
  out[, tag := sprintf("ext_p2_relevance_twfe_%s_lag1_ctrl4_w9901_cl-state_ln_sales_com_pc_50s_%s", lab, gsub(" ", "", version))]; REL[[lab]] <<- out }
relevance("ai518210", "jobs_lag1", P); relevance("aipostp1000", "post_lag1", P)
fwrite(rbindlist(REL), file.path(OUT, "p2_relevance.csv"))
res <- rbindlist(rows, fill=TRUE); stopifnot(!anyDuplicated(res$tag)); fwrite(res, file.path(OUT, "p2_checks.csv"))
print(res[block %like% "p1", .(block, spec, ai_measure, outcome, term, est=signif(estimate,3), p=round(pval,3), N)])
print(dcast(res[block %in% c("p2h1","p2bridge","p2placebo") & status=="ok"], block + ai_measure + outcome ~ spec, value.var="estimate"))
print(rbindlist(REL)[, .(ai_measure, version, slope=signif(slope,3), p=round(pval,3), per_sd=signif(per_within_sd,3))])
cat("DONE\n")

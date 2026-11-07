#!/usr/bin/env Rscript
# 09c_ai_impact.R: prompts/09_extend.md section 3 (EXPERIMENTS.md section 14.3, deviations X1-X2). Family "impact".
# 15 outcomes x 2 AI measures, BH q-values, lead placebo for q < 0.10, AI x restructured for outcomes that pass.
# Usage: Rscript code/R/09c_ai_impact.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date()
need(c("data/extend_outcomes.csv","data/extend_restructured.csv"))
OUT <- file.path("results", date_arg, "extend"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
P <- main_panel()
eo <- fread("data/extend_outcomes.csv")[is_dc==0]
FAM <- c("ln_sales_com_pc","ln_sales_ind_pc","ln_sales_res_pc","price_com861_c_kwh","price_ind_c_kwh","price_res_c_kwh","share_gas","share_coal","share_nuclear",
         "add_gas_per1000","add_solar_per1000","add_wind_per1000","net_imports","ln_co2_power","co2_per_mwh_t")
PRICE <- c("price_com861_c_kwh","price_ind_c_kwh","price_res_c_kwh"); CTRL3 <- setdiff(CTRL4, "price_c_kwh")
newv <- setdiff(FAM, "co2_per_mwh_t")   # co2_per_mwh_t is in the panel and already winsorized by load_panel
P <- merge(P, eo[, c("state","year",newv), with=FALSE], by=c("state","year")); setorder(P, state, year)
for (v in newv) P[, (v) := wz(get(v))]
rs <- fread("data/extend_restructured.csv")[, .(state, restructured, restructured_check_rpm2025)]
P <- merge(P, rs, by="state"); setorder(P, state, year); stopifnot(nrow(P)==550)

for (y in FAM) for (mn in names(AIM)) {
  if (y %in% PRICE) run_main("impact", y, P, AIM[[mn]], "impact", "50s", ctrl=CTRL3, model="twfe-ctrl3", note="ctrl4 without price_c_kwh (deviation X2)")
  else run_main("impact", y, P, AIM[[mn]], "impact", "50s") }
res <- rbindlist(ROWS$r, fill=TRUE); res <- add_bh(res, "impact")
pl <- res[family=="impact" & status=="ok" & qval < 0.10]
for (i in seq_len(nrow(pl))) { m <- AIM[[if (pl$ai_measure[i]=="ai518210") "jobs" else "post"]]; y <- pl$outcome[i]
  run_lead("impact", y, P, m, "impact", "50s", ctrl=if (y %in% PRICE) CTRL3 else CTRL4) }
res <- rbindlist(ROWS$r, fill=TRUE); res <- add_bh(res, "impact")
main <- res[family=="impact" & model %in% c("twfe","twfe-ctrl3")]
main[, `:=`(lead_est=NA_real_, lead_p=NA_real_, lag_est_pl=NA_real_, finding=FALSE)]
pp <- res[model %like% "^placebo"]
for (i in which(main$qval < 0.10)) { a <- pp[outcome==main$outcome[i] & ai_measure==main$ai_measure[i]]; la <- a[lag=="lag1"]; le <- a[lag=="lead1"]
  main[i, `:=`(lead_est=le$estimate, lead_p=le$pval, lag_est_pl=la$estimate, finding=clearly_smaller(la$estimate, le$estimate, le$pval))] }
# AI x restructured for outcomes that pass (finding == TRUE), main classification and check
it <- list()
for (i in which(main$finding)) { y <- main$outcome[i]; m <- AIM[[if (main$ai_measure[i]=="ai518210") "jobs" else "post"]]; ct <- if (y %in% PRICE) CTRL3 else CTRL4
  for (cl in c("restructured","restructured_check_rpm2025")) { d0 <- copy(P[!is.na(get(y)) & !is.na(get(m$lag))]); d0[, ai_x_r := get(m$lag) * get(cl)]
    mod <- fit_main(y, m$lag, d0, extra="ai_x_r", ctrl=ct); ct_ <- coeftable(mod); ci <- confint(mod)
    w <- c(1,1); names(w) <- c(m$lag,"ai_x_r"); b <- coef(mod); V <- vcov(mod); e <- sum(b[names(w)]); s <- sqrt(as.numeric(t(w)%*%V[names(w),names(w)]%*%w)); df <- degrees_freedom(mod,"t")
    it[[length(it)+1]] <- data.table(tag=sprintf("ext_impact_twfe-restr_%s_lag1_%s_w9901_cl-state_%s_50s_%s", m$tag, if (y %in% PRICE) "ctrl3" else "ctrl4", y, cl), outcome=y, ai_measure=m$tag, classification=cl,
      slope_regulated=ct_[m$lag,1], p_regulated=ct_[m$lag,4], difference_restructured=ct_["ai_x_r",1], se_difference=ct_["ai_x_r",2], p_difference=ct_["ai_x_r",4],
      slope_restructured=e, p_restructured=2*pt(-abs(e/s),df), N=mod$nobs, n_restructured=uniqueN(d0[get(cl)==1, state])) } }
fwrite(res, file.path(OUT, "s3_impact_results.csv")); fwrite(main, file.path(OUT, "s3_impact_family.csv"))
if (length(it)) fwrite(rbindlist(it), file.path(OUT, "s3_impact_restructured.csv")) else fwrite(data.table(note="no outcome passed the finding rule; no restructuring model run"), file.path(OUT, "s3_impact_restructured.csv"))
print(main[, .(outcome, ai_measure, est=signif(estimate,3), p=round(pval,4), q=round(qval,3), N, lead=signif(lead_est,3), lead_p=round(lead_p,3), lag_pl=signif(lag_est_pl,3), finding)])
if (length(it)) print(rbindlist(it)[, -1])
cat("DONE\n")

#!/usr/bin/env Rscript
# 04e4_weather_check.R
# One labeled check: ln_ec with heating and cooling degree days as controls (EXPERIMENTS.md section 0, item 31).
# Gate: reproduce the 4b ln_ec baseline first. Degree days cover the 48 contiguous states, so a same-sample row without weather sits beside it.
# Usage: Rscript code/R/04e4_weather_check.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)
args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
H1 <- "results/2026-11-02/h1/h1_core.csv"; NO <- "data/noaa_degree_days.csv"
for (f in c("code/R/load_panel.R",H1,NO)) if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "robustness"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
source("code/R/load_panel.R"); dt <- load_panel()$panel
stopifnot(nrow(dt)==550, uniqueN(dt$state)==50)
w <- fread(NO); stopifnot(nrow(w)==528, uniqueN(w$state)==48, !anyNA(w), !any(c("AK","HI") %in% w$state))
AI <- "ai_dc_per1000_lag1"; CC4 <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth")
fit <- function(d,extra=NULL) feols(as.formula(paste("ln_ec ~",paste(c(AI,CC4,extra),collapse=" + "),"| state + year")),data=d,vcov=~state)
base <- fit(dt); old <- fread(H1)[outcome=="ln_ec" & controls=="ctrl4"]
ok <- abs(coef(base)[[AI]]-old$estimate)<1e-10 && abs(se(base)[[AI]]-old$se)<1e-10 && base$nobs==old$N
gate <- data.table(check="4b ln_ec baseline reproduced",new_estimate=coef(base)[[AI]],old_estimate=old$estimate,ok=ok); print(gate); if(!ok){ cat("GATE FAILED\n"); quit(status=1) }
d48 <- merge(dt,w,by=c("state","year")); stopifnot(nrow(d48)==528, uniqueN(d48$state)==48); d48[,`:=`(hdd_k=hdd/1000,cdd_k=cdd/1000)]
rows <- list()
rec <- function(mod,spec,lab,sample,terms){ ct<-coeftable(mod); cc<-confint(mod); r2<-as.numeric(fitstat(mod,"wr2")[[1]]); for(tm in terms) rows[[length(rows)+1]] <<- data.table(tag=sprintf("rob_%s_ai518210_lag1_ctrl4_w9901_cl-state_ln_ec_%s_%s",spec,sample,tm),spec=spec,label=lab,outcome="ln_ec",coef=tm,estimate=ct[tm,1],se=ct[tm,2],pval=ct[tm,4],ci_lo=cc[tm,1],ci_hi=cc[tm,2],N=mod$nobs,within_r2=r2,vcov_type="cl-state",sample=sample,controls="ctrl4",status="ok") }
rec(base,"weather-base50","Baseline, 50 states","50s2015_2025",AI)
rec(fit(d48),"weather-base48","Same 48 states, no weather","48s2015_2025",AI)
rec(fit(d48,c("hdd_k","cdd_k")),"weather-hddcdd","48 states, + HDD and CDD","48s2015_2025",c(AI,"hdd_k","cdd_k"))
res <- rbindlist(rows); fwrite(res,file.path(OUT,"weather_check.csv")); print(res[,.(label,coef,estimate,se,pval,N,within_r2)])

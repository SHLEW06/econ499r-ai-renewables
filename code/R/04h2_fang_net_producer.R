#!/usr/bin/env Rscript
# 04h2_fang_net_producer.R
# Net-producer definitions against Fang's 76 state-years (EXPERIMENTS.md F15, F19), and which SEDS basis Fang's outcome level fits (F18).
# Gate: our definition reproduces the net-producer rows in fang_results.csv. Same specs as 04h_fang_test.R.
# Usage: Rscript code/R/04h2_fang_net_producer.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)
args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
OUT <- file.path("results", date_arg, "fang"); FR <- file.path(OUT,"fang_results.csv")
for (f in c("data/fang_panel.csv","data/fang_net_producer_definitions.csv",FR)) if (!file.exists(f)) stop("Missing input: ", f)
d <- fread("data/fang_panel.csv"); df <- fread("data/fang_net_producer_definitions.csv"); stopifnot(nrow(d)==561, nrow(df)==204, uniqueN(df$state)==51)
setorder(d,state,year)
d[, `:=`(lnET=log(re_bbtu), lnEPU=log(epu_composite), lnEP=log(ep_tetcd), lnGDP=log(gdp_real_musd2017), lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000), lnAIp=log(ai_postings), lnAIj=log(dc_jobs))]
g <- unique(df[,.(state,gen_gt_sales,teprb_gt_tetcb,elisb_negative)]); stopifnot(nrow(g)==51)
d <- merge(d,g,by="state"); setorder(d,state,year); S18 <- d[year %between% c(2018,2021)]
CF <- c("lnEPU","lnEP","lnGDP","lnPOP","lnEDU")
fit <- function(y,x,dd) feols(as.formula(paste(y,"~",paste(c(x,CF),collapse=" + "),"| state")),data=dd,vcov="iid")
DEF <- list(gen_gt_sales="EIA generation above retail sales (main)",teprb_gt_tetcb="SEDS total energy production above consumption",elisb_negative="SEDS net interstate electricity flow below zero")
M <- list(aipostings="lnAIp",dcjobs="lnAIj"); rows <- list()
rec <- function(mod,x,dn,grp,mn,term,e=NULL,s=NULL,p=NULL){ ct<-coeftable(mod); rows[[length(rows)+1]] <<- data.table(tag=sprintf("fang_netdef_%s_%s_%s_%s",dn,grp,mn,term),definition=dn,label=DEF[[dn]],group=grp,ai_measure=mn,term=term,estimate=ct[x,1],se=ct[x,2],pval=ct[x,4],N=mod$nobs,net_producer_state_years=sum(S18[[dn]]),status="ok") }
for(dn in names(DEF)) for(mn in names(M)){ x<-M[[mn]]
  for(val in 0:1){ rec(fit("lnET",x,S18[get(dn)==val]),x,dn,if(val==1) "net_producer" else "net_consumer",mn,"AI") }
  dd<-copy(S18); dd[,ai_h:=get(x)*get(dn)]; rec(feols(as.formula(paste("lnET ~",x,"+ ai_h +",paste(CF,collapse=" + "),"| state")),data=dd,vcov="iid"),"ai_h",dn,"difference",mn,"producer_minus_consumer") }
res <- rbindlist(rows)
# ---- Gate ----
old <- fread(FR)[block=="split" & spec %in% c("net_producer-high","net_producer-low") & ai_measure=="aipostings"]; new <- res[definition=="gen_gt_sales" & ai_measure=="aipostings" & term=="AI"]
chk <- all(abs(sort(old$estimate)-sort(new$estimate))<1e-10) && sort(old$N)[1]==sort(new$N)[1] && sum(S18$gen_gt_sales)==120
cat("gate: our definition reproduces fang_results.csv:",chk,"\n"); if(!chk) quit(status=1)
fwrite(res,file.path(OUT,"net_producer_check.csv")); print(res[ai_measure=="aipostings",.(definition,group,estimate,se,pval,N,net_producer_state_years)])
print(res[ai_measure=="dcjobs" & term!="AI",.(definition,group,estimate,se,pval)])
# ---- Which basis fits Fang's outcome level? Fang Table 2 constants plus slopes at our sample means ----
mA <- mean(S18$lnAIp); mE <- mean(S18$lnEPU); S18[,nc:=wind_bbtu+solar_bbtu+hydro_bbtu+geothermal_bbtu]
lev <- rbindlist(list(
  data.table(row="Fang Table 2 col. 1: constant + 0.0428 x mean ln(AI)",basis="implied by Fang",mean_lnET=11.4563+0.0428*mA),
  data.table(row="Fang Table 2 col. 2: constant + 0.0452 x mean ln(AI) - 0.0284 x mean ln(EPU)",basis="implied by Fang",mean_lnET=11.5882+0.0452*mA-0.0284*mE),
  data.table(row="Current SEDS (captured energy)",basis="current",mean_lnET=mean(S18$lnET)),
  data.table(row="Approximate old basis, k = 2.3",basis="approx. old",mean_lnET=mean(log(S18$biomass_bbtu+2.3*S18$nc))),
  data.table(row="Approximate old basis, k = 2.6",basis="approx. old",mean_lnET=mean(log(S18$biomass_bbtu+2.6*S18$nc))),
  data.table(row="Approximate old basis, k = 2.9",basis="approx. old",mean_lnET=mean(log(S18$biomass_bbtu+2.9*S18$nc)))))
lev[,`:=`(tag=paste0("fang_level_",.I),mean_ln_ai=mA,mean_ln_epu=mE)]; fwrite(lev,file.path(OUT,"seds_basis_level_check.csv")); print(lev[,.(row,mean_lnET)])

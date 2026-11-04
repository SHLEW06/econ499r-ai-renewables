#!/usr/bin/env Rscript
# 04e3_stretch.R
# Stretch goals (EXPERIMENTS.md section 10; prompts/06_finish.md section 3): shift-share IV, then broadband and R&D moderation.
# Zhang spec throughout: ctrl4, AI(t-1) winsorized, two-way FE, clustered by state, 50 states. Hansen threshold: recorded as not run.
# Usage: Rscript code/R/04e3_stretch.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)
args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
BASE<-file.path("results",date_arg,"robustness","robustness.csv")
for (f in c("code/R/load_panel.R","data/fang_panel.csv","data/acs_broadband.csv","data/nsf_state_rd.csv",BASE)) if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "stretch"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
source("code/R/load_panel.R"); dt <- load_panel()$panel; stopifnot(nrow(dt)==550,uniqueN(dt$state)==50)
AI<-"ai_dc_per1000_lag1"; CC4<-c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth"); CTRL4<-paste(CC4,collapse=" + ")
setorder(dt,state,year); b0<-dt[year==2015,.(state,cap_total_2015=cap_total_mw)]; dt<-merge(dt,b0,by="state"); dt[,new_renew_per_1000mw:=new_renew_mw/cap_total_2015*1000]
Y<-c("ln_ec","ln_ee","renew_share","new_renew_mw"); CL<-~state
rows<-list(); add<-function(block,spec,y,term,e,s,p,lo,hi,N,sample,status="ok",note="") rows[[length(rows)+1]]<<-data.table(tag=sprintf("stretch_%s_%s_ai518210_lag1_ctrl4_w9901_cl-state_%s_%s_%s",block,spec,y,sample,term),block=block,spec=spec,outcome=y,term=term,estimate=e,se=s,pval=p,ci_lo=lo,ci_hi=hi,N=N,sample=sample,status=status,note=note)

# ---- Gate: the baseline on this panel must match the 4e rows ----
rb<-fread(BASE); g<-list()
for(y in Y){ m<-feols(as.formula(paste(y,"~",AI,"+",CTRL4,"| state + year")),dt,vcov=CL); o<-rb[spec=="base"&outcome==y]; stopifnot(nrow(o)==1); g[[y]]<-data.table(outcome=y,new=coef(m)[[AI]],old=o$estimate,new_se=se(m)[[AI]],old_se=o$se,ok=abs(coef(m)[[AI]]-o$estimate)<1e-8&abs(se(m)[[AI]]-o$se)<1e-8) }
g<-rbindlist(g); fwrite(g,file.path(OUT,"gate.csv")); print(g); if(!all(g$ok)){cat("GATE FAILED\n");quit(status=1)}; cat("GATE PASSED\n")

# ---- Instrument ----
f<-fread("data/fang_panel.csv"); j<-rbind(f[year==2015,.(state,year=2014L,jobs=dc_jobs_lag1)],f[year<=2024,.(state,year,jobs=dc_jobs)]); stopifnot(!anyNA(j$jobs),uniqueN(j$state)==51)
nat<-j[,.(N=sum(jobs)),by=year]; j<-merge(j,nat,by="year"); j[,N_loo:=N-jobs]
mk<-function(by){ s<-j[year==by,.(state,share=jobs/N,base=N_loo)]; z<-merge(j[,.(state,year,N_loo)],s,by="state"); z[,.(state,ai_year=year,Z=1000*share*N_loo/base)] }
z15<-mk(2015); z14<-mk(2014); setnames(z14,"Z","Z14")
dt[,ai_year:=year-1L]; dt<-merge(dt,z15,by=c("state","ai_year"),all.x=TRUE); dt<-merge(dt,z14,by=c("state","ai_year"),all.x=TRUE); stopifnot(!anyNA(dt$Z),!anyNA(dt$Z14)); setorder(dt,state,year)
cat("Z: mean",mean(dt$Z)," within-state SD",sd(dt$Z-ave(dt$Z,dt$state))," corr with AI lag, within state",cor(dt$Z-ave(dt$Z,dt$state),dt[[AI]]-ave(dt[[AI]],dt$state)),"\n")
for(zn in c("Z","Z14")){ sp<-if(zn=="Z") "base2015" else "base2014"
  fs<-feols(as.formula(paste(AI,"~",zn,"+",CTRL4,"| state + year")),dt,vcov=CL); ct<-coeftable(fs); ci<-confint(fs); add("iv",sp,"first_stage","Z_on_AI",ct[zn,1],ct[zn,2],ct[zn,4],ci[zn,1],ci[zn,2],fs$nobs,"50s2015_2025",note="first stage: AI(t-1) on the instrument")
  fsf<-as.numeric(wald(fs,zn,print=FALSE)$stat); add("iv",sp,"first_stage","first_stage_F_clustered",fsf,NA,as.numeric(wald(fs,zn,print=FALSE)$p),NA,NA,fs$nobs,"50s2015_2025",note="F below 10 means the IV is uninformative")
  # KP F: with one instrument, fixest's clustered first-stage Wald. KP rank LM: fixest's kpr errors with clustering here, so it's computed directly.
  # With one endogenous variable and one instrument, it is the cluster-robust score test of pi = 0, after partialling out controls and FE.
  iv0<-feols(as.formula(paste("ln_ec ~",CTRL4,"| state + year |",AI,"~",zn)),dt,vcov=CL); kf<-fitstat(iv0,"ivwald",simplify=FALSE)[[1]]; add("iv",sp,"first_stage","KP_F",as.numeric(kf$stat),NA,as.numeric(kf$p),NA,NA,iv0$nobs,"50s2015_2025",note="cluster-robust first-stage F; with one instrument this is the Kleibergen-Paap F")
  xt<-resid(feols(as.formula(paste(AI,"~",CTRL4,"| state + year")),dt)); zt<-resid(feols(as.formula(paste(zn,"~",CTRL4,"| state + year")),dt)); sc<-tapply(xt*zt,dt$state,sum); lm_kp<-sum(xt*zt)^2/sum(sc^2); add("iv",sp,"first_stage","KP_rank_LM",lm_kp,NA,pchisq(lm_kp,1,lower.tail=FALSE),NA,NA,iv0$nobs,"50s2015_2025",note="Kleibergen-Paap rank LM, under-identification; computed directly: cluster-robust score test of pi = 0")
  for(y in Y){ rf<-feols(as.formula(paste(y,"~",zn,"+",CTRL4,"| state + year")),dt,vcov=CL); ct<-coeftable(rf); ci<-confint(rf); add("iv",sp,y,"reduced_form",ct[zn,1],ct[zn,2],ct[zn,4],ci[zn,1],ci[zn,2],rf$nobs,"50s2015_2025")
    iv<-feols(as.formula(paste(y,"~",CTRL4,"| state + year |",AI,"~",zn)),dt,vcov=CL); ct<-coeftable(iv); ci<-confint(iv); nm<-paste0("fit_",AI); add("iv",sp,y,"iv_second_stage",ct[nm,1],ct[nm,2],ct[nm,4],ci[nm,1],ci[nm,2],iv$nobs,"50s2015_2025")
    ols<-feols(as.formula(paste(y,"~",AI,"+",CTRL4,"| state + year")),dt,vcov=CL); ct<-coeftable(ols); ci<-confint(ols); add("iv",sp,y,"ols_same_sample",ct[AI,1],ct[AI,2],ct[AI,4],ci[AI,1],ci[AI,2],ols$nobs,"50s2015_2025") } }

# ---- Moderators ----
ac<-fread("data/acs_broadband.csv"); rd<-fread("data/nsf_state_rd.csv")
dt<-merge(dt,ac[,.(state,year,broadband_pct)],by=c("state","year"),all.x=TRUE); dt<-merge(dt,rd[,.(state,year,rd_total_musd)],by=c("state","year"),all.x=TRUE); dt[,rd_share_pct:=100*rd_total_musd/gdp_nom_musd]
run_mod<-function(mv,dd,sample,lab,unit){ dd<-copy(dd); stopifnot(!anyNA(dd[[mv]])); dd[,`:=`(ai_c=get(AI)-mean(get(AI)),m_c=get(mv)-mean(get(mv)))]; dd[,ai_x_m:=ai_c*m_c]; q<-quantile(dd$m_c,c(.25,.75)); qr<-quantile(dd[[mv]],c(.25,.75))
  for(y in Y){ mod<-feols(as.formula(paste(y,"~ ai_c + m_c + ai_x_m +",CTRL4,"| state + year")),dd,vcov=CL); ct<-coeftable(mod); ci<-confint(mod); V<-vcov(mod); df<-degrees_freedom(mod,"t"); tq<-qt(.975,df)
    for(p in list(c("ai_x_m","interaction"),c("m_c","main_effect"),c("ai_c","AI_at_mean"))) add("mod",lab,y,p[2],ct[p[1],1],ct[p[1],2],ct[p[1],4],ci[p[1],1],ci[p[1],2],mod$nobs,sample,note=unit)
    for(i in 1:2){ e<-ct["ai_c",1]+q[[i]]*ct["ai_x_m",1]; s<-sqrt(V["ai_c","ai_c"]+q[[i]]^2*V["ai_x_m","ai_x_m"]+2*q[[i]]*V["ai_c","ai_x_m"]); add("mod",lab,y,c("AI_slope_p25","AI_slope_p75")[i],e,s,2*pt(-abs(e/s),df),e-tq*s,e+tq*s,mod$nobs,sample,note=sprintf("moderator = %.3f %s",qr[[i]],unit)) } } }
d1<-dt[year %between% c(2016,2024)&year!=2020]; stopifnot(nrow(d1)==400); run_mod("broadband_pct",d1,"50s2016_2024no2020","broadband","percent of households")
d2<-dt[year %between% c(2017,2023)]; stopifnot(nrow(d2)==350); run_mod("rd_share_pct",d2,"50s2017_2023","rdshare","R&D as percent of nominal GDP")
add("hansen","threshold","all","not_run",NA,NA,NA,NA,NA,NA_integer_,"none",status="NOT_RUN",note="Dropped by team decision 2026-11-04: the AI squared model in 4b covers nonlinearity, and all Lind-Mehlum tests failed there")
add("mod","epu","all","see_fang_test",NA,NA,NA,NA,NA,NA_integer_,"none",status="NOT_RUN",note="AI x EPU was run in the Fang test, results/<date>/fang/")
res<-rbindlist(rows,fill=TRUE); stopifnot(!anyDuplicated(res$tag)); fwrite(res,file.path(OUT,"stretch.csv")); cat(nrow(res),"rows\nDONE\n")

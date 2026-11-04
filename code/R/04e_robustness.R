#!/usr/bin/env Rscript
# 04e_robustness.R
# Phase 4e robustness: gate, then A1-A8, P1, P2 and the all-ownership row (EXPERIMENTS.md section 9). No stretch goals here.
# Gate: reproduce the 4b baselines and 4d SLX before anything else; stop if they do not match.
# Usage: Rscript code/R/04e_robustness.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)

args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
H1 <- "results/2026-11-02/h1"; H3 <- "results/2026-11-03/h3"
INPUTS <- c("code/R/load_panel.R","data/out/W_border_binary.csv","data/out/state_centroids_land.csv","data/lbnl_rps_targets.csv","data/ai_allown_518210.csv",
            file.path(H1,c("h1_core.csv","h1_extras.csv","se_check.csv","dynamics.csv")),file.path(H3,"h3_slx.csv"))
for (f in INPUTS) if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "robustness"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
RPS_FILE <- "data/lbnl_rps_targets.csv"

source("code/R/load_panel.R"); dt <- load_panel()$panel
stopifnot(nrow(dt)==550, uniqueN(dt$state)==50)
AI <- "ai_dc_per1000_lag1"; CC4 <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth"); CTRL4 <- paste(CC4,collapse=" + ")
CORE <- c("ln_ec","ln_ee","renew_share"); NRM <- c("new_renew_mw","new_renew_per_1000mw"); ALL5 <- c(CORE,NRM)

# ---- Derived columns ----
setorder(dt,state,year)
dt <- merge(dt, dt[year==2015,.(state,cap_total_2015=cap_total_mw)], by="state"); setorder(dt,state,year)
dt[, new_renew_per_1000mw := new_renew_mw/cap_total_2015*1000]
# Lead: load_panel leaves it unwinsorized, so apply the same 1/99 pooled rule as lag1.
dt[, ai_lead1_w := winsorize(ai_dc_per1000_lead1)]
# Distributed lags from lag1, so 2014 is usable (load_panel's lag2/lag3 start from 2015 and are unwinsorized).
dt[, ai_l2 := shift(get(AI),1), by=state]; dt[, ai_l3 := shift(get(AI),2), by=state]
cen <- fread("data/out/state_centroids_land.csv"); dt <- merge(dt, cen[,.(state=USPS,lat,lon)], by="state", all.x=TRUE)
stopifnot(!anyNA(dt$lat)); setorder(dt,state,year)

rows <- list()
add <- function(spec,outcome,coef,est,se,p,N,vcov_type,sample,tag,status="ok",note="",lo=NA_real_,hi=NA_real_)
  rows[[length(rows)+1]] <<- data.table(tag=tag,spec=spec,outcome=outcome,coef=coef,estimate=est,se=se,pval=p,ci_lo=lo,ci_hi=hi,N=N,vcov_type=vcov_type,sample=sample,controls="ctrl4",status=status,note=note)
mk_tag <- function(spec,lag,se,y,sample,w="w9901") sprintf("rob_%s_ai518210_%s_ctrl4_%s_%s_%s_%s",spec,lag,w,se,y,sample)
fm <- function(y,x=AI,extra=NULL) as.formula(paste(y,"~",paste(c(x,CC4,extra),collapse=" + "),"| state + year"))
twfe <- function(y,d,x=AI,vc=~state,extra=NULL,...) feols(fm(y,x,extra),data=d,vcov=vc,...)
rec <- function(m,spec,y,sample,lag="lag1",se="cl-state",x=AI,note="",vtype="CRV1-state"){
  ct<-coeftable(m); ci<-confint(m)
  add(spec,y,x,ct[x,1],ct[x,2],ct[x,4],m$nobs,vtype,sample,mk_tag(spec,lag,se,y,sample),note=note,lo=ci[x,1],hi=ci[x,2]) ; invisible(m) }

W_read <- function(p){r<-fread(p); W<-as.matrix(r[,-1]); rownames(W)<-colnames(W)<-r[[1]]; W}
keep48 <- sort(unique(dt[!state %in% c("AK","HI"),state]))
# Same order as 4d: W rows kept in file order, subset, row-standardized.
Wb <- W_read("data/out/W_border_binary.csv"); st48 <- rownames(Wb)[!rownames(Wb) %in% c("AK","HI")]
Wb <- Wb[st48,st48]; stopifnot(all(rowSums(Wb)>0)); Wb <- Wb/rowSums(Wb)
slx_data <- function(W,st){ d<-copy(dt[state %in% st])[order(year,match(state,st))]
  for(v in c(AI,CC4)){ nc<-paste0("W_",v); d[,(nc):=0.0]
    for(y in unique(d$year)){ s<-d[year==y][order(match(state,st))]; stopifnot(identical(s$state,st)); d[year==y,(nc):=as.numeric(W%*%s[[v]])] } }
  d }
dslx <- slx_data(Wb,st48)
slx <- function(y){ feols(as.formula(paste(y,"~",AI,"+ W_",AI,"+",CTRL4,"+",paste(paste0("W_",CC4),collapse=" + "),"| state + year",sep="")),data=dslx,vcov=~state) }

# ================ GATE ================
cat("=== GATE ===\n")
core<-fread(file.path(H1,"h1_core.csv")); ex<-fread(file.path(H1,"h1_extras.csv")); se<-fread(file.path(H1,"se_check.csv")); dyn<-fread(file.path(H1,"dynamics.csv")); s4d<-fread(file.path(H3,"h3_slx.csv"))
g<-list(); TOL<-1e-8
gchk<-function(lbl,new_e,new_s,old_e,old_s) g[[length(g)+1]]<<-data.table(check=lbl,new_estimate=new_e,old_estimate=old_e,new_se=new_s,old_se=old_s,ok=abs(new_e-old_e)<TOL&abs(new_s-old_s)<TOL)
for(y in CORE){ m<-twfe(y,dt); ct<-coeftable(m); o<-core[tag==sprintf("h1_twfe_ai518210_lag1_ctrl4_w9901_cl-state_%s_50s2015_2025",y)]; stopifnot(nrow(o)==1)
  gchk(paste0("4b core ",y),ct[AI,1],ct[AI,2],o$estimate,o$se)
  md<-feols(fm(y),data=dt,vcov="DK",panel.id=~state+year); ctd<-coeftable(md); o<-se[tag==sprintf("h1_twfe_ai518210_lag1_ctrl4_w9901_dk_%s_50s2015_2025",y)]; stopifnot(nrow(o)==1)
  gchk(paste0("4b DK ",y),ctd[AI,1],ctd[AI,2],o$estimate,o$se) }
for(p in list(list(y="new_renew_mw",t="h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025"),
              list(y="fossil_to_renew",t="h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_fossil_to_renew_50s2015_2025"),
              list(y="new_renew_per_1000mw",t="h1x_rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per1000mw_50s2015_2025"))){
  m<-twfe(p$y,dt); ct<-coeftable(m); o<-ex[tag==p$t]; stopifnot(nrow(o)==1); gchk(paste0("4b ",p$y),ct[AI,1],ct[AI,2],o$estimate,o$se) }
for(y in CORE){ m<-slx(y); ct<-coeftable(m); o<-s4d[outcome==y&W_version=="border48"]; stopifnot(nrow(o)==1)
  gchk(paste0("4d SLX border48 b1 ",y),ct[AI,1],ct[AI,2],o$b1,o$se_b1)
  gchk(paste0("4d SLX border48 theta1 ",y),ct[paste0("W_",AI),1],ct[paste0("W_",AI),2],o$theta1,o$se_theta1) }
# 4b long difference (version with the bug) must reproduce before it is corrected
ld_build<-function(fix){ a<-dt[year==2015,.(state,Y15_renew_share=renew_share,Y15_ln_ec=ln_ec,Y15_ln_ee=ln_ee,ai_2014=get(AI),g=ln_gdp_pc,pr=price_c_kwh,mf=manuf_share,po=population)]
  b<-dt[year==2025,.(state,Y25_renew_share=renew_share,Y25_ln_ec=ln_ec,Y25_ln_ee=ln_ee,ai_end=if(fix) get(AI) else ai_dc_per1000,g2=ln_gdp_pc,pr2=price_c_kwh,mf2=manuf_share,po2=population)]
  l<-merge(a,b,by="state"); l[,`:=`(renew_share=Y25_renew_share-Y15_renew_share,ln_ec=Y25_ln_ec-Y15_ln_ec,ln_ee=Y25_ln_ee-Y15_ln_ee,dAI=ai_end-ai_2014,dlngdp=g2-g,dprice=pr2-pr,dmanuf=mf2-mf,dpop=log(po2/po))]; l[complete.cases(l[,.(dAI,dlngdp,dprice,dmanuf,dpop)])] }
lb<-ld_build(FALSE)
for(y in CORE){ m<-lm(as.formula(paste(y,"~ dAI + dlngdp + dprice + dmanuf + dpop")),data=lb); ct<-summary(m)$coefficients
  o<-dyn[tag==sprintf("dyn_longdiff_ai518210_ctrl4_w9901_rob_%s_50s2015_2025",y)]; stopifnot(nrow(o)==1); gchk(paste0("4b long diff (bug) ",y),ct["dAI",1],ct["dAI",2],o$estimate,o$se) }
g<-rbindlist(g); fwrite(g,file.path(OUT,"gate.csv")); print(g[,.(check,new_estimate,old_estimate,ok)])
if(!all(g$ok)){ cat("\nGATE FAILED: stopping before any new model.\n"); print(g[ok==FALSE]); quit(status=1) }
cat(sprintf("\nGATE PASSED: %d of %d checks match within %g\n\n",sum(g$ok),nrow(g),TOL))

# ================ BASELINE ================
for(y in ALL5) rec(twfe(y,dt),"base",y,"50s2015_2025")

# A1 swap outcome
for(y in c("fossil_to_renew","seds_mmbtu_pc")){ d<-dt[!is.na(get(y))]; ss<-if(y=="seds_mmbtu_pc") "50s2015_2024" else "50s2015_2025"
  m<-rec(twfe(y,d),"swapY",y,ss); stopifnot(m$nobs==if(y=="seds_mmbtu_pc") 500 else 550) }
# A2 swap cause
for(y in CORE) add("swapAI-dcmw",y,"data_center_mw",NA,NA,NA,NA_integer_,"","50s2015_2025",mk_tag("swapAI-dcmw","lag1","cl-state",y,"50s2015_2025"),status="NOT_RUN",note="not available: Phase 2 built no state-year data-center MW series; Epoch covers large AI campuses only and has no 2015-2025 state panel")
# A3 samples
for(y in ALL5){ m<-rec(twfe(y,dt[year!=2020]),"drop2020",y,"50s2015_2025no2020"); stopifnot(m$nobs==500)
  m<-rec(twfe(y,dt[!state %in% c("AK","HI")]),"dropAKHI",y,"48s2015_2025"); stopifnot(m$nobs==528)
  m<-rec(twfe(y,dt[state!="VA"]),"dropVA",y,"49s2015_2025noVA"); stopifnot(m$nobs==539) }
# A4 border SLX
for(y in ALL5){ m<-slx(y); ct<-coeftable(m); V<-vcov(m); th<-paste0("W_",AI); ci<-confint(m)
  rec(m,"slxborder",y,"48s2015_2025",note="b1: own AI")
  add("slxborder",y,"theta1",ct[th,1],ct[th,2],ct[th,4],m$nobs,"CRV1-state","48s2015_2025",mk_tag("slxborder-theta","lag1","cl-state",y,"48s2015_2025"),lo=ci[th,1],hi=ci[th,2])
  tot<-ct[AI,1]+ct[th,1]; st<-sqrt(sum(V[c(AI,th),c(AI,th)])); tq<-qt(.975,47)
  add("slxborder",y,"total",tot,st,2*pt(-abs(tot/st),47),m$nobs,"CRV1-state","48s2015_2025",mk_tag("slxborder-total","lag1","cl-state",y,"48s2015_2025"),lo=tot-tq*st,hi=tot+tq*st) }
# A5 RPS control: LBNL current RPS/CES schedule (EXPERIMENTS.md section 0 item 21)
r<-fread(RPS_FILE); stopifnot(all(c("state","year","target_pct","rps_target_pct","target_pct_ed2023") %in% names(r)),!anyDuplicated(r[,.(state,year)]))
d<-merge(dt,r[,.(state,year,target_pct,rps_target_pct,target_pct_ed2023)],by=c("state","year"),all.x=TRUE); stopifnot(nrow(d)==550,!anyNA(d$target_pct),!anyNA(d$target_pct_ed2023))
rps_run<-function(spec,y,dd,ctl,sample,n,note){ m<-twfe(y,dd,extra=ctl); stopifnot(m$nobs==n); rec(m,spec,y,sample,note=note)
  ct<-coeftable(m); ci<-confint(m); add(spec,y,ctl,ct[ctl,1],ct[ctl,2],ct[ctl,4],m$nobs,"CRV1-state",sample,mk_tag(paste0(spec,"-coef"),"lag1","cl-state",y,sample),note=paste("coefficient on the RPS control;",note),lo=ci[ctl,1],hi=ci[ctl,2]) }
for(y in ALL5){ rps_run("rps",y,d,"target_pct","50s2015_2025",550,"LBNL current RPS/CES schedule: larger of RPS and CES")
  rps_run("rps-rpsonly",y,d,"rps_target_pct","50s2015_2025",550,"check: RPS target only")
  rps_run("rps-ed2023",y,d,"target_pct_ed2023","50s2015_2025",550,"check: June 2023 edition; its 2024-2025 values were planned levels when published")
  rps_run("rps-ed2023-to2023",y,d[year<=2023],"target_pct_ed2023","50s2015_2023",450,"check: June 2023 edition, 2015-2023")
  rps_run("rps-to2023",y,d[year<=2023],"target_pct","50s2015_2023",450,"LBNL current RPS/CES schedule on 2015-2023, to compare with the 2023 edition")
  rps_run("rps-noNY",y,d[state!="NY"],"target_pct","49s2015_2025noNY",539,"check: without NY, whose series breaks in 2018") }
# Added 2026-11-04: AI with all ownerships in the numerator (EXPERIMENTS.md section 0 item 24)
ao<-fread("data/ai_allown_518210.csv"); stopifnot(!anyDuplicated(ao[,.(state,year)]))
da<-merge(dt,ao[,.(state,year,ai_allown_per1000_lag1)],by=c("state","year"),all.x=TRUE); stopifnot(nrow(da)==550,!anyNA(da$ai_allown_per1000_lag1))
da[,ai_allown_lag1_w:=winsorize(ai_allown_per1000_lag1)]
AO<-"ai_allown_lag1_w"
for(y in c(CORE,"new_renew_mw")){ m<-twfe(y,da,x=AO); ct<-coeftable(m); ci<-confint(m); stopifnot(m$nobs==550)
  add("allown",y,AO,ct[AO,1],ct[AO,2],ct[AO,4],m$nobs,"CRV1-state","50s2015_2025",sprintf("rob_allown_ai518210allown_lag1_ctrl4_w9901_cl-state_%s_50s2015_2025",y),note="check: private + published government 518210 jobs; suppressed government rows count as 0",lo=ci[AO,1],hi=ci[AO,2]) }
# Added 2026-11-04: new_renew_mw with Gavins Point held in NE in every year (EXPERIMENTS.md section 0 item 29).
# EIA's state file counts this 132.3 MW plant in SD in 2016-2017. The panel keeps EIA's data as published.
GP<-132.3; pr<-fread("data/out/state_panel_2015_2025.csv")[is_dc==0,.(state,year,nr=new_renew_mw)]
pr[,chk:=winsorize(nr)]; g0<-merge(dt[,.(state,year,new_renew_mw)],pr,by=c("state","year")); stopifnot(nrow(g0)==550,max(abs(g0$new_renew_mw-g0$chk))<1e-9)
pr[,nr_gp:=nr]; pr[state=="NE"&year==2016,nr_gp:=nr+GP]; pr[state=="NE"&year==2018,nr_gp:=nr-GP]; pr[state=="SD"&year==2016,nr_gp:=nr-GP]; pr[state=="SD"&year==2018,nr_gp:=nr+GP]
stopifnot(sum(pr$nr!=pr$nr_gp)==4); cat("Gavins Point cells:\n"); print(pr[nr!=nr_gp,.(state,year,published=nr,held_in_NE=nr_gp)])
pr[,new_renew_gp:=winsorize(nr_gp)]; dg<-merge(dt,pr[,.(state,year,new_renew_gp)],by=c("state","year")); stopifnot(nrow(dg)==550)
m<-twfe("new_renew_gp",dg); ct<-coeftable(m); ci<-confint(m); add("gavins-ne","new_renew_mw",AI,ct[AI,1],ct[AI,2],ct[AI,4],m$nobs,"CRV1-state","50s2015_2025",mk_tag("gavins-ne","lag1","cl-state","new_renew_mw","50s2015_2025"),note="check: Gavins Point held in NE in every year; NE and SD adjusted in 2016 and 2018",lo=ci[AI,1],hi=ci[AI,2])
cat(sprintf("Winsor cutoffs: published [%.1f, %.1f]; held in NE [%.1f, %.1f]\n",quantile(pr$nr,.01),quantile(pr$nr,.99),quantile(pr$nr_gp,.01),quantile(pr$nr_gp,.99)))
# A6 placebo, plus lag1 on the same observations
dp<-dt[year<=2024&!is.na(ai_lead1_w)]; stopifnot(nrow(dp)==496)
for(y in ALL5){ m<-rec(twfe(y,dp,x="ai_lead1_w"),"placebo",y,"50s2015_2024",lag="lead1",x="ai_lead1_w"); stopifnot(m$nobs==496)
  rec(twfe(y,dp),"placebo-compare",y,"50s2015_2024",note="AI(t-1) on the placebo sample")
  # Diagnostics: is the result due to winsorizing the lead? Does the lead survive next to the lag?
  rec(twfe(y,dp,x="ai_dc_per1000_lead1"),"placebo-nowins",y,"50s2015_2024",lag="lead1",x="ai_dc_per1000_lead1",note="diagnostic: lead not winsorized")
  mj<-feols(fm(y,c("ai_lead1_w",AI)),data=dp,vcov=~state); cj<-coeftable(mj); ij<-confint(mj)
  for(x in c("ai_lead1_w",AI)) add("placebo-joint",y,x,cj[x,1],cj[x,2],cj[x,4],mj$nobs,"CRV1-state","50s2015_2024",mk_tag(if(x==AI) "placebo-joint-lag" else "placebo-joint-lead","lead1lag1","cl-state",y,"50s2015_2024"),note="diagnostic: lead and lag in one model",lo=ij[x,1],hi=ij[x,2]) }
wc<-dp[,.(a=ai_lead1_w-mean(ai_lead1_w),b=get(AI)-mean(get(AI))),by=state]; cat(sprintf("Within-state corr(lead, lag): %.3f\n",cor(wc$a,wc$b)))
# A7 DK (labeled sensitivity)
for(y in ALL5) rec(feols(fm(y),data=dt,vcov="DK",panel.id=~state+year),"dk",y,"50s2015_2025",se="dk",vtype="DK",note="sensitivity only; T=11")
# A8 Conley (labeled check)
cchk<-list()
for(k in c(500,1000)) for(y in ALL5){ m0<-feols(fm(y),data=dt)
  raw<-suppressWarnings(vcov_conley(m0,lat=~lat,lon=~lon,cutoff=k,distance="spherical",vcov_fix=FALSE))
  v<-suppressWarnings(vcov_conley(m0,lat=~lat,lon=~lon,cutoff=k,distance="spherical",vcov_fix=TRUE))
  me<-min(eigen(raw,only.values=TRUE)$values); bad<-me<0
  ct<-coeftable(m0,vcov=v); ci<-confint(m0,vcov=v)
  cchk[[length(cchk)+1]]<-data.table(outcome=y,cutoff_km=k,min_eigenvalue=me,not_pd=bad,se_raw=sqrt(raw[AI,AI]),se_fixed=sqrt(v[AI,AI]),se_cluster=sqrt(vcov(m0,vcov=~state)[AI,AI]))
  add(sprintf("conley%d",k),y,AI,ct[AI,1],ct[AI,2],ct[AI,4],m0$nobs,sprintf("Conley-%dkm",k),"50s2015_2025",mk_tag(sprintf("conley%d",k),"lag1",sprintf("conley%d",k),y,"50s2015_2025"),note=if(bad) "check only; UNRELIABLE: VCOV not positive definite, eigenvalue-fixed" else "check only",lo=ci[AI,1],hi=ci[AI,2]) }
fwrite(rbindlist(cchk),file.path(OUT,"conley_vcov_check.csv"))
# Does fixest's Conley cover the same state across years? A tiny cutoff should then behave like clustering by state.
ck<-rbindlist(lapply(CORE,function(y){ m0<-feols(fm(y),data=dt); data.table(outcome=y,se_conley_1km=sqrt(suppressWarnings(vcov_conley(m0,lat=~lat,lon=~lon,cutoff=1,distance="spherical"))[AI,AI]),se_cluster=sqrt(vcov(m0,vcov=~state)[AI,AI]),se_cluster_noadj=sqrt(vcov(m0,vcov=~state,ssc=ssc(K.adj=FALSE,G.adj=FALSE))[AI,AI])) }))
print(ck); fwrite(ck,file.path(OUT,"conley_check.csv"))
ce<-unique(dt[,.(state,lat,lon)]); hav<-function(a,b,c,d){R<-6371;p<-pi/180;2*R*asin(sqrt(sin((c-a)*p/2)^2+cos(a*p)*cos(c*p)*sin((d-b)*p/2)^2))}
DM<-outer(1:50,1:50,function(i,j) hav(ce$lat[i],ce$lon[i],ce$lat[j],ce$lon[j])); diag(DM)<-NA
nb<-data.table(cutoff_km=c(500,1000),mean_states_within=c(mean(rowSums(DM<500,na.rm=TRUE)),mean(rowSums(DM<1000,na.rm=TRUE))),states_with_none=c(sum(rowSums(DM<500,na.rm=TRUE)==0),sum(rowSums(DM<1000,na.rm=TRUE)==0)))
print(nb); fwrite(nb,file.path(OUT,"conley_neighbors.csv"))
# P1 distributed lags 2017-2025
dl<-dt[!is.na(ai_l3)]; stopifnot(nrow(dl)==450,min(dl$year)==2017)
for(y in ALL5){ m<-feols(fm(y,c(AI,"ai_l2","ai_l3")),data=dl,vcov=~state); ct<-coeftable(m); V<-vcov(m); nm<-c(AI,"ai_l2","ai_l3"); ci<-confint(m); S<-"50s2017_2025"
  for(k in 1:3) add("distlag",y,nm[k],ct[nm[k],1],ct[nm[k],2],ct[nm[k],4],m$nobs,"CRV1-state",S,sprintf("dyn_twfe_ai518210_lag%d_ctrl4_w9901_cl-state_%s_%s",k,y,S),lo=ci[nm[k],1],hi=ci[nm[k],2])
  s<-sum(ct[nm,1]); ses<-sqrt(sum(V[nm,nm])); tq<-qt(.975,49)
  add("distlag",y,"sum_lag1to3",s,ses,2*pt(-abs(s/ses),49),m$nobs,"CRV1-state",S,sprintf("dyn_twfe_ai518210_lag1to3sum_ctrl4_w9901_cl-state_%s_%s",y,S),note="delta-method SE; df = 49",lo=s-tq*ses,hi=s+tq*ses)
  m1<-feols(fm(y),data=dl,vcov=~state); ct1<-coeftable(m1); ci1<-confint(m1)
  add("distlag-compare",y,AI,ct1[AI,1],ct1[AI,2],ct1[AI,4],m1$nobs,"CRV1-state",S,sprintf("dyn_twfe-compare_ai518210_lag1_ctrl4_w9901_cl-state_%s_%s",y,S),note="t-1 alone on the same sample",lo=ci1[AI,1],hi=ci1[AI,2]) }
# P2 corrected long difference, plus 4b's version labeled
lf<-ld_build(TRUE); stopifnot(nrow(lf)==50)
for(y in CORE){ m<-feols(as.formula(paste(y,"~ dAI + dlngdp + dprice + dmanuf + dpop")),data=lf,vcov="hetero"); ct<-coeftable(m); ci<-confint(m)
  add("longdiff",y,"dAI_2014_2024",ct["dAI",1],ct["dAI",2],ct["dAI",4],m$nobs,"HC1","50 states, 2015-2025",sprintf("dyn_longdiff-fixed_ai518210_longdiff_ctrl4_w9901_hc1_%s_50s2015_2025",y),note="corrected: dAI = 2014->2024",lo=ci["dAI",1],hi=ci["dAI",2])
  mi<-summary(lm(as.formula(paste(y,"~ dAI + dlngdp + dprice + dmanuf + dpop")),data=lf))$coefficients
  add("longdiff",y,"dAI_2014_2024",mi["dAI",1],mi["dAI",2],mi["dAI",4],nrow(lf),"classical","50 states, 2015-2025",sprintf("dyn_longdiff-fixed_ai518210_longdiff_ctrl4_w9901_classical_%s_50s2015_2025",y),note="corrected dAI; classical SE, comparable to 4b")
  o<-dyn[tag==sprintf("dyn_longdiff_ai518210_ctrl4_w9901_rob_%s_50s2015_2025",y)]
  add("longdiff-4b-bug",y,"dAI_as_run",o$estimate,o$se,o$pval,o$N,"classical (mislabeled HC0)","46 states",o$tag,note="4b version with the bug: dAI is really 2014->2025; copied from results/2026-11-02/h1/dynamics.csv",lo=o$ci_lo,hi=o$ci_hi) }

res<-rbindlist(rows,fill=TRUE); stopifnot(!anyDuplicated(res$tag))
fwrite(res,file.path(OUT,"robustness.csv"))
cat(sprintf("robustness.csv: %d rows (%s)\n",nrow(res),paste(names(table(res$status)),table(res$status),collapse=", ")))
cat("DONE\n")

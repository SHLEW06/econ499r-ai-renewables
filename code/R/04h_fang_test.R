#!/usr/bin/env Rscript
# 04h_fang_test.R
# Fang, Lee & Li (2025) test, Part B (EXPERIMENTS.md section 9b; prompts/04h_fang_test.md).
# All variables in logs except the RPS target and ctrl4. Two AI measures side by side: ln(AI postings), Fang's,
# and ln(data-center jobs), the consistent BLS series; ln(per 1,000) is a check.
# Usage: Rscript code/R/04h_fang_test.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)
args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
for (f in c("data/fang_panel.csv","data/fang_split_vars.csv","data/out/state_panel_2015_2025.csv")) if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "fang"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)

d <- fread("data/fang_panel.csv"); sp <- fread("data/fang_split_vars.csv")
stopifnot(nrow(d)==561, uniqueN(d$state)==51)
setorder(d,state,year)
d[, `:=`(lnET=log(re_bbtu), lnEPU=log(epu_composite), lnEPUN=log(epu_national), lnEPUS=log(epu_state), lnEP=log(ep_tetcd),
         lnGDP=log(gdp_real_musd2017), lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000),
         lnAIp=log(ai_postings), lnAIs=log(ai_share_us_pct), lnAIj=log(dc_jobs), lnAIk=log(ai_dc_per1000),
         lnShare=log(re_bbtu/total_energy_bbtu), lnWind=fifelse(wind_bbtu>0,log(wind_bbtu),NA_real_), lnSolar=fifelse(solar_bbtu>0,log(solar_bbtu),NA_real_),
         lnGeo=fifelse(geothermal_bbtu>0,log(geothermal_bbtu),NA_real_), lnBio=fifelse(biomass_bbtu>0,log(biomass_bbtu),NA_real_), lnHydro=fifelse(hydro_bbtu>0,log(hydro_bbtu),NA_real_))]
d[, `:=`(lnAIp_l1=shift(lnAIp,1), lnAIs_l1=shift(lnAIs,1), lnAIp_f1=shift(lnAIp,-1), lnAIs_f1=shift(lnAIs,-1), lnAIj_f1=shift(lnAIj,-1), lnAIk_f1=shift(lnAIk,-1)), by=state]
d[, `:=`(lnAIj_l1=log(dc_jobs_lag1), lnAIk_l1=log(ai_dc_per1000_lag1))]
M <- list(post=list(v="lnAIp",l="lnAIp_l1",f="lnAIp_f1",tag="aipostings",lab="ln(AI postings)"), jobs=list(v="lnAIj",l="lnAIj_l1",f="lnAIj_f1",tag="dcjobs",lab="ln(data-center jobs)"),
          per1000=list(v="lnAIk",l="lnAIk_l1",f="lnAIk_f1",tag="dcper1000",lab="ln(data-center jobs per 1,000)"), share=list(v="lnAIs",l="lnAIs_l1",f="lnAIs_f1",tag="aipostingshare",lab="ln(state share of national postings)"))
CF <- c("lnEP","lnGDP","lnPOP","lnEDU"); CTRL4 <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth")
rows <- list()
add <- function(block,spec,m,outcome,term,e,s,p,lo,hi,N,r2,fe,vc,sample,lag,note="",status="ok",x=NA_character_) rows[[length(rows)+1]] <<- data.table(tag=sprintf("fang_%s_%s_%s_%s_%s_%s_%s_%s_%s",block,spec,m$tag,lag,fe,vc,outcome,sample,term),block=block,spec=spec,ai_measure=m$tag,outcome=outcome,term=term,variable=x,estimate=e,se=s,pval=p,ci_lo=lo,ci_hi=hi,N=N,adj_r2=r2,fe=fe,vcov=vc,sample=sample,lag=lag,status=status,note=note)
fit <- function(y,x,dd,fe="state",vc="iid",ctrl=c("lnEPU",CF)){ f<-as.formula(paste(y,"~",paste(c(x,ctrl),collapse=" + "),"|",fe)); feols(f,data=dd,vcov=if(vc=="iid") "iid" else ~state) }
ar2 <- function(m) as.numeric(fitstat(m,"ar2")[[1]])
rec1 <- function(mod,block,spec,mm,y,x,fe,vc,sample,lag,term="AI",note=""){ ct<-coeftable(mod); ci<-confint(mod); add(block,spec,mm,y,term,ct[x,1],ct[x,2],ct[x,4],ci[x,1],ci[x,2],mod$nobs,ar2(mod),gsub(" \\+ ","-",fe),vc,sample,lag,note=note,x=x); invisible(mod) }
lincom <- function(mod,w){ b<-coef(mod); V<-vcov(mod); n<-names(w); e<-sum(b[n]*w); s<-sqrt(as.numeric(t(w)%*%V[n,n,drop=FALSE]%*%w)); df<-degrees_freedom(mod,"t"); q<-qt(.975,df); c(e=e,s=s,p=2*pt(-abs(e/s),df),lo=e-q*s,hi=e+q*s) }
FE2 <- "state + year"; S18 <- d[year %between% c(2018,2021)]; S19 <- d[year %between% c(2019,2021)]

# ================ GATE ================
cat("=== GATE ===\n"); g<-list(); chk<-function(l,ok,detail="") {g[[length(g)+1]]<<-data.table(check=l,ok=isTRUE(ok),detail=detail)}
chk("N = 204 on the full Fang sample, 2018-2021",nrow(S18[complete.cases(S18[,.(lnET,lnAIp,lnEPU,lnEP,lnGDP,lnPOP,lnEDU)])])==204)
chk("N = 153 on 2019-2021",nrow(S19[complete.cases(S19[,.(lnET,lnAIp,lnEPU,lnEP,lnGDP,lnPOP,lnEDU)])])==153)
ld<-lm(lnET~lnAIp+lnEPU+lnEP+lnGDP+lnPOP+lnEDU+factor(state),S18); fx<-fit("lnET","lnAIp",S18); chk("fixest state FE matches LSDV",abs(coef(ld)[["lnAIp"]]-coef(fx)[["lnAIp"]])<1e-8&&abs(summary(ld)$coefficients["lnAIp",2]-se(fx)[["lnAIp"]])<1e-8)
mp<-fread("data/out/state_panel_2015_2025.csv"); x<-merge(d[,.(state,year,dc_jobs,total_energy_bbtu,gdp_real_musd2017)],mp[,.(state,year,j=dc_jobs,s=seds_total_energy_bbtu,g=gdp_real_musd2017)],by=c("state","year"))
chk("fang_panel matches the master panel (jobs, SEDS total, GDP)",nrow(x)==561&&max(abs(x$dc_jobs-x$j),na.rm=TRUE)==0&&max(abs(x$total_energy_bbtu-x$s),na.rm=TRUE)==0&&max(abs(x$gdp_real_musd2017-x$g))==0)
xx<-d[,.(state,year,lnAIj,l=shift(lnAIj,1),lnAIj_l1),by=state]; chk("Jobs lag consistent with panel",max(abs(xx$l-xx$lnAIj_l1),na.rm=TRUE)<1e-12)
chk("Sum of 51 postings, 2021 = 404,074",sum(d[year==2021,ai_postings])==404074)
g<-rbindlist(g); fwrite(g,file.path(OUT,"gate.csv")); print(g)
if(!all(g$ok)){ cat("GATE FAILED: stopping.\n"); quit(status=1) }
cat("GATE PASSED\n\n")

FIN0 <- function(mn) if(mn %in% c("post","share")) d[year %between% c(2019,2024)&is_dc==0] else d[year %between% c(2015,2024)&is_dc==0]
# ================ 1. Replication: Fang Table 2 columns 1-6 ================
COLS <- list(c1=character(0),c2="lnEPU",c3=c("lnEPU","lnEP"),c4=c("lnEPU","lnEP","lnGDP"),c5=c("lnEPU","lnEP","lnGDP","lnPOP"),c6=c("lnEPU",CF))
for(mn in c("post","jobs")) for(cn in names(COLS)) for(vc in c("iid","cl-state")) for(smp in c("51s2018_2021","51s2019_2021")){ m<-M[[mn]]; dd<-if(smp=="51s2018_2021") S18 else S19
  mod<-fit("lnET",m$v,dd,"state",vc,COLS[[cn]]); ct<-coeftable(mod); ci<-confint(mod)
  for(x in rownames(ct)) add("rep",cn,m,"lnET",if(x==m$v)"AI" else x,ct[x,1],ct[x,2],ct[x,4],ci[x,1],ci[x,2],mod$nobs,ar2(mod),"state",vc,smp,"contemp",x=x) }

# Variant: each year as first published (EXPERIMENTS.md section 9b, F17). 2019 is Jan-Sep only.
alt<-fread("data/ai_job_postings_overlap_rows.csv"); FP<-copy(S18)
FP<-merge(FP,alt[year==2019,.(state,a19=postings)],by="state"); FP<-merge(FP,alt[year==2020,.(state,a20=postings)],by="state")
FP[year==2019,ai_postings:=a19]; FP[year==2020,ai_postings:=a20]; FP[,lnAIp:=log(ai_postings)]; stopifnot(nrow(FP)==204,!anyNA(FP$lnAIp))
for(cn in names(COLS)) for(vc in c("iid","cl-state")){ mod<-fit("lnET","lnAIp",FP,"state",vc,COLS[[cn]]); ct<-coeftable(mod); ci<-confint(mod); add("rep",paste0(cn,"-firstpub"),M$post,"lnET","AI",ct["lnAIp",1],ct["lnAIp",2],ct["lnAIp",4],ci["lnAIp",1],ci["lnAIp",2],mod$nobs,ar2(mod),"state",vc,"51s2018_2021","contemp",note="each year as first published; 2019 is Jan-Sep",x="lnAIp") }
# Also the by-type models on the first-published series, to compare with Fang's Table 7
for(tn in c("lnWind","lnSolar","lnGeo","lnBio","lnHydro")){ dz<-FP[!is.na(get(tn))]; rec1(fit(tn,"lnAIp",dz),"rep","type-firstpub",M$post,tn,"lnAIp","state","iid","51s2018_2021nz","contemp",note="each year as first published") }

# Sensitivity: rebuild renewables on approximately the old SEDS basis (EXPERIMENTS.md section 9b, F18).
for(k in c(2.3,2.6,2.9)){ kk<-sprintf("ffe%02.0f",k*10); S18[,lnET_k:=log(biomass_bbtu+k*(wind_bbtu+solar_bbtu+hydro_bbtu+geothermal_bbtu))]; d[,lnET_k:=log(biomass_bbtu+k*(wind_bbtu+solar_bbtu+hydro_bbtu+geothermal_bbtu))]
  for(mn in c("post","jobs")){ m<-M[[mn]]; for(cn in names(COLS)){ mod<-fit("lnET_k",m$v,S18,"state","iid",COLS[[cn]]); ct<-coeftable(mod); ci<-confint(mod); add("rep",paste0(cn,"-",kk),m,"lnET_k","AI",ct[m$v,1],ct[m$v,2],ct[m$v,4],ci[m$v,1],ci[m$v,2],mod$nobs,ar2(mod),"state","iid","51s2018_2021","contemp",note=sprintf("approximate old-SEDS basis, k = %.1f",k),x=m$v)
      if(cn=="c6"){ for(tm in c("lnEPU",CF)) add("rep",paste0(cn,"-",kk),m,"lnET_k",tm,ct[tm,1],ct[tm,2],ct[tm,4],ci[tm,1],ci[tm,2],mod$nobs,ar2(mod),"state","iid","51s2018_2021","contemp",note=sprintf("approximate old-SEDS basis, k = %.1f",k),x=tm) } }
    if(k==2.6){ mod<-fit("lnET_k",m$l,FIN0(mn),FE2,"cl"); ct<-coeftable(mod); ci<-confint(mod); add("rep","final-ffe26",m,"lnET_k","AI",ct[m$l,1],ct[m$l,2],ct[m$l,4],ci[m$l,1],ci[m$l,2],mod$nobs,ar2(mod),"state-year","cl-state",if(mn=="post") "50s2019_2024" else "50s2015_2024","lag1",note="final spec on the approximate old-SEDS basis, k = 2.6",x=m$l) } } }

# ================ 2. Bridge, one change at a time ================
bridge <- function(mn){ m<-M[[mn]]
  rec1(fit("lnET",m$v,S18),"bridge","s0-fang",m,"lnET",m$v,"state","iid","51s2018_2021","contemp",note="Fang's spec")
  rec1(fit("lnET",m$v,S18,FE2),"bridge","s1-yearfe",m,"lnET",m$v,FE2,"iid","51s2018_2021","contemp",note="add year FE")
  rec1(fit("lnET",m$v,S19,FE2),"bridge","s2-sample",m,"lnET",m$v,FE2,"iid","51s2019_2021","contemp",note="same years the lag can use")
  rec1(fit("lnET",m$l,S19,FE2),"bridge","s3-lag",m,"lnET",m$l,FE2,"iid","51s2019_2021","lag1",note="lag AI one year")
  rec1(fit("lnET",m$l,S19,FE2,"cl"),"bridge","s4-cluster",m,"lnET",m$l,FE2,"cl-state","51s2019_2021","lag1",note="cluster by state")
  ext<-if(mn %in% c("post","share")) c(2019,2024) else c(2015,2024); sm<-sprintf("%%ds%d_%d",ext[1],ext[2]); DX<-d[year %between% ext]
  a<-rec1(fit("lnET",m$l,DX,FE2,"cl"),"bridge","s5-extend",m,"lnET",m$l,FE2,"cl-state",sprintf(sm,51),"lag1",note="extend the sample")
  b<-rec1(fit("lnET",m$l,DX[is_dc==0],FE2,"cl"),"bridge","s6-noDC",m,"lnET",m$l,FE2,"cl-state",sprintf(sm,50),"lag1",note="drop DC")
  if(mn %in% c("jobs","per1000")){ D2<-d[year %between% c(2019,2024)]; rec1(fit("lnET",m$l,D2,FE2,"cl"),"bridge","s5b-extend1924",m,"lnET",m$l,FE2,"cl-state","51s2019_2024","lag1",note="same years as postings")
    rec1(fit("lnET",m$l,D2[is_dc==0],FE2,"cl"),"bridge","s6b-noDC1924",m,"lnET",m$l,FE2,"cl-state","50s2019_2024","lag1",note="same years as postings, no DC") } }
for(mn in c("post","jobs","per1000","share")) bridge(mn)

# Final (our) spec: lag, two-way FE, clustered, no DC
FIN <- function(mn) if(mn %in% c("post","share")) d[year %between% c(2019,2024)&is_dc==0] else d[year %between% c(2015,2024)&is_dc==0]
FS <- function(mn) if(mn %in% c("post","share")) "50s2019_2024" else "50s2015_2024"

# ================ 3. Moderation: AI x EPU (Fang eq. 3), centered ================
modn <- function(y,ai,ep,dd,fe,vc,mn,spec,sample,lag){ m<-M[[mn]]; dd<-copy(dd[complete.cases(dd[,c(y,ai,ep,CF),with=FALSE])]); dd[,`:=`(ai_c=get(ai)-mean(get(ai)),e_c=get(ep)-mean(get(ep)))]; dd[,ai_x_e:=ai_c*e_c]
  mod<-feols(as.formula(paste(y,"~ ai_c + e_c + ai_x_e +",paste(CF,collapse="+"),"|",fe)),data=dd,vcov=if(vc=="iid") "iid" else ~state); ct<-coeftable(mod); ci<-confint(mod); f<-gsub(" \\+ ","-",fe); ss<-paste0(spec,"-",ep)
  for(p in list(c("ai_c","AI"),c("e_c","EPU"),c("ai_x_e","AI_x_EPU"))) add("mod",ss,m,y,p[2],ct[p[1],1],ct[p[1],2],ct[p[1],4],ci[p[1],1],ci[p[1],2],mod$nobs,ar2(mod),f,vc,sample,lag,x=p[1])
  q<-quantile(dd$e_c,c(.25,.75)); for(i in 1:2){ w<-c(ai_c=1,ai_x_e=as.numeric(q[i])); l<-lincom(mod,w); add("mod",ss,m,y,c("AI_slope_p25","AI_slope_p75")[i],l[["e"]],l[["s"]],l[["p"]],l[["lo"]],l[["hi"]],mod$nobs,ar2(mod),f,vc,sample,lag,note=sprintf("centered ln EPU at %.3f",q[i]),x="lincom") } }
for(ep in c("lnEPU","lnEPUN","lnEPUS")) for(mn in c("post","jobs")){ m<-M[[mn]]
  modn("lnET",m$v,ep,S18,"state","iid",mn,"fang","51s2018_2021","contemp"); modn("lnET",m$l,ep,FIN(mn),FE2,"cl",mn,"twfe",FS(mn),"lag1") }

# ================ 4. By type ================
TY <- c(wind="lnWind",solar="lnSolar",geothermal="lnGeo",biomass="lnBio",hydro="lnHydro")
for(mn in c("post","jobs")) for(tn in names(TY)){ m<-M[[mn]]; y<-TY[[tn]]; dz<-S18[!is.na(get(y))]
  rec1(fit(y,m$v,dz),"type","fang",m,y,m$v,"state","iid","51s2018_2021nz","contemp",note="zero-consumption state-years dropped")
  f<-FIN(mn); f<-f[!is.na(get(y))]; rec1(fit(y,m$l,f,FE2,"cl"),"type","twfe",m,y,m$l,FE2,"cl-state",paste0(FS(mn),"nz"),"lag1",note="zero-consumption state-years dropped") }

# ================ 5. Heterogeneity ================
sg<-sp[year %between% c(2018,2021),.(e=mean(elec_consumption_mwh),p=mean(elec_price_c_kwh),r=mean(rd_total_musd),i=mean(income_pc_usd),gen=mean(gen_total_mwh),region=census_region[1]),by=state]
GR<-sg[,.(state,region,net=as.integer(gen>e),h_e_mean=as.integer(e>mean(e)),h_p_mean=as.integer(p>mean(p)),h_r_mean=as.integer(r>mean(r)),h_i_mean=as.integer(i>mean(i)),h_e_med=as.integer(e>median(e)),h_p_med=as.integer(p>median(p)),h_r_med=as.integer(r>median(r)),h_i_med=as.integer(i>median(i)))]
fwrite(GR,file.path(OUT,"split_groups.csv")); d<-merge(d,GR,by="state"); setorder(d,state,year); S18<-d[year %between% c(2018,2021)]
SPL<-list(elec_mean="h_e_mean",price_mean="h_p_mean",rd_mean="h_r_mean",income_mean="h_i_mean",net_producer="net",elec_median="h_e_med",price_median="h_p_med",rd_median="h_r_med",income_median="h_i_med")
for(sn in names(SPL)) for(mn in c("post","jobs")){ m<-M[[mn]]; v<-SPL[[sn]]
  for(val in 0:1){ dd<-S18[get(v)==val]; rec1(fit("lnET",m$v,dd),"split",paste0(sn,"-",if(val==1)"high" else "low"),m,"lnET",m$v,"state","iid","fang2018_2021","contemp") }
  for(sp2 in list(list(dd=S18,ai=m$v,fe="state",vc="iid",sm="51s2018_2021",lg="contemp",lab="fang"),list(dd=FIN(mn),ai=m$l,fe=FE2,vc="cl",sm=FS(mn),lg="lag1",lab="twfe"))){
    dd<-copy(sp2$dd); dd[,ai_h:=get(sp2$ai)*get(v)]; mod<-feols(as.formula(paste("lnET ~",sp2$ai,"+ ai_h + lnEPU +",paste(CF,collapse="+"),"|",sp2$fe)),data=dd,vcov=if(sp2$vc=="iid") "iid" else ~state); ct<-coeftable(mod); ci<-confint(mod); f<-gsub(" \\+ ","-",sp2$fe); vv<-if(sp2$vc=="iid") "iid" else "cl-state"
    add("inter",paste0(sp2$lab,"-",sn),m,"lnET","difference_high_minus_low",ct["ai_h",1],ct["ai_h",2],ct["ai_h",4],ci["ai_h",1],ci["ai_h",2],mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x="ai_h")
    add("inter",paste0(sp2$lab,"-",sn),m,"lnET","slope_low",ct[sp2$ai,1],ct[sp2$ai,2],ct[sp2$ai,4],ci[sp2$ai,1],ci[sp2$ai,2],mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x=sp2$ai)
    w<-c(1,1); names(w)<-c(sp2$ai,"ai_h"); l<-lincom(mod,w); add("inter",paste0(sp2$lab,"-",sn),m,"lnET","slope_high",l[["e"]],l[["s"]],l[["p"]],l[["lo"]],l[["hi"]],mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x="lincom") } }
REG<-c("West","South","Northeast","Midwest")
for(mn in c("post","jobs")){ m<-M[[mn]]
  for(r in REG) rec1(fit("lnET",m$v,S18[region==r]),"split",paste0("region-",r),m,"lnET",m$v,"state","iid","fang2018_2021","contemp")
  for(sp2 in list(list(dd=S18,ai=m$v,fe="state",vc="iid",sm="51s2018_2021",lg="contemp",lab="fang"),list(dd=FIN(mn),ai=m$l,fe=FE2,vc="cl",sm=FS(mn),lg="lag1",lab="twfe"))){
    dd<-copy(sp2$dd); for(r in REG[-2]) dd[,(paste0("ai_",r)):=get(sp2$ai)*(region==r)]; hx<-paste0("ai_",REG[-2]); mod<-feols(as.formula(paste("lnET ~",sp2$ai,"+",paste(hx,collapse="+"),"+ lnEPU +",paste(CF,collapse="+"),"|",sp2$fe)),data=dd,vcov=if(sp2$vc=="iid") "iid" else ~state); f<-gsub(" \\+ ","-",sp2$fe); vv<-if(sp2$vc=="iid") "iid" else "cl-state"
    for(r in REG){ w<-if(r=="South"){z<-1;names(z)<-sp2$ai;z}else{z<-c(1,1);names(z)<-c(sp2$ai,paste0("ai_",r));z}; l<-lincom(mod,w); add("inter",paste0(sp2$lab,"-region"),m,"lnET",paste0("slope_",r),l[["e"]],l[["s"]],l[["p"]],l[["lo"]],l[["hi"]],mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x="lincom") }
    w<-wald(mod,hx,print=FALSE); add("inter",paste0(sp2$lab,"-region"),m,"lnET","joint_F_regions_differ",w$stat,NA_real_,w$p,NA_real_,NA_real_,mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x="wald") } }

# ================ 6. Placebo ================
for(mn in c("post","jobs")){ m<-M[[mn]]; dd<-FIN(mn); dd<-dd[!is.na(get(m$f))&!is.na(get(m$l))]; ss<-sub("_2024$","_2024pl",FS(mn))
  rec1(fit("lnET",m$l,dd,FE2,"cl"),"placebo","lag",m,"lnET",m$l,FE2,"cl-state",ss,"lag1",note="AI(t-1) on the placebo sample")
  rec1(fit("lnET",m$f,dd,FE2,"cl"),"placebo","lead",m,"lnET",m$f,FE2,"cl-state",ss,"lead1",note="AI(t+1) in place of AI(t-1)")
  mod<-fit("lnET",c(m$f,m$l),dd,FE2,"cl"); ct<-coeftable(mod); ci<-confint(mod)
  for(p in list(list(m$f,"lead"),list(m$l,"lag"))) add("placebo",paste0("both-",p[[2]]),m,"lnET",p[[2]],ct[p[[1]],1],ct[p[[1]],2],ct[p[[1]],4],ci[p[[1]],1],ci[p[[1]],2],mod$nobs,ar2(mod),"state-year","cl-state",ss,"lead1lag1",note="both in one model",x=p[[1]])
  wc<-dd[,.(a=get(m$f)-mean(get(m$f)),b=get(m$l)-mean(get(m$l))),by=state]; add("placebo","corr",m,"lnET","within_corr_lead_lag",cor(wc$a,wc$b),NA_real_,NA_real_,NA_real_,NA_real_,nrow(dd),NA_real_,"state","none",ss,"lead1lag1",x="corr") }

# ================ 7. Robustness (our final spec) ================
for(mn in c("post","jobs")){ m<-M[[mn]]; dd<-FIN(mn); s0<-FS(mn)
  rec1(fit("lnET",m$l,dd,FE2,"cl"),"rob","base",m,"lnET",m$l,FE2,"cl-state",s0,"lag1",note="final bridge spec")
  rec1(fit("lnShare",m$l,dd,FE2,"cl"),"rob","share-outcome",m,"lnShare",m$l,FE2,"cl-state",s0,"lag1",note="ln(RETCB / TETCB)")
  rec1(fit("lnET",m$l,dd[year!=2020],FE2,"cl"),"rob","drop2020",m,"lnET",m$l,FE2,"cl-state",paste0(s0,"no2020"),"lag1",note="drop 2020")
  a<-fit("lnET",m$l,dd,FE2,"cl",c("lnEPU",CF,"target_pct")); rec1(a,"rob","rps",m,"lnET",m$l,FE2,"cl-state",s0,"lag1",note="add LBNL current RPS/CES schedule, in percent, not logged because of zeros"); rec1(a,"rob","rps-coef",m,"lnET","target_pct",FE2,"cl-state",s0,"lag1",term="target_pct",note="coefficient on the RPS control")
  rec1(fit("lnET",m$l,dd,FE2,"cl",c("lnEPU",CTRL4)),"rob","ctrl4",m,"lnET",m$l,FE2,"cl-state",s0,"lag1",note="ctrl4 in place of EP, GDP, POP, EDU; EPU kept") }
rec1(fit("lnET",M$per1000$l,FIN("jobs"),FE2,"cl"),"rob","base",M$per1000,"lnET",M$per1000$l,FE2,"cl-state","50s2015_2024","lag1",note="check")

res<-rbindlist(rows,fill=TRUE); stopifnot(!anyDuplicated(res$tag)); fwrite(res,file.path(OUT,"fang_results.csv"))
cat(sprintf("fang_results.csv: %d rows; status %s\n",nrow(res),paste(names(table(res$status)),table(res$status),collapse=", ")))
cat("DONE\n")

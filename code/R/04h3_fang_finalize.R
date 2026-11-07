#!/usr/bin/env Rscript
# 04h3_fang_finalize.R
# Fang, Lee & Li (2025): the rest of the method set (prompts/08_finalize.md section 1; EXPERIMENTS.md section 9b, F20-F26).
# Splits table (Tables 3-5), negative indicator (Supplement B), extreme-weather split (Table 4), exact old SEDS basis
# (year-by-year rebuild and the archived June 2023 values), Table 2 on each basis, our spec on the rebuilt basis, event study.
# Usage: Rscript code/R/04h3_fang_finalize.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)
args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
OLD <- "results/2026-11-04/fang/fang_results.csv"
for (f in c("data/fang_panel.csv","data/fang_split_vars.csv","data/seds_old_basis.csv","data/storm_events_state.csv",OLD)) if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "fang"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)

d <- fread("data/fang_panel.csv"); sp <- fread("data/fang_split_vars.csv"); sb <- fread("data/seds_old_basis.csv"); se <- fread("data/storm_events_state.csv")
stopifnot(nrow(d)==561, nrow(sb)==510, nrow(se)==510)
d <- merge(d, sb[,.(state,year,re_bbtu_current,re_bbtu_rebuilt,re_bbtu_rebuilt_allconv,re_bbtu_k26,RETCB_arch2021,fossil_bbtu,TETCB,fossil_share_total)], by=c("state","year"), all.x=TRUE)
setorder(d,state,year)
d[, `:=`(lnET=log(re_bbtu), lnEPU=log(epu_composite), lnEP=log(ep_tetcd), lnGDP=log(gdp_real_musd2017), lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000),
         lnAIp=log(ai_postings), lnAIj=log(dc_jobs), lnET_rb=log(re_bbtu_rebuilt), lnET_ac=log(re_bbtu_rebuilt_allconv), lnET_k26=log(re_bbtu_k26),
         lnET_arch=log(RETCB_arch2021), lnFossil=log(fossil_bbtu), fossilShare=fossil_share_total)]
d[, `:=`(lnAIp_l1=shift(lnAIp,1)), by=state]; d[, lnAIj_l1:=log(dc_jobs_lag1)]
M <- list(post=list(v="lnAIp",l="lnAIp_l1",tag="aipostings"), jobs=list(v="lnAIj",l="lnAIj_l1",tag="dcjobs"))
CF <- c("lnEP","lnGDP","lnPOP","lnEDU"); FE2 <- "state + year"
rows <- list()
add <- function(block,spec,m,outcome,term,e,s,p,lo,hi,N,r2,fe,vc,sample,lag,note="",x=NA_character_) rows[[length(rows)+1]] <<- data.table(tag=sprintf("fang8_%s_%s_%s_%s_%s_%s_%s_%s_%s",block,spec,m$tag,lag,fe,vc,outcome,sample,term),block=block,spec=spec,ai_measure=m$tag,outcome=outcome,term=term,variable=x,estimate=e,se=s,pval=p,ci_lo=lo,ci_hi=hi,N=N,adj_r2=r2,fe=fe,vcov=vc,sample=sample,lag=lag,status="ok",note=note)
fit <- function(y,x,dd,fe="state",vc="iid",ctrl=c("lnEPU",CF)){ f<-as.formula(paste(y,"~",paste(c(x,ctrl),collapse=" + "),"|",fe)); feols(f,data=dd,vcov=if(vc=="iid") "iid" else ~state) }
ar2 <- function(m) as.numeric(fitstat(m,"ar2")[[1]])
rec1 <- function(mod,block,spec,mm,y,x,fe,vc,sample,lag,term="AI",note=""){ ct<-coeftable(mod); ci<-confint(mod); add(block,spec,mm,y,term,ct[x,1],ct[x,2],ct[x,4],ci[x,1],ci[x,2],mod$nobs,ar2(mod),gsub(" \\+ ","-",fe),vc,sample,lag,note=note,x=x); invisible(mod) }
lincom <- function(mod,w){ b<-coef(mod); V<-vcov(mod); n<-names(w); e<-sum(b[n]*w); s<-sqrt(as.numeric(t(w)%*%V[n,n,drop=FALSE]%*%w)); df<-degrees_freedom(mod,"t"); q<-qt(.975,df); c(e=e,s=s,p=2*pt(-abs(e/s),df),lo=e-q*s,hi=e+q*s) }
S18 <- d[year %between% c(2018,2021)]
FIN <- function(mn) if(mn=="post") d[year %between% c(2019,2024)&is_dc==0] else d[year %between% c(2015,2024)&is_dc==0]
FS <- function(mn) if(mn=="post") "50s2019_2024" else "50s2015_2024"

# ---------------- groups (same rules as 04h_fang_test.R, plus extreme weather) ----------------
sg<-sp[year %between% c(2018,2021),.(e=mean(elec_consumption_mwh),p=mean(elec_price_c_kwh),r=mean(rd_total_musd),i=mean(income_pc_usd),gen=mean(gen_total_mwh),region=census_region[1]),by=state]
GR<-sg[,.(state,region,net=as.integer(gen>e),h_e_mean=as.integer(e>mean(e)),h_p_mean=as.integer(p>mean(p)),h_r_mean=as.integer(r>mean(r)),h_i_mean=as.integer(i>mean(i)),h_e_med=as.integer(e>median(e)),h_p_med=as.integer(p>median(p)),h_r_med=as.integer(r>median(r)),h_i_med=as.integer(i>median(i)))]
ew <- se[year %between% c(2018,2021), .(w=mean(extreme_events), wep=mean(extreme_episodes)), by=state]
GR <- merge(GR, ew[,.(state, ew_count=w, h_w_mean=as.integer(w>mean(w)), h_w_med=as.integer(w>median(w)), h_wep_mean=as.integer(wep>mean(wep)))], by="state")
fwrite(GR, file.path(OUT,"split_groups_08.csv")); d <- merge(d, GR, by="state"); setorder(d,state,year); S18 <- d[year %between% c(2018,2021)]

# ================ GATE ================
cat("=== GATE ===\n"); g<-list(); chk<-function(l,ok,detail="") {g[[length(g)+1]]<<-data.table(check=l,ok=isTRUE(ok),detail=detail)}
old <- fread(OLD)
chk("SEDS side table equals fang_panel re_bbtu", max(abs(d$re_bbtu-d$re_bbtu_current),na.rm=TRUE)==0)
chk("k = 2.6 side-table series equals 04h's in-script k = 2.6", max(abs(d$re_bbtu_k26-(d$biomass_bbtu+2.6*(d$wind_bbtu+d$solar_bbtu+d$hydro_bbtu+d$geothermal_bbtu))),na.rm=TRUE)<1e-6)
b6 <- coef(fit("lnET","lnAIp",S18))[["lnAIp"]]; o6 <- old[tag=="fang_rep_c6_aipostings_contemp_state_iid_lnET_51s2018_2021_AI", estimate]
chk("Reproduces 11-04 Table 2 col. 6, postings, current SEDS", abs(b6-o6)<1e-10, sprintf("%.6f vs %.6f",b6,o6))
bk <- coef(fit("lnET_k26","lnAIp",S18))[["lnAIp"]]; ok <- old[spec=="c6-ffe26" & ai_measure=="aipostings" & term=="AI", estimate]
chk("Reproduces 11-04 k = 2.6 col. 6", abs(bk-ok)<1e-10, sprintf("%.6f vs %.6f",bk,ok))
oldsp <- old[block=="split" & spec=="elec_mean-high" & ai_measure=="aipostings", estimate]; nsp <- coef(fit("lnET","lnAIp",S18[h_e_mean==1]))[["lnAIp"]]
chk("Reproduces 11-04 split (elec mean, high, postings)", abs(oldsp-nsp)<1e-10)
chk("N = 204 for rebuilt and archived outcomes, 2018-2021", nrow(S18[!is.na(lnET_rb)&!is.na(lnET_arch)&!is.na(lnAIp)])==204)
chk("Storm groups: 51 states", nrow(GR)==51)
g<-rbindlist(g); fwrite(g,file.path(OUT,"gate_08.csv")); print(g)
if(!all(g$ok)){ cat("GATE FAILED: stopping.\n"); quit(status=1) }
cat("GATE PASSED\n\n")

# ================ F20/F22. Splits ================
SPL<-list(elec_mean="h_e_mean",price_mean="h_p_mean",rd_mean="h_r_mean",income_mean="h_i_mean",weather_mean="h_w_mean",net_producer="net",
          elec_median="h_e_med",price_median="h_p_med",rd_median="h_r_med",income_median="h_i_med",weather_median="h_w_med",weather_episodes_mean="h_wep_mean")
for(sn in names(SPL)) for(mn in names(M)){ m<-M[[mn]]; v<-SPL[[sn]]
  for(val in 0:1){ hl<-if(val==1)"high" else "low"
    rec1(fit("lnET",m$v,S18[get(v)==val]),"split",paste0(sn,"-",hl),m,"lnET",m$v,"state","iid","51s2018_2021","contemp",note="Fang spec, separate regression")
    rec1(fit("lnET",m$l,FIN(mn)[get(v)==val],FE2,"cl"),"splittw",paste0(sn,"-",hl),m,"lnET",m$l,FE2,"cl-state",FS(mn),"lag1",note="our spec, separate regression") }
  for(sp2 in list(list(dd=S18,ai=m$v,fe="state",vc="iid",sm="51s2018_2021",lg="contemp",lab="fang"),list(dd=FIN(mn),ai=m$l,fe=FE2,vc="cl",sm=FS(mn),lg="lag1",lab="twfe"))){
    dd<-copy(sp2$dd); dd[,ai_h:=get(sp2$ai)*get(v)]; mod<-feols(as.formula(paste("lnET ~",sp2$ai,"+ ai_h + lnEPU +",paste(CF,collapse="+"),"|",sp2$fe)),data=dd,vcov=if(sp2$vc=="iid") "iid" else ~state); ct<-coeftable(mod); ci<-confint(mod); f<-gsub(" \\+ ","-",sp2$fe); vv<-if(sp2$vc=="iid") "iid" else "cl-state"
    add("inter",paste0(sp2$lab,"-",sn),m,"lnET","difference_high_minus_low",ct["ai_h",1],ct["ai_h",2],ct["ai_h",4],ci["ai_h",1],ci["ai_h",2],mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x="ai_h") } }
REG<-c("West","South","Northeast","Midwest")
for(mn in names(M)){ m<-M[[mn]]
  for(r in REG){ rec1(fit("lnET",m$v,S18[region==r]),"split",paste0("region-",r),m,"lnET",m$v,"state","iid","51s2018_2021","contemp",note="Fang spec, separate regression")
    rec1(fit("lnET",m$l,FIN(mn)[region==r],FE2,"cl"),"splittw",paste0("region-",r),m,"lnET",m$l,FE2,"cl-state",FS(mn),"lag1",note="our spec, separate regression") }
  for(sp2 in list(list(dd=S18,ai=m$v,fe="state",vc="iid",sm="51s2018_2021",lg="contemp",lab="fang"),list(dd=FIN(mn),ai=m$l,fe=FE2,vc="cl",sm=FS(mn),lg="lag1",lab="twfe"))){
    dd<-copy(sp2$dd); for(r in REG[-2]) dd[,(paste0("ai_",r)):=get(sp2$ai)*(region==r)]; hx<-paste0("ai_",REG[-2]); mod<-feols(as.formula(paste("lnET ~",sp2$ai,"+",paste(hx,collapse="+"),"+ lnEPU +",paste(CF,collapse="+"),"|",sp2$fe)),data=dd,vcov=if(sp2$vc=="iid") "iid" else ~state); f<-gsub(" \\+ ","-",sp2$fe); vv<-if(sp2$vc=="iid") "iid" else "cl-state"
    w<-wald(mod,hx,print=FALSE); add("inter",paste0(sp2$lab,"-region"),m,"lnET","joint_F_regions_differ",w$stat,NA_real_,w$p,NA_real_,NA_real_,mod$nobs,ar2(mod),f,vv,sp2$sm,sp2$lg,x="wald") } }

# ================ F27 (deviation, added after F24). Splits on the archived basis, Fang's spec ================
for(sn in names(SPL)) for(mn in names(M)){ m<-M[[mn]]; v<-SPL[[sn]]
  for(val in 0:1) rec1(fit("lnET_arch",m$v,S18[get(v)==val]),"splitarch",paste0(sn,"-",if(val==1)"high" else "low"),m,"lnET_arch",m$v,"state","iid","51s2018_2021","contemp",note="Fang spec, archived June 2023 SEDS; added after F24 (F27)")
  dd<-copy(S18); dd[,ai_h:=get(m$v)*get(v)]; mod<-feols(as.formula(paste("lnET_arch ~",m$v,"+ ai_h + lnEPU +",paste(CF,collapse="+"),"| state")),data=dd,vcov="iid"); ct<-coeftable(mod); ci<-confint(mod)
  add("interarch",paste0("fang-",sn),m,"lnET_arch","difference_high_minus_low",ct["ai_h",1],ct["ai_h",2],ct["ai_h",4],ci["ai_h",1],ci["ai_h",2],mod$nobs,ar2(mod),"state","iid","51s2018_2021","contemp",note="F27",x="ai_h") }
for(mn in names(M)){ m<-M[[mn]]; for(r in REG) rec1(fit("lnET_arch",m$v,S18[region==r]),"splitarch",paste0("region-",r),m,"lnET_arch",m$v,"state","iid","51s2018_2021","contemp",note="F27") }

# ================ F21. Negative indicator ================
for(mn in names(M)){ m<-M[[mn]]
  for(y in c("lnFossil","fossilShare")){ rec1(fit(y,m$v,S18),"neg","fang",m,y,m$v,"state","iid","51s2018_2021","contemp",note="Fang spec")
    rec1(fit(y,m$l,FIN(mn),FE2,"cl"),"neg","twfe",m,y,m$l,FE2,"cl-state",FS(mn),"lag1",note="our spec") } }

# ================ F23/F24. Table 2 on each basis ================
COLS <- list(c1=character(0),c2="lnEPU",c3=c("lnEPU","lnEP"),c4=c("lnEPU","lnEP","lnGDP"),c5=c("lnEPU","lnEP","lnGDP","lnPOP"),c6=c("lnEPU",CF))
BAS <- list(current="lnET", k26="lnET_k26", rebuilt="lnET_rb", archived="lnET_arch", allconv="lnET_ac")
for(bn in names(BAS)) for(mn in names(M)) for(cn in names(COLS)){ m<-M[[mn]]; y<-BAS[[bn]]
  mod<-fit(y,m$v,S18,"state","iid",COLS[[cn]]); ct<-coeftable(mod); ci<-confint(mod)
  for(x in rownames(ct)) add("t2",paste0(cn,"-",bn),m,y,if(x==m$v)"AI" else x,ct[x,1],ct[x,2],ct[x,4],ci[x,1],ci[x,2],mod$nobs,ar2(mod),"state","iid","51s2018_2021","contemp",note=paste("basis:",bn),x=x)
  add("t2",paste0(cn,"-",bn),m,y,"mean_lnET",mean(S18[[y]]),NA_real_,NA_real_,NA_real_,NA_real_,nrow(S18),NA_real_,"state","none","51s2018_2021","contemp",note="mean of the outcome",x="mean") }

# ================ F25. Our final spec on each basis ================
for(bn in c("current","k26","rebuilt","allconv")) for(mn in names(M)){ m<-M[[mn]]; rec1(fit(BAS[[bn]],m$l,FIN(mn),FE2,"cl"),"final",bn,m,BAS[[bn]],m$l,FE2,"cl-state",FS(mn),"lag1",note=paste("our final spec, basis:",bn)) }

# ================ F26. Event study ================
ex <- d[year==2019 & ai_edition==2022, .(state, expo=ai_share_us_pct)]; stopifnot(nrow(ex)==51)
ES <- merge(d[year %between% c(2015,2024) & is_dc==0], ex, by="state")
for(bn in c("current","rebuilt")){ y<-BAS[[bn]]
  mod <- feols(as.formula(paste(y,"~ i(year, expo, ref=2021) + ln_gdp_pc + manuf_share + price_c_kwh + pop_growth | state + year")), data=ES, vcov=~state)
  ct<-coeftable(mod); ci<-confint(mod); ev<-grep("year::",rownames(ct),value=TRUE)
  for(x in ev) add("es",bn,list(tag="aishare2019"),y,sub("year::(\\d+):expo","b\\1",x),ct[x,1],ct[x,2],ct[x,4],ci[x,1],ci[x,2],mod$nobs,ar2(mod),"state-year","cl-state","50s2015_2024","event",note="per 1 pp of 2019 U.S. postings share (2022 edition); base 2021; ctrl4",x=x)
  pre<-ev[as.integer(sub("year::(\\d+):expo","\\1",ev))<2021]; post<-ev[as.integer(sub("year::(\\d+):expo","\\1",ev))>2021]
  for(pp in list(list(pre,"joint_pre_2015_2020"),list(post,"joint_post_2022_2024"))){ w<-wald(mod,paste0("^",gsub("([:.])","\\\\\\1",pp[[1]]),"$",collapse="|"),print=FALSE); add("es",bn,list(tag="aishare2019"),y,pp[[2]],w$stat,NA_real_,w$p,NA_real_,NA_real_,mod$nobs,ar2(mod),"state-year","cl-state","50s2015_2024","event",note=sprintf("Wald F, df1 = %d",length(pp[[1]])),x="wald") } }

res<-rbindlist(rows,fill=TRUE); stopifnot(!anyDuplicated(res$tag)); fwrite(res,file.path(OUT,"fang8_results.csv"))
cat(sprintf("fang8_results.csv: %d rows\n",nrow(res)))
# quick prints
print(res[block=="t2" & term=="AI" & spec %like% "^c[26]-", .(spec,ai_measure,estimate=round(estimate,4),se=round(se,4),p=round(pval,3))])
print(res[block %in% c("neg","final"), .(block,spec,ai_measure,outcome,estimate=round(estimate,4),p=round(pval,3),N)])
print(res[block=="es", .(spec,term,estimate=round(estimate,4),p=round(pval,3))])
cat("DONE\n")

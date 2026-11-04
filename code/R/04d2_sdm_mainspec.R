#!/usr/bin/env Rscript
# 04d2_sdm_mainspec.R
# Applies the one-estimator rule for the H3 SDM (EXPERIMENTS.md section 0 items 15-16).
#   Estimators: LY-demn (LYtrans=TRUE, demn=TRUE), ML (LYtrans=FALSE), LY-bias (LYtrans=TRUE, demn=FALSE; 4d)
#   W: invdist-50 (main), invdist-48, border-48. Outcomes: ln_ec, ln_ee, renew_share.
#   Impacts: plug-in point estimates; simulation draws for SEs and CIs only.
#   Also: within-state variation in W*AI after FE, and a splm Lee-Yu cross-check.
# Usage: Rscript code/R/04d2_sdm_mainspec.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(SDPDmod); library(splm); library(spdep); library(plm); library(data.table)})

args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
PRIOR <- "results/2026-11-03/h3/h3_sdm_impacts.csv"
for (f in c("code/R/load_panel.R","data/out/W_inverse_distance_rowstd.csv","data/out/W_border_binary.csv",PRIOR))
  if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "h3_mainspec"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)

source("code/R/load_panel.R"); dt <- load_panel()$panel
stopifnot(nrow(dt)==550, uniqueN(dt$state)==50)
OUTCOMES <- c("ln_ec","ln_ee","renew_share"); AI <- "ai_dc_per1000_lag1"
CC4 <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth"); CTRL4 <- paste(CC4, collapse=" + ")
NSIM <- 2000L

read_W <- function(p){r<-fread(p); W<-as.matrix(r[,-1]); rownames(W)<-colnames(W)<-r[[1]]; W}
Wi50 <- read_W("data/out/W_inverse_distance_rowstd.csv"); Wb50 <- read_W("data/out/W_border_binary.csv")
keep48 <- rownames(Wi50)[!rownames(Wi50) %in% c("AK","HI")]
Wi48 <- Wi50[keep48,keep48]; Wi48 <- Wi48/rowSums(Wi48)
Wb48 <- Wb50[keep48,keep48]; Wb48 <- Wb48/rowSums(Wb48)
Ws <- list(invdist50=Wi50, invdist48=Wi48, border48=Wb48)
ESTS <- list("LY-demn"=list(LYt=TRUE,demn=TRUE), "ML"=list(LYt=FALSE,demn=FALSE), "LY-bias"=list(LYt=TRUE,demn=FALSE))

impact_at <- function(b,th,rho,W){ N<-nrow(W); SC<-solve(diag(N)-rho*W)%*%(b*diag(N)+th*W)
  d<-sum(diag(SC))/N; t<-sum(SC)/N; c(direct=d,indirect=t-d,total=t) }

# Same draw scheme as SDPDmod::impactsSDPDm (seed = 12345 + 10*sim), keeping the draws.
draw_impacts <- function(m,W,nsim){
  npar<-length(m$coefficients); varb<-c(m$coefficients,m$rho,m$sige); L<-t(chol(m$varcov))
  ib<-match(AI,names(m$coefficients)); it<-match(paste0("W*",AI),names(m$coefficients))
  out<-matrix(NA_real_,nsim,4,dimnames=list(NULL,c("direct","indirect","total","rho")))
  for(s in seq_len(nsim)){ set.seed(12345+10*s); p<-L%*%rnorm(npar+2)+varb
    out[s,]<-c(impact_at(p[ib],p[it],p[npar+1],W),p[npar+1]) }
  out }

core<-list(); imps<-list()
for(wn in names(Ws)) for(Y in OUTCOMES) for(en in names(ESTS)){
  W0<-Ws[[wn]]; e<-ESTS[[en]]
  d<-dt[state %in% rownames(W0)]; al<-sort(unique(d$state)); d<-as.data.frame(d[order(match(state,al),year)]); W<-W0[al,al]
  stopifnot(all(abs(rowSums(W)-1)<1e-5))
  # SDPDm silently drops demn unless rows sum to exactly 1. The invdist-50 CSV has rounding error (< 1e-5),
  # so normalize exactly for LY-demn only; ML and LY-bias keep the 4d W so they reproduce 4d.
  if(e$demn) W<-W/rowSums(W)
  ev<-Re(eigen(W,only.values=TRUE)$values); rmax<-1/max(ev); rmin<-1/min(ev)
  ss<-sprintf("%ds2015_2025",length(al))
  tag<-sprintf("h3_sdm-%s_ai518210_lag1_ctrl4_w9901_ml_%s_%s_%s",en,Y,ss,wn)
  r<-tryCatch({
    m<-SDPDm(as.formula(paste(Y,"~",AI,"+",CTRL4)),data=d,W=W,index=c("state","year"),model="sdm",effect="twoways",
             LYtrans=e$LYt,demn=e$demn,dynamic=FALSE)
    if(e$demn && !isTRUE(m$demn)) stop("demn=TRUE was requested but SDPDm did not apply it")
    rho<-as.numeric(m$rho); valid<-is.finite(rho)&&rho>rmin&&rho<rmax
    nm<-names(m$coefficients); b<-as.numeric(m$coefficients[AI]); th<-as.numeric(m$coefficients[paste0("W*",AI)])
    core[[length(core)+1]]<-data.table(tag=tag,outcome=Y,W_version=wn,estimator=en,LYtrans=e$LYt,demn_requested=e$demn,demn_used=isTRUE(m$demn),
      N=nrow(d),rho=rho,rho_se=as.numeric(m$rho.se),rho_lo=rmin,rho_hi=rmax,rho_valid=valid,
      b1=b,se_b1=as.numeric(m$std[AI]),p_b1=as.numeric(m$pval[AI]),
      theta1=th,se_theta1=as.numeric(m$std[paste0("W*",AI)]),p_theta1=as.numeric(m$pval[paste0("W*",AI)]),
      plugin_total_check=(b+th)/(1-rho),status=if(valid)"ok" else "FAILED",
      note=if(valid)"" else "rho outside valid interval")
    pl<-impact_at(b,th,rho,W); dr<-draw_impacts(m,W,NSIM)
    oob<-sum(dr[,"rho"]>=rmax|dr[,"rho"]<=rmin)
    pk<-if(wn=="invdist50"||e$LYt) impactsSDPDm(m,NSIM=500) else NULL
    for(k in c("direct","indirect","total")){
      x<-dr[,k]; se<-sd(x); ok<-dr[,"rho"]<rmax&dr[,"rho"]>rmin
      tb<-if(!is.null(pk)) pk[[paste0(toupper(k),".tab")]] else NULL
      imps[[length(imps)+1]]<-data.table(tag=tag,outcome=Y,W_version=wn,estimator=en,effect=k,rho=rho,rho_valid=valid,
        plugin=pl[[k]],se_draws=se,p=2*pnorm(-abs(pl[[k]]/se)),ci_lo=quantile(x,.025),ci_hi=quantile(x,.975),
        mean_draws=mean(x),se_draws_in_interval=sd(x[ok]),rho_draws_out=oob,nsim=NSIM,
        pkg500_est=if(!is.null(tb)) tb[AI,1] else NA_real_,mine500_est=mean(x[1:500]),
        pkg500_se=if(!is.null(tb)) tb[AI,2] else NA_real_,mine500_se=sd(x[1:500]),
        status=if(valid)"ok" else "FAILED")
    }
    cat(sprintf("%-10s %-11s %-8s rho=%8.4f [%s] demn_used=%s indirect plug-in=%9.5f se=%8.5f out=%d\n",wn,Y,en,rho,if(valid)"ok" else "OUT",isTRUE(m$demn),pl[["indirect"]],sd(dr[,"indirect"]),oob))
    TRUE
  },error=function(err){ cat(sprintf("%-10s %-11s %-8s ERROR %s\n",wn,Y,en,conditionMessage(err)))
    core[[length(core)+1]]<<-data.table(tag=tag,outcome=Y,W_version=wn,estimator=en,LYtrans=e$LYt,demn_requested=e$demn,N=nrow(d),status="FAILED",note=conditionMessage(err)); FALSE})
}
core<-rbindlist(core,fill=TRUE); imps<-rbindlist(imps,fill=TRUE)
fwrite(core,file.path(OUT,"sdm_core.csv")); fwrite(imps,file.path(OUT,"sdm_impacts.csv"))

# ---- Checks ----
cat("\nCheck 1: my first 500 draws vs impactsSDPDm(NSIM=500)\n")
print(imps[!is.na(pkg500_est)&rho_valid,.(max_est_diff=max(abs(mine500_est-pkg500_est)),max_se_diff=max(abs(mine500_se-pkg500_se)))])
prior<-fread(PRIOR)
cat("Check 2: same estimators vs 4d (rho-valid rows; 4d means of draws)\n")
cmp<-imps[effect=="indirect"&estimator!="LY-demn"]; cmp[,LYtrans:=estimator=="LY-bias"]
cmp<-merge(cmp,prior[,.(outcome,W_version,LYtrans,prior=indirect)],by=c("outcome","W_version","LYtrans"))
print(cmp[,.(outcome,W_version,estimator,mine500_est,prior,diff=abs(mine500_est-prior))])
cat("Check 3: LY-bias rho predicted from ML fit: rho + T*Var(rho)/(1-rho)\n")
ch3<-merge(core[estimator=="ML",.(outcome,W_version,rho_ml=rho,se=rho_se)],core[estimator=="LY-bias",.(outcome,W_version,rho_lybias=rho)],by=c("outcome","W_version"))
ch3[,predicted:=rho_ml+11*se^2/(1-rho_ml)]; print(ch3); fwrite(ch3,file.path(OUT,"rho_overshoot_check.csv"))

# ---- Main-spec decision ----
A<-core[estimator=="LY-demn"&W_version=="invdist50"]
main<-if(nrow(A)==3&&all(A$rho_valid %in% TRUE)) "LY-demn" else "ML"
cat(sprintf("\nMAIN SPEC per rule: %s\n",main)); print(A[,.(outcome,rho,rho_valid,demn_used)])

# ---- W*AI variation ----
vr<-list()
for(wn in names(Ws)){ W<-Ws[[wn]]; st<-rownames(W); d<-copy(dt[state %in% st])
  for(v in c(AI,CC4)){ nc<-paste0("W_",v); d[,(nc):=0.0]
    for(y in unique(d$year)){ s<-d[year==y][order(match(state,st))]; stopifnot(identical(s$state,st)); d[year==y,(nc):=as.numeric(W%*%s[[v]])[match(state,st)]] } }
  wv<-paste0("W_",AI)
  for(pair in list(list(lbl="W*AI",v=wv),list(lbl="own AI",v=AI))){
    x<-d[[pair$v]]; r1<-resid(feols(as.formula(paste(pair$v,"~1|state")),d)); r2<-resid(feols(as.formula(paste(pair$v,"~1|state+year")),d))
    wc<-paste0("W_",CC4)
    rhs<-if(pair$lbl=="W*AI") c(AI,CC4,wc) else c(wv,CC4,wc)
    r3<-resid(feols(as.formula(paste(pair$v,"~",paste(rhs,collapse="+"),"|state+year")),d))
    vr[[length(vr)+1]]<-data.table(W_version=wn,variable=pair$lbl,N=nrow(d),sd_raw=sd(x),sd_after_state_fe=sd(r1),sd_after_state_year_fe=sd(r2),
      share_var_left_after_fe=var(r2)/var(x),sd_after_fe_and_model_x=sd(r3),range_after_fe=diff(range(r2))) } }
vr<-rbindlist(vr); print(vr)
sc<-merge(imps[outcome=="renew_share"&effect=="indirect"&rho_valid==TRUE,.(W_version,estimator,indirect=plugin,se=se_draws,p,ci_lo,ci_hi)],
          vr[variable=="W*AI",.(W_version,sd_wai=sd_after_state_year_fe)],by="W_version")
sc[,`:=`(indirect_per_1sd=indirect*sd_wai,se_per_1sd=se*sd_wai)]; print(sc)
fwrite(vr,file.path(OUT,"wai_variation.csv")); fwrite(sc,file.path(OUT,"indirect_per_1sd.csv"))

# ---- splm Lee-Yu cross-check on invdist-50 ----
sp<-list(); W<-Wi50; st<-rownames(W); d<-copy(dt)
for(v in c(AI,CC4)){ nc<-paste0("W_",v); d[,(nc):=0.0]; for(y in unique(d$year)){ s<-d[year==y][order(match(state,st))]; d[year==y,(nc):=as.numeric(W%*%s[[v]])[match(state,st)]] } }
d<-d[order(match(state,st),year)]; lw<-spdep::mat2listw(W,style="W")
for(Y in OUTCOMES){ f<-as.formula(paste(Y,"~",AI,"+",CTRL4,"+",paste0("W_",c(AI,CC4),collapse="+")))
  r<-tryCatch({ m<-spml(f,data=as.data.frame(d),index=c("state","year"),listw=lw,model="within",effect="twoways",lag=TRUE,spatial.error="none",LeeYu=TRUE,Hess=FALSE,quiet=TRUE)
    data.table(outcome=Y,rho_splm=as.numeric(m$spat.coef),b1_splm=coef(m)[[AI]],theta1_splm=coef(m)[[paste0("W_",AI)]],status="ok",note="") },
    error=function(e) data.table(outcome=Y,status="FAILED",note=conditionMessage(e)))
  sp[[length(sp)+1]]<-r }
sp<-rbindlist(sp,fill=TRUE)
if("rho_splm"%in%names(sp)) sp<-merge(sp,core[estimator=="LY-demn"&W_version=="invdist50",.(outcome,rho_sdpdm=rho,b1_sdpdm=b1,theta1_sdpdm=theta1)],by="outcome",all.x=TRUE)
print(sp); fwrite(sp,file.path(OUT,"splm_leeyu_check.csv"))
writeLines(main,file.path(OUT,"MAIN_SPEC.txt"))
cat("\nDONE\n")

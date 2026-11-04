#!/usr/bin/env Rscript
# 04e2_spillover_placebo.R
# Spillover placebo for H3 (EXPERIMENTS.md section 0 item 28): SLX (clustered) and SDM (LYtrans=FALSE main spec)
# with W*AI(t+1), on 2015-2023. W*AI(t+1) in 2024 would need 2025 AI for AK, ND, SD and WY, which BLS suppresses.
# Gate: reproduce the stored SLX and SDM main-spec results on the full sample before any new model.
# SDM versions use SDPDm model="sar" with W*X columns built here, so W*AI(t+1) can enter without W*AI(t-1).
# Usage: Rscript code/R/04e2_spillover_placebo.R --date YYYY-MM-DD
suppressPackageStartupMessages({library(fixest); library(SDPDmod); library(data.table)})
setFixest_notes(FALSE)

args <- commandArgs(trailingOnly=TRUE); date_arg <- NULL
for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
if (is.null(date_arg) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date YYYY-MM-DD required")
H3 <- "results/2026-11-03/h3"; MS <- "results/2026-11-03/h3_mainspec"
for (f in c("code/R/load_panel.R","data/out/W_inverse_distance_rowstd.csv","data/out/W_border_binary.csv",file.path(H3,"h3_slx.csv"),file.path(MS,"sdm_core.csv"),file.path(MS,"sdm_impacts.csv")))
  if (!file.exists(f)) stop("Missing input: ", f)
OUT <- file.path("results", date_arg, "h3_placebo"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)

source("code/R/load_panel.R"); dt <- load_panel()$panel
stopifnot(nrow(dt)==550, uniqueN(dt$state)==50)
OUTCOMES <- c("ln_ec","ln_ee","renew_share"); L <- "ai_dc_per1000_lag1"; F1 <- "ai_lead1_w"
CC4 <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth"); NSIM <- 2000L
setorder(dt,state,year); dt[, (F1) := winsorize(ai_dc_per1000_lead1)]   # same rule as the own-AI placebo in 04e

read_W <- function(p){r<-fread(p); W<-as.matrix(r[,-1]); rownames(W)<-colnames(W)<-r[[1]]; W}
Wi50 <- read_W("data/out/W_inverse_distance_rowstd.csv")
Wb <- read_W("data/out/W_border_binary.csv"); k48 <- rownames(Wb)[!rownames(Wb) %in% c("AK","HI")]; Wb48 <- Wb[k48,k48]; Wb48 <- Wb48/rowSums(Wb48)
Ws <- list(invdist50=Wi50, border48=Wb48)

build <- function(d0,W,vars){ al<-sort(rownames(W)); W<-W[al,al]; d<-copy(d0[state %in% al])[order(match(state,al),year)]
  stopifnot(uniqueN(d[,.N,by=state]$N)==1)
  for(v in vars){ nc<-paste0("W_",v); d[,(nc):=NA_real_]
    for(y in unique(d$year)){ i<-which(d$year==y); stopifnot(identical(d$state[i],al),!anyNA(d[[v]][i])); set(d,i,nc,as.numeric(W%*%d[[v]][i])) } }
  list(d=d,W=W) }
impact_at <- function(b,th,rho,W){ N<-nrow(W); SC<-solve(diag(N)-rho*W)%*%(b*diag(N)+th*W); d<-sum(diag(SC))/N; t<-sum(SC)/N; c(direct=d,indirect=t-d,total=t) }

# Versions: own and neighbor terms
VERS <- list(a_lag=list(own=L,wx=L,lab="AI(t-1), W*AI(t-1)"), b_lead=list(own=F1,wx=F1,lab="AI(t+1), W*AI(t+1)"),
             c_ownlag_wlead=list(own=L,wx=F1,lab="AI(t-1), W*AI(t+1)"), d_both=list(own=L,wx=c(L,F1),lab="AI(t-1), W*AI(t-1), W*AI(t+1)"),
             e_both_ownlead=list(own=c(L,F1),wx=c(L,F1),lab="AI(t-1), AI(t+1), W*AI(t-1), W*AI(t+1)"))
term <- function(v) if(v==L) "lag" else "lead"
fslx <- function(Y,v) as.formula(paste(Y,"~",paste(c(v$own,paste0("W_",v$wx),CC4,paste0("W_",CC4)),collapse=" + "),"| state + year"))
fsar <- function(Y,v) as.formula(paste(Y,"~",paste(c(v$own,CC4,paste0("W_",v$wx),paste0("W_",CC4)),collapse=" + ")))
sar <- function(Y,v,b) SDPDm(fsar(Y,v),data=as.data.frame(b$d),W=b$W,index=c("state","year"),model="sar",effect="twoways",LYtrans=FALSE,demn=FALSE,dynamic=FALSE)
draws <- function(m,v,W){ npar<-length(m$coefficients); vb<-c(m$coefficients,m$rho,m$sige); Lc<-t(chol(m$varcov)); nm<-names(m$coefficients)
  ix<-unique(c(v$own,v$wx)); out<-array(NA_real_,c(NSIM,length(ix),3),dimnames=list(NULL,ix,c("direct","indirect","total"))); rr<-numeric(NSIM)
  for(s in seq_len(NSIM)){ set.seed(12345+10*s); p<-as.numeric(Lc%*%rnorm(npar+2)+vb); rr[s]<-p[npar+1]
    for(x in ix){ b<-if(x %in% nm) p[match(x,nm)] else 0; wn<-paste0("W_",x); th<-if(wn %in% nm) p[match(wn,nm)] else 0; out[s,x,]<-impact_at(b,th,p[npar+1],W) } }
  list(i=out,rho=rr) }

# ================ GATE ================
cat("=== GATE ===\n"); g<-list(); chk<-function(l,new,old,tol) g[[length(g)+1]]<<-data.table(check=l,new=new,old=old,diff=abs(new-old),tol=tol,ok=abs(new-old)<tol)
sx<-fread(file.path(H3,"h3_slx.csv")); co<-fread(file.path(MS,"sdm_core.csv")); im<-fread(file.path(MS,"sdm_impacts.csv"))
b0<-build(dt,Wi50,c(L,CC4)); v0<-list(own=L,wx=L)
for(Y in OUTCOMES){ m<-feols(fslx(Y,v0),data=b0$d,vcov=~state); ct<-coeftable(m); o<-sx[outcome==Y&W_version=="invdist50"]; stopifnot(nrow(o)==1)
  chk(paste("SLX b1",Y),ct[L,1],o$b1,1e-8); chk(paste("SLX se_b1",Y),ct[L,2],o$se_b1,1e-8); chk(paste("SLX theta1",Y),ct[paste0("W_",L),1],o$theta1,1e-8); chk(paste("SLX se_theta1",Y),ct[paste0("W_",L),2],o$se_theta1,1e-8)
  ms<-sar(Y,v0,b0); oc<-co[outcome==Y&W_version=="invdist50"&estimator=="ML"]; stopifnot(nrow(oc)==1)
  chk(paste("SDM rho",Y),as.numeric(ms$rho),oc$rho,1e-5); chk(paste("SDM b1",Y),as.numeric(ms$coefficients[L]),oc$b1,1e-5); chk(paste("SDM theta1",Y),as.numeric(ms$coefficients[paste0("W_",L)]),oc$theta1,1e-5)
  dr<-draws(ms,v0,b0$W); pl<-impact_at(as.numeric(ms$coefficients[L]),as.numeric(ms$coefficients[paste0("W_",L)]),as.numeric(ms$rho),b0$W)
  for(k in c("direct","indirect","total")){ oi<-im[outcome==Y&W_version=="invdist50"&estimator=="ML"&effect==k]; stopifnot(nrow(oi)==1)
    chk(paste("SDM plug-in",k,Y),pl[[k]],oi$plugin,1e-5); chk(paste("SDM se_draws",k,Y),sd(dr$i[,L,k]),oi$se_draws,0.01*max(oi$se_draws,1e-3)) } }
g<-rbindlist(g); fwrite(g,file.path(OUT,"gate.csv")); print(g[,.(check,new,old,diff,ok)],nrows=100)
if(!all(g$ok)){ cat("\nGATE FAILED: stopping before any new model.\n"); print(g[ok==FALSE]); quit(status=1) }
cat(sprintf("GATE PASSED: %d of %d\n\n",sum(g$ok),nrow(g)))

# ================ PLACEBO ================
d0<-dt[year<=2023]; stopifnot(nrow(d0)==450,!anyNA(d0[[F1]]))
slxr<-list(); corer<-list(); impr<-list(); corrr<-list()
for(wn in names(Ws)){ b<-build(d0,Ws[[wn]],c(L,F1,CC4)); ss<-sprintf("%ds2015_2023",uniqueN(b$d$state)); ev<-Re(eigen(b$W,only.values=TRUE)$values); rmax<-1/max(ev); rmin<-1/min(ev)
  w<-function(x) resid(feols(as.formula(paste(x,"~1|state+year")),b$d))
  x1<-w(paste0("W_",L)); x2<-w(paste0("W_",F1)); o1<-w(L); o2<-w(F1)
  x3<-resid(lm(x2~x1+o1)); corrr[[wn]]<-data.table(W_version=wn,N=nrow(b$d),sd_W_lag=sd(x1),sd_W_lead=sd(x2),corr_W_lag_W_lead=cor(x1,x2),corr_own_lag_own_lead=cor(o1,o2),sd_W_lead_given_W_lag_and_own_lag=sd(x3))
  for(vn in names(VERS)) for(Y in OUTCOMES){ v<-VERS[[vn]]; tagb<-sprintf("%s_ai518210_%s_ctrl4_w9901",vn,"lead1lag1")
    m<-feols(fslx(Y,v),data=b$d,vcov=~state); ct<-coeftable(m); ci<-confint(m); V<-vcov(m); G<-uniqueN(b$d$state); nb<-nrow(b$d)
    rec<-function(tn,e,s,p,lo,hi) slxr[[length(slxr)+1]]<<-data.table(tag=sprintf("h3_slx-placebo-%s_cl-state_%s_%s_%s_%s",tagb,Y,ss,wn,tn),version=vn,spec=v$lab,W_version=wn,outcome=Y,term=tn,estimate=e,se=s,pval=p,ci_lo=lo,ci_hi=hi,N=m$nobs,vcov_type="CRV1-state",status="ok")
    for(x in v$own) rec(paste0("own_",term(x)),ct[x,1],ct[x,2],ct[x,4],ci[x,1],ci[x,2])
    for(x in v$wx){ wx<-paste0("W_",x); rec(paste0("theta_",term(x)),ct[wx,1],ct[wx,2],ct[wx,4],ci[wx,1],ci[wx,2])
      if(x %in% v$own){ s<-sqrt(sum(V[c(x,wx),c(x,wx)])); t0<-ct[x,1]+ct[wx,1]; q<-qt(.975,G-1); rec(paste0("total_",term(x)),t0,s,2*pt(-abs(t0/s),G-1),t0-q*s,t0+q*s) } }
    if(length(v$wx)==2){ h<-c(paste0("W_",L),paste0("W_",F1)); bv<-coef(m)[h]; Wald<-as.numeric(t(bv)%*%solve(V[h,h])%*%bv)/2; slxr[[length(slxr)+1]]<-data.table(tag=sprintf("h3_slx-placebo-%s_cl-state_%s_%s_%s_jointF",tagb,Y,ss,wn),version=vn,spec=v$lab,W_version=wn,outcome=Y,term="joint_F_theta_lag_lead",estimate=Wald,se=NA_real_,pval=pf(Wald,2,G-1,lower.tail=FALSE),ci_lo=NA_real_,ci_hi=NA_real_,N=m$nobs,vcov_type="CRV1-state",status="ok") }
    tags<-sprintf("h3_sdm-ML-placebo-%s_ml_%s_%s_%s",tagb,Y,ss,wn)
    r<-tryCatch({ ms<-sar(Y,v,b); rho<-as.numeric(ms$rho); valid<-is.finite(rho)&&rho>rmin&&rho<rmax; cf<-ms$coefficients; nm<-names(cf)
      for(x in unique(c(v$own,paste0("W_",v$wx)))) corer[[length(corer)+1]]<-data.table(tag=tags,version=vn,spec=v$lab,W_version=wn,outcome=Y,rho=rho,rho_se=as.numeric(ms$rho.se),rho_lo=rmin,rho_hi=rmax,rho_valid=valid,coef=x,estimate=as.numeric(cf[x]),se=as.numeric(ms$std[x]),pval=as.numeric(ms$pval[x]),N=nb,status=if(valid)"ok" else "FAILED")
      dr<-draws(ms,v,b$W); oob<-sum(dr$rho>=rmax|dr$rho<=rmin)
      for(x in unique(c(v$own,v$wx))){ bb<-if(x %in% nm) as.numeric(cf[x]) else 0; wx<-paste0("W_",x); th<-if(wx %in% nm) as.numeric(cf[wx]) else 0; pl<-impact_at(bb,th,rho,b$W)
        for(k in c("direct","indirect","total")){ z<-dr$i[,x,k]; se<-sd(z); impr[[length(impr)+1]]<-data.table(tag=tags,version=vn,spec=v$lab,W_version=wn,outcome=Y,variable=term(x),effect=k,rho=rho,rho_valid=valid,plugin=pl[[k]],se_draws=se,p=2*pnorm(-abs(pl[[k]]/se)),ci_lo=quantile(z,.025),ci_hi=quantile(z,.975),rho_draws_out=oob,nsim=NSIM,N=nb,status=if(valid)"ok" else "FAILED") } }
      cat(sprintf("%-10s %-15s %-11s rho=%7.4f [%s] out=%d\n",wn,vn,Y,rho,if(valid)"ok" else "OUT",oob)); TRUE },
      error=function(e){ cat(sprintf("%-10s %-15s %-11s ERROR %s\n",wn,vn,Y,conditionMessage(e))); corer[[length(corer)+1]]<<-data.table(tag=tags,version=vn,spec=v$lab,W_version=wn,outcome=Y,N=nb,status="FAILED",note=conditionMessage(e)); FALSE }) } }
fwrite(rbindlist(slxr),file.path(OUT,"placebo_slx.csv")); fwrite(rbindlist(corer,fill=TRUE),file.path(OUT,"placebo_sdm_core.csv")); fwrite(rbindlist(impr),file.path(OUT,"placebo_sdm_impacts.csv")); cr<-rbindlist(corrr); fwrite(cr,file.path(OUT,"lead_lag_variation.csv")); print(cr)
cat("DONE\n")

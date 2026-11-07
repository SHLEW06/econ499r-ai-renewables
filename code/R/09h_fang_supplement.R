#!/usr/bin/env Rscript
# 09h_fang_supplement.R: B2 (EXPERIMENTS.md 14.6): our data vs Fang's Table A1, and Supplement B1's negative indicators by number.
# Fang's published values are typed from literature/Fang_Lee_Li_2025_supplement.docx (Tables A1 and B1).
# Usage: Rscript code/R/09h_fang_supplement.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date(); OUT <- file.path("results", date_arg, "extend")
need(c("data/fang_panel.csv","data/seds_old_basis.csv","data/raw/eia/seds/use_all_btu.csv","data/raw/eia/seds_archive/complete_seds_2021.zip"))
d <- fread("data/fang_panel.csv"); sb <- fread("data/seds_old_basis.csv")
d <- merge(d, sb[,.(state,year,re_bbtu_rebuilt,re_bbtu_k26,RETCB_arch2021)], by=c("state","year"), all.x=TRUE)
u <- fread("data/raw/eia/seds/use_all_btu.csv", header=TRUE); u <- u[MSN %in% c("CLTCB","NGTCB","PATCB")]
u <- melt(u, id.vars=c("Data_Status","State","MSN"), variable.name="year", value.name="v")[, .(state=State, MSN, year=as.integer(as.character(year)), v=as.numeric(v))]
a <- fread(cmd="unzip -p data/raw/eia/seds_archive/complete_seds_2021.zip complete_seds_2021.csv", header=TRUE)[MSN %in% c("CLTCB","NGTCB","PATCB"), .(state=StateCode, MSN, year=Year, va=Data)]
w <- dcast(merge(u, a, by=c("state","MSN","year"), all.x=TRUE), state + year ~ MSN, value.var=c("v","va"))
d <- merge(d, w, by=c("state","year"), all.x=TRUE); setorder(d, state, year)
S <- d[year %between% c(2018,2021)]
S[, `:=`(lnET=log(re_bbtu), lnET_arch=log(RETCB_arch2021), lnET_rb=log(re_bbtu_rebuilt), lnET_k26=log(re_bbtu_k26), lnAIp=log(ai_postings), lnEPU=log(epu_composite), lnEP=log(ep_tetcd),
         lnGDP=log(gdp_real_musd2017), lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000))]
stopifnot(nrow(S)==204)
# ---- Table A1 ----
A1 <- data.table(var=c("ET","AI","EPU","EP","GDP","POP","EDU"), N=204, mean=c(11.790,7.700,6.090,2.930,12.260,8.270,4.230), sd=c(1.260,1.480,0.610,0.190,1.050,1.040,0.300),
                 min=c(7.380,4.540,4.190,2.130,10.280,6.360,3.320), max=c(14.000,11.290,7.750,3.490,14.870,10.580,5.250))
V <- list(c("lnET","ET","current SEDS"), c("lnET_arch","ET","June 2023 SEDS"), c("lnET_rb","ET","rebuilt"), c("lnET_k26","ET","k = 2.6"), c("lnAIp","AI",""), c("lnEPU","EPU",""), c("lnEP","EP",""),
          c("lnGDP","GDP",""), c("lnPOP","POP",""), c("lnEDU","EDU",""))
UN <- list(EPU=c("doubled index (ln 2)"=log(2)), POP=c("thousands vs persons"=log(1000)), GDP=c("chained 2012 vs 2017 dollars"=log(1.0757)))
T1 <- rbindlist(lapply(V, function(z) { x <- S[[z[1]]]; f <- A1[var==z[2]]; dd <- mean(x) - f$mean
  u_ <- UN[[z[2]]]; um <- if (!is.null(u_)) { m <- names(u_)[abs(abs(dd) - u_) < 0.05]; if (length(m)) sprintf("consistent with %s (expected %.3f)", m[1], u_[[m[1]]]) else "" } else ""
  data.table(tag=sprintf("ext_a1_%s_%s", z[1], gsub(" ", "", z[3])), variable=z[1], fang_var=z[2], basis=z[3], N=sum(!is.na(x)), mean=mean(x), sd=sd(x), min=min(x), max=max(x),
             fang_N=f$N, fang_mean=f$mean, fang_sd=f$sd, fang_min=f$min, fang_max=f$max, diff=dd, diff_in_our_sd=dd/sd(x), diff_in_fang_sd=dd/f$sd,
             sd_ratio=sd(x)/f$sd, flag=abs(dd/sd(x)) > 0.25, unit_shift_match=um) }))
fwrite(T1, file.path(OUT, "e1_descriptives_vs_tableA1.csv"))
# ---- Supplement B1 negative indicators ----
CF <- c("lnEPU","lnEP","lnGDP","lnPOP","lnEDU")
FB <- data.table(outcome=c("coal","gas","petroleum"), fang_ai=c(-0.178,0.0023,-0.0160), fang_t=c(-1.43,0.13,-1.08), fang_N=c(192,204,204))
NB <- list()
for (o in list(c("coal","CLTCB"), c("gas","NGTCB"), c("petroleum","PATCB"))) for (bs in c("current","june2023")) {
  col <- if (bs=="current") paste0("v_", o[2]) else paste0("va_", o[2]); dd <- copy(S[get(col) > 0]); dd[, y := log(get(col))]
  m <- feols(as.formula(paste("y ~ lnAIp +", paste(CF, collapse=" + "), "| state")), data=dd, vcov="iid"); ct <- coeftable(m); ci <- confint(m); f <- FB[outcome==o[1]]
  NB[[length(NB)+1]] <- data.table(tag=sprintf("ext_b1_fang6_aipostings_ln_%s_%s", o[1], bs), outcome=o[1], msn=o[2], basis=bs, estimate=ct["lnAIp",1], t=ct["lnAIp",3], pval=ct["lnAIp",4],
    ci_lo=ci["lnAIp",1], ci_hi=ci["lnAIp",2], N=m$nobs, fang_ai=f$fang_ai, fang_t=f$fang_t, fang_N=f$fang_N, fang_inside_ci=(f$fang_ai >= ci["lnAIp",1] & f$fang_ai <= ci["lnAIp",2])) }
NB <- rbindlist(NB); fwrite(NB, file.path(OUT, "e1_negative_indicator_vs_B1.csv"))
print(T1[, .(variable, basis, mean=round(mean,3), fang_mean, sd=round(sd,3), fang_sd, diff_our_sd=round(diff_in_our_sd,2), flag, unit_shift_match)])
print(NB[, .(outcome, basis, est=signif(estimate,3), t=round(t,2), N, fang_ai, fang_t, fang_N, fang_inside_ci)])

#!/usr/bin/env Rscript
# 09d_national_drivers.R: prompts/09_extend.md section 4 (EXPERIMENTS.md section 14.4, deviations X3-X4).
# E4.1 year effects; E4.3 drivers model (interim: no wind cost, no PTC until the blocked sources arrive);
# fitted driver path vs year effects; AI coefficient with state FE only, drivers, and two-way FE.
# Usage: Rscript code/R/09d_national_drivers.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date()
need(c("data/extend_outcomes.csv","data/extend_drivers_national.csv","data/extend_drivers_state.csv"))
OUT <- file.path("results", date_arg, "extend"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
P <- main_panel()
eo <- fread("data/extend_outcomes.csv")[is_dc==0, .(state, year, ln_gen_wind, ln_gen_solar)]
P <- merge(P, eo, by=c("state","year")); for (v in c("ln_gen_wind","ln_gen_solar")) P[, (v) := wz(get(v))]
nat <- fread("data/extend_drivers_national.csv"); stt <- fread("data/extend_drivers_state.csv")
rps <- fread("data/fang_panel.csv")[, .(state, year, rps=target_pct)]
P <- merge(P, nat[, .(year, solar_lcoe=solar_lcoe_2025usd_mwh/100, itc=itc_pct/100, hh=hh_usd_mmbtu, wind_lcoe=wind_lcoe_2025usd_mwh/100, ptc=ptc_pct_of_full/100)], by="year")
P <- merge(P, stt[, .(state, wind_cf, solar_cf, gas15=gas_share_2015)], by="state"); P <- merge(P, rps, by=c("state","year")); setorder(P, state, year)
P[, `:=`(scf_x_slcoe=solar_cf*solar_lcoe, scf_x_itc=solar_cf*itc, gas_x_hh=gas15*hh, wcf_x_wlcoe=wind_cf*wind_lcoe, wcf_x_ptc=wind_cf*ptc)]
stopifnot(nrow(P)==550, !anyNA(P$solar_lcoe), !anyNA(P$hh), !anyNA(P$rps))
FULL <- !anyNA(P$wind_lcoe) && !anyNA(P$ptc)
DRV <- c("rps","scf_x_slcoe","scf_x_itc","gas_x_hh","solar_lcoe","itc","hh"); if (FULL) DRV <- c(DRV, "wcf_x_wlcoe","wcf_x_ptc","wind_lcoe","ptc")
DLAB <- if (FULL) "drivers" else "drivers-interim"
YS <- c(renew_share="renew_share", ln_gen_wind="ln_gen_wind", ln_gen_solar="ln_gen_solar")
rows <- list(); rec <- function(...) rows[[length(rows)+1]] <<- data.table(...)

# ---------------- E4.1 year effects (jobs, main spec, year dummies base 2015) ----------------
ye <- list()
for (y in YS) { d0 <- P[!is.na(get(y)) & !is.na(jobs_lag1)]
  mod <- feols(as.formula(paste(y, "~ jobs_lag1 + i(year, ref=2015) +", paste(CTRL4, collapse=" + "), "| state")), data=d0, vcov=~state)
  ct <- coeftable(mod); ci <- confint(mod); yy <- grep("^year::", rownames(ct), value=TRUE)
  ye[[y]] <- rbind(data.table(outcome=y, year=2015L, estimate=0, se=0, ci_lo=0, ci_hi=0, pval=NA_real_),
                   data.table(outcome=y, year=as.integer(sub("year::", "", yy)), estimate=ct[yy,1], se=ct[yy,2], ci_lo=ci[yy,1], ci_hi=ci[yy,2], pval=ct[yy,4]))
  ye[[y]][, tag := sprintf("ext_natl_yeareffects_ai518210_lag1_ctrl4_w9901_cl-state_%s_50s_%d", y, year)] }
YE <- rbindlist(ye); fwrite(YE, file.path(OUT, "s4_year_effects.csv"))

# ---------------- E4.3 drivers model, three AI models, path fit ----------------
path <- list()
for (y in YS) for (mn in names(AIM)) { m <- AIM[[mn]]; d0 <- P[!is.na(get(y)) & !is.na(get(m$lag))]
  fits <- list(statefe=feols(as.formula(paste(y, "~", m$lag, "+", paste(CTRL4, collapse=" + "), "| state")), data=d0, vcov=~state),
               drivers=feols(as.formula(paste(y, "~", m$lag, "+", paste(c(DRV, CTRL4), collapse=" + "), "| state")), data=d0, vcov=~state),
               twfe=fit_main(y, m$lag, d0))
  for (k in names(fits)) { mod <- fits[[k]]; ct <- coeftable(mod); ci <- confint(mod); kk <- if (k=="drivers") DLAB else k
    rec(tag=sprintf("ext_natl_%s_%s_lag1_ctrl4_w9901_cl-state_%s_50s", kk, m$tag, y), outcome=y, ai_measure=m$tag, model=kk, term="AI", estimate=ct[m$lag,1], se=ct[m$lag,2],
        pval=ct[m$lag,4], ci_lo=ci[m$lag,1], ci_hi=ci[m$lag,2], N=mod$nobs, years=paste(range(d0$year), collapse="-"), within_r2=as.numeric(fitstat(mod,"wr2")[[1]]))
    if (k=="drivers") { for (x in DRV) rec(tag=sprintf("ext_natl_%s_%s_lag1_ctrl4_w9901_cl-state_%s_50s_%s", kk, m$tag, y, x), outcome=y, ai_measure=m$tag, model=kk, term=x,
                                          estimate=ct[x,1], se=ct[x,2], pval=ct[x,4], ci_lo=ci[x,1], ci_hi=ci[x,2], N=mod$nobs, years=paste(range(d0$year), collapse="-"), within_r2=NA_real_)
      b <- coef(mod)[DRV]; d0[, drv := as.matrix(.SD) %*% b, .SDcols=DRV]
      pth <- d0[, .(driver_path=mean(drv)), by=year][order(year)]; pth[, driver_path := driver_path - driver_path[1]]
      if (mn=="jobs") { z <- merge(pth, YE[outcome==y, .(year, year_effect=estimate)], by="year"); z[, year_effect := year_effect - year_effect[1]]
        r <- cor(z$driver_path, z$year_effect)
        path[[y]] <- data.table(tag=sprintf("ext_natl_pathfit_ai518210_%s_%s", DLAB, y), outcome=y, model=DLAB, years=paste(range(z$year), collapse="-"), n_years=nrow(z),
                                correlation=r, r_squared=r^2, slope=coef(lm(year_effect ~ driver_path, z))[2], note="driver path = mean over states of the fitted driver terms, 2015 = 0")
        fwrite(z, file.path(OUT, sprintf("s4_path_%s.csv", y))) } } } }
res <- rbindlist(rows); fwrite(res, file.path(OUT, "s4_drivers_models.csv")); PF <- rbindlist(path); fwrite(PF, file.path(OUT, "s4_path_fit.csv"))
print(PF[, .(outcome, model, correlation=round(correlation,3), r_squared=round(r_squared,3))])
print(res[term=="AI", .(outcome, ai_measure, model, est=signif(estimate,3), p=round(pval,3), N)])
print(res[term!="AI" & ai_measure=="ai518210", .(outcome, term, est=signif(estimate,3), p=round(pval,3))])
cat(sprintf("Drivers model: %s (wind cost and PTC %s)\nDONE\n", DLAB, if (FULL) "included" else "pending, deviation X3"))

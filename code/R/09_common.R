# 09_common.R: shared setup for prompts/09_extend.md drivers (EXPERIMENTS.md section 14).
# Main spec: 50 states, two-way FE, AI(t-1), ctrl4, clustered by state, winsorized 1/99, via load_panel.R.
# Two AI measures: data-center jobs per 1,000 workers (ai_dc_per1000) and AI postings per 1,000 workers.
suppressPackageStartupMessages({library(fixest); library(data.table)})
setFixest_notes(FALSE)
source("code/R/load_panel.R")

parse_date <- function() {
  args <- commandArgs(trailingOnly=TRUE); d <- NULL
  for (i in seq_along(args)) if (args[i]=="--date" && i<length(args)) d <- args[i+1]
  if (is.null(d) || !grepl("^\\d{4}-\\d{2}-\\d{2}$", d)) stop("--date YYYY-MM-DD required")
  d
}
need <- function(f) for (x in f) if (!file.exists(x)) stop("Missing input: ", x)
CTRL4 <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth")
wz <- function(x) winsorize(x, 0.01, 0.99)

# Panel with both AI measures, lags and leads (AI winsorized pooled, as load_panel does for jobs)
main_panel <- function() {
  need(c("data/out/state_panel_2015_2025.csv","data/fang_panel.csv"))
  P <- load_panel()$panel
  fp <- fread("data/fang_panel.csv")[, .(state, year, ai_postings)]
  P <- merge(P, fp, by=c("state","year"), all.x=TRUE); setorder(P, state, year)
  P[, post_per1000 := ai_postings / total_jobs * 1000]
  P[, `:=`(post_lag1 = shift(post_per1000, 1), post_lead1 = shift(post_per1000, -1)), by=state]
  P[, `:=`(post_lag1 = wz(post_lag1), post_lead1 = wz(post_lead1), jobs_lag1 = ai_dc_per1000_lag1, jobs_lead1 = wz(ai_dc_per1000_lead1))]
  stopifnot(uniqueN(P$state)==50, nrow(P)==550)
  P
}
AIM <- list(jobs=list(lag="jobs_lag1", lead="jobs_lead1", tag="ai518210", lab="Data-center jobs per 1,000 (t-1)"),
            post=list(lag="post_lag1", lead="post_lead1", tag="aipostp1000", lab="AI postings per 1,000 (t-1)"))

fit_main <- function(y, x, dd, extra=character(0), fe="state + year")
  feols(as.formula(paste(y, "~", paste(c(x, extra, CTRL4), collapse=" + "), "|", fe)), data=dd, vcov=~state)

ROWS <- new.env(); ROWS$r <- list()
addrow <- function(block, model, m, lag, y, sample, term, mod, x, note="", family=NA_character_, extra=list()) {
  ct <- coeftable(mod); ci <- confint(mod)
  row <- data.table(tag=sprintf("ext_%s_%s_%s_%s_ctrl4_w9901_cl-state_%s_%s%s", block, model, m$tag, lag, y, sample, if (term=="AI") "" else paste0("_", term)),
                    block=block, model=model, family=family, ai_measure=m$tag, lag=lag, outcome=y, term=term, variable=x,
                    estimate=ct[x,1], se=ct[x,2], pval=ct[x,4], ci_lo=ci[x,1], ci_hi=ci[x,2], N=mod$nobs, n_states=length(unique(mod$fixef_id$state %||% NA)),
                    within_r2=as.numeric(fitstat(mod, "wr2")[[1]]), status="ok", note=note)
  for (k in names(extra)) row[[k]] <- extra[[k]]
  ROWS$r[[length(ROWS$r)+1]] <- row; invisible(row)
}
`%||%` <- function(a, b) if (is.null(a)) b else a
failrow <- function(block, model, m, lag, y, sample, note, family=NA_character_)
  ROWS$r[[length(ROWS$r)+1]] <- data.table(tag=sprintf("ext_%s_%s_%s_%s_ctrl4_w9901_cl-state_%s_%s", block, model, m$tag, lag, y, sample), block=block, model=model,
                                           family=family, ai_measure=m$tag, lag=lag, outcome=y, term="AI", status="FAILED", note=note)

# Main-spec AI(t-1) row and, on request, the lead placebo on the same sample
run_main <- function(block, y, dd, m, family, sample_lab, note="") {
  d0 <- dd[!is.na(get(y)) & !is.na(get(m$lag))]
  if (nrow(d0) < 60 || uniqueN(d0$state) < 10 || sd(d0[[y]]) == 0) { failrow(block, "twfe", m, "lag1", y, sample_lab, "too few observations or no variation", family); return(NULL) }
  mod <- tryCatch(fit_main(y, m$lag, d0), error=function(e) NULL)
  if (is.null(mod) || !(m$lag %in% names(coef(mod)))) { failrow(block, "twfe", m, "lag1", y, sample_lab, "fit failed", family); return(NULL) }
  addrow(block, "twfe", m, "lag1", y, sample_lab, "AI", mod, m$lag, note=note, family=family,
         extra=list(sd_within_ai=sd(d0[[m$lag]] - ave(d0[[m$lag]], d0$state)), years=paste(range(d0$year), collapse="-")))
}
run_lead <- function(block, y, dd, m, family, sample_lab) {
  d0 <- dd[!is.na(get(y)) & !is.na(get(m$lag)) & !is.na(get(m$lead))]
  a <- fit_main(y, m$lag, d0); b <- fit_main(y, m$lead, d0)
  la <- addrow(block, "placebo", m, "lag1", y, paste0(sample_lab, "pl"), "AI", a, m$lag, note="AI(t-1) on the placebo sample", family=family)
  le <- addrow(block, "placebo", m, "lead1", y, paste0(sample_lab, "pl"), "AI", b, m$lead, note="AI(t+1) in place of AI(t-1)", family=family)
  list(lag=la, lead=le)
}
add_bh <- function(dt, fam) { i <- which(dt$family==fam & dt$model=="twfe" & dt$lag=="lag1" & dt$term=="AI" & dt$status=="ok"); dt[i, qval := p.adjust(pval, "BH")]; dt }
clearly_smaller <- function(lag_est, lead_est, lead_p) abs(lead_est) < 0.5*abs(lag_est) & lead_p >= 0.10

#!/usr/bin/env Rscript
# 04b_extras2.R
# Two targeted additions requested after Phase 4b/4c review:
#   A) hydro_share and other_renew_share (geothermal + wood + otherbio / total)
#      TWFE ctrl4, same spec as H1 extras. Appended to h1_extras.csv.
#   B) AI × high_price linear combinations:
#      slope for low-price states and high-price states separately,
#      each with clustered SE and p. Written to het_lincom.csv.
# No existing results are overwritten.
# Usage: Rscript code/R/04b_extras2.R --date 2026-11-02

suppressPackageStartupMessages({
  library(fixest)
  library(data.table)
})

args <- commandArgs(trailingOnly = TRUE)
date_arg <- NULL
for (i in seq_along(args)) {
  if (args[i] == "--date" && i < length(args)) date_arg <- args[i + 1]
}
if (is.null(date_arg)) stop("--date YYYY-MM-DD required")

OUT <- file.path("results", date_arg, "h1")
if (!dir.exists(OUT)) stop("Output directory not found: ", OUT)

source("code/R/load_panel.R")
res <- load_panel()
dt  <- res$panel

# ---- Build new share outcomes ----------------------------------------------
dt[, hydro_share      := gen_hydro_mwh / gen_total_mwh]
dt[, other_renew_share := (gen_geothermal_mwh + gen_wood_mwh + gen_otherbio_mwh) / gen_total_mwh]

# Winsorize at 1/99 (same policy as other outcomes)
winsorize <- function(x, p_lo=0.01, p_hi=0.99) {
  lo <- quantile(x, p_lo, na.rm=TRUE); hi <- quantile(x, p_hi, na.rm=TRUE)
  pmax(pmin(x, hi), lo)
}
dt[, hydro_share       := winsorize(hydro_share)]
dt[, other_renew_share := winsorize(other_renew_share)]
cat(sprintf("hydro_share:       min=%.4f  median=%.4f  max=%.4f  NAs=%d\n",
            min(dt$hydro_share, na.rm=TRUE), median(dt$hydro_share, na.rm=TRUE),
            max(dt$hydro_share, na.rm=TRUE), sum(is.na(dt$hydro_share))))
cat(sprintf("other_renew_share: min=%.4f  median=%.4f  max=%.4f  NAs=%d\n",
            min(dt$other_renew_share, na.rm=TRUE), median(dt$other_renew_share, na.rm=TRUE),
            max(dt$other_renew_share, na.rm=TRUE), sum(is.na(dt$other_renew_share))))

ctrl4 <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"
cc4   <- c("ai_dc_per1000_lag1","ln_gdp_pc","manuf_share","price_c_kwh","pop_growth")

tidy_row <- function(m, tag, outcome) {
  ct <- coeftable(m)
  cn <- "ai_dc_per1000_lag1"
  row <- ct[cn, ]; ci <- confint(m)[cn, ]
  data.table(tag=tag, outcome=outcome, coef=cn,
             estimate=as.numeric(row[["Estimate"]]),
             se      =as.numeric(row[["Std. Error"]]),
             tstat   =as.numeric(row[["t value"]]),
             pval    =as.numeric(row[["Pr(>|t|)"]]),
             ci_lo   =as.numeric(ci[1]), ci_hi=as.numeric(ci[2]),
             N=m$nobs, within_r2=r2(m,"wr2"),
             vcov_type="CRV1-state", sample="50s2015_2025",
             controls="ctrl4", status="ok")
}

# ---- A: hydro_share and other_renew_share ----------------------------------
cat("\n=== A: hydro_share and other_renew_share ===\n")
share_rows <- list()
for (Y in c("hydro_share","other_renew_share")) {
  cc_y <- c(Y, cc4)
  d_cc <- dt[complete.cases(dt[, ..cc_y])]
  tag  <- sprintf("h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_%s_50s2015_2025", Y)
  m    <- feols(as.formula(paste(Y, "~ ai_dc_per1000_lag1 +", ctrl4, "| state + year")),
                data=d_cc, vcov=~state)
  r    <- tidy_row(m, tag, Y)
  share_rows[[Y]] <- r
  cat(sprintf("  %-20s  a1=%9.5f  SE=%8.5f  p=%.3f  N=%d\n",
              Y, r$estimate, r$se, r$pval, r$N))
}
share_dt <- rbindlist(share_rows)
ext_path <- file.path(OUT, "h1_extras.csv")
fwrite(share_dt, ext_path, append=TRUE)
cat(sprintf("Appended %d rows to %s\n", nrow(share_dt), ext_path))

# ---- B: AI × high_price linear combinations --------------------------------
cat("\n=== B: AI x high_price linear combinations (renew_share) ===\n")

# Rebuild frozen 2015 moderators (same as 04b_step1_twfe_ctrl4.R)
base2015 <- dt[year==2015, .(state,
  net_exporter_2015 = net_exporter,
  high_price_2015   = high_price)]
dt <- merge(dt, base2015, by="state")
dt[, high_price_2015_c := high_price_2015 - mean(high_price_2015, na.rm=TRUE)]

mean_hp <- mean(dt[year==2015, high_price_2015], na.rm=TRUE)
cat(sprintf("  mean(high_price_2015) = %.4f  → low-price_c=%.4f  high-price_c=%.4f\n",
            mean_hp, 0-mean_hp, 1-mean_hp))

cc_h <- c("renew_share","ai_lag1_c","high_price_2015_c", strsplit(ctrl4," \\+ ")[[1]])
d_h  <- dt[complete.cases(dt[, ..cc_h])]

m_hp <- feols(renew_share ~ ai_lag1_c * high_price_2015_c + ln_gdp_pc + manuf_share +
                price_c_kwh + pop_growth | state + year,
              data=d_h, vcov=~state)

ct  <- coeftable(m_hp)
V   <- vcov(m_hp)
alpha_hat <- ct["ai_lag1_c","Estimate"]
gamma_hat <- ct["ai_lag1_c:high_price_2015_c","Estimate"]
cat(sprintf("  alpha (ai_lag1_c main):       %.6f  (p=%.3f)\n",
            alpha_hat, ct["ai_lag1_c","Pr(>|t|)"]))
cat(sprintf("  gamma (interaction):          %.6f  (p=%.3f)\n",
            gamma_hat, ct["ai_lag1_c:high_price_2015_c","Pr(>|t|)"]))

coef_names <- c("ai_lag1_c","ai_lag1_c:high_price_2015_c")
Vsub <- V[coef_names, coef_names]

# Slope for low-price state (high_price_2015=0 → high_price_2015_c = -mean_hp)
c_low  <- c(1, 0 - mean_hp)
slope_low  <- sum(c_low * c(alpha_hat, gamma_hat))
se_low     <- sqrt(as.numeric(t(c_low) %*% Vsub %*% c_low))
t_low      <- slope_low / se_low
p_low      <- 2 * pt(-abs(t_low), df=49)   # 50 clusters → df≈49

# Slope for high-price state (high_price_2015=1 → high_price_2015_c = 1-mean_hp)
c_high <- c(1, 1 - mean_hp)
slope_high <- sum(c_high * c(alpha_hat, gamma_hat))
se_high    <- sqrt(as.numeric(t(c_high) %*% Vsub %*% c_high))
t_high     <- slope_high / se_high
p_high     <- 2 * pt(-abs(t_high), df=49)

cat(sprintf("\n  Slope for LOW-price state:    %.6f  SE=%.6f  t=%.3f  p=%.3f\n",
            slope_low, se_low, t_low, p_low))
cat(sprintf("  Slope for HIGH-price state:   %.6f  SE=%.6f  t=%.3f  p=%.3f\n",
            slope_high, se_high, t_high, p_high))

lincom_dt <- data.table(
  outcome="renew_share", moderator="high_price_2015",
  group=c("low_price","high_price","interaction"),
  hp_value=c(0,1,NA_real_),
  hp_c_value=c(0-mean_hp, 1-mean_hp, NA_real_),
  mean_hp=mean_hp,
  estimate=c(slope_low, slope_high, gamma_hat),
  se=c(se_low, se_high, ct["ai_lag1_c:high_price_2015_c","Std. Error"]),
  tstat=c(t_low, t_high, ct["ai_lag1_c:high_price_2015_c","t value"]),
  pval=c(p_low, p_high, ct["ai_lag1_c:high_price_2015_c","Pr(>|t|)"]),
  df=c(49,49,NA_real_),
  vcov_type="CRV1-state", controls="ctrl4", N=nrow(d_h), status="ok"
)
lincom_path <- file.path(OUT, "het_lincom.csv")
fwrite(lincom_dt, lincom_path)
cat(sprintf("\nWrote %s\n", lincom_path))
cat("=== 04b_extras2.R complete ===\n")

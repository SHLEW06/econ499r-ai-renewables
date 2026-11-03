#!/usr/bin/env Rscript
# 04b_step1_twfe_checks.R — Phase 4b review checks
# Usage: Rscript code/R/04b_step1_twfe_checks.R --date 2026-11-02
# Appends new rows to h1_extras.csv. Writes lm_proper.csv.

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
if (!dir.exists(OUT)) stop(paste("Output dir not found:", OUT))

cat("\n=== 04b checks ===\nDate:", date_arg, "\nOutput:", OUT, "\n\n")

source("code/R/load_panel.R")
res <- load_panel()
dt  <- res$panel

write_append <- function(df, fname) {
  path <- file.path(OUT, fname)
  fwrite(df, path, append = file.exists(path))
  invisible(path)
}

tidy_row <- function(m, tag, outcome, vcov_type, sample_desc, controls_desc,
                     coef_name = "ai_dc_per1000_lag1") {
  ct <- coeftable(m)
  if (!coef_name %in% rownames(ct))
    return(data.table(tag=tag, outcome=outcome, coef=coef_name,
                      estimate=NA_real_, se=NA_real_, tstat=NA_real_,
                      pval=NA_real_, ci_lo=NA_real_, ci_hi=NA_real_,
                      N=m$nobs, within_r2=NA_real_,
                      vcov_type=vcov_type, sample=sample_desc,
                      controls=controls_desc, status="COEF_MISSING"))
  row <- ct[coef_name, ]
  ci  <- confint(m)[coef_name, ]
  data.table(tag=tag, outcome=outcome, coef=coef_name,
             estimate=as.numeric(row[["Estimate"]]),
             se      =as.numeric(row[["Std. Error"]]),
             tstat   =as.numeric(row[["t value"]]),
             pval    =as.numeric(row[["Pr(>|t|)"]]),
             ci_lo   =as.numeric(ci[1]),
             ci_hi   =as.numeric(ci[2]),
             N=m$nobs, within_r2=r2(m, "wr2"),
             vcov_type=vcov_type, sample=sample_desc,
             controls=controls_desc, status="ok")
}

ctrl5 <- "ln_gdp_pc + price_c_kwh + tech_share + manuf_share + pop_growth"
cc5   <- c("ai_dc_per1000_lag1", "ln_gdp_pc", "price_c_kwh",
           "tech_share", "manuf_share", "pop_growth")

# -----------------------------------------------------------------------
# 0. Within-state SD of ai_dc_per1000_lag1
# -----------------------------------------------------------------------
cat("---- 0. Within-state SD of lagged AI ----\n")
dt[, ai_lag1_state_mean := mean(ai_dc_per1000_lag1, na.rm = TRUE), by = state]
dt[, ai_lag1_within     := ai_dc_per1000_lag1 - ai_lag1_state_mean]
within_sd <- dt[!is.na(ai_lag1_within), sd(ai_lag1_within)]
pooled_sd <- dt[!is.na(ai_dc_per1000_lag1), sd(ai_dc_per1000_lag1)]
cat(sprintf("Pooled SD:       %.4f\n", pooled_sd))
cat(sprintf("Within-state SD: %.4f\n", within_sd))
cat(sprintf("1-SD (within) move in new_renew_mw: %.1f MW\n\n", within_sd * 74.514))

# -----------------------------------------------------------------------
# 1. Zero / negative check for generation variables (before logging)
# -----------------------------------------------------------------------
cat("---- 1. Generation variable zero/negative check ----\n")
gen_vars <- c("gen_renew_mwh", "gen_fossil_mwh", "gen_total_mwh")
for (v in gen_vars) {
  vals  <- dt[[v]]
  n_obs  <- sum(!is.na(vals))
  n_zero <- sum(vals == 0,  na.rm = TRUE)
  n_neg  <- sum(vals < 0,   na.rm = TRUE)
  cat(sprintf("%-22s  N=%-4d  zeros=%-3d  negatives=%-3d  min=%.0f\n",
              v, n_obs, n_zero, n_neg, min(vals, na.rm = TRUE)))
  if (n_zero + n_neg > 0) {
    bad <- dt[(!is.na(get(v))) & get(v) <= 0, .(state, year, val = get(v))]
    print(bad)
  }
}
cat("\n")

# -----------------------------------------------------------------------
# 2. new_renew_mw robustness (3a)
# -----------------------------------------------------------------------
cat("---- 2. new_renew_mw robustness (3a) ----\n")

# Merge 2015 anchors (fixed per state)
anchors <- dt[year == 2015, .(state,
                               cap_total_2015 = cap_total_mw,
                               pop_2015       = population)]
dt2 <- merge(dt, anchors, by = "state", all.x = TRUE)

dt2[, new_renew_per_1000mw := new_renew_mw / cap_total_2015 * 1000]
dt2[, new_renew_per_mpop   := new_renew_mw / (pop_2015 / 1e6)]

rob_rows <- list()

# 2a: per 1,000 MW of 2015 total capacity
cc_a <- c("new_renew_per_1000mw", cc5)
d_a  <- dt2[complete.cases(dt2[, ..cc_a])]
cat(sprintf("Per 1,000 MW 2015 capacity: N = %d (expected 550)\n", nrow(d_a)))
m_a  <- feols(as.formula(paste("new_renew_per_1000mw ~ ai_dc_per1000_lag1 +",
               ctrl5, "| state + year")), data = d_a, vcov = ~state)
rob_rows[[1]] <- tidy_row(m_a,
  "h1x_rob_twfe_ai518210_lag1_ctrl5_w9901_cl-state_new_renew_per1000mw_50s2015_2025",
  "new_renew_per_1000mw", "CRV1-state", "50s2015_2025", "ctrl5")
cat(sprintf("  a1=%.2f  se=%.2f  p=%.3f  N=%d\n\n",
    rob_rows[[1]]$estimate, rob_rows[[1]]$se, rob_rows[[1]]$pval, rob_rows[[1]]$N))

# 2b: per million people (2015 population fixed)
cc_b <- c("new_renew_per_mpop", cc5)
d_b  <- dt2[complete.cases(dt2[, ..cc_b])]
cat(sprintf("Per million people (2015 pop): N = %d (expected 550)\n", nrow(d_b)))
m_b  <- feols(as.formula(paste("new_renew_per_mpop ~ ai_dc_per1000_lag1 +",
               ctrl5, "| state + year")), data = d_b, vcov = ~state)
rob_rows[[2]] <- tidy_row(m_b,
  "h1x_rob_twfe_ai518210_lag1_ctrl5_w9901_cl-state_new_renew_per_mpop_50s2015_2025",
  "new_renew_per_mpop", "CRV1-state", "50s2015_2025", "ctrl5")
cat(sprintf("  a1=%.2f  se=%.2f  p=%.3f  N=%d\n\n",
    rob_rows[[2]]$estimate, rob_rows[[2]]$se, rob_rows[[2]]$pval, rob_rows[[2]]$N))

# 2c: drop TX (TX adds the most renewable capacity; test if result survives)
cc_c <- c("new_renew_mw", cc5)
d_c  <- dt[state != "TX" & complete.cases(dt[, ..cc_c])]
cat(sprintf("Drop TX: N = %d (expected 539 = 49 x 11)\n", nrow(d_c)))
if (nrow(d_c) != 539)
  cat(sprintf("  *** N mismatch: %d rows, not 539. Investigating...\n", nrow(d_c)))
m_c  <- feols(as.formula(paste("new_renew_mw ~ ai_dc_per1000_lag1 +",
               ctrl5, "| state + year")), data = d_c, vcov = ~state)
rob_rows[[3]] <- tidy_row(m_c,
  "h1x_rob_twfe_ai518210_lag1_ctrl5_w9901_cl-state_new_renew_mw_49snoTX2015_2025",
  "new_renew_mw", "CRV1-state", "49snoTX2015_2025", "ctrl5")
cat(sprintf("  a1=%.1f  se=%.1f  p=%.3f  N=%d\n\n",
    rob_rows[[3]]$estimate, rob_rows[[3]]$se, rob_rows[[3]]$pval, rob_rows[[3]]$N))

# 2d: leave-one-state-out
cat("Leave-one-state-out:\n")
states_all  <- sort(unique(dt$state))
d_full_cc   <- dt[complete.cases(dt[, ..cc_c])]  # cc_c = new_renew_mw + ctrl5 vars
loso_coefs  <- setNames(numeric(length(states_all)), states_all)
loso_ns     <- setNames(integer(length(states_all)),  states_all)
for (s in states_all) {
  d_s       <- d_full_cc[state != s]
  loso_ns[s] <- nrow(d_s)
  if (loso_ns[s] != 539)
    cat(sprintf("  WARNING: drop %s gives N=%d not 539\n", s, loso_ns[s]))
  m_s <- feols(as.formula(paste("new_renew_mw ~ ai_dc_per1000_lag1 +",
                ctrl5, "| state + year")), data = d_s,
               vcov = ~state, warn = FALSE, notes = FALSE)
  loso_coefs[s] <- coef(m_s)["ai_dc_per1000_lag1"]
}
loso_min_s <- names(which.min(loso_coefs))
loso_max_s <- names(which.max(loso_coefs))
cat(sprintf("  LOSO min a1: %.1f (drop %s)\n", min(loso_coefs), loso_min_s))
cat(sprintf("  LOSO max a1: %.1f (drop %s)\n", max(loso_coefs), loso_max_s))
cat(sprintf("  LOSO mean:   %.1f  SD: %.1f\n\n",
            mean(loso_coefs), sd(loso_coefs)))

rob_rows[[4]] <- data.table(
  tag     = "h1x_loso_twfe_ai518210_lag1_ctrl5_w9901_cl-state_new_renew_mw_50s2015_2025",
  outcome = "new_renew_mw", coef = "ai_dc_per1000_lag1",
  estimate = mean(loso_coefs), se = sd(loso_coefs),
  tstat = NA_real_, pval = NA_real_,
  ci_lo = min(loso_coefs), ci_hi = max(loso_coefs),
  N = NA_integer_, within_r2 = NA_real_,
  vcov_type = "LOSO",
  sample   = "50s2015_2025", controls = "ctrl5",
  status   = sprintf("min=%s(%.1f),max=%s(%.1f)",
                     loso_min_s, min(loso_coefs),
                     loso_max_s, max(loso_coefs)))

rob_all <- rbindlist(rob_rows, fill = TRUE)
write_append(rob_all, "h1_extras.csv")
cat("3a rows appended to h1_extras.csv\n\n")

# -----------------------------------------------------------------------
# 3. Generation channels (3b)
# -----------------------------------------------------------------------
cat("---- 3. Generation channels (3b) ----\n")

for (v in c("gen_renew_mwh", "gen_fossil_mwh", "gen_total_mwh")) {
  n_bad <- sum(dt[[v]] <= 0, na.rm = TRUE)
  cat(sprintf("  %s: %d zero-or-negative values", v, n_bad))
  if (n_bad > 0) {
    cat(" — rows:\n")
    print(dt[!is.na(get(v)) & get(v) <= 0, .(state, year, val = get(v))])
  } else {
    cat(" — safe to log\n")
  }
}
cat("\n")

dt[gen_renew_mwh  > 0, ln_renew_mwh  := log(gen_renew_mwh)]
dt[gen_fossil_mwh > 0, ln_fossil_mwh := log(gen_fossil_mwh)]
dt[gen_total_mwh  > 0, ln_total_mwh  := log(gen_total_mwh)]

gen_specs <- list(
  list(y = "ln_renew_mwh",  suffix = "ln_renew_mwh"),
  list(y = "ln_fossil_mwh", suffix = "ln_fossil_mwh"),
  list(y = "ln_total_mwh",  suffix = "ln_total_mwh")
)
gen_rows <- list()
for (sp in gen_specs) {
  cc_g <- c(sp$y, cc5)
  d_g  <- dt[complete.cases(dt[, ..cc_g])]
  cat(sprintf("%s: N = %d\n", sp$y, nrow(d_g)))
  m_g  <- feols(as.formula(paste(sp$y, "~ ai_dc_per1000_lag1 +",
                ctrl5, "| state + year")), data = d_g, vcov = ~state)
  tag  <- sprintf("h1x_twfe_ai518210_lag1_ctrl5_w9901_cl-state_%s_50s2015_2025", sp$suffix)
  gen_rows[[sp$y]] <- tidy_row(m_g, tag, sp$y, "CRV1-state", "50s2015_2025", "ctrl5")
  cat(sprintf("  a1=%.5f  se=%.5f  p=%.3f\n",
      gen_rows[[sp$y]]$estimate, gen_rows[[sp$y]]$se, gen_rows[[sp$y]]$pval))
}
gen_all <- rbindlist(gen_rows)
write_append(gen_all, "h1_extras.csv")
cat("3b rows appended to h1_extras.csv\n\n")

# -----------------------------------------------------------------------
# 4. Proper Lind-Mehlum test (3c)
# -----------------------------------------------------------------------
cat("---- 4. Proper Lind-Mehlum test (delta-method, cov(b1,b2)) ----\n")

outcomes_nl <- c("ln_ec", "ln_ee", "renew_share", "solar_share", "wind_share",
                 "new_renew_mw", "fossil_to_renew", "coal_share")

lm_rows <- list()
for (y in outcomes_nl) {
  cc_nl <- c(y, "ai_dc_per1000_lag1", "ai_sq_lag1", strsplit(ctrl5, " \\+ ")[[1]])
  d_nl  <- dt[complete.cases(dt[, ..cc_nl])]
  m_nl  <- feols(as.formula(paste(y, "~ ai_dc_per1000_lag1 + ai_sq_lag1 +",
                 ctrl5, "| state + year")), data = d_nl, vcov = ~state)

  ct     <- coeftable(m_nl)
  b1     <- as.numeric(ct["ai_dc_per1000_lag1", "Estimate"])
  b2     <- as.numeric(ct["ai_sq_lag1",         "Estimate"])
  b2_se  <- as.numeric(ct["ai_sq_lag1",         "Std. Error"])
  b2_p   <- as.numeric(ct["ai_sq_lag1",         "Pr(>|t|)"])

  # Full vcov for the two nonlinear terms
  V12 <- vcov(m_nl)[c("ai_dc_per1000_lag1", "ai_sq_lag1"),
                    c("ai_dc_per1000_lag1", "ai_sq_lag1")]

  ai_min <- min(d_nl$ai_dc_per1000_lag1, na.rm = TRUE)
  ai_max <- max(d_nl$ai_dc_per1000_lag1, na.rm = TRUE)

  slope_min <- b1 + 2 * b2 * ai_min
  slope_max <- b1 + 2 * b2 * ai_max

  # Delta-method SE: Var(b1 + 2*b2*x) = Var(b1) + 4x²Var(b2) + 4x·Cov(b1,b2)
  grad <- function(x) c(1, 2 * x)
  se_min <- sqrt(as.numeric(t(grad(ai_min)) %*% V12 %*% grad(ai_min)))
  se_max <- sqrt(as.numeric(t(grad(ai_max)) %*% V12 %*% grad(ai_max)))

  t_min <- slope_min / se_min
  t_max <- slope_max / se_max

  # Inverted-U: t_min > 1.645 (positive slope at min) AND t_max < -1.645 (negative at max)
  # U-shape:    t_min < -1.645 AND t_max > 1.645
  lm_inverted_u <- (t_min > 1.645 && t_max < -1.645)
  lm_u_shape    <- (t_min < -1.645 && t_max > 1.645)
  lm_pass       <- lm_inverted_u || lm_u_shape
  shape_label   <- ifelse(lm_inverted_u, "inverted-U",
                   ifelse(lm_u_shape, "U-shape", "no curve"))
  t_weaker      <- ifelse(abs(t_min) <= abs(t_max), t_min, t_max)

  cat(sprintf("%-16s b2=%.5f p=%.3f | slope_min=%.4f(t=%.2f) slope_max=%.4f(t=%.2f) | LM=%s\n",
              y, b2, b2_p, slope_min, t_min, slope_max, t_max,
              ifelse(lm_pass, paste("PASS", shape_label), "FAIL")))

  lm_rows[[y]] <- data.table(
    outcome      = y,
    b2           = b2,
    b2_se        = b2_se,
    b2_pval      = b2_p,
    ai_min       = ai_min,
    ai_max       = ai_max,
    slope_at_min = slope_min,
    se_slope_min = se_min,
    t_slope_min  = t_min,
    slope_at_max = slope_max,
    se_slope_max = se_max,
    t_slope_max  = t_max,
    lm_pass      = lm_pass,
    shape        = shape_label,
    t_weaker     = t_weaker,
    N            = m_nl$nobs
  )
}

lm_results <- rbindlist(lm_rows)
cat("\nSummary:\n")
print(lm_results[, .(outcome, b2, b2_pval, lm_pass, shape, t_weaker)])
fwrite(lm_results, file.path(OUT, "lm_proper.csv"))
cat("Saved to lm_proper.csv\n\n")

cat("=== Checks complete ===\n")

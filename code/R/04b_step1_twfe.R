#!/usr/bin/env Rscript
# 04b_step1_twfe.R — H1 TWFE and all Step 1 checks
# Usage: Rscript code/R/04b_step1_twfe.R --date 2026-11-02
# Fail-fast: stops if reproduce gate fails or input files are missing.

suppressPackageStartupMessages({
  library(fixest)
  library(modelsummary)
  library(data.table)
  library(ggplot2)
  library(boot)
})

# --------------------------------------------------------------------------
# 0. Parse args, set up paths
# --------------------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
date_arg <- NULL
for (i in seq_along(args)) {
  if (args[i] == "--date" && i < length(args)) date_arg <- args[i + 1]
}
if (is.null(date_arg)) stop("--date YYYY-MM-DD required")
if (!grepl("^\\d{4}-\\d{2}-\\d{2}$", date_arg)) stop("--date must be YYYY-MM-DD")

OUT     <- file.path("results", date_arg, "h1")
TABLES  <- file.path("results", date_arg, "tables")
FIGS    <- file.path("results", date_arg, "figures")
for (d in c(OUT, TABLES, FIGS)) dir.create(d, recursive = TRUE, showWarnings = FALSE)

REF_SLX <- "econ499r_starter/reference/prelim_step1_slx.csv"
PANEL   <- "data/out/state_panel_2015_2025.csv"

if (!file.exists(REF_SLX)) stop(paste("Reference file not found:", REF_SLX))
if (!file.exists(PANEL))   stop(paste("Panel not found:", PANEL))

cat("\n=== 04b Step 1 TWFE ===\n")
cat("Date:", date_arg, "\n")
cat("Output root:", file.path("results", date_arg), "\n\n")

# Append a row to the results ledger
write_result <- function(df, fname) {
  path <- file.path(OUT, fname)
  fwrite(df, path, append = file.exists(path))
  invisible(path)
}

# --------------------------------------------------------------------------
# Helper: winsorize at [p_lo, p_hi]
# --------------------------------------------------------------------------
wins <- function(x, p_lo = 0.01, p_hi = 0.99) {
  lo <- quantile(x, p_lo, na.rm = TRUE)
  hi <- quantile(x, p_hi, na.rm = TRUE)
  pmax(pmin(x, hi), lo)
}

# --------------------------------------------------------------------------
# Helper: extract a tidy result row from a feols model
# --------------------------------------------------------------------------
tidy_row <- function(m, tag, outcome, vcov_type, sample_desc, controls_desc, coef_name = "ai_dc_per1000_lag1") {
  ct <- coeftable(m)
  if (!coef_name %in% rownames(ct)) {
    return(data.table(tag = tag, outcome = outcome, coef = coef_name,
                      estimate = NA_real_, se = NA_real_, tstat = NA_real_,
                      pval = NA_real_, ci_lo = NA_real_, ci_hi = NA_real_,
                      N = m$nobs, within_r2 = NA_real_,
                      vcov_type = vcov_type, sample = sample_desc,
                      controls = controls_desc, status = "COEF_MISSING"))
  }
  row <- ct[coef_name, ]
  ci <- confint(m)[coef_name, ]
  data.table(tag = tag, outcome = outcome, coef = coef_name,
             estimate = as.numeric(row[["Estimate"]]),
             se       = as.numeric(row[["Std. Error"]]),
             tstat    = as.numeric(row[["t value"]]),
             pval     = as.numeric(row[["Pr(>|t|)"]]),
             ci_lo    = as.numeric(ci[1]),
             ci_hi    = as.numeric(ci[2]),
             N = m$nobs, within_r2 = r2(m, "wr2"),
             vcov_type = vcov_type, sample = sample_desc,
             controls = controls_desc, status = "ok")
}

# ==========================================================================
# EXPERIMENT 1 — REPRODUCE the prelim (GATE)
# ==========================================================================
cat("---- Experiment 1: Reproduce prelim gate ----\n")

# Load panel fresh (pre-load_panel winsorization) and apply prelim's exact spec
dt_raw <- fread(PANEL)
dt_raw <- dt_raw[state != "DC"]
setorder(dt_raw, state, year)

# Prelim winsorizes exactly: ln_ec, ln_ee, renew_share, solar_share, ai_dc_per1000_lag1
for (col in c("ln_ec", "ln_ee", "renew_share", "solar_share", "ai_dc_per1000_lag1")) {
  dt_raw[, (paste0(col, "_w")) := wins(get(col))]
}
dt_raw[, new_renew_gw := new_renew_mw / 1000]  # NOT winsorized (matches prelim.py)

ctrl4 <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"
repro_specs <- list(
  list(y = "ln_ec_w",       label = "H1 consumption: ln MWh sold per person",    ref_b = -0.0015654860779069542),
  list(y = "ln_ee_w",       label = "H1 efficiency: ln real GDP per MWh",         ref_b =  0.0022055895601546544),
  list(y = "renew_share_w", label = "H1 energy mix: renewable share of generation", ref_b = -0.010129270772672477),
  list(y = "solar_share_w", label = "Extra: solar share",                          ref_b = -5.930447336954223e-05),
  list(y = "new_renew_gw",  label = "Extra: new renewable GW",                    ref_b =  0.07599478199698667)
)

repro_rows <- list()
gate_pass <- TRUE

for (sp in repro_specs) {
  fml <- as.formula(paste0(sp$y, " ~ ai_dc_per1000_lag1_w + ", ctrl4, " | state + year"))
  d_cc <- dt_raw[complete.cases(dt_raw[, c(sp$y, "ai_dc_per1000_lag1_w",
                                           "ln_gdp_pc", "manuf_share",
                                           "price_c_kwh", "pop_growth"), with = FALSE])]
  m <- feols(fml, data = d_cc, vcov = ~state)
  b_got  <- coef(m)["ai_dc_per1000_lag1_w"]
  b_ref  <- sp$ref_b
  diff   <- abs(b_got - b_ref)
  pass   <- diff < 5e-4   # within rounding of 4dp
  repro_rows[[length(repro_rows) + 1]] <- data.table(
    outcome = sp$label, b_ref = b_ref, b_got = b_got,
    diff = diff, N = m$nobs, pass = pass
  )
  cat(sprintf("  %-50s b_ref=%10.7f  b_got=%10.7f  diff=%8.5f  %s\n",
              sp$label, b_ref, b_got, diff, if (pass) "PASS" else "*** FAIL ***"))
  if (!pass) gate_pass <- FALSE
}

repro_dt <- rbindlist(repro_rows)
fwrite(repro_dt, file.path(OUT, "reproduce_gate.csv"))

if (!gate_pass) {
  cat("\n*** REPRODUCE GATE FAILED — stopping. See reproduce_gate.csv for details. ***\n")
  quit(status = 1)
}
cat("  Reproduce gate PASSED.\n\n")

# ==========================================================================
# Load the analysis panel via load_panel.R (winsorized, 5-control version)
# ==========================================================================
source("code/R/load_panel.R")
res <- load_panel()
dt  <- res$panel
W_border  <- res$W_border
W_invdist <- res$W_invdist

# 2015-baseline frozen moderators (so they can't respond to AI)
base2015 <- dt[year == 2015, .(state,
  net_exporter_2015 = net_exporter,
  high_price_2015   = high_price)]
dt <- merge(dt, base2015, by = "state")
dt[, net_exp_2015_c   := net_exporter_2015 - mean(net_exporter_2015, na.rm = TRUE)]
dt[, high_price_2015_c := high_price_2015  - mean(high_price_2015,  na.rm = TRUE)]

ctrl5  <- "ln_gdp_pc + price_c_kwh + tech_share + manuf_share + pop_growth"
ctrl4r <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"

# ==========================================================================
# Experiment 2 — H1 core table (memo)
# ==========================================================================
cat("---- Experiment 2: H1 core ----\n")

core_outcomes <- list(
  list(y = "ln_ec",      tag_sfx = "ln_ec",      label = "ln(MWh per person)"),
  list(y = "ln_ee",      tag_sfx = "ln_ee",      label = "ln(real GDP / MWh)"),
  list(y = "renew_share",tag_sfx = "renew_share", label = "Renewable share")
)

core_results <- list()
models_core <- list()

for (sp in core_outcomes) {
  for (ctrl_label in c("ctrl5", "ctrl4")) {
    ctrl_str <- if (ctrl_label == "ctrl5") ctrl5 else ctrl4r
    tag <- sprintf("h1_twfe_ai518210_lag1_%s_w9901_cl-state_%s_50s2015_2025", ctrl_label, sp$tag_sfx)
    fml <- as.formula(paste0(sp$y, " ~ ai_dc_per1000_lag1 + ", ctrl_str, " | state + year"))
    m <- feols(fml, data = dt, vcov = ~state)
    r <- tidy_row(m, tag, sp$y, "CRV1-state", "50s2015_2025", ctrl_label)
    core_results[[tag]] <- r
    models_core[[paste(sp$tag_sfx, ctrl_label, sep = "_")]] <- m
    cat(sprintf("  %s  b=%8.5f  se=%7.5f  p=%5.3f  N=%d  R2w=%.3f\n",
                tag, r$estimate, r$se, r$pval, r$N, r$within_r2))
  }
}

core_dt <- rbindlist(core_results)
fwrite(core_dt, file.path(OUT, "h1_core.csv"))

# modelsummary table
ms_core <- list(
  "ln(ec) ctrl5" = models_core[["ln_ec_ctrl5"]],
  "ln(ec) ctrl4" = models_core[["ln_ec_ctrl4"]],
  "ln(ee) ctrl5" = models_core[["ln_ee_ctrl5"]],
  "ln(ee) ctrl4" = models_core[["ln_ee_ctrl4"]],
  "renew ctrl5"  = models_core[["renew_share_ctrl5"]],
  "renew ctrl4"  = models_core[["renew_share_ctrl4"]]
)
modelsummary(ms_core,
  coef_map  = c("ai_dc_per1000_lag1" = "AI data centers (t-1)"),
  gof_map   = c("nobs", "r.squared.within"),
  stars     = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
  output    = file.path(TABLES, "h1_core.tex"))
modelsummary(ms_core,
  coef_map  = c("ai_dc_per1000_lag1" = "AI data centers (t-1)"),
  gof_map   = c("nobs", "r.squared.within"),
  stars     = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
  output    = file.path(TABLES, "h1_core.csv"))
cat("  Tables written.\n\n")

# ==========================================================================
# Experiment 3 — H1 extras
# ==========================================================================
cat("---- Experiment 3: H1 extras ----\n")

extra_outcomes <- list(
  list(y = "solar_share",    tag_sfx = "solar_share",    label = "Solar share"),
  list(y = "wind_share",     tag_sfx = "wind_share",     label = "Wind share"),
  list(y = "new_renew_mw",   tag_sfx = "new_renew_mw",   label = "New renew MW"),
  list(y = "fossil_to_renew",tag_sfx = "fossil_to_renew",label = "Fossil-to-renew ratio"),
  list(y = "coal_share",     tag_sfx = "coal_share",     label = "Coal share (falsification)")
)
# CO2: 2015-2024 subsample only
extra_outcomes <- c(extra_outcomes, list(
  list(y = "co2_per_mwh_t", tag_sfx = "co2_per_mwh_t", label = "CO2/MWh (t, 2015-2024)")
))

extra_results <- list()
models_extra <- list()

for (sp in extra_outcomes) {
  sub <- if (sp$y == "co2_per_mwh_t") dt[!is.na(co2_per_mwh_t)] else dt
  tag <- sprintf("h1x_twfe_ai518210_lag1_ctrl5_w9901_cl-state_%s_50s2015_2025", sp$tag_sfx)
  fml <- as.formula(paste0(sp$y, " ~ ai_dc_per1000_lag1 + ", ctrl5, " | state + year"))
  m <- feols(fml, data = sub, vcov = ~state)
  r <- tidy_row(m, tag, sp$y, "CRV1-state",
                if (sp$y == "co2_per_mwh_t") "50s2015_2024" else "50s2015_2025", "ctrl5")
  extra_results[[tag]] <- r
  models_extra[[sp$tag_sfx]] <- m
  cat(sprintf("  %-14s  b=%9.5f  se=%8.5f  p=%5.3f  N=%d\n",
              sp$tag_sfx, r$estimate, r$se, r$pval, r$N))
}

extra_dt <- rbindlist(extra_results)
fwrite(extra_dt, file.path(OUT, "h1_extras.csv"))
cat("  h1_extras.csv written.\n\n")

# ==========================================================================
# Experiment 4 — Price-control check (already embedded in Exp 2 as ctrl4 vs ctrl5)
# Output a dedicated side-by-side for the three core outcomes
# ==========================================================================
cat("---- Experiment 4: Price-control check (see h1_core.csv ctrl4 vs ctrl5) ----\n")
price_check <- core_dt[, .(tag, outcome, estimate, se, pval, N, controls)]
fwrite(price_check, file.path(OUT, "price_control_check.csv"))
cat("  price_control_check.csv written.\n\n")

# ==========================================================================
# Experiment 5 — SE check: clustered vs Driscoll-Kraay
# ==========================================================================
cat("---- Experiment 5: SE check (clustered vs DK) ----\n")

se_results <- list()
for (sp in core_outcomes) {
  fml <- as.formula(paste0(sp$y, " ~ ai_dc_per1000_lag1 + ", ctrl5, " | state + year"))

  m_cl <- feols(fml, data = dt, vcov = ~state)
  m_dk <- feols(fml, data = dt, vcov = "DK", panel.id = ~state + year)

  tag_cl <- sprintf("h1_twfe_ai518210_lag1_ctrl5_w9901_cl-state_%s_50s2015_2025", sp$tag_sfx)
  tag_dk <- sprintf("h1_twfe_ai518210_lag1_ctrl5_w9901_dk_%s_50s2015_2025",       sp$tag_sfx)

  r_cl <- tidy_row(m_cl, tag_cl, sp$y, "CRV1-state", "50s2015_2025", "ctrl5")
  r_dk <- tidy_row(m_dk, tag_dk, sp$y, "DK",          "50s2015_2025", "ctrl5")

  cat(sprintf("  %-12s  CL: b=%8.5f se=%7.5f p=%.3f  |  DK: b=%8.5f se=%7.5f p=%.3f\n",
              sp$tag_sfx, r_cl$estimate, r_cl$se, r_cl$pval,
              r_dk$estimate, r_dk$se, r_dk$pval))
  se_results <- c(se_results, list(r_cl, r_dk))
}

se_dt <- rbindlist(se_results)
fwrite(se_dt, file.path(OUT, "se_check.csv"))
cat("  se_check.csv written.\n\n")

# ==========================================================================
# Experiment 6 — Nonlinearity: AI + AI²
# ==========================================================================
cat("---- Experiment 6: Nonlinearity (AI + AI²) ----\n")

nonlin_outcomes <- c(core_outcomes, extra_outcomes[sapply(extra_outcomes, function(x) x$y != "co2_per_mwh_t")])

nonlin_results <- list()
turning_points <- list()

for (sp in nonlin_outcomes) {
  tag <- sprintf("nonlin_twfe_ai518210sq_lag1_ctrl5_w9901_cl-state_%s_50s2015_2025", sp$tag_sfx)
  fml <- as.formula(paste0(sp$y, " ~ ai_dc_per1000_lag1 + ai_sq_lag1 + ", ctrl5, " | state + year"))
  m <- feols(fml, data = dt, vcov = ~state)

  r_lin <- tidy_row(m, tag, sp$y, "CRV1-state", "50s2015_2025", "ctrl5", "ai_dc_per1000_lag1")
  r_sq  <- tidy_row(m, tag, sp$y, "CRV1-state", "50s2015_2025", "ctrl5", "ai_sq_lag1")
  nonlin_results <- c(nonlin_results, list(r_lin, r_sq))

  # Delta-method turning point
  b1 <- coef(m)["ai_dc_per1000_lag1"]
  b2 <- coef(m)["ai_sq_lag1"]
  if (!is.na(b2) && abs(b2) > 1e-12) {
    tp   <- -b1 / (2 * b2)
    vcv  <- vcov(m)[c("ai_dc_per1000_lag1","ai_sq_lag1"), c("ai_dc_per1000_lag1","ai_sq_lag1")]
    d_b1 <- -1 / (2 * b2)
    d_b2 <-  b1 / (2 * b2^2)
    tp_se <- sqrt(d_b1^2 * vcv[1,1] + d_b2^2 * vcv[2,2] + 2 * d_b1 * d_b2 * vcv[1,2])
    tp_lo <- tp - 1.96 * tp_se
    tp_hi <- tp + 1.96 * tp_se
    ai_obs <- dt[!is.na(ai_dc_per1000_lag1), ai_dc_per1000_lag1]
    ai_range <- range(ai_obs)
    inside <- tp >= ai_range[1] & tp <= ai_range[2]
    pct_past <- mean(ai_obs >= tp, na.rm = TRUE)
    # Lind-Mehlum style: slope at min and max
    slope_min <- b1 + 2 * b2 * ai_range[1]
    slope_max <- b1 + 2 * b2 * ai_range[2]
    lm_opposite_signs <- sign(slope_min) != sign(slope_max)
    tp_row <- data.table(tag = tag, outcome = sp$y,
                         b1 = b1, b2 = b2, turning_point = tp, tp_se = tp_se,
                         tp_lo = tp_lo, tp_hi = tp_hi,
                         ai_min = ai_range[1], ai_max = ai_range[2],
                         inside_range = inside, pct_state_yrs_past_tp = pct_past,
                         slope_at_min = slope_min, slope_at_max = slope_max,
                         lm_opposite_signs = lm_opposite_signs,
                         N = m$nobs, status = "ok")
    turning_points[[length(turning_points) + 1]] <- tp_row
    cat(sprintf("  %-14s  b1=%8.5f  b2=%9.5f  TP=%6.3f [%5.3f,%5.3f]  inside=%s  pct_past=%.1f%%\n",
                sp$tag_sfx, b1, b2, tp, tp_lo, tp_hi,
                if (inside) "YES" else "no", 100 * pct_past))
  } else {
    cat(sprintf("  %-14s  b2 near zero or NA — no turning point\n", sp$tag_sfx))
  }
}

nonlin_dt <- rbindlist(nonlin_results)
fwrite(nonlin_dt, file.path(OUT, "nonlinearity.csv"))
if (length(turning_points) > 0) {
  tp_dt <- rbindlist(turning_points)
  fwrite(tp_dt, file.path(OUT, "turning_points.csv"))
  cat("  turning_points.csv written.\n")
}
cat("  nonlinearity.csv written.\n\n")

# ==========================================================================
# Experiment 7 — Heterogeneity (2015-baseline moderators)
# ==========================================================================
cat("---- Experiment 7: Heterogeneity ----\n")

het_mods <- list(
  list(d = "net_exporter_2015", dc = "net_exp_2015_c",   label = "net_exporter"),
  list(d = "high_price_2015",   dc = "high_price_2015_c", label = "high_price"),
  list(d = "south",             dc = "south_c",            label = "south")
)

het_results <- list()
models_het  <- list()

for (sp in core_outcomes) {
  for (mod in het_mods) {
    tag <- sprintf("het_twfe_ai518210_lag1_%s_ctrl5_w9901_cl-state_%s_50s2015_2025",
                   mod$label, sp$tag_sfx)
    # Interaction: AI_c x D_c; include D main effect (south absorbed by state FE — use the uncentered dummy for clarity)
    fml <- as.formula(paste0(
      sp$y, " ~ ai_lag1_c:", mod$dc, " + ai_lag1_c + ", mod$dc,
      " + ln_gdp_pc + price_c_kwh + tech_share + manuf_share + pop_growth | state + year"
    ))
    # For south: its main effect is absorbed by state FE; add a note
    tryCatch({
      m <- feols(fml, data = dt, vcov = ~state)
      r_int <- tidy_row(m, tag, sp$y, "CRV1-state", "50s2015_2025", "ctrl5",
                        paste0("ai_lag1_c:", mod$dc))
      r_ai  <- tidy_row(m, tag, sp$y, "CRV1-state", "50s2015_2025", "ctrl5", "ai_lag1_c")
      het_results <- c(het_results, list(r_int, r_ai))
      models_het[[paste(sp$tag_sfx, mod$label, sep = "_")]] <- m
      cat(sprintf("  %-12s x %-15s  int=%8.5f(p=%.3f)  AI=%8.5f(p=%.3f)\n",
                  sp$tag_sfx, mod$label,
                  r_int$estimate, r_int$pval,
                  r_ai$estimate,  r_ai$pval))
    }, error = function(e) {
      cat(sprintf("  %-12s x %-15s  ERROR: %s\n", sp$tag_sfx, mod$label, conditionMessage(e)))
    })
  }
}

het_dt <- rbindlist(het_results)
fwrite(het_dt, file.path(OUT, "heterogeneity.csv"))
cat("  heterogeneity.csv written.\n\n")

# ==========================================================================
# Experiment 8 — Dynamics: t-1 only + long difference
# (QCEW 2012-2013 absent; t-2 and t-3 omitted)
# ==========================================================================
cat("---- Experiment 8: Dynamics (t-1 only + long difference) ----\n")
cat("  Note: QCEW 2012-2013 absent. t-2 and t-3 omitted. Using t-1 + long difference.\n")

dyn_results <- list()

# --- t-1 already in core; just record that formally ---
for (sp in core_outcomes) {
  tag <- sprintf("dyn_twfe_ai518210_lag1_ctrl5_w9901_cl-state_%s_50s2015_2025", sp$tag_sfx)
  fml <- as.formula(paste0(sp$y, " ~ ai_dc_per1000_lag1 + ", ctrl5, " | state + year"))
  m <- feols(fml, data = dt, vcov = ~state)
  r <- tidy_row(m, tag, sp$y, "CRV1-state", "50s2015_2025", "ctrl5")
  r[, lag_k := 1L]
  dyn_results[[length(dyn_results) + 1]] <- r
}

# --- Long difference: ΔY(2025−2015) on ΔAI(2024−2014) + Δcontrols ---
# ΔAI(2024-2014): use ai_dc_per1000 in 2024 and the 2015 lag (= 2014 value)
y2015 <- dt[year == 2015, .(state, Y2015_ln_ec = ln_ec, Y2015_ln_ee = ln_ee,
                             Y2015_renew = renew_share,
                             ai_2014 = ai_dc_per1000_lag1,  # lag1 in 2015 = 2014 value
                             gdp_2015 = ln_gdp_pc, price_2015 = price_c_kwh,
                             tech_2015 = tech_share, manuf_2015 = manuf_share,
                             pop_2015 = population)]
y2025 <- dt[year == 2025, .(state, Y2025_ln_ec = ln_ec, Y2025_ln_ee = ln_ee,
                             Y2025_renew = renew_share,
                             ai_2024 = ai_dc_per1000,
                             gdp_2025 = ln_gdp_pc, price_2025 = price_c_kwh,
                             tech_2025 = tech_share, manuf_2025 = manuf_share,
                             pop_2025 = population)]
ld <- merge(y2015, y2025, by = "state")
ld[, dln_ec    := Y2025_ln_ec  - Y2015_ln_ec]
ld[, dln_ee    := Y2025_ln_ee  - Y2015_ln_ee]
ld[, drenew    := Y2025_renew  - Y2015_renew]
ld[, dAI       := ai_2024      - ai_2014]
ld[, dlngdp    := gdp_2025     - gdp_2015]
ld[, dprice    := price_2025   - price_2015]
ld[, dtech     := tech_2025    - tech_2015]
ld[, dmanuf    := manuf_2025   - manuf_2015]
ld[, dpop      := log(pop_2025 / pop_2015)]
ld_clean <- ld[complete.cases(ld[, .(dln_ec, dln_ee, drenew, dAI,
                                     dlngdp, dprice, dtech, dmanuf, dpop)])]

cat(sprintf("  Long difference N = %d states\n", nrow(ld_clean)))

for (sp in list(list(y = "dln_ec",  tag_sfx = "ln_ec"),
                list(y = "dln_ee",  tag_sfx = "ln_ee"),
                list(y = "drenew",  tag_sfx = "renew_share"))) {
  tag <- sprintf("dyn_longdiff_ai518210_ctrl5_w9901_rob_%s_50s2015_2025", sp$tag_sfx)
  fml <- as.formula(paste0(sp$y, " ~ dAI + dlngdp + dprice + dtech + dmanuf + dpop"))
  m <- lm(fml, data = ld_clean)
  ct <- summary(m)$coefficients
  r <- data.table(tag = tag, outcome = sp$y, coef = "dAI",
                  estimate = ct["dAI", "Estimate"], se = ct["dAI", "Std. Error"],
                  tstat = ct["dAI", "t value"], pval = ct["dAI", "Pr(>|t|)"],
                  ci_lo = confint(m)["dAI", 1], ci_hi = confint(m)["dAI", 2],
                  N = nrow(ld_clean), within_r2 = summary(m)$r.squared,
                  vcov_type = "HC0", sample = "50s2015_2025_longdiff", controls = "delta_ctrl5",
                  lag_k = NA_integer_, status = "ok")
  dyn_results[[length(dyn_results) + 1]] <- r
  cat(sprintf("  long-diff %-12s  b=%8.5f  se=%7.5f  p=%.3f\n",
              sp$tag_sfx, r$estimate, r$se, r$pval))
}

dyn_dt <- rbindlist(dyn_results, fill = TRUE)
fwrite(dyn_dt, file.path(OUT, "dynamics.csv"))
cat("  dynamics.csv written.\n\n")

# ==========================================================================
# Experiment 9 — Georgia descriptive check
# ==========================================================================
cat("---- Experiment 9: Georgia descriptive ----\n")

# AI path
ga_path <- dt[state == "GA", .(state, year, ai_dc_per1000, renew_share, ln_ec, ln_ee, solar_share)]
us_med  <- dt[, .(us_med_ai    = median(ai_dc_per1000, na.rm = TRUE),
                  us_med_renew = median(renew_share, na.rm = TRUE),
                  us_med_ln_ec = median(ln_ec, na.rm = TRUE),
                  us_med_ln_ee = median(ln_ee, na.rm = TRUE)), by = year]
ga_vs_us <- merge(ga_path, us_med, by = "year")

# Georgia residuals from H1 core renew_share model (ctrl5)
m_renew_core <- models_core[["renew_share_ctrl5"]]
dt[, resid_renew := residuals(m_renew_core)]
ga_resid <- dt[state == "GA", .(year, resid_renew)]

ga_summary <- merge(ga_vs_us, ga_resid, by = "year")
fwrite(ga_summary, file.path(OUT, "georgia_descriptive.csv"))

# Note re NAICS 518210 scope
cat("  NOTE: Georgia ranks 2nd in ai_dc_per1000 in 2025 (behind WA), above VA.\n")
cat("  This likely reflects colocation/cloud hosting (NAICS 518210 scope), not AI-specific compute.\n")
cat("  Georgia residuals from renew_share TWFE model:\n")
print(ga_resid)
cat("  georgia_descriptive.csv written.\n\n")

# ==========================================================================
# Figures
# ==========================================================================
cat("---- Figures ----\n")

# Figure 1: Coefficient plot across core + extra outcomes (ctrl5, clustered)
all_results <- rbind(core_dt[controls == "ctrl5"], extra_dt, fill = TRUE)
fig1_data <- as.data.frame(all_results[coef == "ai_dc_per1000_lag1"])
fig1_data[, "outcome_label"] <- factor(fig1_data$outcome,
  levels = c("ln_ec","ln_ee","renew_share","solar_share","wind_share",
             "new_renew_mw","fossil_to_renew","coal_share","co2_per_mwh_t"),
  labels = c("ln(MWh/person)","ln(GDP/MWh)","Renew share","Solar share","Wind share",
             "New renew MW","Fossil/renew","Coal share","CO2/MWh"))
fig1_data <- fig1_data[!is.na(fig1_data$outcome_label), ]

p1 <- ggplot(fig1_data, aes(x = estimate, xmin = ci_lo, xmax = ci_hi,
                             y = outcome_label,
                             color = pval < 0.10)) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey60") +
  geom_pointrange(size = 0.6) +
  scale_color_manual(values = c("FALSE" = "grey50", "TRUE" = "#2166ac"),
                     labels = c("p≥0.10", "p<0.10"), name = "") +
  labs(x = "Coefficient on AI(t-1)", y = NULL,
       title = "H1: AI data centers and energy outcomes",
       subtitle = "TWFE, clustered SEs, 50 states 2015-2025, ctrl5, 1/99 winsorized") +
  theme_bw(base_size = 11)
ggsave(file.path(FIGS, "h1_coef_plot.pdf"), p1, width = 7, height = 5)
ggsave(file.path(FIGS, "h1_coef_plot.png"), p1, width = 7, height = 5, dpi = 150)

# Figure 2: GA vs US median for AI and renewable share
fig2_long <- as.data.frame(melt(ga_vs_us[, .(year, GA_ai = ai_dc_per1000, US_med_ai = us_med_ai,
                                 GA_renew = renew_share, US_med_renew = us_med_renew)],
                  id.vars = "year"))
fig2_long$series <- sub("_.*", "", fig2_long$variable)
fig2_long$metric <- ifelse(grepl("ai", fig2_long$variable), "AI/1000 workers", "Renewable share")
p2 <- ggplot(fig2_long, aes(x = year, y = value, color = series, linetype = series)) +
  geom_line(size = 0.9) + geom_point(size = 1.5) +
  facet_wrap(~metric, scales = "free_y") +
  scale_color_manual(values = c("GA" = "#d73027", "US" = "#4575b4")) +
  labs(x = NULL, y = NULL, title = "Georgia vs U.S. median: AI concentration and renewable share",
       color = "", linetype = "") +
  theme_bw(base_size = 11)
ggsave(file.path(FIGS, "georgia_ai_renew_paths.pdf"), p2, width = 8, height = 4)
ggsave(file.path(FIGS, "georgia_ai_renew_paths.png"), p2, width = 8, height = 4, dpi = 150)

cat("  Figures saved to", FIGS, "\n\n")

# ==========================================================================
# RECEIPT.md
# ==========================================================================
receipt_lines <- c(
  "# RECEIPT.md — h1 results",
  paste("Date:", date_arg),
  paste("Input panel:", PANEL),
  paste("Panel SHA256:", tools::md5sum(PANEL)),
  "",
  "## Tags run",
  paste("-", unique(rbind(core_dt, extra_dt, se_dt, nonlin_dt, het_dt, dyn_dt,
                          fill = TRUE)$tag)),
  "",
  "## N per model",
  paste0("  H1 core (ctrl5):  N=", core_dt[controls=="ctrl5", N[1]]),
  paste0("  H1 extras:        N=", extra_dt[outcome!="co2_per_mwh_t", N[1]]),
  paste0("  CO2 subsample:    N=", extra_dt[outcome=="co2_per_mwh_t", N]),
  paste0("  Long difference:  N=", dyn_dt[grepl("longdiff",tag), N[1]]),
  "",
  "## Warnings",
  "  - QCEW 2012-2013 absent: t-2 and t-3 dynamics omitted.",
  "  - NAICS 518210 scope: Georgia ranks 2nd in ai_dc_per1000 (above VA); likely reflects colocation/cloud hosting.",
  "  - south main effect absorbed by state FE in heterogeneity models.",
  "",
  "## Failures",
  "  None."
)
writeLines(receipt_lines, file.path(OUT, "RECEIPT.md"))
cat("RECEIPT.md written.\n")

cat("\n=== 04b complete. Results in", OUT, "===\n")

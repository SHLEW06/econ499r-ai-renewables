# load_panel.R — single panel loader for all Phase 4 experiments
# Every experiment sources this file and calls load_panel().
# Guarantees identical sample, variables, winsorization, and W-matrix
# order across experiments.

library(data.table)

# --------------------------------------------------------------------------
# Helper: winsorize a numeric vector at [p_lo, p_hi] quantiles
# --------------------------------------------------------------------------
winsorize <- function(x, p_lo = 0.01, p_hi = 0.99) {
  lo <- quantile(x, p_lo, na.rm = TRUE)
  hi <- quantile(x, p_hi, na.rm = TRUE)
  pmax(pmin(x, hi), lo)
}

# --------------------------------------------------------------------------
# load_panel()
#
# Returns a list:
#   $panel  — analysis-ready data.table (50 states, 2015-2025, DC dropped)
#   $W_border — row-standardised border contiguity matrix (48 states)
#   $W_invdist — row-standardised inverse-distance matrix (48 states; NULL if file missing)
#   $log   — character vector of actions taken
# --------------------------------------------------------------------------
load_panel <- function(
    panel_path  = "data/out/state_panel_2015_2025.csv",
    W_border_path = "data/out/W_border_binary.csv",
    W_invdist_path = "data/out/W_inverse_distance_rowstd.csv",
    centroids_path = "data/out/state_centroids_land.csv",
    winsor_outcomes = c("ln_ec", "ln_ee", "renew_share",
                        "solar_share", "wind_share", "new_renew_mw",
                        "co2_per_mwh_t", "fossil_to_renew", "seds_mmbtu_pc"),
    winsor_ai = TRUE,
    p_lo = 0.01,
    p_hi = 0.99
) {

  log <- character(0)

  # ---- 1. Read panel -------------------------------------------------------
  dt <- fread(panel_path)
  log <- c(log, sprintf("Read panel: %d rows x %d cols from %s",
                        nrow(dt), ncol(dt), panel_path))

  # ---- 2. Drop DC ----------------------------------------------------------
  n_before <- nrow(dt)
  dt <- dt[is_dc == 0]
  log <- c(log, sprintf("Dropped DC: %d rows removed, %d remain",
                        n_before - nrow(dt), nrow(dt)))

  # ---- 3. Sort -------------------------------------------------------------
  setorder(dt, state, year)

  # ---- 4. Build coal_share (falsification outcome) -------------------------
  dt[, coal_share := gen_coal_mwh / gen_total_mwh]
  log <- c(log, "Built coal_share = gen_coal_mwh / gen_total_mwh")

  # ---- 5. Build net_exporter flag ------------------------------------------
  dt[, net_exporter := as.integer(gen_total_mwh > sales_mwh)]
  log <- c(log, "Built net_exporter = (gen_total_mwh > sales_mwh)")

  # ---- 6. Build high_price flag (above national median by year) -----------
  dt[, price_med_yr := median(price_c_kwh, na.rm = TRUE), by = year]
  dt[, high_price := as.integer(price_c_kwh > price_med_yr)]
  dt[, price_med_yr := NULL]
  log <- c(log, "Built high_price = (price_c_kwh > national median by year)")

  # ---- 7. Build south flag -------------------------------------------------
  south_states <- c("AL", "AR", "DE", "FL", "GA", "KY", "LA",
                    "MD", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "WV")
  dt[, south := as.integer(state %in% south_states)]
  log <- c(log, sprintf("Built south flag: %d states", length(south_states)))

  # ---- 8. Build AI squared -------------------------------------------------
  dt[, ai_sq_lag1 := ai_dc_per1000_lag1^2]
  log <- c(log, "Built ai_sq_lag1 = ai_dc_per1000_lag1^2")

  # ---- 9. Build lags t-2 and t-3 (NA if source year not in panel) ---------
  setorder(dt, state, year)
  dt[, ai_dc_per1000_lag2 := shift(ai_dc_per1000, n = 2, type = "lag"), by = state]
  dt[, ai_dc_per1000_lag3 := shift(ai_dc_per1000, n = 3, type = "lag"), by = state]
  log <- c(log, "Built ai_dc_per1000_lag2 and lag3 (NA for years without prior data)")

  # ---- 10. Build AI lead (for placebo) ------------------------------------
  dt[, ai_dc_per1000_lead1 := shift(ai_dc_per1000, n = 1, type = "lead"), by = state]
  log <- c(log, "Built ai_dc_per1000_lead1 (for placebo robustness check)")

  # ---- 11. Mean-center interaction terms ----------------------------------
  # Center AI and the three binary moderators over the pooled sample
  dt[, ai_lag1_c    := ai_dc_per1000_lag1 - mean(ai_dc_per1000_lag1, na.rm = TRUE)]
  dt[, net_exp_c    := net_exporter       - mean(net_exporter,        na.rm = TRUE)]
  dt[, high_price_c := high_price         - mean(high_price,          na.rm = TRUE)]
  dt[, south_c      := south              - mean(south,               na.rm = TRUE)]
  log <- c(log, "Mean-centered: ai_lag1_c, net_exp_c, high_price_c, south_c")

  # ---- 12. Winsorize outcomes and AI at 1/99 (pooled 2015-2025) ----------
  wins_cols <- intersect(winsor_outcomes, names(dt))
  for (col in wins_cols) {
    vals <- dt[[col]]
    if (sum(!is.na(vals)) > 10) {
      dt[, (col) := winsorize(get(col), p_lo, p_hi)]
    }
  }
  log <- c(log, sprintf("Winsorized outcomes at [%g, %g]: %s",
                        p_lo, p_hi, paste(wins_cols, collapse = ", ")))

  if (winsor_ai) {
    dt[, ai_dc_per1000_lag1 := winsorize(ai_dc_per1000_lag1, p_lo, p_hi)]
    dt[, ai_sq_lag1         := ai_dc_per1000_lag1^2]  # rebuild after winsorizing
    dt[, ai_lag1_c          := ai_dc_per1000_lag1 - mean(ai_dc_per1000_lag1, na.rm = TRUE)]
    log <- c(log, "Winsorized ai_dc_per1000_lag1 and rebuilt ai_sq_lag1, ai_lag1_c")
  }

  # ---- 13. State and year as factors (for fixest) -------------------------
  dt[, state_f := factor(state)]
  dt[, year_f  := factor(year)]

  # ---- 14. Load W matrices -------------------------------------------------
  W_border <- NULL
  W_invdist <- NULL

  load_w_matrix <- function(path, label) {
    dt_w <- fread(path, header = TRUE)
    # First column is the row-label (state abbreviation); extract it and drop
    row_labels <- dt_w[[1]]
    col_labels <- names(dt_w)[-1]
    mat <- as.matrix(dt_w[, -1, with = FALSE])
    storage.mode(mat) <- "numeric"
    rownames(mat) <- row_labels
    colnames(mat) <- col_labels
    # Row-standardise (skip zero rows — states with no neighbours, e.g. AK/HI in border W)
    rs <- rowSums(mat, na.rm = TRUE)
    rs[rs == 0] <- 1
    mat_std <- mat / rs
    list(mat = mat_std, rows = row_labels, cols = col_labels)
  }

  if (file.exists(W_border_path)) {
    wb <- load_w_matrix(W_border_path, "W_border")
    W_border <- wb$mat
    w_state_names <- wb$rows
    panel_states_48 <- sort(unique(dt[contig48 == 1, state]))
    if (!setequal(w_state_names, c(panel_states_48, setdiff(w_state_names, panel_states_48)))) {
      log <- c(log, sprintf("W_border rows: %s", paste(sort(w_state_names), collapse = ",")))
    }
    log <- c(log, sprintf("W_border loaded and row-standardised: %d x %d (rows: %s ... %s)",
                          nrow(W_border), ncol(W_border), wb$rows[1], wb$rows[length(wb$rows)]))
  } else {
    log <- c(log, sprintf("W_border not found at %s", W_border_path))
  }

  if (file.exists(W_invdist_path)) {
    wd <- load_w_matrix(W_invdist_path, "W_invdist")
    W_invdist <- wd$mat
    log <- c(log, sprintf("W_invdist loaded and row-standardised: %d x %d", nrow(W_invdist), ncol(W_invdist)))
  } else {
    log <- c(log, sprintf("W_invdist not found at %s; build from state_centroids_land.csv if needed", W_invdist_path))
  }

  list(panel = dt, W_border = W_border, W_invdist = W_invdist, log = log)
}

# --------------------------------------------------------------------------
# smoke_check()
#
# Prints N by year, missingness for every model variable, and ranges.
# Call after load_panel() to confirm N = 550 for the lagged core sample.
# --------------------------------------------------------------------------
smoke_check <- function(res) {
  dt <- res$panel

  cat("\n=== SMOKE CHECK ===\n\n")

  # N by year
  cat("--- N by year (all 50 states) ---\n")
  print(dt[, .N, by = year][order(year)])

  # Lagged core sample
  core_vars <- c("ai_dc_per1000_lag1", "ln_ec", "ln_ee", "renew_share",
                 "ln_gdp_pc", "price_c_kwh", "tech_share", "manuf_share", "pop_growth")
  core_sample <- dt[complete.cases(dt[, ..core_vars])]
  cat(sprintf("\n--- Lagged core sample (all core vars non-missing): N = %d ---\n", nrow(core_sample)))
  cat(sprintf("  Expected: 550 (50 states x 11 years minus 4 suppressed AK/ND/SD/WY in 2015 lag)\n"))
  if (nrow(core_sample) != 550)
    cat(sprintf("  *** MISMATCH: got %d, expected 550 ***\n", nrow(core_sample)))

  # Missingness for model variables
  model_vars <- c(
    "ai_dc_per1000_lag1", "ai_sq_lag1",
    "ln_ec", "ln_ee", "renew_share", "solar_share", "wind_share",
    "new_renew_mw", "co2_per_mwh_t", "fossil_to_renew", "coal_share",
    "seds_mmbtu_pc", "new_renew_mw",
    "ln_gdp_pc", "price_c_kwh", "tech_share", "manuf_share", "pop_growth",
    "hma", "ln_ea",
    "net_exporter", "high_price", "south"
  )
  model_vars <- intersect(model_vars, names(dt))

  cat("\n--- Missingness for model variables ---\n")
  miss <- data.frame(
    variable = model_vars,
    n_miss   = sapply(model_vars, function(v) sum(is.na(dt[[v]]))),
    pct_miss = sapply(model_vars, function(v) round(100 * mean(is.na(dt[[v]])), 1))
  )
  print(miss[miss$n_miss > 0, ])
  cat(sprintf("  (%d variables with zero missingness not shown)\n", sum(miss$n_miss == 0)))

  # Ranges of AI and core outcomes
  cat("\n--- Ranges (pooled, winsorized) ---\n")
  range_vars <- c("ai_dc_per1000_lag1", "ln_ec", "ln_ee", "renew_share",
                  "solar_share", "wind_share", "fossil_to_renew")
  range_vars <- intersect(range_vars, names(dt))
  for (v in range_vars) {
    vals <- dt[[v]]
    cat(sprintf("  %-30s  min=%8.4f  median=%8.4f  max=%8.4f  NAs=%d\n",
                v, min(vals, na.rm=TRUE), median(vals, na.rm=TRUE),
                max(vals, na.rm=TRUE), sum(is.na(vals))))
  }

  cat("\n=== END SMOKE CHECK ===\n")
  invisible(res)
}

#!/usr/bin/env Rscript
# 04d_step3_spatial.R
# Phase 4d: H3 Spatial analysis
#   Block 0: W matrices (invdist-50 main; invdist-48, border-48 checks)
#   Block 1: Moran's I — 4 vars × 11 years × 3 W + residual Moran's I
#   Block 2: LM pre-tests (optional) via splm::slmtest
#   Block 3: SLX — feols clustered SEs; total lincom b1+theta1
#   Block 4+5: SDM via SDPDmod — LYtrans=TRUE (main) and FALSE; invdist/border checks
#   Block 6: splm cross-check (compare rho/b1/theta1 with SDPDm LYtrans=FALSE)
#   Block 7: Maps and figures
# Usage: Rscript code/R/04d_step3_spatial.R --date YYYY-MM-DD

suppressPackageStartupMessages({
  library(fixest)
  library(spdep)
  library(splm)
  library(SDPDmod)
  library(sf)
  library(ggplot2)
  library(maps)
  library(data.table)
})

# ---- Argument parsing ----
args <- commandArgs(trailingOnly=TRUE)
date_arg <- NULL
for (i in seq_along(args)) {
  if (args[i]=="--date" && i<length(args)) date_arg <- args[i+1]
}
if (is.null(date_arg)) stop("--date YYYY-MM-DD required")

OUT_H3  <- file.path("results", date_arg, "h3")
OUT_TAB <- file.path("results", date_arg, "tables")
OUT_FIG <- file.path("results", date_arg, "figures")
for (d in c(OUT_H3, OUT_TAB, OUT_FIG))
  dir.create(d, recursive=TRUE, showWarnings=FALSE)

cat("=== Phase 4d: Spatial Analysis ===\n")
cat(sprintf("Date: %s | h3 -> %s\n", date_arg, OUT_H3))

# ---- Panel ----
source("code/R/load_panel.R")
res <- load_panel()
dt  <- res$panel
cat(sprintf("Panel: N=%d obs, %d states, %d years\n",
            nrow(dt), dt[,uniqueN(state)], dt[,uniqueN(year)]))

OUTCOMES <- c("ln_ec","ln_ee","renew_share")
CTRL4    <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"
CC4      <- c("ln_gdp_pc","manuf_share","price_c_kwh","pop_growth")
YEARS    <- 2015:2025

# ================================================================
# BLOCK 0: W matrices
# ================================================================
cat("\n=== Block 0: W matrices ===\n")

read_W <- function(path) {
  raw    <- fread(path)
  states <- raw[[1]]
  W      <- as.matrix(raw[, -1])
  rownames(W) <- colnames(W) <- states
  W
}

Wi50 <- read_W("data/out/W_inverse_distance_rowstd.csv")
Wb50 <- read_W("data/out/W_border_binary.csv")

# invdist-50: already row-standardized
stopifnot(all(abs(rowSums(Wi50) - 1) < 1e-5))
cat("invdist-50: 50x50, row-standardized OK\n")

# invdist-48: drop AK, HI; re-row-normalize
keep48 <- rownames(Wi50)[!rownames(Wi50) %in% c("AK","HI")]
Wi48   <- Wi50[keep48, keep48]
Wi48   <- Wi48 / rowSums(Wi48)
stopifnot(all(abs(rowSums(Wi48) - 1) < 1e-5), length(keep48) == 48)
cat("invdist-48: 48x48, re-normalized OK\n")

# border-48: subset binary W to 48 states; row-standardize
Wb48 <- Wb50[keep48, keep48]
rs_b <- rowSums(Wb48)
stopifnot(all(rs_b > 0))
Wb48 <- Wb48 / rs_b
stopifnot(all(abs(rowSums(Wb48) - 1) < 1e-5))
cat("border-48: 48x48, row-standardized OK\n")

Ws <- list(
  invdist50 = list(W=Wi50, states=rownames(Wi50), N=50, label="invdist-50"),
  invdist48 = list(W=Wi48, states=keep48,         N=48, label="invdist-48"),
  border48  = list(W=Wb48, states=keep48,         N=48, label="border-48")
)
for (nm in names(Ws))
  Ws[[nm]]$listw <- spdep::mat2listw(Ws[[nm]]$W, style="W", zero.policy=TRUE)

# ---- Helpers ----
assert_order <- function(dt_sub, Wstates, context) {
  obs <- dt_sub$state
  if (!identical(obs, Wstates)) {
    mm <- which(obs != Wstates)[1]
    stop(sprintf("State order mismatch in [%s]: pos %d got '%s' expected '%s'",
                 context, mm, obs[mm], Wstates[mm]))
  }
}

make_Wcols <- function(panel, Wmat, Wstates, varnames) {
  d <- copy(panel[state %in% Wstates])
  # sort by W row order (not alphabetical) within each year
  d <- d[order(year, match(state, Wstates))]
  for (vn in varnames) {
    newcol <- paste0("W_", vn)
    d[, (newcol) := 0.0]
    for (yr in unique(d$year)) {
      sub <- d[year==yr]
      sub <- sub[order(match(state, Wstates))]
      assert_order(sub, Wstates, sprintf("make_Wcols %s yr=%d", vn, yr))
      d[year==yr, (newcol) := as.numeric(Wmat %*% sub[[vn]])]
    }
  }
  d
}

# ================================================================
# BLOCK 1: Moran's I
# ================================================================
cat("\n=== Block 1: Moran's I ===\n")

MORAN_VARS <- c("ai_dc_per1000_lag1","ln_ec","ln_ee","renew_share")
moran_rows <- list()

for (wname in names(Ws)) {
  winfo <- Ws[[wname]]
  for (yr in YEARS) {
    sub <- dt[year==yr & state %in% winfo$states]
    sub <- sub[order(match(state, winfo$states))]  # sort by W row order, not alphabetical
    assert_order(sub, winfo$states, sprintf("Moran raw %s yr=%d", wname, yr))
    for (vn in MORAN_VARS) {
      x <- sub[[vn]]
      if (sum(!is.na(x)) < winfo$N - 4) {
        cat(sprintf("  SKIP Moran %s yr=%d %s: NAs\n", vn, yr, wname)); next
      }
      x[is.na(x)] <- mean(x, na.rm=TRUE)
      mc <- spdep::moran.mc(x, listw=winfo$listw, nsim=999,
                            alternative="greater", zero.policy=TRUE)
      moran_rows[[length(moran_rows)+1]] <- data.table(
        variable=vn, year=yr, W_version=wname, N=winfo$N,
        moran_I=mc$statistic, p_value=mc$p.value, type="raw"
      )
    }
  }
}

# Residual Moran's I on TWFE residuals
for (Y in OUTCOMES) {
  cc_y <- c(Y,"ai_dc_per1000_lag1",CC4)
  d_full <- dt[complete.cases(dt[, ..cc_y])]
  m_base <- feols(as.formula(paste(Y,"~ ai_dc_per1000_lag1 +",CTRL4,"| state + year")),
                  data=d_full, vcov="iid")
  d_full[, resid := residuals(m_base)]

  for (wname in names(Ws)) {
    winfo <- Ws[[wname]]
    for (yr in YEARS) {
      sub <- d_full[year==yr & state %in% winfo$states]
      sub <- sub[order(match(state, winfo$states))]
      if (nrow(sub) < winfo$N) next
      assert_order(sub, winfo$states, sprintf("Resid Moran %s %s yr=%d", Y, wname, yr))
      mc <- spdep::moran.mc(sub$resid, listw=winfo$listw, nsim=999,
                            alternative="greater", zero.policy=TRUE)
      moran_rows[[length(moran_rows)+1]] <- data.table(
        variable=paste0("resid_",Y), year=yr, W_version=wname, N=winfo$N,
        moran_I=mc$statistic, p_value=mc$p.value, type="resid"
      )
    }
  }
}

moran_dt <- rbindlist(moran_rows)
fwrite(moran_dt, file.path(OUT_H3,"h3_moran.csv"))
cat(sprintf("Moran's I: %d rows\n", nrow(moran_dt)))

cat("\nMoran's I: renew_share, invdist-50, by year:\n")
print(moran_dt[variable=="renew_share" & W_version=="invdist50",
               .(year, I=round(moran_I,4), p=round(p_value,4))])

# ================================================================
# BLOCK 2: LM pre-tests (optional)
# ================================================================
cat("\n=== Block 2: LM pre-tests (optional) ===\n")

lm_rows <- list()
for (Y in OUTCOMES) {
  cc_y <- c(Y,"ai_dc_per1000_lag1",CC4)
  d_lm <- dt[complete.cases(dt[, ..cc_y])]
  for (test in c("lml","lme","rlml","rlme")) {
    tryCatch({
      res_lm <- slmtest(
        as.formula(paste(Y,"~ ai_dc_per1000_lag1 +",CTRL4,"+ factor(year)")),
        data   = as.data.frame(d_lm),
        listw  = Ws$invdist50$listw,
        model  = "within",
        test   = test,
        index  = c("state","year"),
        zero.policy = TRUE
      )
      lm_rows[[length(lm_rows)+1]] <- data.table(
        outcome=Y, test=test,
        statistic=as.numeric(res_lm$statistic),
        p_value=as.numeric(res_lm$p.value),
        df=as.numeric(res_lm$parameter)
      )
      cat(sprintf("  %s/%s: stat=%.3f p=%.3f\n", Y, test,
                  res_lm$statistic, res_lm$p.value))
    }, error=function(e) {
      cat(sprintf("  SKIP %s/%s: %s\n", Y, test, conditionMessage(e)))
      lm_rows[[length(lm_rows)+1]] <<- data.table(
        outcome=Y, test=test, statistic=NA_real_, p_value=NA_real_, df=NA_real_)
    })
  }
}
lm_dt <- rbindlist(lm_rows, fill=TRUE)
fwrite(lm_dt, file.path(OUT_H3,"h3_lm_tests.csv"))
cat(sprintf("LM tests: %d rows\n", nrow(lm_dt)))

# ================================================================
# BLOCK 3: SLX (H3b companion — only spatial model with clustered SEs)
# ================================================================
cat("\n=== Block 3: SLX ===\n")
# SLX = spatial lag of X only (no spatial lag of Y, no rho).
# Memo's fallback and the clustered-SE companion to the SDM.
# Total = b1 + theta1 reported with delta-method clustered SE.

W_vars_slx <- c("ai_dc_per1000_lag1", CC4)
slx_rows   <- list()

for (wname in names(Ws)) {
  winfo <- Ws[[wname]]
  for (Y in OUTCOMES) {
    cc_y <- c(Y,"ai_dc_per1000_lag1",CC4)
    d_slx <- make_Wcols(dt[complete.cases(dt[,..cc_y])], winfo$W, winfo$states, W_vars_slx)

    slx_form <- as.formula(paste(
      Y, "~ ai_dc_per1000_lag1 + W_ai_dc_per1000_lag1 +",
      CTRL4, "+",
      paste(paste0("W_",CC4), collapse=" + "),
      "| state + year"
    ))
    m  <- feols(slx_form, data=d_slx, vcov=~state)
    ct <- coeftable(m)
    V  <- vcov(m)

    b1    <- ct["ai_dc_per1000_lag1","Estimate"]
    se_b1 <- ct["ai_dc_per1000_lag1","Std. Error"]
    p_b1  <- ct["ai_dc_per1000_lag1","Pr(>|t|)"]
    th1   <- ct["W_ai_dc_per1000_lag1","Estimate"]
    se_th <- ct["W_ai_dc_per1000_lag1","Std. Error"]
    p_th  <- ct["W_ai_dc_per1000_lag1","Pr(>|t|)"]

    # Total lincom: b1 + theta1; delta-method SE from clustered vcov
    nm2    <- c("ai_dc_per1000_lag1","W_ai_dc_per1000_lag1")
    Vsub   <- V[nm2, nm2]
    tot    <- b1 + th1
    se_tot <- sqrt(sum(Vsub))
    df_cl  <- length(unique(d_slx$state)) - 1
    p_tot  <- 2 * pt(-abs(tot/se_tot), df=df_cl)

    slx_rows[[length(slx_rows)+1]] <- data.table(
      outcome=Y, W_version=wname, N=m$nobs,
      b1=b1, se_b1=se_b1, p_b1=p_b1,
      theta1=th1, se_theta1=se_th, p_theta1=p_th,
      total=tot, se_total=se_tot, p_total=p_tot,
      within_r2=r2(m,"wr2"), vcov_type="CRV1-state"
    )
    cat(sprintf("  SLX %s/%s: b1=%.5f(p=%.3f) theta1=%.5f(p=%.3f) total=%.5f(p=%.3f)\n",
                Y, wname, b1, p_b1, th1, p_th, tot, p_tot))
  }
}
slx_dt <- rbindlist(slx_rows)
fwrite(slx_dt, file.path(OUT_H3,"h3_slx.csv"))
cat(sprintf("SLX: %d rows\n", nrow(slx_dt)))

# ================================================================
# BLOCK 4+5: SDM via SDPDmod
# ================================================================
cat("\n=== Block 4+5: SDM (SDPDmod) ===\n")
# ?SDPDm documents:
#   LYtrans=TRUE:  Lee-Yu (2010) bias correction; applied to remove incidental-parameter
#                  bias from two-way FE with finite T. Recommended for static panel.
#   demn=TRUE:     Lee-Yu demeaning to remove FE (static models only). We use
#                  effect="twoways" instead, so demn=FALSE throughout.
# Main: LYtrans=TRUE (bias-corrected). LYtrans=FALSE shown beside it for splm comparison.
# SEs are asymptotic ML (not clustered); compare b1 and theta1 with SLX above.
# Coefficient names: original vars unchanged; W-lagged vars use "W*" prefix.
# Impacts extracted from impactsSDPDm: DIRECT.tab, INDIRECT.tab, TOTAL.tab
#   (each a matrix: rows=variables, cols=Estimate/SE/t/p).

# Eigenvalue bounds for invdist-50 (valid rho interval)
Wi50_ev      <- eigen(Wi50, only.values=TRUE)$values
rho_lo_global <- 1 / max(Re(Wi50_ev))          # ≈ 1  (upper bound)
rho_hi_global <- 1 / min(Re(Wi50_ev[Re(Wi50_ev)<0]))  # lower bound (most negative ev)
# valid interval: (rho_hi_global, rho_lo_global) = e.g. (-4.74, 1)
cat(sprintf("W eigenvalue range: [%.4f, %.4f] → valid rho in (%.3f, %.3f)\n",
            min(Re(Wi50_ev)), max(Re(Wi50_ev)), rho_hi_global, rho_lo_global))

run_sdm_fit <- function(Y, Wmat, Wstates, wname, LYt) {
  cc_y  <- c(Y,"ai_dc_per1000_lag1",CC4)
  d_raw <- dt[state %in% Wstates & complete.cases(dt[,..cc_y])]
  # SDPDm sorts the panel alphabetically by the first index variable (state).
  # W must be reordered to match that alphabetical order.
  al_states <- sort(unique(d_raw$state))
  d_sdm     <- as.data.frame(d_raw[order(match(state, al_states), year)])
  Wmat_al   <- Wmat[al_states, al_states]
  stopifnot(all(abs(rowSums(Wmat_al) - 1) < 1e-5))
  n_st  <- length(al_states)
  if (n_st != nrow(Wmat_al)) {
    cat(sprintf("  SKIP SDM %s/%s LYtrans=%s: data N=%d != W N=%d\n",
                Y, wname, LYt, n_st, nrow(Wmat_al)))
    return(NULL)
  }
  # Eigenvalue-based validity bounds for this W
  ev_w    <- eigen(Wmat_al, only.values=TRUE)$values
  rho_max <- 1 / max(Re(ev_w))
  ev_neg  <- Re(ev_w[Re(ev_w) < 0])
  rho_min <- if (length(ev_neg) > 0) 1 / max(ev_neg) else -Inf
  tryCatch({
    m <- SDPDm(
      formula = as.formula(paste(Y,"~ ai_dc_per1000_lag1 +",CTRL4)),
      data    = d_sdm,
      W       = Wmat_al,
      index   = c("state","year"),
      model   = "sdm",
      effect  = "twoways",
      LYtrans = LYt,
      demn    = FALSE,
      dynamic = FALSE
    )
    b1_nm  <- "ai_dc_per1000_lag1"
    th_nm  <- paste0("W*",b1_nm)
    b1  <- as.numeric(m$coefficients[b1_nm])
    th1 <- as.numeric(m$coefficients[th_nm])
    rho <- as.numeric(m$rho)

    # Validity check: rho must be in (rho_min, rho_max)
    rho_valid <- (rho > rho_min) & (rho < rho_max)
    if (!rho_valid) {
      cat(sprintf("    FLAG: rho=%.4f outside valid interval (%.3f, %.3f) — SDPDmod convergence issue\n",
                  rho, rho_min, rho_max))
    }

    imp  <- impactsSDPDm(m, NSIM=500)

    # Extract AI row from impact tables
    dir_tab <- imp$DIRECT.tab;  ind_tab <- imp$INDIRECT.tab; tot_tab <- imp$TOTAL.tab
    dir_e <- dir_tab[b1_nm,"Estimate"];  dir_se <- dir_tab[b1_nm,"Std. Error"]
    ind_e <- ind_tab[b1_nm,"Estimate"];  ind_se <- ind_tab[b1_nm,"Std. Error"]
    tot_e <- tot_tab[b1_nm,"Estimate"];  tot_se <- tot_tab[b1_nm,"Std. Error"]
    dir_p <- dir_tab[b1_nm,"Pr(>|t|)"]; ind_p <- ind_tab[b1_nm,"Pr(>|t|)"]
    tot_p <- tot_tab[b1_nm,"Pr(>|t|)"]

    # Impact check: analytical (b1+theta1)/(1-rho) vs simulated total
    # Flag large ABSOLUTE discrepancy (> 0.01); skip percentage for near-zero values
    theoretical  <- (b1 + th1) / (1 - rho)
    disc_abs     <- abs(tot_e - theoretical)
    disc_flag    <- disc_abs > 0.01

    cat(sprintf("    rho=%.4f [%s]  b1=%.6f  theta1=%.6f\n",
                rho, if(rho_valid) "valid" else "INVALID", b1, th1))
    cat(sprintf("    Impact: direct=%.6f(p=%.3f) indirect=%.6f(p=%.3f) total=%.6f(p=%.3f)\n",
                dir_e, dir_p, ind_e, ind_p, tot_e, tot_p))
    cat(sprintf("    Impact check: analytical=(b1+th1)/(1-rho)=%.6f  sim_total=%.6f  |diff|=%.6f%s\n",
                theoretical, tot_e, disc_abs, if(disc_flag) " FLAG" else ""))

    list(rho=rho, rho_valid=rho_valid, b1=b1, theta1=th1, theoretical=theoretical,
         dir_e=dir_e, dir_se=dir_se, dir_p=dir_p,
         ind_e=ind_e, ind_se=ind_se, ind_p=ind_p,
         tot_e=tot_e, tot_se=tot_se, tot_p=tot_p,
         disc_abs=disc_abs, llik=m$llik, Nobs=nrow(d_sdm))
  }, error=function(e) {
    cat(sprintf("  ERROR SDM %s/%s LYtrans=%s: %s\n", Y, wname, LYt, conditionMessage(e)))
    NULL
  })
}

sdm_coef_rows <- list()
sdm_imp_rows  <- list()

# Main W: all 3 outcomes × LYtrans TRUE and FALSE
for (Y in OUTCOMES) {
  for (LYt in c(TRUE, FALSE)) {
    cat(sprintf("\n  SDM %s / invdist-50 / LYtrans=%s ...\n", Y, LYt))
    r <- run_sdm_fit(Y, Wi50, rownames(Wi50), "invdist50", LYt)
    if (is.null(r)) next

    sdm_coef_rows[[length(sdm_coef_rows)+1]] <- data.table(
      outcome=Y, W_version="invdist50", LYtrans=LYt, N=r$Nobs,
      rho=r$rho, rho_valid=r$rho_valid, b1=r$b1, theta1=r$theta1,
      analytical_total=r$theoretical, llik=r$llik
    )
    sdm_imp_rows[[length(sdm_imp_rows)+1]] <- data.table(
      outcome=Y, W_version="invdist50", LYtrans=LYt, var="ai_dc_per1000_lag1",
      direct=r$dir_e,   sd_direct=r$dir_se,   p_direct=r$dir_p,
      indirect=r$ind_e, sd_indirect=r$ind_se, p_indirect=r$ind_p,
      total=r$tot_e,    sd_total=r$tot_se,    p_total=r$tot_p,
      disc_abs=r$disc_abs, rho_valid=r$rho_valid
    )
  }
}

# Sensitivity: invdist-48 and border-48, all 3 outcomes, LYtrans=TRUE
for (wname in c("invdist48","border48")) {
  Wmat_s <- Ws[[wname]]$W; Wst_s <- Ws[[wname]]$states
  for (Y in OUTCOMES) {
    cat(sprintf("\n  SDM sensitivity %s / %s / LYtrans=TRUE ...\n", Y, wname))
    r <- run_sdm_fit(Y, Wmat_s, Wst_s, wname, TRUE)
    if (is.null(r)) next

    sdm_coef_rows[[length(sdm_coef_rows)+1]] <- data.table(
      outcome=Y, W_version=wname, LYtrans=TRUE, N=r$Nobs,
      rho=r$rho, rho_valid=r$rho_valid, b1=r$b1, theta1=r$theta1,
      analytical_total=r$theoretical, llik=r$llik
    )
    sdm_imp_rows[[length(sdm_imp_rows)+1]] <- data.table(
      outcome=Y, W_version=wname, LYtrans=TRUE, var="ai_dc_per1000_lag1",
      direct=r$dir_e,   sd_direct=r$dir_se,   p_direct=r$dir_p,
      indirect=r$ind_e, sd_indirect=r$ind_se, p_indirect=r$ind_p,
      total=r$tot_e,    sd_total=r$tot_se,    p_total=r$tot_p,
      disc_abs=r$disc_abs, rho_valid=r$rho_valid
    )
  }
}

sdm_coef_dt <- rbindlist(sdm_coef_rows, fill=TRUE)
sdm_imp_dt  <- rbindlist(sdm_imp_rows,  fill=TRUE)
fwrite(sdm_coef_dt, file.path(OUT_H3,"h3_sdm_core.csv"))
fwrite(sdm_imp_dt,  file.path(OUT_H3,"h3_sdm_impacts.csv"))
cat(sprintf("\nSDM: %d coef rows, %d impact rows written\n",
            nrow(sdm_coef_dt), nrow(sdm_imp_dt)))

# ================================================================
# BLOCK 6: splm cross-check
# ================================================================
cat("\n=== Block 6: splm cross-check ===\n")
# SDM formula with hand-made W*X columns; effect="twoways"; lag=TRUE (rho).
# Compare rho, b1, theta1 with SDPDm LYtrans=FALSE.
# Do NOT take impacts from splm (W*AI is treated as a separate regressor,
# not inside the spatial lag machinery).

splm_rows <- list()
# splm also sorts by state (alphabetically), so sort data and W the same way
al50 <- sort(rownames(Wi50))
Wi50_al <- Wi50[al50, al50]
stopifnot(all(abs(rowSums(Wi50_al) - 1) < 1e-5))
listw50_al <- spdep::mat2listw(Wi50_al, style="W", zero.policy=TRUE)

for (Y in OUTCOMES) {
  cc_y  <- c(Y,"ai_dc_per1000_lag1",CC4)
  d_sp  <- make_Wcols(dt[complete.cases(dt[,..cc_y])], Wi50_al, al50, W_vars_slx)
  d_sp  <- d_sp[order(state, year)]

  sp_form <- as.formula(paste(
    Y,"~ ai_dc_per1000_lag1 + W_ai_dc_per1000_lag1 +",
    CTRL4,"+",
    paste(paste0("W_",CC4), collapse=" + ")
  ))
  tryCatch({
    m_sp <- splm::spml(sp_form,
                       data   = as.data.frame(d_sp),
                       index  = c("state","year"),
                       listw  = listw50_al,
                       lag    = TRUE,
                       spatial.error = "none",
                       effect = "twoways")
    rho_sp <- as.numeric(m_sp$spat.coef)[1]
    b1_sp  <- as.numeric(coef(m_sp)["ai_dc_per1000_lag1"])
    th_sp  <- as.numeric(coef(m_sp)["W_ai_dc_per1000_lag1"])
    cat(sprintf("  splm %s: rho=%.4f b1=%.6f theta1=%.6f\n", Y, rho_sp, b1_sp, th_sp))
    splm_rows[[length(splm_rows)+1]] <- data.table(
      outcome=Y, W_version="invdist50", method="splm",
      rho=rho_sp, b1=b1_sp, theta1=th_sp
    )
  }, error=function(e) {
    cat(sprintf("  ERROR splm %s: %s\n", Y, conditionMessage(e)))
    splm_rows[[length(splm_rows)+1]] <<- data.table(
      outcome=Y, W_version="invdist50", method="splm",
      rho=NA_real_, b1=NA_real_, theta1=NA_real_)
  })
}
splm_dt <- rbindlist(splm_rows, fill=TRUE)
fwrite(splm_dt, file.path(OUT_H3,"h3_splm_check.csv"))

cat("\nComparison SDPDm (LYtrans=FALSE) vs splm (invdist-50):\n")
sdm0 <- as.data.frame(sdm_coef_dt)[
  sdm_coef_dt$W_version=="invdist50" & !sdm_coef_dt$LYtrans,
  c("outcome","rho","b1","theta1")]
sp_c <- as.data.frame(splm_dt)[, c("outcome","rho","b1","theta1")]
if (nrow(sdm0)>0 && nrow(sp_c)>0) {
  comp <- merge(sdm0, sp_c, by="outcome", suffixes=c("_sdm","_spl"))
  comp[, c("rho_sdm","b1_sdm","theta1_sdm","rho_spl","b1_spl","theta1_spl")] <-
    round(comp[, c("rho_sdm","b1_sdm","theta1_sdm","rho_spl","b1_spl","theta1_spl")], 5)
  print(comp)
}

# ================================================================
# BLOCK 7: Maps and figures
# ================================================================
cat("\n=== Block 7: Figures ===\n")

state_lu <- data.table(
  state = c("AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
            "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
            "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
            "VA","WA","WV","WI","WY"),
  region = c("alabama","alaska","arizona","arkansas","california","colorado","connecticut",
             "delaware","florida","georgia","hawaii","idaho","illinois","indiana","iowa",
             "kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan",
             "minnesota","mississippi","missouri","montana","nebraska","nevada","new hampshire",
             "new jersey","new mexico","new york","north carolina","north dakota","ohio",
             "oklahoma","oregon","pennsylvania","rhode island","south carolina","south dakota",
             "tennessee","texas","utah","vermont","virginia","washington","west virginia",
             "wisconsin","wyoming")
)
map_base <- as.data.table(map_data("state"))
map_base <- merge(map_base, state_lu, by="region", all.x=TRUE)

map_titles <- c(
  ln_ec             = "ln(Electricity Consumption)",
  ln_ee             = "ln(Energy Efficiency)",
  renew_share       = "Renewable Share",
  ai_dc_per1000_lag1= "AI DC per 1,000 Workers (lag1)"
)

for (yr in c(2015, 2025)) {
  dt_yr <- dt[year==yr]
  for (vn in c(OUTCOMES, "ai_dc_per1000_lag1")) {
    map_dt <- merge(map_base,
                    dt_yr[, .(state, val=.SD[[vn]])],
                    by="state", all.x=TRUE)
    setorder(map_dt, group, order)
    p <- ggplot(map_dt, aes(x=long, y=lat, group=group, fill=val)) +
      geom_polygon(color="white", linewidth=0.1) +
      scale_fill_viridis_c(name=map_titles[vn], na.value="grey80", option="plasma") +
      coord_quickmap() +
      labs(title=sprintf("%s — %d", map_titles[vn], yr),
           subtitle="48 contiguous states shown") +
      theme_void(base_size=10) +
      theme(legend.position="bottom", legend.key.width=unit(2,"cm"))
    fn <- sprintf("h3_map_%s_%d.png", gsub("[^a-z0-9]","_",tolower(vn)), yr)
    ggsave(file.path(OUT_FIG,fn), p, width=8, height=5, dpi=150)
  }
}
cat("  Saved 8 maps (4 vars × 2 years)\n")

# Moran's I time series — renew_share and AI, all 3 W
for (vn_m in c("renew_share","ai_dc_per1000_lag1")) {
  moran_sub <- moran_dt[variable==vn_m & type=="raw"]
  moran_sub[, W_lab := factor(W_version, levels=c("invdist50","invdist48","border48"),
                              labels=c("invdist-50","invdist-48","border-48"))]
  p_m <- ggplot(moran_sub, aes(x=year, y=moran_I, color=W_lab, shape=W_lab)) +
    geom_line() + geom_point(size=2) +
    geom_hline(yintercept=0, linetype="dashed", color="grey50") +
    scale_color_brewer(palette="Set1") +
    labs(title=sprintf("Moran's I: %s by year", vn_m),
         x="Year", y="Moran's I", color="W", shape="W") +
    theme_minimal(base_size=11)
  fn_m <- sprintf("h3_moran_time_%s.png", gsub("[^a-z0-9]","_",tolower(vn_m)))
  ggsave(file.path(OUT_FIG,fn_m), p_m, width=7, height=4, dpi=150)
}
cat("  Saved 2 Moran time series\n")

# SDM impacts bar chart (main W, LYtrans=TRUE)
sdm_main <- sdm_imp_dt[W_version=="invdist50" & LYtrans==TRUE]
if (nrow(sdm_main) > 0) {
  sdm_long <- melt(sdm_main[, .(outcome, direct, indirect, total)],
                   id.vars="outcome", variable.name="type", value.name="value")
  sdm_long[, type := factor(type, levels=c("direct","indirect","total"))]
  sdm_long[, outcome := factor(outcome, levels=OUTCOMES)]
  p_bar <- ggplot(sdm_long, aes(x=outcome, y=value, fill=type)) +
    geom_col(position="dodge") +
    geom_hline(yintercept=0, linetype="dashed") +
    scale_fill_brewer(palette="Set2") +
    labs(title="SDM: AI Direct/Indirect/Total Impacts\n(invdist-50, LYtrans=TRUE)",
         x="Outcome", y="Impact", fill="Type") +
    theme_minimal(base_size=11)
  ggsave(file.path(OUT_FIG,"h3_sdm_impacts_bar.png"), p_bar, width=7, height=4, dpi=150)
  cat("  Saved SDM impacts bar chart\n")
}

# SLX coefficient plot
slx_long <- rbind(
  slx_dt[, .(outcome, W_version, coef_type="b1 (direct)",    value=b1,     se=se_b1)],
  slx_dt[, .(outcome, W_version, coef_type="θ1 (neighbor)",  value=theta1, se=se_theta1)]
)
slx_long[, W_lab := factor(W_version, levels=c("invdist50","invdist48","border48"),
                            labels=c("invdist-50","invdist-48","border-48"))]
p_slx <- ggplot(slx_long, aes(x=value, y=outcome, color=W_lab)) +
  geom_point(position=position_dodge(0.5), size=2.5) +
  geom_errorbarh(aes(xmin=value-1.96*se, xmax=value+1.96*se),
                 position=position_dodge(0.5), height=0.2) +
  geom_vline(xintercept=0, linetype="dashed", color="grey60") +
  facet_wrap(~coef_type, ncol=2, scales="free_x") +
  scale_color_brewer(palette="Set1") +
  labs(title="SLX: AI coefficients by W (95% CI, clustered SE)",
       x="Coefficient", y="Outcome", color="W") +
  theme_minimal(base_size=10)
ggsave(file.path(OUT_FIG,"h3_slx_coefplot.png"), p_slx, width=9, height=4, dpi=150)
cat("  Saved SLX coefficient plot\n")

# ================================================================
# RECEIPT
# ================================================================
cat("\n=== Writing RECEIPT ===\n")
receipt <- c(
  sprintf("# Phase 4d RECEIPT — %s", date_arg),
  sprintf("Run completed: %s", Sys.time()),
  "",
  "## W matrices",
  "  invdist-50: W_inverse_distance_rowstd.csv (50x50, row-std as-is)",
  "  invdist-48: subset invdist-50 drop AK+HI, re-row-normalized",
  "  border-48:  W_border_binary.csv subset drop AK+HI, row-standardized",
  "",
  "## SDPDm notes",
  "  LYtrans=TRUE: Lee-Yu (2010) bias correction for two-way FE panel (main)",
  "  LYtrans=FALSE: uncorrected ML (for splm comparison)",
  "  demn=FALSE: effect='twoways' handles FE removal internally",
  "  SEs: asymptotic ML (not clustered); NSIM=500 for impactsSDPDm",
  "",
  "## Outputs",
  sprintf("  h3_moran.csv:        %d rows", nrow(moran_dt)),
  sprintf("  h3_lm_tests.csv:     %d rows", nrow(lm_dt)),
  sprintf("  h3_slx.csv:          %d rows (%d outcomes x 3 W)", nrow(slx_dt), length(OUTCOMES)),
  sprintf("  h3_sdm_core.csv:     %d rows", nrow(sdm_coef_dt)),
  sprintf("  h3_sdm_impacts.csv:  %d rows", nrow(sdm_imp_dt)),
  sprintf("  h3_splm_check.csv:   %d rows", nrow(splm_dt)),
  sprintf("  figures:             %s/*.png", OUT_FIG)
)
writeLines(receipt, file.path(OUT_H3,"RECEIPT.md"))
cat("RECEIPT written.\n")
cat("\n=== Phase 4d complete ===\n")

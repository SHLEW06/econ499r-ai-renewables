#!/usr/bin/env Rscript
# 04b_step1_twfe_ctrl4.R
# Reruns all Phase 4b experiments with ctrl4 (correct H1 spec).
# tech_share excluded: it is the H2a mediator (bad control for Step 1).
# ctrl4 = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth (memo spec)
# Appends ctrl4-tagged rows; does not overwrite or delete ctrl5 rows.
# Rebuilds tables and figures using ctrl4 as baseline.
# Usage: Rscript code/R/04b_step1_twfe_ctrl4.R --date 2026-11-02

suppressPackageStartupMessages({
  library(fixest)
  library(modelsummary)
  library(data.table)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = TRUE)
date_arg <- NULL
for (i in seq_along(args)) {
  if (args[i] == "--date" && i < length(args)) date_arg <- args[i + 1]
}
if (is.null(date_arg)) stop("--date YYYY-MM-DD required")
OUT    <- file.path("results", date_arg, "h1")
TABLES <- file.path("results", date_arg, "tables")
FIGS   <- file.path("results", date_arg, "figures")
for (d in c(OUT, TABLES, FIGS)) dir.create(d, recursive = TRUE, showWarnings = FALSE)

source("code/R/load_panel.R")

# Standard panel (new_renew_mw winsorized — this is the spec)
res <- load_panel()
dt  <- res$panel

# Panel with new_renew_mw NOT winsorized (for side-by-side comparison only)
res_nw <- load_panel(winsor_outcomes = c("ln_ec","ln_ee","renew_share",
                                          "solar_share","wind_share",
                                          "co2_per_mwh_t","fossil_to_renew",
                                          "seds_mmbtu_pc"))
dt_nw <- res_nw$panel

# 2015-baseline frozen moderators
base2015 <- dt[year == 2015, .(state,
  net_exporter_2015 = net_exporter,
  high_price_2015   = high_price)]
dt     <- merge(dt,    base2015, by = "state")
dt_nw  <- merge(dt_nw, base2015, by = "state")
dt[,    net_exp_2015_c    := net_exporter_2015 - mean(net_exporter_2015, na.rm = TRUE)]
dt[,    high_price_2015_c := high_price_2015   - mean(high_price_2015,   na.rm = TRUE)]
dt_nw[, net_exp_2015_c    := net_exporter_2015 - mean(net_exporter_2015, na.rm = TRUE)]
dt_nw[, high_price_2015_c := high_price_2015   - mean(high_price_2015,   na.rm = TRUE)]

ctrl4 <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"
cc4   <- c("ai_dc_per1000_lag1","ln_gdp_pc","manuf_share","price_c_kwh","pop_growth")

cat("\n=== 04b ctrl4 rerun ===\n")
cat("ctrl4 =", ctrl4, "\n\n")

write_append <- function(df, fname) {
  # Appended rows must match the file's header (fix of 2026-11-09: lm_proper.csv got
  # ctrl4 rows with a 'controls' column its header lacked; docs/2026-11-09/lm-proper-header-fix.md).
  # Columns the header has but df lacks are filled with NA; columns df has but the header
  # lacks stop the run rather than shifting fields.
  path <- file.path(OUT, fname)
  df <- as.data.table(df)
  if (file.exists(path)) {
    have  <- strsplit(readLines(path, n = 1L), ",", fixed = TRUE)[[1]]   # header line as written; fread may guess on a ragged file
    extra <- setdiff(names(df), have)
    if (length(extra))
      stop(sprintf("%s: new rows have column(s) the header lacks: %s. Write a new file or align the writers.",
                   path, paste(extra, collapse = ", ")))
    for (m in setdiff(have, names(df))) df[, (m) := NA]
    setcolorder(df, have)
  }
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
             N=m$nobs, within_r2=r2(m,"wr2"),
             vcov_type=vcov_type, sample=sample_desc,
             controls=controls_desc, status="ok")
}

# -----------------------------------------------------------------------
# 1. H1 extras with ctrl4 (+ new_renew_mw unwinsorized for comparison)
# -----------------------------------------------------------------------
cat("---- 1. H1 extras ctrl4 ----\n")
extras_specs <- list(
  list(y="solar_share",     data=dt,    samp="50s2015_2025", out_tag="solar_share"),
  list(y="wind_share",      data=dt,    samp="50s2015_2025", out_tag="wind_share"),
  list(y="new_renew_mw",    data=dt,    samp="50s2015_2025", out_tag="new_renew_mw"),
  list(y="new_renew_mw",    data=dt_nw, samp="50s2015_2025", out_tag="new_renew_mw_raw"),
  list(y="fossil_to_renew", data=dt,    samp="50s2015_2025", out_tag="fossil_to_renew"),
  list(y="coal_share",      data=dt,    samp="50s2015_2025", out_tag="coal_share"),
  list(y="co2_per_mwh_t",   data=dt,    samp="50s2015_2024", out_tag="co2_per_mwh_t")
)

ext_rows <- list()
for (sp in extras_specs) {
  d_use <- if (sp$samp == "50s2015_2024") sp$data[year <= 2024] else sp$data
  cc_y  <- c(sp$y, cc4)
  d_cc  <- d_use[complete.cases(d_use[, ..cc_y])]
  winsor_tag <- if (sp$out_tag == "new_renew_mw_raw") "w9901ai" else "w9901"
  tag <- sprintf("h1x_twfe_ai518210_lag1_ctrl4_%s_cl-state_%s_%s",
                 winsor_tag, sp$out_tag, sp$samp)
  m   <- feols(as.formula(paste(sp$y, "~ ai_dc_per1000_lag1 +", ctrl4, "| state + year")),
               data=d_cc, vcov=~state)
  r   <- tidy_row(m, tag, sp$out_tag, "CRV1-state", sp$samp, "ctrl4")
  ext_rows[[length(ext_rows)+1]] <- r
  cat(sprintf("  %-25s N=%d  a1=%9.5f  p=%.3f\n", sp$out_tag, r$N, r$estimate, r$pval))
}
write_append(rbindlist(ext_rows), "h1_extras.csv")

# -----------------------------------------------------------------------
# 2. SE check (DK) with ctrl4
# -----------------------------------------------------------------------
cat("\n---- 2. DK check ctrl4 ----\n")
dk_rows <- list()
for (y in c("ln_ec","ln_ee","renew_share")) {
  cc_y <- c(y, cc4)
  d_cc <- dt[complete.cases(dt[, ..cc_y])]
  m_dk <- feols(as.formula(paste(y, "~ ai_dc_per1000_lag1 +", ctrl4, "| state + year")),
                data=d_cc, vcov="DK", panel.id=~state+year)
  tag  <- sprintf("h1_twfe_ai518210_lag1_ctrl4_w9901_dk_%s_50s2015_2025", y)
  r    <- tidy_row(m_dk, tag, y, "DK", "50s2015_2025", "ctrl4")
  dk_rows[[y]] <- r
  cat(sprintf("  %-14s DK p=%.3f  (SE=%.5f)\n", y, r$pval, r$se))
}
write_append(rbindlist(dk_rows), "se_check.csv")

# -----------------------------------------------------------------------
# 3. Nonlinearity + proper LM test with ctrl4
# -----------------------------------------------------------------------
cat("\n---- 3. Nonlinearity + LM ctrl4 ----\n")
nl_outcomes <- c("ln_ec","ln_ee","renew_share","solar_share","wind_share",
                 "new_renew_mw","fossil_to_renew","coal_share")
nl_rows  <- list()
lm_rows4 <- list()

for (y in nl_outcomes) {
  ctrl4_terms <- strsplit(ctrl4, " \\+ ")[[1]]
  cc_nl <- c(y, "ai_dc_per1000_lag1","ai_sq_lag1", ctrl4_terms)
  d_nl  <- dt[complete.cases(dt[, ..cc_nl])]
  m     <- feols(as.formula(paste(y, "~ ai_dc_per1000_lag1 + ai_sq_lag1 +",
                                  ctrl4, "| state + year")),
                 data=d_nl, vcov=~state)
  ct    <- coeftable(m)
  tag   <- sprintf("nonlin_twfe_ai518210sq_lag1_ctrl4_w9901_cl-state_%s_50s2015_2025", y)
  ci1   <- confint(m)["ai_dc_per1000_lag1",]
  ci2   <- confint(m)["ai_sq_lag1",]

  nl_rows[[length(nl_rows)+1]] <- data.table(
    tag=tag, outcome=y, coef="ai_dc_per1000_lag1",
    estimate=as.numeric(ct["ai_dc_per1000_lag1","Estimate"]),
    se=as.numeric(ct["ai_dc_per1000_lag1","Std. Error"]),
    tstat=as.numeric(ct["ai_dc_per1000_lag1","t value"]),
    pval=as.numeric(ct["ai_dc_per1000_lag1","Pr(>|t|)"]),
    ci_lo=as.numeric(ci1[1]), ci_hi=as.numeric(ci1[2]),
    N=m$nobs, within_r2=r2(m,"wr2"),
    vcov_type="CRV1-state", sample="50s2015_2025", controls="ctrl4", status="ok")
  nl_rows[[length(nl_rows)+1]] <- data.table(
    tag=tag, outcome=y, coef="ai_sq_lag1",
    estimate=as.numeric(ct["ai_sq_lag1","Estimate"]),
    se=as.numeric(ct["ai_sq_lag1","Std. Error"]),
    tstat=as.numeric(ct["ai_sq_lag1","t value"]),
    pval=as.numeric(ct["ai_sq_lag1","Pr(>|t|)"]),
    ci_lo=as.numeric(ci2[1]), ci_hi=as.numeric(ci2[2]),
    N=m$nobs, within_r2=r2(m,"wr2"),
    vcov_type="CRV1-state", sample="50s2015_2025", controls="ctrl4", status="ok")

  b1 <- as.numeric(ct["ai_dc_per1000_lag1","Estimate"])
  b2 <- as.numeric(ct["ai_sq_lag1","Estimate"])
  b2_p <- as.numeric(ct["ai_sq_lag1","Pr(>|t|)"])
  V12 <- vcov(m)[c("ai_dc_per1000_lag1","ai_sq_lag1"),
                  c("ai_dc_per1000_lag1","ai_sq_lag1")]
  ai_min <- min(d_nl$ai_dc_per1000_lag1, na.rm=TRUE)
  ai_max <- max(d_nl$ai_dc_per1000_lag1, na.rm=TRUE)
  slope_min <- b1 + 2*b2*ai_min;   slope_max <- b1 + 2*b2*ai_max
  grad <- function(x) c(1, 2*x)
  se_min <- sqrt(as.numeric(t(grad(ai_min)) %*% V12 %*% grad(ai_min)))
  se_max <- sqrt(as.numeric(t(grad(ai_max)) %*% V12 %*% grad(ai_max)))
  t_min <- slope_min/se_min;   t_max <- slope_max/se_max
  lm_inv <- (t_min > 1.645 && t_max < -1.645)
  lm_u   <- (t_min < -1.645 && t_max > 1.645)
  lm_pass <- lm_inv || lm_u
  shape  <- ifelse(lm_inv,"inverted-U", ifelse(lm_u,"U-shape","no curve"))
  cat(sprintf("  %-16s b2=%9.5f p=%.3f  t_min=%5.2f t_max=%5.2f  LM=%s\n",
              y, b2, b2_p, t_min, t_max, ifelse(lm_pass, paste("PASS",shape),"FAIL")))
  lm_rows4[[y]] <- data.table(
    outcome=y, controls="ctrl4", b2=b2,
    b2_se=sqrt(V12["ai_sq_lag1","ai_sq_lag1"]), b2_pval=b2_p,
    ai_min=ai_min, ai_max=ai_max,
    slope_at_min=slope_min, se_slope_min=se_min, t_slope_min=t_min,
    slope_at_max=slope_max, se_slope_max=se_max, t_slope_max=t_max,
    lm_pass=lm_pass, shape=shape,
    t_weaker=ifelse(abs(t_min)<=abs(t_max), t_min, t_max), N=m$nobs)
}
write_append(rbindlist(nl_rows), "nonlinearity.csv")
write_append(rbindlist(lm_rows4), "lm_proper.csv")

# -----------------------------------------------------------------------
# 4. Heterogeneity with ctrl4
# -----------------------------------------------------------------------
cat("\n---- 4. Heterogeneity ctrl4 ----\n")
het_mods <- list(
  list(label="net_exp",    d_col="net_exp_2015_c"),
  list(label="high_price", d_col="high_price_2015_c"),
  list(label="south",      d_col="south_c")
)
het_outcomes <- c("renew_share","ln_ec","ln_ee")
het_rows <- list()

for (y in het_outcomes) {
  for (mod in het_mods) {
    cc_h <- c(y,"ai_lag1_c", mod$d_col, strsplit(ctrl4," \\+ ")[[1]])
    d_h  <- dt[complete.cases(dt[, ..cc_h])]
    fml  <- as.formula(paste(y, "~ ai_lag1_c *", mod$d_col, "+", ctrl4,
                              "| state + year"))
    m_h  <- feols(fml, data=d_h, vcov=~state)
    tag  <- sprintf("het_twfe_ai518210_lag1_%s_ctrl4_w9901_cl-state_%s_50s2015_2025",
                    mod$label, y)
    ct   <- coeftable(m_h)
    r_main <- tidy_row(m_h, tag, y, "CRV1-state","50s2015_2025","ctrl4",
                       coef_name="ai_lag1_c")
    het_rows[[length(het_rows)+1]] <- r_main
    int_name <- paste0("ai_lag1_c:", mod$d_col)
    if (int_name %in% rownames(ct)) {
      r_int <- tidy_row(m_h, tag, y, "CRV1-state","50s2015_2025","ctrl4",
                        coef_name=int_name)
      het_rows[[length(het_rows)+1]] <- r_int
      cat(sprintf("  %-12s x %-12s  γ1=%8.5f p=%.3f\n",
                  y, mod$label, r_int$estimate, r_int$pval))
    }
  }
}
write_append(rbindlist(het_rows, fill=TRUE), "heterogeneity.csv")

# -----------------------------------------------------------------------
# 5. Dynamics — long difference with ctrl4 (drop dtech)
# -----------------------------------------------------------------------
cat("\n---- 5. Long difference ctrl4 ----\n")
y2015ld <- dt[year == 2015, .(state,
  Y15_renew=renew_share, Y15_lnec=ln_ec, Y15_lnee=ln_ee,
  ai_2014=ai_dc_per1000_lag1,
  gdp_15=ln_gdp_pc, price_15=price_c_kwh, manuf_15=manuf_share, pop_15=population)]
y2025ld <- dt[year == 2025, .(state,
  Y25_renew=renew_share, Y25_lnec=ln_ec, Y25_lnee=ln_ee,
  ai_2024=ai_dc_per1000,
  gdp_25=ln_gdp_pc, price_25=price_c_kwh, manuf_25=manuf_share, pop_25=population)]
ld <- merge(y2015ld, y2025ld, by="state")
ld[, drenew:=Y25_renew-Y15_renew]; ld[, dlnec:=Y25_lnec-Y15_lnec]
ld[, dlnee:=Y25_lnee-Y15_lnee];   ld[, dAI:=ai_2024-ai_2014]
ld[, dlngdp:=gdp_25-gdp_15];       ld[, dprice:=price_25-price_15]
ld[, dmanuf:=manuf_25-manuf_15];   ld[, dpop:=log(pop_25/pop_15)]
ld_cc <- ld[complete.cases(ld[,.(drenew,dlnec,dlnee,dAI,dlngdp,dprice,dmanuf,dpop)])]
cat(sprintf("  Long diff N = %d states\n", nrow(ld_cc)))

dyn_rows4 <- list()
for (spec in list(list(y="drenew",out="renew_share"), list(y="dlnec",out="ln_ec"),
                  list(y="dlnee",out="ln_ee"))) {
  m_ld <- lm(as.formula(paste(spec$y,"~ dAI + dlngdp + dprice + dmanuf + dpop")),
             data=ld_cc)
  ct <- summary(m_ld)$coefficients
  ci_ld <- confint(m_ld)
  r <- data.table(tag=sprintf("dyn_longdiff_ai518210_ctrl4_w9901_rob_%s_50s2015_2025",spec$out),
    outcome=spec$out, coef="dAI",
    estimate=ct["dAI","Estimate"], se=ct["dAI","Std. Error"],
    tstat=ct["dAI","t value"], pval=ct["dAI","Pr(>|t|)"],
    ci_lo=ci_ld["dAI",1], ci_hi=ci_ld["dAI",2],
    N=nrow(ld_cc), within_r2=summary(m_ld)$r.squared,
    vcov_type="HC0", sample="50s2015_2025_longdiff", controls="delta_ctrl4",
    lag_k=NA_integer_, status="ok")
  dyn_rows4[[spec$out]] <- r
  cat(sprintf("  %-12s  b=%8.5f p=%.3f\n", spec$out, r$estimate, r$pval))
}
write_append(rbindlist(dyn_rows4, fill=TRUE), "dynamics.csv")

# -----------------------------------------------------------------------
# 6. new_renew_mw robustness with ctrl4
# -----------------------------------------------------------------------
cat("\n---- 6. new_renew_mw robustness ctrl4 ----\n")

anchors <- dt[year==2015, .(state, cap_total_2015=cap_total_mw, pop_2015=population)]
dt4r  <- merge(dt,    anchors, by="state", all.x=TRUE)
dt4r_nw <- merge(dt_nw, anchors, by="state", all.x=TRUE)
dt4r[, new_renew_per_1000mw := new_renew_mw / cap_total_2015 * 1000]
dt4r[, new_renew_per_mpop   := new_renew_mw / (pop_2015 / 1e6)]

rob4 <- list()

# Scaled: per 1,000 MW 2015 capacity
cc_a <- c("new_renew_per_1000mw", cc4)
d_a  <- dt4r[complete.cases(dt4r[, ..cc_a])]
cat(sprintf("  Per 1,000 MW: N=%d\n", nrow(d_a)))
m_a  <- feols(as.formula(paste("new_renew_per_1000mw ~ ai_dc_per1000_lag1 +",
               ctrl4, "| state + year")), data=d_a, vcov=~state)
rob4[[1]] <- tidy_row(m_a,
  "h1x_rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per1000mw_50s2015_2025",
  "new_renew_per_1000mw","CRV1-state","50s2015_2025","ctrl4")
cat(sprintf("    a1=%.3f  p=%.3f\n", rob4[[1]]$estimate, rob4[[1]]$pval))

# Scaled: per million people (2015 pop)
cc_b <- c("new_renew_per_mpop", cc4)
d_b  <- dt4r[complete.cases(dt4r[, ..cc_b])]
cat(sprintf("  Per mpop:     N=%d\n", nrow(d_b)))
m_b  <- feols(as.formula(paste("new_renew_per_mpop ~ ai_dc_per1000_lag1 +",
               ctrl4, "| state + year")), data=d_b, vcov=~state)
rob4[[2]] <- tidy_row(m_b,
  "h1x_rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_per_mpop_50s2015_2025",
  "new_renew_per_mpop","CRV1-state","50s2015_2025","ctrl4")
cat(sprintf("    a1=%.3f  p=%.3f\n", rob4[[2]]$estimate, rob4[[2]]$pval))

# Drop TX
cc_c <- c("new_renew_mw", cc4)
d_c  <- dt[state != "TX" & complete.cases(dt[, ..cc_c])]
cat(sprintf("  Drop TX:      N=%d (expected 539)\n", nrow(d_c)))
if (nrow(d_c) != 539) cat(sprintf("  *** N mismatch: %d\n", nrow(d_c)))
m_c  <- feols(as.formula(paste("new_renew_mw ~ ai_dc_per1000_lag1 +",
               ctrl4, "| state + year")), data=d_c, vcov=~state)
rob4[[3]] <- tidy_row(m_c,
  "h1x_rob_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_49snoTX2015_2025",
  "new_renew_mw","CRV1-state","49snoTX2015_2025","ctrl4")
cat(sprintf("    a1=%.1f  se=%.1f  p=%.3f\n",
    rob4[[3]]$estimate, rob4[[3]]$se, rob4[[3]]$pval))

# LOSO
cat("  LOSO:\n")
d_full <- dt[complete.cases(dt[, ..cc_c])]
states_all <- sort(unique(dt$state))
loso4 <- setNames(numeric(length(states_all)), states_all)
loso4_n <- setNames(integer(length(states_all)), states_all)
for (s in states_all) {
  d_s <- d_full[state != s]
  loso4_n[s] <- nrow(d_s)
  if (loso4_n[s] != 539) cat(sprintf("  WARNING: drop %s N=%d\n", s, loso4_n[s]))
  m_s <- feols(as.formula(paste("new_renew_mw ~ ai_dc_per1000_lag1 +",
                ctrl4, "| state + year")), data=d_s, vcov=~state,
               warn=FALSE, notes=FALSE)
  loso4[s] <- coef(m_s)["ai_dc_per1000_lag1"]
}
loso_min_s <- names(which.min(loso4)); loso_max_s <- names(which.max(loso4))
cat(sprintf("    min: %.1f (drop %s)\n", min(loso4), loso_min_s))
cat(sprintf("    max: %.1f (drop %s)\n", max(loso4), loso_max_s))
cat(sprintf("    mean: %.1f  SD: %.1f\n", mean(loso4), sd(loso4)))
rob4[[4]] <- data.table(
  tag="h1x_loso_twfe_ai518210_lag1_ctrl4_w9901_cl-state_new_renew_mw_50s2015_2025",
  outcome="new_renew_mw", coef="ai_dc_per1000_lag1",
  estimate=mean(loso4), se=sd(loso4), tstat=NA_real_, pval=NA_real_,
  ci_lo=min(loso4), ci_hi=max(loso4), N=NA_integer_, within_r2=NA_real_,
  vcov_type="LOSO", sample="50s2015_2025", controls="ctrl4",
  status=sprintf("min=%s(%.1f),max=%s(%.1f)", loso_min_s, min(loso4), loso_max_s, max(loso4)))
write_append(rbindlist(rob4, fill=TRUE), "h1_extras.csv")

# -----------------------------------------------------------------------
# 7. Generation channels with ctrl4
# -----------------------------------------------------------------------
cat("\n---- 7. Generation channels ctrl4 ----\n")
dt[, ln_renew_mwh  := log(gen_renew_mwh)]
dt[, ln_fossil_mwh := log(gen_fossil_mwh)]
dt[, ln_total_mwh  := log(gen_total_mwh)]

gen4 <- list()
for (y in c("ln_renew_mwh","ln_fossil_mwh","ln_total_mwh")) {
  cc_g <- c(y, cc4)
  d_g  <- dt[complete.cases(dt[, ..cc_g])]
  m_g  <- feols(as.formula(paste(y,"~ ai_dc_per1000_lag1 +",ctrl4,"| state + year")),
                data=d_g, vcov=~state)
  tag  <- sprintf("h1x_twfe_ai518210_lag1_ctrl4_w9901_cl-state_%s_50s2015_2025", y)
  gen4[[y]] <- tidy_row(m_g, tag, y, "CRV1-state","50s2015_2025","ctrl4")
  cat(sprintf("  %-18s a1=%9.5f  se=%8.5f  p=%.3f  N=%d\n",
      y, gen4[[y]]$estimate, gen4[[y]]$se, gen4[[y]]$pval, gen4[[y]]$N))
}
write_append(rbindlist(gen4), "h1_extras.csv")

# -----------------------------------------------------------------------
# 8. Rebuild modelsummary table and coefficient plot (ctrl4 baseline)
# -----------------------------------------------------------------------
cat("\n---- 8. Rebuild table and figure (ctrl4) ----\n")

# Load current result rows
h1c <- fread(file.path(OUT, "h1_core.csv"))
h1e <- fread(file.path(OUT, "h1_extras.csv"))

# ctrl4 main rows for each unique outcome (excluding rob/loso/per1000/per_mpop/raw/gen channels)
skip_pat <- "rob|loso|per1000|per_mpop|new_renew_mw_raw|ln_renew|ln_fossil|ln_total|unwinsorized"
core4 <- h1c[controls=="ctrl4" & vcov_type=="CRV1-state"]
ext4  <- h1e[grepl("ctrl4", controls) &
              vcov_type == "CRV1-state" &
              !grepl(skip_pat, tag)]

fig_data <- rbind(
  core4[, .(outcome, estimate, ci_lo, ci_hi)],
  ext4[ , .(outcome, estimate, ci_lo, ci_hi)]
)
fig_data <- fig_data[!duplicated(outcome)]

outcome_order <- c("ln_ec","ln_ee","renew_share","solar_share","wind_share",
                   "new_renew_mw","fossil_to_renew","coal_share","co2_per_mwh_t")
outcome_labels <- c(
  ln_ec="ln(MWh/person)", ln_ee="ln(GDP/MWh)", renew_share="Renew share",
  solar_share="Solar share", wind_share="Wind share",
  new_renew_mw="New renew MW", fossil_to_renew="Fossil/renew ratio",
  coal_share="Coal share (falsi.)", co2_per_mwh_t="CO₂/MWh"
)

fig_data <- fig_data[outcome %in% outcome_order]
fig_data[, outcome_f := factor(outcome, levels=rev(outcome_order),
                                labels=rev(outcome_labels[outcome_order]))]
fig_data[, color := ifelse(ci_lo > 0, "positive",
                    ifelse(ci_hi < 0, "negative", "null"))]

p <- ggplot(as.data.frame(fig_data), aes(x=estimate, y=outcome_f,
       xmin=ci_lo, xmax=ci_hi, color=color)) +
  geom_vline(xintercept=0, linetype="dashed", color="grey60") +
  geom_pointrange(size=0.45, linewidth=0.7) +
  scale_color_manual(values=c(positive="steelblue3", negative="tomato3", null="grey40"),
                     guide="none") +
  labs(x="Coefficient on lagged AI (ctrl4 = memo spec, clustered SE)",
       y=NULL,
       title="H1: AI data-center concentration and energy outcomes",
       subtitle="ctrl4: ln_gdp_pc + manuf_share + price_c_kwh + pop_growth") +
  theme_bw(base_size=11)

ggsave(file.path(FIGS, "h1_coef_plot_ctrl4.pdf"), p, width=7, height=5)
ggsave(file.path(FIGS, "h1_coef_plot_ctrl4.png"), p, width=7, height=5, dpi=150)

# Print summary table to console
cat("\n=== ctrl4 summary table ===\n")
all4 <- rbind(core4[, .(outcome, estimate, se, pval, N, controls)],
              ext4[, .(outcome, estimate, se, pval, N, controls)],
              fill=TRUE)
all4 <- all4[!duplicated(outcome)]
setorder(all4, outcome)
print(all4[, .(outcome, estimate=round(estimate,5), se=round(se,5),
               pval=round(pval,3), N)])

cat("\nSaved h1_coef_plot_ctrl4.pdf/.png\n")
cat("=== ctrl4 rerun complete ===\n")

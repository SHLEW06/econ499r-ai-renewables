#!/usr/bin/env Rscript
# 04c_step2_mediation.R
# Phase 4c: H2a/H2b mediation (tech_share [main], hma [memo], ln_ea [H2b])
# Three Baron-Kenny equations per (mediator, outcome).
# Indirect effect: Sobel z + cluster bootstrap (999 reps, seed=42) + share mediated.
# Controls: ctrl4 = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth (H1 baseline).
# NOTE: EXPERIMENTS.md §6/§7 tags said "ctrl5"; corrected to ctrl4 here and in
#       EXPERIMENTS.md — ctrl4 is the H1 baseline and keeps X consistent across steps.
# Usage: Rscript code/R/04c_step2_mediation.R --date 2026-11-03

suppressPackageStartupMessages({
  library(fixest)
  library(data.table)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = TRUE)
date_arg <- NULL
for (i in seq_along(args)) {
  if (args[i] == "--date" && i < length(args)) date_arg <- args[i + 1]
}
if (is.null(date_arg)) stop("--date YYYY-MM-DD required")

OUT    <- file.path("results", date_arg, "h2")
TABLES <- file.path("results", date_arg, "tables")
FIGS   <- file.path("results", date_arg, "figures")
for (d in c(OUT, TABLES, FIGS)) dir.create(d, recursive = TRUE, showWarnings = FALSE)

source("code/R/load_panel.R")
res <- load_panel()
dt  <- res$panel
cat(sprintf("Panel loaded: %d rows x %d cols\n", nrow(dt), ncol(dt)))

# ---- Fail-fast checks -------------------------------------------------------
required_cols <- c("tech_share", "hma", "ln_ea",
                   "ai_dc_per1000_lag1", "ln_ec", "ln_ee", "renew_share",
                   "ln_gdp_pc", "manuf_share", "price_c_kwh", "pop_growth",
                   "state", "year")
missing_cols <- setdiff(required_cols, names(dt))
if (length(missing_cols) > 0) stop("Missing columns: ", paste(missing_cols, collapse=", "))

# ---- Load H1 a1 for share-mediated calculation ------------------------------
h1_path <- file.path("results", "2026-11-02", "h1", "h1_core.csv")
if (!file.exists(h1_path)) stop("H1 core results not found: ", h1_path)
h1_core <- fread(h1_path)
a1_tbl  <- h1_core[controls == "ctrl4" & vcov_type == "CRV1-state",
                    .(outcome, a1 = estimate)]
cat("\na1 values loaded from H1 ctrl4 CL baseline:\n")
print(a1_tbl)

# ---- Mean-center tech_share -------------------------------------------------
tech_mean <- mean(dt$tech_share, na.rm = TRUE)
dt[, tech_share_c := tech_share - tech_mean]
cat(sprintf("\ntech_share mean-centered: mean=%.6f  SD=%.6f  (subtracted from raw)\n",
            tech_mean, sd(dt$tech_share, na.rm = TRUE)))

ctrl4 <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"
cc4   <- c("ai_dc_per1000_lag1", "ln_gdp_pc", "manuf_share", "price_c_kwh", "pop_growth")
outcomes <- c("ln_ec", "ln_ee", "renew_share")

# ---- Helpers ----------------------------------------------------------------
tidy_row <- function(m, tag, outcome, mediator, equation, coef_name) {
  ct <- coeftable(m)
  if (!coef_name %in% rownames(ct))
    return(data.table(tag=tag, outcome=outcome, mediator=mediator, equation=equation,
                      coef=coef_name, estimate=NA_real_, se=NA_real_, tstat=NA_real_,
                      pval=NA_real_, ci_lo=NA_real_, ci_hi=NA_real_,
                      N=m$nobs, within_r2=NA_real_, vcov_type="CRV1-state",
                      sample="50s2015_2025", controls="ctrl4", status="COEF_MISSING"))
  row <- ct[coef_name, ]
  ci  <- confint(m)[coef_name, ]
  data.table(tag=tag, outcome=outcome, mediator=mediator, equation=equation,
             coef=coef_name,
             estimate = as.numeric(row[["Estimate"]]),
             se       = as.numeric(row[["Std. Error"]]),
             tstat    = as.numeric(row[["t value"]]),
             pval     = as.numeric(row[["Pr(>|t|)"]]),
             ci_lo    = as.numeric(ci[1]),
             ci_hi    = as.numeric(ci[2]),
             N = m$nobs, within_r2 = r2(m, "wr2"),
             vcov_type = "CRV1-state", sample = "50s2015_2025",
             controls = "ctrl4", status = "ok")
}

cluster_bootstrap_indirect <- function(d, M_col, Y_col, ctrl4_str,
                                        n_reps = 999, seed = 42) {
  set.seed(seed)
  states      <- unique(d$state)
  n_states    <- length(states)
  boot_vals   <- numeric(n_reps)
  n_failed    <- 0L

  for (r in seq_len(n_reps)) {
    sampled <- sample(states, n_states, replace = TRUE)
    boot_dt <- rbindlist(lapply(seq_along(sampled), function(k) {
      sub <- d[state == sampled[k]]
      sub[, .boot_clust := paste0(state, "_", k)]
      sub
    }))
    tryCatch({
      ma <- feols(as.formula(paste(M_col, "~ ai_dc_per1000_lag1 +", ctrl4_str,
                                    "| state + year")),
                  data = boot_dt, vcov = ~.boot_clust, warn = FALSE, notes = FALSE)
      mc <- feols(as.formula(paste(Y_col, "~", M_col, "+ ai_dc_per1000_lag1 +",
                                    ctrl4_str, "| state + year")),
                  data = boot_dt, vcov = ~.boot_clust, warn = FALSE, notes = FALSE)
      boot_vals[r] <- coef(ma)["ai_dc_per1000_lag1"] * coef(mc)[M_col]
    }, error = function(e) {
      n_failed <<- n_failed + 1L
      boot_vals[r] <<- NA_real_
    })
  }
  valid <- boot_vals[!is.na(boot_vals)]
  ci    <- quantile(valid, c(0.025, 0.975), na.rm = TRUE)
  list(ci_lo = as.numeric(ci[1]), ci_hi = as.numeric(ci[2]),
       n_valid = length(valid), n_failed = n_failed)
}

# ---- Mediators definition ---------------------------------------------------
mediators <- list(
  list(label    = "tech_share_c",
       col      = "tech_share_c",
       tag_id   = "M-techshare",
       h_block  = "h2a",
       display  = "tech_share (mean-centered)",
       note     = "Main H2a mediator. tech_share mean-centered (mean subtracted)."),
  list(label    = "hma",
       col      = "hma",
       tag_id   = "M-hma",
       h_block  = "h2a",
       display  = "hma",
       note     = "Memo version. CAUTION: b1>0 is mechanical — HMA is built as AI x tech_share."),
  list(label    = "ln_ea",
       col      = "ln_ea",
       tag_id   = "M-lnea",
       h_block  = "h2b",
       display  = "ln_ea",
       note     = "H2b. CAVEAT: ln_ea nearly redundant under state FE (within-state variation = nonfarm GDP growth).")
)

# ---- Main loop: mediators x outcomes ----------------------------------------
all_rows    <- list()
summary_tbl <- list()   # for path diagram data

for (med in mediators) {
  M <- med$col
  cat(sprintf("\n=== Mediator: %s ===\n", med$display))
  cat(sprintf("    Note: %s\n", med$note))

  med_summary <- list()

  for (Y in outcomes) {
    cat(sprintf("  --- Outcome: %s ---\n", Y))

    cc_use <- unique(c(Y, M, cc4))
    d_cc   <- dt[complete.cases(dt[, ..cc_use])]
    n_cc   <- nrow(d_cc)

    tag_base <- sprintf("%s_med_ai518210_lag1_%s_ctrl4_w9901_cl-state_%s_50s2015_2025",
                        med$h_block, med$tag_id, Y)

    # (a) First stage: M = b1*AI(t-1) + ctrl4 + FE
    m_a <- feols(as.formula(paste(M, "~ ai_dc_per1000_lag1 +", ctrl4, "| state + year")),
                 data = d_cc, vcov = ~state)
    r_a <- tidy_row(m_a, paste0(tag_base, "_eq-a"), Y, med$label, "eq-a",
                    "ai_dc_per1000_lag1")
    b1    <- r_a$estimate
    SE_b1 <- r_a$se
    cat(sprintf("    (a) b1=%.6f  SE=%.6f  p=%.3f  N=%d\n", b1, SE_b1, r_a$pval, r_a$N))
    all_rows[[length(all_rows)+1]] <- r_a

    # (b) Reduced form: Y = c1*M + ctrl4 + FE
    m_b <- feols(as.formula(paste(Y, "~", M, "+", ctrl4, "| state + year")),
                 data = d_cc, vcov = ~state)
    r_b <- tidy_row(m_b, paste0(tag_base, "_eq-b"), Y, med$label, "eq-b", M)
    c1    <- r_b$estimate
    SE_c1 <- r_b$se
    cat(sprintf("    (b) c1=%.6f  SE=%.6f  p=%.3f\n", c1, SE_c1, r_b$pval))
    all_rows[[length(all_rows)+1]] <- r_b

    # (c) Direct effect: Y = e1*M + e2*AI(t-1) + ctrl4 + FE
    m_c <- feols(as.formula(paste(Y, "~", M, "+ ai_dc_per1000_lag1 +",
                                   ctrl4, "| state + year")),
                 data = d_cc, vcov = ~state)
    r_cM  <- tidy_row(m_c, paste0(tag_base, "_eq-c"), Y, med$label, "eq-c", M)
    r_cAI <- tidy_row(m_c, paste0(tag_base, "_eq-c"), Y, med$label, "eq-c",
                      "ai_dc_per1000_lag1")
    e1    <- r_cM$estimate
    SE_e1 <- r_cM$se
    e2    <- r_cAI$estimate
    cat(sprintf("    (c) e1=%.6f  p=%.3f  |  e2(AI direct)=%.6f  p=%.3f\n",
                e1, r_cM$pval, e2, r_cAI$pval))
    all_rows[[length(all_rows)+1]] <- r_cM
    all_rows[[length(all_rows)+1]] <- r_cAI

    # ---- Channel check (paper rule) -----------------------------------------
    channel_holds <- (r_a$pval < 0.05 && r_b$pval < 0.05 && r_cM$pval < 0.05)
    cat(sprintf("    Channel holds (b1 & c1 & e1 all p<0.05): %s\n",
                ifelse(channel_holds, "YES", "no")))

    # ---- Indirect effect ----------------------------------------------------
    indirect <- b1 * e1

    # Sobel z
    sobel_se <- sqrt(e1^2 * SE_b1^2 + b1^2 * SE_e1^2)
    sobel_z  <- if (sobel_se > 0) indirect / sobel_se else NA_real_
    sobel_p  <- if (!is.na(sobel_z)) 2 * pnorm(-abs(sobel_z)) else NA_real_
    cat(sprintf("    Sobel: indirect=%.7f  z=%.3f  p=%.3f\n",
                indirect, sobel_z, sobel_p))

    # Cluster bootstrap
    cat(sprintf("    Bootstrap (999 reps, seed=42)..."))
    boot <- cluster_bootstrap_indirect(d_cc, M, Y, ctrl4)
    cat(sprintf(" CI=[%.6f, %.6f]  (valid=%d, failed=%d)\n",
                boot$ci_lo, boot$ci_hi, boot$n_valid, boot$n_failed))

    # Share mediated
    a1_val    <- a1_tbl[outcome == Y, a1]
    share_med <- if (length(a1_val) == 1 && !is.na(a1_val) && a1_val != 0)
                   indirect / a1_val else NA_real_

    # ---- Write indirect rows ------------------------------------------------
    all_rows[[length(all_rows)+1]] <- data.table(
      tag = paste0(tag_base, "_indirect-sobel"),
      outcome=Y, mediator=med$label, equation="indirect",
      coef="b1_x_e1",
      estimate=indirect, se=sobel_se, tstat=sobel_z, pval=sobel_p,
      ci_lo=NA_real_, ci_hi=NA_real_,
      N=n_cc, within_r2=NA_real_,
      vcov_type="Sobel", sample="50s2015_2025", controls="ctrl4", status="ok")

    all_rows[[length(all_rows)+1]] <- data.table(
      tag = paste0(tag_base, "_indirect-bootstrap"),
      outcome=Y, mediator=med$label, equation="indirect",
      coef="b1_x_e1",
      estimate=indirect, se=NA_real_, tstat=NA_real_, pval=NA_real_,
      ci_lo=boot$ci_lo, ci_hi=boot$ci_hi,
      N=n_cc, within_r2=NA_real_,
      vcov_type=sprintf("bootstrap-cl-state-%dreps-seed42", boot$n_valid),
      sample="50s2015_2025", controls="ctrl4",
      status=sprintf("n_valid=%d,n_failed=%d", boot$n_valid, boot$n_failed))

    all_rows[[length(all_rows)+1]] <- data.table(
      tag = paste0(tag_base, "_share-mediated"),
      outcome=Y, mediator=med$label, equation="indirect",
      coef="b1xe1_over_a1",
      estimate=share_med, se=NA_real_, tstat=NA_real_, pval=NA_real_,
      ci_lo=NA_real_, ci_hi=NA_real_,
      N=n_cc, within_r2=NA_real_,
      vcov_type="share_mediated", sample="50s2015_2025", controls="ctrl4",
      status=sprintf("a1=%.7f", ifelse(length(a1_val)==1, a1_val, NA)))

    # ---- Accumulate summary for table/diagram --------------------------------
    med_summary[[Y]] <- list(
      outcome=Y, b1=b1, b1_se=SE_b1, b1_p=r_a$pval,
      c1=c1, c1_se=SE_c1, c1_p=r_b$pval,
      e1=e1, e1_se=SE_e1, e1_p=r_cM$pval,
      e2=e2, e2_se=r_cAI$se, e2_p=r_cAI$pval,
      indirect=indirect, sobel_z=sobel_z, sobel_p=sobel_p,
      boot_ci_lo=boot$ci_lo, boot_ci_hi=boot$ci_hi,
      share_med=share_med, N=n_cc, channel=channel_holds)
  }
  summary_tbl[[med$label]] <- med_summary
}

# ---- Write h2_results.csv ---------------------------------------------------
results_dt <- rbindlist(all_rows, fill = TRUE)
fwrite(results_dt, file.path(OUT, "h2_results.csv"))
cat(sprintf("\nWrote %d rows to %s\n", nrow(results_dt), file.path(OUT, "h2_results.csv")))

# ---- ln_ea redundancy check -------------------------------------------------
cat("\n=== ln_ea redundancy check ===\n")
ea_vars <- c("ln_ea", "ln_gdp_pc", "pop_growth")
dt_ea   <- dt[complete.cases(dt[, ..ea_vars])]
dt_ea[, ln_ea_w    := ln_ea    - mean(ln_ea,    na.rm=TRUE), by=state]
dt_ea[, ln_gdp_w   := ln_gdp_pc - mean(ln_gdp_pc, na.rm=TRUE), by=state]
dt_ea[, pop_grow_w := pop_growth - mean(pop_growth, na.rm=TRUE), by=state]
cor_ea_gdp <- cor(dt_ea$ln_ea_w, dt_ea$ln_gdp_w,   use="complete.obs")
cor_ea_pop <- cor(dt_ea$ln_ea_w, dt_ea$pop_grow_w, use="complete.obs")
cat(sprintf("  Within-state cor(ln_ea, ln_gdp_pc): %.3f\n", cor_ea_gdp))
cat(sprintf("  Within-state cor(ln_ea, pop_growth): %.3f\n", cor_ea_pop))
cat("  Interpretation: if |r| > 0.85, ln_ea is nearly redundant under state FE.\n")

# Save redundancy check
fwrite(data.table(
  check = c("cor_ln_ea_ln_gdp_pc_within", "cor_ln_ea_pop_growth_within"),
  value = c(cor_ea_gdp, cor_ea_pop),
  note  = c("within-state correlation", "within-state correlation")
), file.path(OUT, "ln_ea_redundancy.csv"))

# ---- Summary tables per mediator -------------------------------------------
make_table <- function(med_label, med_summary, tables_dir) {
  outcomes_ord <- c("ln_ec", "ln_ee", "renew_share")

  rows <- list(
    list(stat="b1 (AI→M)",       fn=function(s) sprintf("%.5f",  s$b1)),
    list(stat="SE(b1)",          fn=function(s) sprintf("(%.5f)", s$b1_se)),
    list(stat="p(b1)",           fn=function(s) sprintf("%.3f",   s$b1_p)),
    list(stat="c1 (M→Y, eq-b)", fn=function(s) sprintf("%.5f",  s$c1)),
    list(stat="SE(c1)",          fn=function(s) sprintf("(%.5f)", s$c1_se)),
    list(stat="p(c1)",           fn=function(s) sprintf("%.3f",   s$c1_p)),
    list(stat="e1 (M→Y, eq-c)", fn=function(s) sprintf("%.5f",  s$e1)),
    list(stat="SE(e1)",          fn=function(s) sprintf("(%.5f)", s$e1_se)),
    list(stat="p(e1)",           fn=function(s) sprintf("%.3f",   s$e1_p)),
    list(stat="e2 (AI direct)", fn=function(s) sprintf("%.5f",  s$e2)),
    list(stat="p(e2)",           fn=function(s) sprintf("%.3f",   s$e2_p)),
    list(stat="Indirect b1xe1",  fn=function(s) sprintf("%.7f",  s$indirect)),
    list(stat="Sobel p",         fn=function(s) sprintf("%.3f",   s$sobel_p)),
    list(stat="Bootstrap 95% CI",fn=function(s) sprintf("[%.5f, %.5f]",
                                                          s$boot_ci_lo, s$boot_ci_hi)),
    list(stat="Share mediated",  fn=function(s) if (!is.na(s$share_med))
                                   sprintf("%.3f", s$share_med) else "NA"),
    list(stat="Channel holds",   fn=function(s) if (s$channel) "YES" else "no"),
    list(stat="N",               fn=function(s) as.character(s$N))
  )

  tbl <- data.table(Statistic = sapply(rows, `[[`, "stat"))
  for (Y in outcomes_ord) {
    if (Y %in% names(med_summary)) {
      s <- med_summary[[Y]]
      tbl[, (Y) := sapply(rows, function(r) r$fn(s))]
    } else {
      tbl[, (Y) := NA_character_]
    }
  }

  fname <- file.path(tables_dir, sprintf("h2_%s.csv",
                       gsub("[^a-z0-9]", "_", tolower(med_label))))
  fwrite(tbl, fname)

  # LaTeX
  tex_fname <- sub("\\.csv$", ".tex", fname)
  tex_lines <- c(
    "\\begin{table}[htbp]",
    "\\centering",
    sprintf("\\caption{Mediation results: M = %s}", med_label),
    "\\begin{tabular}{lccc}",
    "\\toprule",
    "Statistic & ln\\_ec & ln\\_ee & renew\\_share \\\\",
    "\\midrule"
  )
  for (i in seq_len(nrow(tbl))) {
    row_str <- paste(
      tbl[i, Statistic],
      tbl[i, ln_ec],
      tbl[i, ln_ee],
      tbl[i, renew_share],
      sep = " & "
    )
    # add midrule before N
    if (tbl[i, Statistic] == "N") tex_lines <- c(tex_lines, "\\midrule")
    tex_lines <- c(tex_lines, paste0(row_str, " \\\\"))
  }
  tex_lines <- c(tex_lines,
    "\\bottomrule",
    "\\end{tabular}",
    sprintf("\\label{tab:h2_%s}", gsub("[^a-z0-9]", "_", tolower(med_label))),
    "\\end{table}")
  writeLines(tex_lines, tex_fname)
  cat(sprintf("  Table: %s + .tex\n", fname))
}

cat("\n=== Writing tables ===\n")
for (med in mediators) {
  make_table(med$display, summary_tbl[[med$label]], TABLES)
}

# ---- PROVENANCE.md ----------------------------------------------------------
prov_lines <- c(
  "# PROVENANCE — H2 tables",
  sprintf("Generated: %s", date_arg),
  sprintf("Script: code/R/04c_step2_mediation.R --date %s", date_arg),
  "Panel: data/out/state_panel_2015_2025.csv (via load_panel.R)",
  "H1 a1 source: results/2026-11-02/h1/h1_core.csv (ctrl4, CRV1-state rows)",
  "Controls: ctrl4 = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth",
  "SE: clustered by state (CRV1) for all three equations",
  "Bootstrap: 999 reps, seed=42, cluster-by-state (pairs cluster bootstrap)",
  "tech_share: mean-centered (grand mean subtracted)",
  "Equations: (a) M ~ AI + ctrl4 + FE; (b) Y ~ M + ctrl4 + FE; (c) Y ~ M + AI + ctrl4 + FE"
)
writeLines(prov_lines, file.path(TABLES, "PROVENANCE.md"))

# ---- Path diagrams ----------------------------------------------------------
outcome_labels <- c(ln_ec = "ln(MWh/person)", ln_ee = "ln(GDP/MWh)",
                    renew_share = "Renew share")

make_path_diagram <- function(med_label, med_display, med_summary, fig_dir) {
  # Build per-outcome rows
  pd <- rbindlist(lapply(outcomes, function(Y) {
    s <- med_summary[[Y]]
    data.table(
      outcome_f = outcome_labels[Y],
      b1 = s$b1, b1_p = s$b1_p,
      e1 = s$e1, e1_p = s$e1_p,
      indirect = s$indirect,
      boot_lo = s$boot_ci_lo, boot_hi = s$boot_ci_hi,
      sobel_p = s$sobel_p
    )
  }))
  pd[, outcome_f := factor(outcome_f, levels = outcome_labels[outcomes])]

  stars <- function(p) ifelse(p < 0.001, "***", ifelse(p < 0.01, "**",
                        ifelse(p < 0.05, "*", "")))

  # Node positions: AI=0, M=2, Y=4 on x; y=0
  # One panel per outcome (facet)
  node_data <- pd[, .(
    x     = c(0,   2,   4),
    y     = c(0,   0,   0),
    label = c("AI(t-1)", med_label, as.character(outcome_f))
  ), by = outcome_f]

  edge_data <- pd[, .(
    x    = c(0.45, 2.45),
    xend = c(1.55, 3.55),
    y    = c(0.0,  0.0),
    yend = c(0.0,  0.0)
  ), by = outcome_f]

  label_data <- pd[, .(
    x     = c(1.0, 3.0),
    y     = c(0.18, 0.18),
    label = c(
      sprintf("b1=%.4f%s", b1, stars(b1_p)),
      sprintf("e1=%.4f%s", e1, stars(e1_p))
    )
  ), by = outcome_f]

  indir_data <- pd[, .(
    x = 2, y = -0.28,
    label = sprintf("ind=%.5f\nSobel p=%.3f\nCI=[%.5f,%.5f]",
                    indirect, sobel_p, boot_lo, boot_hi)
  ), by = outcome_f]

  p <- ggplot() +
    geom_segment(data = as.data.frame(edge_data),
                 aes(x=x, xend=xend, y=y, yend=yend),
                 arrow = arrow(length=unit(0.18,"cm"), type="closed"),
                 linewidth = 0.7, color = "grey30") +
    geom_label(data = as.data.frame(node_data),
               aes(x=x, y=y, label=label),
               size = 2.8, label.padding = unit(0.25, "lines"),
               fill = "white", color = "black") +
    geom_text(data = as.data.frame(label_data),
              aes(x=x, y=y, label=label),
              size = 2.6, color = "steelblue4") +
    geom_text(data = as.data.frame(indir_data),
              aes(x=x, y=y, label=label),
              size = 2.3, color = "grey40", lineheight = 1.1) +
    facet_wrap(~outcome_f, ncol = 3) +
    coord_cartesian(xlim = c(-0.7, 4.7), ylim = c(-0.55, 0.4)) +
    labs(title = sprintf("Mediation path: AI(t-1) → %s → Y", med_label),
         caption = "* p<0.05  ** p<0.01  *** p<0.001  (clustered by state)\nind = indirect effect b1×e1; CI = bootstrap 95%") +
    theme_void(base_size = 10) +
    theme(strip.text      = element_text(size = 9, face = "bold"),
          plot.title      = element_text(size = 11, hjust = 0.5),
          plot.caption    = element_text(size = 7, color = "grey50", hjust = 0),
          panel.spacing   = unit(1.5, "lines"),
          plot.margin     = margin(8, 8, 8, 8))

  base  <- file.path(fig_dir, sprintf("h2_path_%s",
                       gsub("[^a-z0-9]", "_", tolower(med_label))))
  ggsave(paste0(base, ".pdf"), p, width = 11, height = 4)
  ggsave(paste0(base, ".png"), p, width = 11, height = 4, dpi = 150)
  cat(sprintf("  Path diagram: %s.pdf/.png\n", base))
}

cat("\n=== Generating path diagrams ===\n")
for (med in mediators) {
  make_path_diagram(med$label, med$display, summary_tbl[[med$label]], FIGS)
}

# ---- RECEIPT.md -------------------------------------------------------------
receipt_lines <- c(
  "# RECEIPT — Phase 4c mediation",
  sprintf("Date: %s", date_arg),
  sprintf("Script: code/R/04c_step2_mediation.R --date %s", date_arg),
  "",
  "## Inputs",
  "  data/out/state_panel_2015_2025.csv (via load_panel.R)",
  "  results/2026-11-02/h1/h1_core.csv (a1 values for share-mediated)",
  "",
  "## Outputs",
  sprintf("  %s/h2_results.csv", OUT),
  sprintf("  %s/ln_ea_redundancy.csv", OUT),
  sprintf("  %s/h2_tech_share_c.csv + .tex", TABLES),
  sprintf("  %s/h2_hma.csv + .tex", TABLES),
  sprintf("  %s/h2_ln_ea.csv + .tex", TABLES),
  sprintf("  %s/PROVENANCE.md", TABLES),
  sprintf("  %s/h2_path_*.pdf + .png (3 diagrams)", FIGS),
  "",
  "## Sample",
  "  N = 550 (50 states, 2015-2025, DC dropped, lag1 complete cases)",
  "  tech_share: mean-centered; hma, ln_ea: as-is from panel",
  "",
  "## Controls",
  "  ctrl4 = ln_gdp_pc + manuf_share + price_c_kwh + pop_growth",
  "  (H1 baseline; EXPERIMENTS.md §6/§7 tags corrected from ctrl5 to ctrl4)",
  "",
  "## Bootstrap",
  "  999 reps (pairs cluster bootstrap, resample by state), seed=42",
  sprintf("  a1 values used for share-mediated: ln_ec=%s  ln_ee=%s  renew_share=%s",
          sprintf("%.7f", a1_tbl[outcome=="ln_ec",    a1]),
          sprintf("%.7f", a1_tbl[outcome=="ln_ee",    a1]),
          sprintf("%.7f", a1_tbl[outcome=="renew_share", a1]))
)
writeLines(receipt_lines, file.path(OUT, "RECEIPT.md"))

cat(sprintf("\n=== Phase 4c complete. Results in results/%s/h2/ ===\n", date_arg))

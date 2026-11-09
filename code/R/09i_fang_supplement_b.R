#!/usr/bin/env Rscript
# 09i_fang_supplement_b.R: Fang Supplement B1 columns 1-2 and B2 (EXPERIMENTS.md section 14.7), next to Fang's numbers.
# Fang's published values are typed from literature/Fang_Lee_Li_2025_supplement.docx (Tables B1 and B2).
# Usage: Rscript code/R/09i_fang_supplement_b.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date(); OUT <- file.path("results", date_arg, "fang_supp"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)
need(c("data/fang_panel.csv","data/noaa_degree_days.csv","data/raw/eia/seds/use_all_btu.csv","data/raw/eia/seds/Prod_dataset.xlsx",
       "data/raw/eia/seds_archive/complete_seds_2021.zip"))
suppressPackageStartupMessages(library(readxl))

d <- fread("data/fang_panel.csv")[year %between% c(2018, 2021)]
# June 2023 SEDS (archive): renewable consumption and production, total energy, total expenditure
a <- fread(cmd="unzip -p data/raw/eia/seds_archive/complete_seds_2021.zip complete_seds_2021.csv", header=TRUE)[
  MSN %in% c("RETCB","REPRB","TETCB","TETCV") & Year %between% c(2018, 2021), .(state=StateCode, year=Year, MSN, v=Data)]
a <- dcast(a, state + year ~ MSN, value.var="v"); setnames(a, c("RETCB","REPRB","TETCB","TETCV"), paste0(c("RETCB","REPRB","TETCB","TETCV"), "_arch"))
# current SEDS: renewable production
pr <- as.data.table(read_excel("data/raw/eia/seds/Prod_dataset.xlsx", sheet="Data"))[MSN == "REPRB"]
pr <- melt(pr, id.vars=c("Data_Status","StateCode","MSN"), variable.name="year", value.name="v")[, .(state=StateCode, year=as.integer(as.character(year)), REPRB_cur=as.numeric(v))]
w <- fread("data/noaa_degree_days.csv")
d <- merge(merge(merge(d, a, by=c("state","year"), all.x=TRUE), pr, by=c("state","year"), all.x=TRUE), w, by=c("state","year"), all.x=TRUE)
stopifnot(nrow(d) == 204, !anyNA(d$RETCB_arch), !anyNA(d$REPRB_cur))

d[, `:=`(lnAIp=log(ai_postings), lnAIshare=log(ai_share_of_state_pct), lnEPU=log(epu_composite), lnEP=log(ep_tetcd),
         lnGDP=log(gdp_real_musd2017), lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000), lnHDD=log(hdd), lnCDD=log(cdd))]
B <- list(current=list(ET="re_bbtu", TRP="REPRB_cur", TE="total_energy_bbtu", EX=NA),
          june2023=list(ET="RETCB_arch", TRP="REPRB_arch", TE="TETCB_arch", EX="TETCV_arch"))
CF <- c("lnEPU","lnEP","lnGDP","lnPOP","lnEDU")
FANG <- data.table(
  table=c("B1","B1","B2","B2","B2","B2","B2"), column=c(1,2,1,2,3,4,5),
  label=c("AI share of postings","Renewable production (TRP)","Winsorized","+ energy intensity","+ HDD","+ CDD","+ energy expenditure per person"),
  fang_ai=c(0.0605,0.0605,0.0374,0.0444,0.0438,0.0427,0.0442), fang_t=c(2.38,2.38,1.99,2.23,2.18,2.12,2.19), fang_N=c(204,204,204,204,203,203,203))
up99 <- function(x) pmin(x, quantile(x, 0.99, na.rm=TRUE))

R <- list()
fit <- function(dd, y, ai, ctrl, tbl_, col_, basis) {
  f <- FANG[table==tbl_ & column==col_]
  m <- feols(as.formula(paste(y, "~", paste(c(ai, ctrl), collapse=" + "), "| state")), data=dd, vcov="iid")
  ct <- coeftable(m); ci <- confint(m)
  R[[length(R)+1]] <<- data.table(tag=sprintf("supp_%s_c%d_%s_fang6", tolower(tbl_), col_, basis), table=tbl_, column=col_, label=f$label, basis=basis,
    ai_var=ai, outcome=y, estimate=ct[ai,1], se=ct[ai,2], t=ct[ai,3], pval=ct[ai,4], ci_lo=ci[ai,1], ci_hi=ci[ai,2], N=m$nobs,
    fang_ai=f$fang_ai, fang_t=f$fang_t, fang_N=f$fang_N, fang_inside_ci=(f$fang_ai >= ci[ai,1] & f$fang_ai <= ci[ai,2]), status="ok")
}
for (bs in names(B)) {
  v <- B[[bs]]; S <- copy(d)
  S[, `:=`(lnET=log(get(v$ET)), lnTRP=log(get(v$TRP)), lnEI=log(get(v$TE) / gdp_real_musd2017))]
  if (!is.na(v$EX)) S[, lnEEP := log(get(v$EX) * 1e6 / population)]
  fit(S, "lnET", "lnAIshare", CF, "B1", 1, bs)
  fit(S[lnTRP > -Inf], "lnTRP", "lnAIp", CF, "B1", 2, bs)
  W <- copy(S)
  wv <- c("lnET","lnAIp","lnEPU","lnEP","lnGDP","lnPOP","lnEDU","lnEI","lnHDD","lnCDD", if (!is.na(v$EX)) "lnEEP")
  for (x in wv) W[, (x) := up99(get(x))]
  fit(W, "lnET", "lnAIp", CF, "B2", 1, bs)
  fit(W, "lnET", "lnAIp", c(CF, "lnEI"), "B2", 2, bs)
  fit(W[!is.na(lnHDD)], "lnET", "lnAIp", c(CF, "lnEI", "lnHDD"), "B2", 3, bs)
  fit(W[!is.na(lnHDD)], "lnET", "lnAIp", c(CF, "lnEI", "lnHDD", "lnCDD"), "B2", 4, bs)
  if (!is.na(v$EX)) fit(W[!is.na(lnHDD)], "lnET", "lnAIp", c(CF, "lnEI", "lnHDD", "lnCDD", "lnEEP"), "B2", 5, bs)
}
R <- rbindlist(R)
nr <- FANG[table=="B2" & column==5][, .(tag="supp_b2_c5_current_fang6", table, column, label, basis="current", ai_var="lnAIp", outcome="lnET",
  estimate=NA_real_, se=NA_real_, t=NA_real_, pval=NA_real_, ci_lo=NA_real_, ci_hi=NA_real_, N=NA_integer_, fang_ai, fang_t, fang_N, fang_inside_ci=NA,
  status="NOT_RUN: current SEDS expenditures (TETCV) not in raw files")]
R <- rbind(R, nr)
setorder(R, table, column, basis)
fwrite(R, file.path(OUT, "fang_supp_b.csv"))
writeLines(c("# RECEIPT.md: fang_supp", sprintf("Date: %s", date_arg), "Driver: code/R/09i_fang_supplement_b.R (EXPERIMENTS.md section 14.7, pre-registered 2026-11-09).",
  "Fang's spec, column 6: state FE, conventional SEs, 2018-2021, 50 states + DC. Fang's values typed from the supplement (Tables B1, B2).",
  "B2 cols. 3-5 use NOAA degree days for the 48 contiguous states (N = 192 vs Fang's 203). B2 col. 5 on current SEDS not run: no current TETCV.",
  sprintf("Rows: %d (%d ok).", nrow(R), sum(R$status=="ok"))), file.path(OUT, "RECEIPT.md"))
print(R[, .(table, column, basis, est=signif(estimate,3), t=round(t,2), p=round(pval,3), N, fang_ai, fang_t, fang_N, fang_inside_ci, status)])

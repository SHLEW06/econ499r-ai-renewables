#!/usr/bin/env Rscript
# 09a_fang_crosscheck.R: prompts/09_extend.md section 1 (EXPERIMENTS.md section 14.1, E1-E4).
# E1 implied means from Fang's Table 2 constants vs our descriptive statistics on three bases;
# E2 is built from results/<date>/fang/fang8_results.csv by the table script; E3 trend; E4 trend placebo.
# Usage: Rscript code/R/09a_fang_crosscheck.R --date YYYY-MM-DD
source("code/R/09_common.R")
date_arg <- parse_date()
need(c("data/fang_panel.csv","data/seds_old_basis.csv", file.path("results", date_arg, "fang", "fang8_results.csv"),
       sprintf("data/raw/bls/placebo/qcew_%d_%s.csv", rep(2014:2024, 2), rep(c("312140","812910"), each=11))))
OUT <- file.path("results", date_arg, "extend"); dir.create(OUT, recursive=TRUE, showWarnings=FALSE)

# ---------------- data ----------------
d <- fread("data/fang_panel.csv"); sb <- fread("data/seds_old_basis.csv")
d <- merge(d, sb[,.(state,year,re_bbtu_rebuilt,re_bbtu_k26)], by=c("state","year"), all.x=TRUE); setorder(d, state, year)
d[, `:=`(lnET=log(re_bbtu), lnET_rb=log(re_bbtu_rebuilt), lnET_k26=log(re_bbtu_k26), lnEPU=log(epu_composite), lnEP=log(ep_tetcd), lnGDP=log(gdp_real_musd2017),
         lnPOP=log(population/1000), lnEDU=log(edu_bach_per1000), lnAIp=log(ai_postings), lnAIj=log(dc_jobs), trend=year-2018)]
q <- rbindlist(lapply(c("312140","812910"), function(c) rbindlist(lapply(2014:2024, function(y) {
  x <- fread(sprintf("data/raw/bls/placebo/qcew_%d_%s.csv", y, c), colClasses=list(character="area_fips"))
  x[agglvl_code==58 & own_code==5 & grepl("000$", area_fips) & area_fips!="US000", .(fips=substr(area_fips,1,2), year=y, naics=c, emp=annual_avg_emplvl)] }))))
fips <- unique(fread("data/raw/bls/qcew_2019_518210.csv", colClasses=list(character="area_fips"))[agglvl_code==50 & own_code==5, .(fips=substr(area_fips,1,2))])
xw <- data.table(state=state.abb, name=state.name); xw <- rbind(xw, data.table(state="DC", name="District of Columbia"))
fp <- data.table(fips=sprintf("%02d", c(1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56)),
                 state=c("AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"))
q <- merge(q, fp, by="fips")[, emp := fifelse(emp > 0, emp, NA_real_)]
q <- dcast(q, state + year ~ naics, value.var="emp"); setnames(q, c("312140","812910"), c("emp_distill","emp_petcare"))

# ================ E1. implied means from Fang's Table 2 constants ================
S18 <- d[year %between% c(2018,2021)]
C <- c(11.4563, 11.5882, 11.1418, 19.3192, 20.0540, 19.2510)
mA <- mean(S18$lnAIp)
mY <- C[1] + 0.0428*mA
mE <- (C[2] - mY + 0.0452*mA) / 0.0284
mP <- (mY - 0.0396*mA + 0.0206*mE - C[3]) / 0.1533
mG <- (C[4] - mY + 0.0548*mA - 0.0242*mE + 0.2645*mP) / 0.7016
mPop <- (C[5] - mY + 0.0561*mA - 0.0239*mE + 0.2622*mP - 0.6911*mG) / 0.1049
mEdu <- (mY - 0.0531*mA + 0.0253*mE - 0.2907*mP + 0.7302*mG + 0.0148*mPop - C[6]) / 0.1143
imp <- c(lnAIp=mA, lnET=mY, lnEPU=mE, lnEP=mP, lnGDP=mG, lnPOP=mPop, lnEDU=mEdu)
# rounding bound: perturb every published constant and coefficient by +/- 0.00005 (500 draws)
set.seed(1); draws <- replicate(500, { e <- function() runif(1,-5e-5,5e-5); cc <- C + runif(6,-5e-5,5e-5)
  y <- cc[1] + (0.0428+e())*mA; E <- (cc[2]-y+(0.0452+e())*mA)/(0.0284+e()); P <- (y-(0.0396+e())*mA+(0.0206+e())*E-cc[3])/(0.1533+e())
  G <- (cc[4]-y+(0.0548+e())*mA-(0.0242+e())*E+(0.2645+e())*P)/(0.7016+e()); Po <- (cc[5]-y+(0.0561+e())*mA-(0.0239+e())*E+(0.2622+e())*P-(0.6911+e())*G)/(0.1049+e())
  Ed <- (y-(0.0531+e())*mA+(0.0253+e())*E-(0.2907+e())*P+(0.7302+e())*G+(0.0148+e())*Po-cc[6])/(0.1143+e()); c(y,E,P,G,Po,Ed) })
rb <- apply(draws, 1, function(z) max(abs(z - median(z)))); names(rb) <- c("lnET","lnEPU","lnEP","lnGDP","lnPOP","lnEDU")
V <- list(lnET="current SEDS", lnET_k26="k = 2.6", lnET_rb="rebuilt", lnAIp="", lnEPU="", lnEP="", lnGDP="", lnPOP="", lnEDU="")
ds <- rbindlist(lapply(names(V), function(v) { x <- S18[[v]]; key <- if (v %like% "^lnET") "lnET" else v
  data.table(variable=v, basis=V[[v]], N=sum(!is.na(x)), mean=mean(x), sd=sd(x), min=min(x), max=max(x), fang_implied_mean=imp[[key]],
             rounding_bound=if (key=="lnAIp") 0 else rb[[key]]) }))
ds[, `:=`(diff=mean-fang_implied_mean, diff_sd=(mean-fang_implied_mean)/sd)]
ds[, flag := abs(diff_sd) > 0.25 & variable != "lnAIp"]
# Unit changes that could apply to each variable (expected ln shift), checked within 0.025
UNITS <- list(lnGDP=c("chained 2012 vs 2017 dollars"=log(1.0757)), lnPOP=c("thousands vs persons"=log(1000)), lnET=c("billion vs trillion Btu"=log(1000)),
              lnET_k26=c("billion vs trillion Btu"=log(1000)), lnET_rb=c("billion vs trillion Btu"=log(1000)), lnEDU=c("per 1,000 vs per person"=log(1000)))
ds[, unit_shift_match := mapply(function(v, z) { u <- UNITS[[v]]; if (is.null(u)) return(""); m <- names(u)[abs(abs(z) - u) < 0.025]
  if (length(m)) sprintf("consistent with %s (expected %.3f, gap %.3f)", m[1], u[[m[1]]], abs(z) - u[[m[1]]]) else "" }, variable, diff)]
ds[, note := fifelse(variable=="lnAIp", "anchor: fixed at our mean to solve the system", "")]
fwrite(ds, file.path(OUT, "e1_descriptives_vs_fang_implied.csv"))
writeLines(c("Fang's descriptive statistics (Table A1) are in Supplementary Material A, which is not in literature/ as of 2026-11-07.",
             "Fang's Table 2 (PDF p. 5) constants are used instead: 11.4563, 11.5882, 11.1418, 19.3192, 20.0540, 19.2510 (columns 1-6).",
             "Only means can be implied; SD, min, max and N for Fang are not available."), file.path(OUT, "fang_table1_published_NOTE.txt"))
fwrite(data.table(variable=names(imp), fang_implied_mean=as.numeric(imp), source="Implied by Table 2 constants, PDF p. 5; lnAIp anchored at our mean",
                  sd=NA, min=NA, max=NA, N=204), file.path(OUT, "fang_table1_published.csv"))
print(ds)

# ================ E3. linear trend in Fang's column 6 ================
CF6 <- c("lnEPU","lnEP","lnGDP","lnPOP","lnEDU")
fang6 <- function(y, x, dd, extra=character(0)) feols(as.formula(paste(y, "~", paste(c(x, CF6, extra), collapse=" + "), "| state")), data=dd, vcov="iid")
rows <- list()
r1 <- function(block, spec, meas, y, x, mod, sample, term="AI", note="") { ct <- coeftable(mod); ci <- confint(mod)
  rows[[length(rows)+1]] <<- data.table(tag=sprintf("ext_%s_%s_%s_%s_%s_%s", block, spec, meas, y, sample, term), block=block, spec=spec, ai_measure=meas, outcome=y, term=term, variable=x,
                                        estimate=ct[x,1], se=ct[x,2], pval=ct[x,4], ci_lo=ci[x,1], ci_hi=ci[x,2], N=mod$nobs, status="ok", note=note) }
for (y in c("lnET","lnET_rb")) for (mm in list(c("aipostings","lnAIp"), c("dcjobs","lnAIj"))) {
  a <- fang6(y, mm[2], S18); r1("trend", "fang6", mm[1], y, mm[2], a, "51s2018_2021", note="Fang col. 6, no trend")
  b <- fang6(y, mm[2], S18, "trend"); r1("trend", "fang6trend", mm[1], y, mm[2], b, "51s2018_2021", note="Fang col. 6 + linear year trend"); r1("trend", "fang6trend", mm[1], y, "trend", b, "51s2018_2021", term="trend", note="trend coefficient") }

# ================ E4. trend placebo ================
dq <- merge(d, q, by=c("state","year"), all.x=TRUE); setorder(dq, state, year)
dq[, `:=`(lnDist=log(emp_distill), lnPet=log(emp_petcare))]
S18q <- dq[year %between% c(2018,2021)]
for (y in c("lnET","lnET_rb")) for (pp in list(c("distilleries","lnDist"), c("petcare","lnPet"))) {
  dd <- S18q[!is.na(get(pp[2]))]; r1("placebo", "fang6", pp[1], y, pp[2], fang6(y, pp[2], dd), sprintf("%ds2018_2021", uniqueN(dd$state)), note="Fang col. 6 with ln industry employment in place of ln AI") }
# our main spec: two-way FE, x(t-1), ctrl4, clustered, 50 states, 2015-2024, winsorized
P <- main_panel()
P <- merge(P, sb[,.(state,year,re_bbtu_current,re_bbtu_rebuilt)], by=c("state","year"), all.x=TRUE)
P <- merge(P, q, by=c("state","year"), all.x=TRUE); setorder(P, state, year)
qq <- merge(q, data.table(state=unique(P$state)), by="state"); setorder(qq, state, year)
qq[, `:=`(lnDist_l1=shift(log(emp_distill)), lnPet_l1=shift(log(emp_petcare))), by=state]
P <- merge(P, qq[,.(state,year,lnDist_l1,lnPet_l1)], by=c("state","year"), all.x=TRUE)
P[, `:=`(lnRE=wz(log(re_bbtu_current)), lnRE_rb=wz(log(re_bbtu_rebuilt)), lnDist_l1=wz(lnDist_l1), lnPet_l1=wz(lnPet_l1))]
PS <- P[year %between% c(2015,2024)]
for (y in c("lnRE","lnRE_rb")) {
  for (pp in list(c("distilleries","lnDist_l1"), c("petcare","lnPet_l1"))) { dd <- PS[!is.na(get(pp[2])) & !is.na(get(y))]
    r1("placebo", "twfe", pp[1], y, pp[2], fit_main(y, pp[2], dd), sprintf("%ds2015_2024", uniqueN(dd$state)), note="main spec with ln industry employment (t-1) in place of AI(t-1)") }
  for (mn in names(AIM)) { m <- AIM[[mn]]; dd <- PS[!is.na(get(m$lag)) & !is.na(get(y))]
    r1("placebo", "twfe", m$tag, y, m$lag, fit_main(y, m$lag, dd), sprintf("50s%d_2024", min(dd$year)), note="main spec, AI for comparison") } }
res <- rbindlist(rows, fill=TRUE); stopifnot(!anyDuplicated(res$tag)); fwrite(res, file.path(OUT, "e3_e4_trend_placebo.csv"))
print(res[, .(block, spec, ai_measure, outcome, term, estimate=round(estimate,4), p=round(pval,3), N)])
cat("DONE\n")

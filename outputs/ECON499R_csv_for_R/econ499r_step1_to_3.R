# ECON 499R: Steps 1 to 3 of the Methods Memo on the starter panel
# Files needed in the working directory: state_panel_2015_2025.csv, W_inverse_distance_rowstd.csv
# Packages: install.packages(c("fixest", "spdep", "dplyr"))
# Note: written to mirror the Python run in the workbook's Prelim Results tab; not run in R yet.

library(fixest)
library(dplyr)
library(spdep)

p <- read.csv("state_panel_2015_2025.csv") |> filter(state != "DC")

winsor <- function(x, lo = 0.01, hi = 0.99) {
  q <- quantile(x, c(lo, hi), na.rm = TRUE)
  pmin(pmax(x, q[1]), q[2])
}
p <- p |> mutate(across(c(ln_ec, ln_ee, renew_share, solar_share, ai_dc_per1000_lag1, tech_share),
                        winsor, .names = "{.col}_w"),
                 new_renew_gw = new_renew_mw / 1000)

# ---- Step 1 (H1): two-way fixed effects, one-year lag, state-clustered SEs ----
ctrl <- "ln_gdp_pc + manuf_share + price_c_kwh + pop_growth"
f1 <- function(y) as.formula(paste(y, "~ ai_dc_per1000_lag1_w +", ctrl, "| state + year"))
step1 <- list(
  consumption = feols(f1("ln_ec_w"),        data = p, cluster = ~state),
  efficiency  = feols(f1("ln_ee_w"),        data = p, cluster = ~state),
  renew_share = feols(f1("renew_share_w"),  data = p, cluster = ~state),
  solar_share = feols(f1("solar_share_w"),  data = p, cluster = ~state),
  new_renew   = feols(f1("new_renew_gw"),   data = p, cluster = ~state)
)
etable(step1)

# ---- Step 3 (H3): Moran's I and the SLX fallback ----
W <- as.matrix(read.csv("W_inverse_distance_rowstd.csv", row.names = 1))
lw <- mat2listw(W, style = "W")
for (yr in c(2015, 2020, 2025)) {
  d <- p |> filter(year == yr) |> arrange(match(state, rownames(W)))
  print(moran.test(d$renew_share, lw))
}

# neighbors' lagged AI: theta in the memo's SDM equation
lagAI <- p |> select(state, year, ai_dc_per1000_lag1_w) |>
  tidyr::pivot_wider(names_from = state, values_from = ai_dc_per1000_lag1_w) |> arrange(year)
yrs <- lagAI$year
A <- as.matrix(lagAI[, rownames(W)]); A[is.na(A)] <- 0
WA <- A %*% t(W)
wai <- data.frame(year = rep(yrs, times = ncol(WA)), state = rep(colnames(W), each = length(yrs)),
                  w_ai_lag1 = as.vector(WA))
p <- left_join(p, wai, by = c("state", "year"))
f3 <- function(y) as.formula(paste(y, "~ ai_dc_per1000_lag1_w + w_ai_lag1 +", ctrl, "| state + year"))
slx <- list(
  consumption = feols(f3("ln_ec_w"),       data = p, cluster = ~state),
  efficiency  = feols(f3("ln_ee_w"),       data = p, cluster = ~state),
  renew_share = feols(f3("renew_share_w"), data = p, cluster = ~state)
)
etable(slx)

# ---- Step 2 (H2a) first leg, using the tech-worker share as the mediator ----
p$tech_share_pct <- 100 * p$tech_share_w
etable(feols(as.formula(paste("tech_share_pct ~ ai_dc_per1000_lag1_w +", ctrl, "| state + year")),
             data = p, cluster = ~state))

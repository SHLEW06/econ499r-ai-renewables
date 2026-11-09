# packages.R — R packages for the Phase 4 and 09 drivers, with the versions the
# 2026-11-07 results were built with (R 4.6.2). renv isn't set up for this project,
# so this file is the package list.
#
# Usage (from the project root):
#   Rscript code/R/packages.R           install any missing package from CRAN, then
#                                       compare installed versions with the pins
#   Rscript code/R/packages.R exact     install the pinned versions (uses renv::install)
#   Rscript code/R/packages.R check     report only; install nothing
#
# Exit code 1 if a package is still missing. A version that differs is reported but
# doesn't fail: the results should match on nearby versions, but if numbers differ
# from results/ in the last digits, run with `exact` first.
#
# sf needs GDAL, GEOS and PROJ. CRAN's macOS and Windows binaries include them; on
# Linux install them first (e.g. apt install libgdal-dev libgeos-dev libproj-dev).

pins <- c(
  data.table   = "1.18.6.1",
  fixest       = "0.14.2",
  modelsummary = "2.6.0",
  ggplot2      = "4.0.3",
  spdep        = "1.4.2",
  spatialreg   = "1.4.3",
  splm         = "1.6.5",
  SDPDmod      = "0.0.8",
  plm          = "2.6.7",
  sf           = "1.1.3",
  maps         = "3.4.4",
  boot         = "1.3.32",
  dplyr        = "1.2.1",
  readxl       = "1.6.0",   # 09i_fang_supplement_b.R (current SEDS production)
  IRkernel     = "1.3.2",   # only for the two R-kernel notebooks
  renv         = "1.3.1"    # only for `exact`
)

mode <- commandArgs(trailingOnly = TRUE)
mode <- if (length(mode)) mode[1] else "install"
if (!mode %in% c("install", "exact", "check")) stop("mode must be install, exact or check")
if (getRversion() < "4.6.0") message("Note: results were built on R 4.6.2; you have ", getRversion())

repos <- getOption("repos")
if (is.null(repos) || identical(unname(repos["CRAN"]), "@CRAN@")) repos <- c(CRAN = "https://cloud.r-project.org")

installed_version <- function(p) {
  tryCatch(as.character(packageVersion(p)), error = function(e) NA_character_)
}

if (mode == "install") {
  missing <- names(pins)[is.na(vapply(names(pins), installed_version, ""))]
  if (length(missing)) install.packages(missing, repos = repos)
}
if (mode == "exact") {
  if (is.na(installed_version("renv"))) install.packages("renv", repos = repos)
  have <- vapply(names(pins), installed_version, "")
  todo <- setdiff(names(pins)[is.na(have) | have != pins], "renv")
  if (length(todo)) renv::install(sprintf("%s@%s", todo, pins[todo]), repos = repos, prompt = FALSE)
}

have <- vapply(names(pins), installed_version, "")
status <- ifelse(is.na(have), "MISSING", ifelse(have == pins, "ok", "differs"))
print(data.frame(package = names(pins), pinned = unname(pins), installed = unname(have),
                 status = unname(status)), row.names = FALSE)
if (any(status == "MISSING")) quit(status = 1)

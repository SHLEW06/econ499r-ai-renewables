# Phase 4h: the Fang et al. (2025) test
**Date:** 2026-11-04  
**Driver:** `code/R/04h_fang_test.R --date 2026-11-04`  
**Notebook:** `notebooks/04h_fang_test.ipynb`  
**Results:** `results/2026-11-04/fang/`

---

## 1. What was done
Part A: data (`data/fang_panel.csv`, receipts, ratings). Part B: replication, bridge, EPU moderation, by type, heterogeneity, placebo, robustness, with postings and data-center jobs side by side.

## 2. Key decisions
- Stitched postings stay main; Lightcast's own series covers only 4 states.
- 2018 comes from the 2019 edition, the only route to N = 204, with a same-vintage row beside it.
- Divergences F1-F18 are in `EXPERIMENTS.md` section 9b.

## 3. Results
All associations. Data-center jobs (BLS, one consistent series) are the more reliable extension measure.

| Step | ln(AI postings) | ln(data-center jobs) |
|---|---|---|
| Fang's spec, 2018-2021 | -0.0188 (p = 0.317) | -0.0655 (p = 0.229) |
| + year FE | -0.1095 (p = 0.004) | -0.0628 (p = 0.262) |
| Final: lag, clustered, longer sample, no DC | -0.0479 (p = 0.109) | -0.0567 (p = 0.208) |

- **Replication:** Fang's +0.0531 doesn't reproduce on current SEDS. EIA's Oct 2023 accounting change explains the sign, not the full size.
- **Moderation:** positive in Fang's spec; none significant under two-way FE.
- **Placebo:** no failure, but weak evidence.

## 4. What did not change
The master panel, the Zhang test results and all earlier result files.

## 5. Decisions still open
Whether to contact Fang et al. about their SEDS vintage and postings series, if an exact match matters for the paper.

## How to resume
1. `CLAUDE.md` section 5
2. `EXPERIMENTS.md` section 9b
3. `results/2026-11-04/fang/RECEIPT.md`
4. `notebooks/04h_fang_test.ipynb`

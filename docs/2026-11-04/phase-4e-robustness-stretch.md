# Phase 4e: Robustness (stretch goals still to come)
**Date:** 2026-11-04  
**Drivers:** `code/R/04e_robustness.R --date 2026-11-04`, `code/R/04e2_spillover_placebo.R --date 2026-11-04`, `code/python/04e_spec_curve.py --date 2026-11-04`  
**Notebook:** `notebooks/04e_robustness_stretch.ipynb`  
**Results:** `results/2026-11-04/robustness/`, `results/2026-11-04/h3_placebo/`

---

## 1. What was done

- Reran the gate and A1-A8, P1 and P2 under 2026-11-04. All 111 rows from Nov 3 are identical.
- Added the RPS control and its checks, an all-ownership AI row, a Gavins Point row and the spillover placebo.
- Stretch goals not run.

## 2. Key decisions

- **RPS control:** main version is `target_pct`, the larger of RPS and CES, labeled "LBNL current RPS/CES schedule" (`EXPERIMENTS.md` §0 item 21).
- **AI measure:** private data-center jobs per 1,000 workers. All-ownership is one labeled row (§0 item 24).
- **Spillover placebo sample:** 2015-2023. W·AI(t+1) in 2024 would need 2025 AI for four suppressed states (§0 item 28).
- **Gavins Point:** the panel keeps EIA's data as published; one labeled row holds the plant in NE (§0 item 29).
- **Stretch order:** the Fang test, then shift-share IV, then broadband and R&D moderation. Hansen threshold dropped (§0 item 30).

## 3. Results and readings

**Readings (team):**
- **`renew_share`:** next year's AI predicts this year's share, and with both in one model the lag is about zero. Describe the negative association as reflecting where and when data-center jobs grow (reverse timing or selection), not AI lowering the renewable share.
- **`new_renew_mw`:** positive in raw MW, not robust to scaling, and its lead is also positive. With both in one model, neither is significant. Same caution.
- **H3:** wording on hold until the team has reviewed the spillover placebo.
- **RPS control and all-ownership AI:** they change no result.

| Own-AI placebo, N = 496 | AI(t+1) | In one model: lead | In one model: lag |
|---|---|---|---|
| `renew_share` | -0.0197 (p = 0.006) | -0.0210 (p = 0.007) | 0.0015 (p = 0.827) |
| `new_renew_mw` | 86.8 (p = 0.028) | 55.9 (p = 0.219) | 37.5 (p = 0.191) |

**Other checks on `new_renew_mw`:** holding Gavins Point in NE gives 71.0 MW against 70.8 MW, both p = 0.033.

**Spillover placebo, `renew_share` (full tables in `results/2026-11-04/h3_placebo/`):**
- Dropping 2024-2025 alone takes the SDM indirect effect from -0.161 (N = 550) to -0.082 (N = 450, CI -0.588 to 0.447).
- Inverse-distance W: neither the lag nor the lead can be told apart from zero.
- Border W: with both in one model, the lead is significant and the lag is about zero. SLX theta -0.0406 (p = 0.028) vs 0.0098 (p = 0.584); SDM indirect -0.0432 (p = 0.025) vs -0.0011 (p = 0.978).

## 4. What did not change

- The master panel's values, except `dc_wages_usd` in 4 suppressed cells, which no model uses.
- W matrices, the 4b to 4d result files, and the Nov 3 robustness files.

## 5. Decisions still open

| Item | Status |
|---|---|
| H3 wording | On hold for team review of the spillover placebo |
| Fang test | Next. Needs its specification |
| Older notebooks and handoffs (4b, 4d) | Their reading text predates the placebo. `CLAUDE.md` §5 says the new readings override it |

## How to resume

Read in this order:
1. `CLAUDE.md` §5
2. `EXPERIMENTS.md` §0 items 21-30 and §9
3. This file
4. `notebooks/04e_robustness_stretch.ipynb`
5. `results/2026-11-04/robustness/RECEIPT.md` and `results/2026-11-04/h3_placebo/RECEIPT.md`

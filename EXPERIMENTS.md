# EXPERIMENTS.md — Divergence Register

Tracks every place where what we actually run differs from the Methods Memo spec.
Log a new entry here BEFORE implementing any deviation. Do not run a deviation unreported.

---

## Data section (confirmed by Part C, 2026-11-02)

| Decision | Choice | Status |
|---|---|---|
| GDP in ln_ee and ln_gdp_pc | Real chained-2017 (BEA SAGDP9) | Confirmed — memo unspecified; corr(real,nom)=0.98 |
| AI numerator | Private 518210 (own_code=5) | Confirmed — no govt rows exist at state level |
| Fossil includes Other Gases | Yes (0.34% of fossil) | Confirmed — matches EIA source structure |
| Renewable: utility-scale only | Yes | Known limitation; rooftop not in EIA gen file |
| Validation: 0 red, 3 yellow, 17 green | — | Full detail in data/DATA_VALIDATION.md |

---

## EXP-001: tech_share vs. HMA for H2a mediator

**Status:** Under review
**Memo spec:** Use HMA (coupling index built from AI × tech_share) as the mediator variable for H2a.
**What we do instead (or additionally):** Use tech_share directly as the mediator; run both and compare.
**Reason:** HMA is a function of AI itself, so a regression of HMA on AI is positive by construction. It cannot falsify H2a — any result is predetermined by the variable definition.
**Effect on results:** Using tech_share instead may attenuate or reverse the H2a finding. Running both makes the comparison transparent.
**Decided by:** Claude, Oct 25 review. Not yet confirmed with Alexander.

---

## EXP-002: SDM direct and indirect impacts

**Status:** Adopted
**Memo spec:** Report theta (the spatial lag coefficient on the dependent variable) as the spillover estimate.
**What we do instead (or additionally):** Report direct, indirect, and total impacts using the LeSage/Pace (2009) decomposition, in addition to theta.
**Reason:** In a Spatial Durbin Model, theta alone is not the spillover. The partial derivative decomposition into direct and indirect impacts is the correct estimand for interpreting spatial effects.
**Effect on results:** Indirect impacts will differ from theta in magnitude and potentially in sign. Total impact is the policy-relevant quantity.
**Decided by:** Claude, Oct 25 review.

---

## EXP-003: RPS control in core model

**Status:** Under review — blocked by missing data
**Memo spec:** No RPS mandate control in the core Step 1 regression equation.
**What we do instead (or additionally):** Add RPS/CES mandate indicator or stringency index as a control variable once the LBNL file is obtained.
**Reason:** State renewable portfolio standards directly drive renew_share. Omitting them risks attributing policy-driven variation to the AI coefficient, biasing it in either direction.
**Effect on results:** Expected to reduce the estimated AI coefficient if AI deployment is correlated with policy ambition (e.g., California).
**Decided by:** Claude, Oct 25 recommendation. Blocked until LBNL RPS spreadsheet is downloaded (browser required).

---

## EXP-004: AI squared for non-linearity

**Status:** Under review
**Memo spec:** No quadratic term; model is linear in ai_dc_per1000.
**What we do instead (or additionally):** Add ai_dc_per1000^2 as an extra robustness column in Step 4 output.
**Reason:** The effect of AI on renewables may be non-linear. At low penetration, AI demand may crowd out investment capacity; at high penetration, scale effects may dominate. A threshold or U-shape is plausible.
**Effect on results:** Unknown. If the quadratic coefficient is significant and the linear term changes sign, the linear specification is misspecified.
**Decided by:** Claude, Oct 25. Include as robustness only; not in core table.

---

## EXP-005: Alternative AI measure — AI patents or job postings

**Status:** Under review — data not yet obtained
**Memo spec:** Primary AI measure is NAICS 518210 employment per 1,000 workers (BLS QCEW).
**What we do instead (or additionally):** Consider USPTO AI patents per capita (available through 2023) or Lightcast AI job-postings share as alternative or auxiliary measures.
**Reason:** NAICS 518210 covers all data processing and hosting, not AI compute specifically. Georgia ranking 2nd (above Virginia) is a red flag — likely reflects colocation/cloud hosting. A narrower measure would reduce measurement error in the main regressor.
**Effect on results:** Expected to reduce attenuation bias. Georgia's anomalous ranking may disappear or reverse. Keep 518210 as primary; alternatives would appear in a robustness table.
**Decided by:** Claude, Oct 25. Not yet confirmed with Alexander. Requires browser downloads not yet completed.

---

## EXP-006: Consumption sign flip (note, not a deviation)

**Status:** Not a deviation — reference note only
**Memo spec:** Hypothesis a1 < 0 for ln_ec: U.S. data centers raise electricity demand, so AI is expected to reduce the renewables share (opposite of the China result in Zhang et al.).
**What we do instead (or additionally):** N/A — this is the specified direction.
**Reason:** Prior Python prelim result: a1 = -0.0016, p = 0.79. Coefficient has the expected negative sign but is not statistically significant. Not a deviation from the memo; recorded here for continuity across sessions.
**Effect on results:** Inconclusive at this stage. Will revisit with the full R specification in Step 2.
**Decided by:** N/A.

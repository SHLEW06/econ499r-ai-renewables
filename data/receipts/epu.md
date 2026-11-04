# Receipt: State Economic Policy Uncertainty

**Source:** Scott R. Baker, Steven J. Davis and Jeffrey Levy, "Local and National Economic Policy Uncertainty in US States," hosted by Economic Policy Uncertainty.
**Link:** https://www.policyuncertainty.com/state_epu.html ; file https://www.policyuncertainty.com/media/State_Policy_Uncertainty.xlsx
**Vintage:** the publisher's server reports Last-Modified Jan 20, 2026. The file has no internal metadata. Data run through December 2025.
**How:** Team browser download; moved from the project root on 2026-11-04.

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/epu/State_Policy_Uncertainty.xlsx` | 837,999 | `e244701f6830dfd2845cc6deb87817cfa4c12aefdf6194858e8ca201c2517d19` |

## What was kept
`data/epu_state_annual.csv`: state, year, `epu_state`, `epu_national`, `epu_composite`, `n_months_state`. 50 states + DC, 1985-2025.

The three indexes differ only in their policy terms:
- **`epu_national`:** uncertainty within a state from national policy.
- **`epu_state`:** from state and local policy.
- **`epu_composite`:** either set of terms.

The stretch plan (`prompts/04e_robustness_stretch.md`) calls for `epu_state`.

## Steps
1. Reshape to long; state is the last two letters of each column name.
2. Average the monthly values by state, year and measure, skipping blanks.
3. Count months per state-year.

**Rows:** in 492 months across 153 series; out 2,091 state-years (51 x 41).

## Checks
- **Publisher:** byte-identical to the file served today.
- **Coverage:** no blanks in 2015-2025, and all 12 months in each of those state-years. Before 2015, 382 state-years have no months and 9 are partial; those stay NA or carry the partial mean, with `n_months_state` showing which.
- **Hand check:** GA 2025 `epu_state` from the monthly rows = 106.665, same as the table.

## Quirks
Paper counts vary widely by state (publisher: median 49, DC 4, IL 279), so small states are noisier.

**Rating: green.**

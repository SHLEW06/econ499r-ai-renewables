# Check values from the Oct 30, 2026 first pass

Panel (out/state_panel_2015_2025.csv from scripts/build_panel.py)
- 561 rows x 80 columns: 50 states + DC, 2015-2025. 550 rows after dropping DC.
- NAICS 518210 suppressed by BLS in 2025 for AK, ND, SD, WY (dc_jobs and ai_dc_per1000 blank).
- Rebuilding from fresh downloads on Nov 1, 2026 gave an identical file.

Georgia
| year | dc_jobs | ai_dc_per1000 | renew_share | solar_share | price_c_kwh | ln_ec | ln_ee |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 | 8,346 | 2.0106 | 0.0609 | 0.0010 | 9.6188 | 2.5902 | 8.2878 |
| 2025 | 24,620 | 5.0346 | 0.1287 | 0.0768 | 12.0600 | 2.6065 | 8.4551 |

Top AI states in 2025: WA 6.479, GA 5.035, MO 4.978 (VA 4.859).

First-pass models (Python pyfixest; 50 states; outcomes and lagged AI winsorized 1/99 over the pooled sample;
state + year FE; SEs clustered by state; N = 550): see prelim_step1_slx.csv and prelim_morans_i.csv.
- Step 1 a1: ln_ec -0.0016 (p 0.79); ln_ee 0.0022 (p 0.71); renew_share -0.0101 (p 0.10); new renewable GW 0.076 (p 0.07).
- SLX theta (neighbors' lagged AI, row-standardized inverse distance; suppressed cells set to 0 in the neighbor average): none significant at 5%.
- Moran's I, renew_share: 0.094 (2015), 0.115 (2020), 0.157 (2025), permutation p <= 0.002.
- Step 2b: tech share (pct) on lagged AI: -0.0165 (p 0.43).

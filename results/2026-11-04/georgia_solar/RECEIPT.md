# Georgia solar module: RECEIPT, 2026-11-04
Driver: `code/python/04f_georgia_solar.py --date 2026-11-04`. Spec: EXPERIMENTS.md section 11; `prompts/04f_georgia_solar_learning_curve.md`; `prompts/06_finish.md` section 4. Log: `logs/2026-11-04/04f_georgia_solar.log`.

**What it answers:** what learning-curve arithmetic implies for utility-scale solar costs in Georgia by 2035. **It has no AI variable and says nothing about whether AI affects renewables.** Learning curves are correlations: the paper says "the direction of causality is not clear" (Bolinger et al. 2022, PDF p. 13). None of these numbers is a forecast of ours.

## Base cost
- **Georgia:** capacity-weighted LCOE without tax credits, $63.81/MWh in 2025 dollars. 17 projects, 1,750 MW-AC, in service 2023-2025. Median $67.85.
- **Comparison:** Southeast $58.69 (131 projects); U.S. $58.64 (592 projects).
- **Source:** LBNL Utility-Scale Solar 2026 Edition, `Individual_Project_Data`, `PV LCOE no Tax Credits`. PPA prices aren't used, because they include tax credits.
- **Assumption:** Georgia has no learning rate of its own. Applying a global rate holds Georgia's proportional gap to the U.S. constant.

## Capacity paths (verified in the primary document)
International Energy Agency, *World Energy Outlook 2025*, Annex A, solar PV capacity (GW). https://iea.blob.core.windows.net/assets/5306bae2-1f99-402f-8d14-542bfa0ae96e/WorldEnergyOutlook2025.pdf

| Path | IEA scenario | Table, page | 2024 | 2035 | Ratio |
|---|---|---|---:|---:|---:|
| Low | Current Policies | A.3a, p. 417 | 2,164 | 8,067 | 3.728 |
| Central | Stated Policies | A.3b, p. 423 | 2,164 | 8,855 | 4.092 |
| High | Net Zero Emissions by 2050 | A.3c, p. 429 | 2,164 | 12,499 | 5.776 |

**Three things are our arithmetic, not IEA's:**
- IEA's capacity base differs from IRENA's (2024: 2,164 vs 1,867 GW), so we apply IEA's growth ratio to IRENA's 2024 value. A learning curve depends only on the ratio.
- 2025 is IRENA's actual value (2,378 GW).
- Years between 2025 and 2035 are log-linear interpolation. IEA's table has no 2030 value.

IEA's Net Zero path is a normative scenario, not a projection. The WEO PDF isn't stored in the project, because it's IEA's copyrighted report; the numbers and pages above are the record.

## Projection, LCOE in 2025 $/MWh, no tax credits
See `projection_table.csv`; all 132 values are in `projection_long.csv`, each with a tag.

| Learning rate | Low, 2035 | Central, 2035 | High, 2035 |
|---|---:|---:|---:|
| 12% | 50.40 | 49.54 | 46.49 |
| 19% (CapEx) | 43.25 | 42.04 | 37.86 |
| **24% (main)** | **38.45** | **37.06** | **32.33** |
| 45% (2014-2020 epoch) | 21.17 | 19.53 | 14.51 |

The curve's 2025 value differs from the $63.81 base because the base sits at the capacity-weighted global capacity for those projects (1,936 GW), not at 2025's level. At 24% it's $58.82.

**Against Bolinger's 47%:** the paper's 47% reduction by 2035 (PDF p. 11) starts from 2020 with its own deployment path. Ours is -37.0% from 2025 on the central path, a different period.

## Learning-rate check
Bolinger's equation 2, on LBNL's published national series (`LCOE Trend (PV only)` tab) against IRENA global capacity. It starts in 2010, not 2007, because the tab does.

| Window | Learning rate | R² |
|---|---:|---:|
| 2010-2024 | 29.0% | 0.938 |
| 2010-2021 | 32.7% | 0.977 |
| 2010-2025 | 26.8% | 0.896 |

Bolinger's 24% is normalized for exogenous influences, and the paper gives 27% on raw data (PDF p. 7), so our raw estimates are comparable. The rate falls as recent years enter, because **LCOE rose from $49.0 in 2022 to $61.0 in 2025 while global capacity more than doubled.** The curve assumes costs resume falling with deployment; recent years don't show that, and the paper links post-2020 increases to supply-chain costs. A 10-year extrapolation is highly uncertain.

## Georgia context
Georgia Power's 2025 IRP plans RFPs to procure energy from up to 4,000 MW of renewable resources by 2035, including a 2026 RFP targeting 1,000 MW of utility-scale resources (2025 IRP Main Document, PDF p. 67). That's the utility's own plan.

## Files
`base_cost.csv`, `capacity_paths.csv`, `projection_long.csv`, `projection_table.csv`, `learning_rate_check.csv`, `national_lcoe_lbnl_tab.csv`, `national_lcoe_series.csv`, `../figures/04f_georgia_fan.png`

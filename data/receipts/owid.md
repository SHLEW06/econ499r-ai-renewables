# Receipt: Global solar PV capacity (IRENA via Our World in Data)

**Source:** IRENA (2026), "Renewable Energy Statistics," processed by Our World in Data. Variable last updated 2026-07-28. **Cite IRENA as the source.**
**Link:** https://ourworldindata.org/grapher/solar-pv-cumulative-capacity
**How:** Team browser download on Nov 4, 2026; moved from the project root.

| File | Bytes | SHA-256 |
|---|---|---|
| `data/raw/owid/solar-pv-cumulative-capacity.csv` | 103,760 | `12703baf933545b13514bb70aad3f6e79dccd45b7b0ade2a3df850b89f12844f` |
| `data/raw/owid/solar-pv-cumulative-capacity.metadata.json` | 1,324 | `0de72bb9742e312d800e77cf7f2feb211a0562a7c7731f2f46518c81c237284c` |
| `data/raw/owid/readme.md` | 5,042 | `41935d88b81592b5e6a2d061d8338fa1385172d3255b0dd1972170899f9c463f` |

## What was kept
`data/owid_global_solar_capacity.csv`: World and United States, 2000-2025, on-grid PV in GW, with a source column. All other countries stay in the raw file.

## Steps
1. Keep `Entity` in World or United States.
2. Rename columns.
3. Add the IRENA source text.

**Rows:** in 3,633, out 52.

## Checks (IRENA, *Renewable Capacity Statistics 2026*, read from a [copy hosted by pS-Eau](https://bdd.pseau.org/outils/ouvrages/irena_renewable_capacity_statistics_2026_2026.pdf), not irena.org)
| Cell | This table (GW) | IRENA total PV (GW) | Note |
|---|---|---|---|
| World 2025 | 2,378.0 | 2,383.2 | 0.2% below |
| World 2024 | 1,866.9 | 1,872.8 | 0.3% below |
| USA 2023 | 138.45 | 138.45 | Match |
| USA 2025 | 209.47 | 210.13 | 0.3% below |

- **World additions in 2025:** 511 GW here; IRENA reports about 510 GW.
- **Unexplained gap:** the table is on-grid and IRENA's row is total PV, but subtracting IRENA's off-grid row doesn't give an exact match (World 2025: 2,372.8 vs 2,378.0). The OWID data come from a later IRENA release (July vs March), which may explain it. I didn't confirm that.

**Rating: green.**

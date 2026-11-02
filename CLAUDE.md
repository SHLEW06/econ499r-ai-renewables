# CLAUDE.md — Project Conventions for AI Impact on Renewables

## §1 Project Overview

Course: ECON 499R, Emory University, Fall 2026
Team: Shunji Lewandowski (modeling) and Alexander Hendricks (data/finance)
Advisor: Prof. Fohlin
Research question: Testing Zhang et al. (2026) "Blessing or Peril?" on 50 U.S. states, 2015–2025.

Deadlines:
- Steps 1–3 complete: Nov 17
- Draft: Nov 24
- Turn-in: Dec 1

---

## §2 Folder Layout

```
data/raw/<source>/          Raw files — never edit, treat as read-only
data/out/                   Panel build outputs:
                              state_panel_2015_2025.csv
                              W_border_binary.csv (and other W matrices)
                              state_centroids_land.csv
data/                       DATA_AUDIT.md, DATA_INDEX.md, DATA_CATALOG.xlsx
data/receipts/              One .md per source documenting provenance
econ499r_starter/scripts/   Download and build scripts:
                              build_panel.py, ferc_fin.py, sec_fin.py,
                              build_xlsx.py, prelim.py, download_all.py
outputs/                    ECON499R_Data_Workbook_<date>.xlsx
                            ECON499R_csv_for_R/ (prior session reference)
notes/                      Context handoffs, Grijalva transcript, methods memo
literature/                 PDFs
docs/<YYYY-MM-DD>/          Dated handoffs per phase
logs/<YYYY-MM-DD>/          Move logs, build logs
archive/                    Saved Claude chats
```

---

## §3 Rebuilding the Panel

```bash
python3 econ499r_starter/scripts/build_panel.py data/raw data/out
```

Run from project root. Takes ~30 seconds.
Dependencies: pandas, numpy, openpyxl, pyarrow.

---

## §4 Key Conventions

- **data/raw/ is read-only.** Never edit any file under data/raw/.
- **No invented data.** If a value is missing, leave it as NA and add a reason in the codebook.
- **Deviations from the Methods Memo** must be logged in EXPERIMENTS.md first with a reason, before running.
- **Script argument convention:** positional args only.
  - `build_panel.py <raw_dir> <out_dir>`
  - `ferc_fin.py <pudl_dir> <out_dir>`
- **Dated handoffs** go in `docs/YYYY-MM-DD/`.
- **Move logs** go in `logs/YYYY-MM-DD/phase2_moves.csv` with columns: old_path, new_path, sha256.
- **Models are Phase 4.** Use R with packages fixest, spdep, spatialreg. Prompt: `prompts/04a_methods_spec.md`.

---

## §5 Project state (as of 2026-11-02)

**Phase 2 complete.** Panel validated; all variables green or yellow (documented gaps only).

- Phase 2A (audit): done — `data/DATA_AUDIT.md`, `docs/2026-11-01/phase-2a-data-audit.md`
- Phase 2B (build): done — `data/out/state_panel_2015_2025.csv` (561×80), workbook, receipts
- Phase 2C (validate): done — `data/DATA_VALIDATION.md`, `logs/2026-11-02/build/validation/`

**Validation verdict:** 0 red, 3 yellow (co2_per_mwh_t, seds_mmbtu_pc, hma — 2025 gaps only), 17 green.

**Next step:** `prompts/04a_methods_spec.md` (Phase 4a: lock spec, set up R, smoke check).

---

## §6 Known Issues and Measurement Caveats

- **NAICS 518210 scope:** counts all data processing and hosting, not AI data centers specifically. Georgia ranks 2nd (above Virginia), which is suspicious and likely reflects colocation/cloud hosting, not AI compute.
- **Within-state AI variation is small:** SD of ai_dc_per1000 is approximately 0.57 per 1,000 workers. Coefficient estimates will be imprecise.
- **CO2 and SEDS data end in 2024:** year 2025 produces 51 NA rows in the panel (one per state).
- **Suppressed 518210 counts (2025):** AK, ND, SD, WY have suppressed BLS data — 4 NA rows for dc_jobs and ai_dc_per1000.
- **Border W matrix (W_border_binary.csv)** excludes AK and HI — neither has contiguous neighbors in the 48-state graph.
- **ln_ee and ln_gdp_pc use real (chained 2017) GDP.** The memo says "State GDP in $" without specifying. Real preferred; corr(real, nominal) = 0.98 under two-way FE.
- **Renewable share is utility-scale only.** Rooftop solar appears in retail sales but not in EIA state generation file.

---

## §7 Data Still Needed

See DATA_AUDIT.md for full details.

| Item | Method | Needed for |
|------|--------|------------|
| LBNL RPS/CES spreadsheet | Browser download | Step 4 RPS control (EXP-003) |
| Q1–Q4 2024 large-load reports (Docket 55378) | Browser, FERC | Georgia case box |
| NOAA HDD/CDD | Script | Climate control (optional) |
| NSF R&D by state | Script | Tech intensity control (optional) |
| Epoch data center counts | Script | Alternative AI measure (optional) |
| SEC company facts | sec_fin.py + SEC_USER_AGENT env var | Finance channel (optional) |

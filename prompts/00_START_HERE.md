# Claude Code prompts for the ECON 499R project: start here

Run these one at a time, in order. Each one is a separate phase, and each ends with a short notebook, a handoff doc, and a stop. Start a fresh Claude Code session per phase if you like; every prompt tells Claude Code to read the latest handoff first.

## Setup for this batch (Nov 1 methods review)
Unzip this batch into the project folder, then have Claude Code do these steps (with your OK, as always):
1. Move methods-review-2026-11-01.md to docs/2026-11-01/methods-review.md. Every prompt from 02 on reads it there.
2. Put the new prompt files in prompts/, replacing 00_START_HERE.md and 02_data_audit_cleaning_excel.md.
3. Move the retired prompts to prompts/_retired/ (kept for history, not run): 02_data_catalog.md, 03_data_cleaning.md and 04_models.md. They are replaced by 02_data_audit_cleaning_excel.md and 04a to 04g.
4. If part of Phase 2 already ran, the 02 prompt picks up from the first unfinished part. Its Part C (proving the data is right) always runs in full.

| Phase | Prompt | What it does | What it does NOT do |
| --- | --- | --- | --- |
| 1 | 01_organize_folder.md | Survey, sort and rename the whole "AI impact on Renewables" folder (notes, notebooks, sources, data, code, admin, interviews, decks); set up project conventions and a local git repo | Touch the contents of any data file |
| 2 | 02_data_audit_cleaning_excel.md | A: inventory every file in the folder and audit it, then stop. B: clean into the master panel, workbook and .md receipts. C: prove the data is right (definitions, cross-checks against published numbers, cell-by-cell reproduction, traced cells, plausibility), then stop | Run any models |
| 4a | 04a_methods_spec.md | Lock the final spec, divergence register and tag grammar in EXPERIMENTS.md; write the memo-corrections doc; set up R and the single panel loader; run a smoke check | Estimate anything |
| 4b | 04b_step1_twfe.md | H1: reproduce the first pass, then the core and extra outcomes, the price check, Driscoll-Kraay SEs, AI², heterogeneity and dynamics | Add a lagged dependent variable |
| 4c | 04c_step2_mediation.md | H2a/H2b mediation with tech_share (main), hma (memo) and ln_ea; Sobel plus a cluster bootstrap | Treat hma's b1 as evidence |
| 4d | 04d_step3_spatial.md | H3: Moran's I, LM tests, SLX, and the SDM with direct, indirect and total impacts | Read SDM theta as the spillover |
| 4e | 04e_robustness_stretch.md | The robustness list, then the stretch goals if there's time: moderation, shift-share IV, Hansen | Start stretch work before robustness is done |
| 4f | 04f_georgia_solar_learning_curve.md | The Georgia solar cost learning curve to 2035 (Bolinger method) | Claim anything about AI |
| 4g | 04g_results_pack.md | The paper tables, figures, findings.md and a number check for the Nov 24 draft | Run new models |
| 5 | 05_github_later.md | Decide how the project goes on GitHub (options only, nothing pushed) | Upload data |

## Rules every phase follows
1. **Read first:** CLAUDE.md, the newest file in docs/, and the project background in docs/2026-11-01/context-handoff-from-chat.md. Before Phase 1 has run, that file is CONTEXT_HANDOFF.md in the starter folder.
2. **Plan, then wait:** write a short plan, then wait for my OK before moving, renaming or creating anything.
3. **Follow my conventions:** use the project-conventions skill if you have it.
   - dated docs in docs/YYYY-MM-DD/<slug>.md, with the 04:00 day boundary (run `date` first)
   - a current-only CLAUDE.md
   - EXPERIMENTS.md as the spec file. Our Methods Memo is the spec of record, so keep a divergence register in it; docs/2026-11-01/methods-review.md lists the agreed changes.
   - dated results/ and logs/ folders
   - delete, don't comment out
4. **Never delete anything permanently** without listing it and getting my yes. Use a `_to_delete/` folder.
5. **Never edit raw data.** Never invent, impute or fill in data. If a file is missing or broken, say so and give its link from data/data_links.md.
6. **Don't download** what I already have. Only fetch something with download_all.py after I approve the specific list.
7. **Keep out of git:** raw data, interview recordings and transcripts, Emory-licensed data (Bloomberg, etc.) and anything with keys. Nothing gets pushed to GitHub until Phase 5.
8. **End of every phase:**
   - **(a)** a short runnable notebook notebooks/NN_<phase>.ipynb. It has markdown cells explaining what was done and why, and code cells that display the results.
   - **(b)** a handoff doc at docs/<date>/phase-N-<slug>.md. It has the five sections (what changed, why, decisions made, what did NOT change, follow-ups) plus "How to resume": the exact files to read and the next prompt to run.
   - **(c)** an update to CLAUDE.md §4 (project state) and §5 (next steps).
   - **(d)** a git commit of code and docs only.
   - **(e)** a short summary to me, then STOP. Don't start the next phase.

## People and names
- Use "Shunji Lewandowski" on all assignment materials.
- Alexander Hendricks is the data and finance side.
- Prof. Caroline Fohlin teaches ECON 499R.
- The project folder is "AI impact on Renewables". Look through all of it, every subfolder. It is the root for every phase.
- Literature PDFs already have APA names with (PR)/(w) prefixes. Never rename them.

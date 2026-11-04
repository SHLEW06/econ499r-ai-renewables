# Finish the analysis and package everything

ECON 499R (Shunji Lewandowski and Alexander Hendricks, Prof. Fohlin). The project root is the "AI impact on Renewables" folder. Core results are due Nov 17, the draft Nov 24, and the turn-in Dec 1.

**Read first:**
- CLAUDE.md
- EXPERIMENTS.md
- the newest handoffs in docs/
- data/receipts/ai_index.md
- prompts/04h_fang_test.md
- prompts/04e_robustness_stretch.md
- prompts/04f_georgia_solar_learning_curve.md
- prompts/04g_results_pack.md
- prompts/04i_master_workbook.md
- prompts/05_github_later.md

## How to run this
- Run `date`. Show me a one-screen plan with time estimates and wait for my OK. Then run sections 1-9 in order without stopping, except under the stop rules below.
- Keep a run log at docs/<date>/finish-run-log.md, and mark each section done once it's committed. If you're interrupted or hit a usage limit, resume from the first section not marked done.
- Commit after each section, one topic per commit.
- Stop and ask me only if:
  - a reproduction gate fails
  - a data check comes out red
  - something would need deleting
  - something would need a download not listed here, or a paid or licensed source
- All earlier rules still hold:
  - never edit raw data or invent data
  - clustered by state is the baseline, and Driscoll-Kraay is a sensitivity check only
  - write "associated with," not causal language
  - results are append-only, with tags
  - the Census key stays in .env and is never printed

## 1. H3 wording (decided)
Use this wording:

> "On 2015-2023, the only years the timing test can run, the renew_share spillover isn't significant, and with border weights neighbors' future AI carries the association rather than their past AI. The full-sample estimate (-0.161, p = 0.026) can't be separated from this reverse timing. H3 is not supported."

Apply it in the 4d and 4e notebooks, the handoffs, EXPERIMENTS.md and the readings block in prompts/04g_results_pack.md.

## 2. Fang test, Part B (prompts/04h_fang_test.md)
- First, identify "Lightcast's own series": which file, which measure, which years, and which states.
  - If it covers all states for several years from one version of the data, make it the main postings measure for the extension, and keep the stitched series as a check.
  - Otherwise, keep the plan.
- Then run Part B as planned:
  - the replication (2018-2021, N = 204, with the same-edition 2019-2021 row)
  - the bridge table
  - EPU moderation
  - results by renewable type
  - heterogeneity (splits and interactions)
  - the placebo
  - robustness
- Use both AI measures. Data-center jobs are the consistent one; say so wherever both appear.

## 3. Stretch goals (prompts/04e_robustness_stretch.md, part B)
1. The shift-share IV comes first. Report the first stage, the reduced form, the KP F and the KP rank test. If the F is below 10, call the IV uninformative.
2. Then broadband moderation (ACS 2016-2024, no 2020) and R&D moderation (NSF 2017-2023), each with its main effect. Report the AI slope at the 25th and 75th percentiles of each moderator.
3. Skip the Hansen threshold, and record it as not run with the reason.

## 4. Georgia solar module (prompts/04f_georgia_solar_learning_curve.md)
- For global capacity scenarios, search for published 2030 or 2035 global solar PV projections (IEA, IRENA, BNEF or similar). Use cited low, central and high paths, with the source and page for each.
- If you can't verify a source's numbers, label the paths "illustrative, based on historical growth" and say so.
- Never present anything as our own forecast.

## 5. Results pack (prompts/04g_results_pack.md), covering both tests
- Tables in LaTeX and CSV, and figures with captions.
- findings.md: one paragraph each for H1, H2 and H3, the Fang test and the Georgia box.
- number_check.csv, and memo-to-paper.md.
- A Methods section draft in LaTeX for Overleaf, saved as docs/<date>/methods_section.tex. It covers the equations, the variables and their sources, why each model was chosen, and how our design differs from the memo, from Zhang and from Fang.

## 6. Master data workbook
Follow prompts/04i_master_workbook.md.

## 7. Project summary
Write docs/<date>/project-summary.md, about 2 pages in plain English, with these parts:
- the question
- the data
- what we ran (model, data, N)
- the results, with numbers and whether each holds up
- the "what we can rule out" ranges (95% CI per one within-state SD of AI)
- what it means
- status and next steps
- where things are

Trace every number to a result tag in an appendix.

## 8. GitHub package (replaces prompts/05_github_later.md)
The current repo has copyrighted PDFs in its history, so don't push it. Build a clean copy instead.

1. **Build** release/github/econ499r-ai-renewables/ with:
   - code, executed notebooks, docs, receipts
   - the data dictionary
   - results tables and figures
   - the methods draft, findings and the summary
   - a README covering the question, data, methods, how to reproduce (from download_all.py), a results summary, the authors (Shunji Lewandowski and Alexander Hendricks) and the course
   - a .gitignore
2. **Cleaned data:** include a file only if every source behind it allows redistribution. List each source's license in DATA_LICENSES.md. Leave out anything unclear, and point to the download script instead.
3. **Never include:**
   - raw data
   - Bloomberg or any other licensed data
   - interview recordings or transcripts
   - journal PDFs or the Lazard PDF
   - .env or any key
   - personal emails
   - absolute paths
4. **Scan and commit:** scan for secrets and email addresses, and list every file over 50 MB (GitHub's limit is 100 MB). Then run git init there and make one commit. Don't add a remote and don't push; I'll do that by hand.
5. **Checklist:** write release/github/CHECKLIST.md listing what's in, what's out and why, and the exact commands I need to push.

## 9. Results and data package for me and Alexander
Build release/results_and_data_<date>/ with:
- the master workbook
- all cleaned data CSVs (this package stays local)
- the results tables and figures
- the notebooks as HTML
- the project summary, findings.md and the methods draft

Then zip it.

## When everything is done, show me:
- the replication and bridge tables
- the moderation and placebo results
- the IV first stage
- the Georgia projection table
- the summary
- the GitHub checklist
- the sizes of both packages

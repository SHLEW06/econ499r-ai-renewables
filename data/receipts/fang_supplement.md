# Receipt: Fang, Lee & Li (2025), supplementary material

**Status: filed 2026-11-07.** Downloaded by hand by the team through Emory Libraries (publisher material; kept out of git by `.gitignore`, rule `literature/*supplement*`).

| Original filename | New path | Source URL | Downloaded (file modified time) | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| `fang supplement.docx` | `literature/Fang_Lee_Li_2025_supplement.docx` | https://doi.org/10.1016/j.renene.2025.122969 (Appendix A, via Emory Libraries) | 2026-11-07 18:36 | 71,354 | `f2380bf5e80faf3a33ae3f014d63378c3e503bd8ba2433c2e51701861bdc0aa5` |

**Identified by content:** title "Assessing the impact of artificial intelligence on the transition to renewable energy? ... Supplementary Material". It holds Table A1 (descriptive statistics: N, mean, SD, min, max for ET, AI, EPU, EP, GDP, POP, EDU; N = 204), Table A2 (pairwise correlations), Table A3 (summary of results), Supplement B1 (robustness by changing the measurement, including the negative indicators coal, gas and petroleum consumption) and B2 (winsorized sample and added controls, including HDD and CDD). The docx passes `unzip -t`.

**Observations, read from the file:** in Table B1, columns (1) "ET, proportion of AI positions" and (2) "TRP, renewable production" have identical coefficients, t statistics and constants in every row. That looks like a duplicated column. In B2, Fang's extreme-weather controls are HDD and CDD, not event counts.

**Used for:** the section 1.1 comparison with Table A1, and the negative-indicator comparison with Supplement B1 (`EXPERIMENTS.md` section 14.6, B2).

An earlier file named `Fang Supplement.pdf` was the article itself (same SHA-256 as `literature/Assessing_AI_Impact_on_Renewable_Energy_Transition.pdf`) and is in `data/raw/_to_delete/`.

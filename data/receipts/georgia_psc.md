# Receipt: Georgia Power IRP and Large Load Reports

## Source

Georgia Public Service Commission (PSC) docket filings and Georgia Power Company publications.
- IRP filings: `https://www.georgiapower.com/company/about-us/integrated-resource-plan.html`
- Large Load reports: `https://www.georgiapower.com/content/dam/georgia-power/pdfs/company-pdfs/large-load-reports/`
- PSC docket search: `https://www.psc.state.ga.us/facets/`

## Raw Files

| File | Description | Approx. size | Obtained |
|---|---|---|---|
| `data/raw/georgia/2025_IRP_Main_Document.pdf` | 2025 Georgia Power IRP, main document | ~8 MB | `download_all.py`, 2026-11-01 |
| `data/raw/georgia/2025_IRP_TOC.pdf` | 2025 IRP table of contents | ~300 KB | `download_all.py`, 2026-11-01 |
| `data/raw/georgia/2025_IRP_one_page_summary.pdf` | 2025 IRP one-page summary | ~400 KB | `download_all.py`, 2026-11-01 |
| `data/raw/georgia/2023_IRP_Update_Main_Document.pdf` | 2023 IRP Update, main document | ~6 MB | `download_all.py`, 2026-11-01 |
| `data/raw/georgia/LargeLoad_Report_Q1_2026.pdf` | Large Load interconnection queue, Q1 2026 | ~2 MB | `download_all.py`, 2026-11-01 |
| `data/raw/georgia/dkt55378_large_load_report_q1_2026_attachment.xlsx` | Docket 55378 Large Load report, Q1 2026 attachment | 43 KB | Browser, Georgia PSC, 2026-11-01; moved here 2026-11-03 |
| `data/raw/georgia/dkt55378_large_load_report_q2_2026.zip` | Docket 55378 Large Load report, Q2 2026 (6 entries: folder, PDF, XLSX, assertion PDF, report DOCX, cover letter DOCX) | 1.2 MB | Browser, Georgia PSC, 2026-11-01; moved here 2026-11-03 |
| `data/raw/georgia/irp_2025_public_disclosure.zip` | 2025 IRP technical appendices, public disclosure (81 entries, including folders) | 104 MB | Browser, Georgia PSC, 2026-11-01; moved here 2026-11-03 |

**Note:** The Q2 2026 Large Load report and technical appendices to the 2025 IRP were
downloaded by hand from the Georgia PSC docket; they are not fetched automatically by
`download_all.py`. The three files added 2026-11-03 came from the former `data/georgia_psc/`
folder, and their SHA-256 hashes are in `logs/2026-11-03/phase4_moves.csv`. That folder's other
five PDFs matched files already listed here by hash, so those copies went to `_to_delete/`.

## What We Kept

These documents are reference material for the Georgia qualitative case box — they are not
processed into tabular data. Key figures extracted manually:

| Metric | Value | Source |
|---|---|---|
| Projected load growth (6-year horizon) | ~8,500 MW | 2025 IRP Main, executive summary |
| New renewables planned by 2035 | Up to 4,000 MW | 2025 IRP Main, resource plan section |
| Large Load queue size (Q1 2026) | ~40 GW of requests on file | LargeLoad_Report_Q1_2026.pdf |
| Data center / hyperscaler share of queue | Majority of new large-load inquiries | LargeLoad_Report_Q1_2026.pdf |
| 2023 IRP original load growth estimate | ~2,600 MW over plan period | 2023 IRP Update, p. 4 |

The jump from ~2,600 MW (2023 IRP) to ~8,500 MW (2025 IRP) in projected load growth
reflects the surge in data-center interconnection requests in 2024–2025 and is a central
data point for the Georgia case narrative.

## Transformations

None — PDFs are read and cited directly. Key figures are quoted in the paper with page
references. No automated parsing is performed; numbers above were transcribed manually.

## Known Quirks

- The 2025 IRP Main Document is large (~8 MB). The TOC PDF is useful for navigating to the
  right sections quickly.
- Georgia Power files IRPs on a roughly 3-year cycle; the 2025 IRP supersedes the 2023 Update
  for forward-looking projections but the 2023 document provides the pre-boom baseline.
- Large Load queue figures are not legally binding; some requests are duplicates or will be
  withdrawn. The report notes this caveat in its methodology section.
- Technical appendices (capacity expansion model assumptions, load forecast details) are in
  separate PSC docket exhibits and must be retrieved manually from the PSC docket system.

## Output

No tabular output. Findings feed directly into the Georgia case-study section of the paper.
Cite as: Georgia Power Company, *2025 Integrated Resource Plan*, filed with the Georgia PSC,
[date]. Large Load Report Q1 2026, Georgia Power Company.

## Script

`download_all.py` fetches the five files listed above. Manual browser download required for
Q2 2026 report and appendices.

## Raw file hashes

From `logs/2026-11-04/raw_sha256_manifest.csv`, recomputed 2026-11-04: 8 files.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data/raw/georgia/2023_IRP_Update_Main_Document.pdf` | 1,266,719 | `90385754caee266cc4ff0a34d8e90c75ef2963332513cb8f057dd32ef3d23922` |
| `data/raw/georgia/2025_IRP_Main_Document.pdf` | 3,038,316 | `0ff3f6e87e2d8b28abb39776d1ac5cc420818b872b407faeba4e5ee94b56225c` |
| `data/raw/georgia/2025_IRP_TOC.pdf` | 152,920 | `88ab1c93cb6ea2d70a3ab0747cbe90a45e34d7f41ae5d17428f62a77aa0f1cab` |
| `data/raw/georgia/2025_IRP_one_page_summary.pdf` | 141,915 | `45ce3cf13152482cb678d416e0dd9ac2fad59e77bf7cc2a67acb02393d1d32c9` |
| `data/raw/georgia/LargeLoad_Report_Q1_2026.pdf` | 841,648 | `5dfc4c931f75509f93ed7dc1b44307ddf613aa0f4397914b1330ab34aca703de` |
| `data/raw/georgia/dkt55378_large_load_report_q1_2026_attachment.xlsx` | 42,604 | `8c1e4da55b10b83643dc5fb8d9dc77d530368448c1bb613469ee0df38b96f0b9` |
| `data/raw/georgia/dkt55378_large_load_report_q2_2026.zip` | 1,192,071 | `52f89780cef574bfa888515a2d4a4b0e8366ac2cd4e30d29b95327ff0eb0ff55` |
| `data/raw/georgia/irp_2025_public_disclosure.zip` | 103,717,722 | `d72ddb87723475599f575acbef01438b08f5aacdf712e5f8fcb653d3ff9cbe6a` |

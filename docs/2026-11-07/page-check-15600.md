# Page check: 15,600 MW (team item 5, 2026-11-07)

**Question:** the Nov 4 notes cite the 15,600 MW commitment at p. 8 of the Q2 2026 Large Load report; pass 1 cited p. 5.

**Checked in the PDF** (`data/raw/georgia/dkt55378_large_load_report_q2_2026.zip`, file `DKT 55378 Lg Load Econ Dev Rept Q2 2026 PD.pdf`, 30 pages, text extracted with pdftotext):
- **PDF p. 5:** "the portfolio of large load customers committed to receiving service from Georgia Power has grown by 3,200 MW, reaching a total of 15,600 MW across 32 customers. By the winter of 2028/2029, these customers will represent a load of 8,700 MW."
- **PDF p. 8:** Table 2 (Commitments, Q2 2026, mid-2030s: 15,600), and "Customer commitments expanded from 3,600 MW to 15,600 MW, representing an increase of 12,000 MW."

**Result:** both pages state the figure. Every citation points to the page that states its claim:
- the Nov 4 project summary, `georgia_psc.md`, `build_georgia_tables.py` and the number checks cite p. 8 for the 3,600 → 15,600 MW change and Table 2
- pass 1 cites p. 5 for "15,600 MW across 32 customers" and 8,700 MW by winter 2028/2029

**No citation needed changing.** From now on: "across 32 customers" and "8,700 MW by 2028/2029" cite p. 5; "from 3,600 MW" and Table 2 cite p. 8. Page headers carry Docket No. 56002; the filing is in Docket No. 55378 (cover letter, p. 1, cites both).

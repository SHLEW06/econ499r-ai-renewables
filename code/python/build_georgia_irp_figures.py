#!/usr/bin/env python3
"""Georgia Power figures with verified cites, for the explained notebook (section 8).

Usage (from the project root):
    python3 code/python/build_georgia_irp_figures.py <YYYY-MM-DD>

Writes results/<date>/georgia/irp_figures.csv: one row per figure, with what it measures,
one document, the printed page and the PDF page. Every quote is checked against the text
of the PDF page cited (pdftotext, whitespace-normalized); the run stops if one isn't there.
The printed page follows each document's numbering: 2025 IRP main document, printed = PDF - 7;
Q1 and Q2 2026 large-load reports, printed = PDF - 4; one-page summary, printed = PDF.
Two totals are sums of table rows, and the script re-adds the rows to check them:
batteries (Attachment C.3) and the Plant Yates combustion turbines (Attachment C.1).
Pages were first located in results/2026-11-07/extend/tables/s2_georgia_irp_summary.md (pass 2).
"""
import csv, os, re, subprocess, sys, tempfile, zipfile

G = "data/raw/georgia"
IRP = f"{G}/2025_IRP_Main_Document.pdf"
SUM = f"{G}/2025_IRP_one_page_summary.pdf"
Q2Z = f"{G}/dkt55378_large_load_report_q2_2026.zip"
Q2M = "DKT 55378 Lg Load Econ Dev Rept Q2 2026 PD/DKT 55378 Lg Load Econ Dev Rept Q2 2026 PD.pdf"
OFFSET = {"irp": 7, "summary": 0, "q2": 4}
DOC = {"irp": "Georgia Power 2025 IRP, main document (Georgia PSC Docket 56002)",
       "summary": "Georgia Power 2025 IRP, one-page summary",
       "q2": "Georgia Power Q2 2026 Large Load Economic Development Report (Georgia PSC Docket 55378)"}

ROWS = [
 ("load_irp", "Load growth, IRP forecast", "about 8,200 MW", "Risk-adjusted load growth forecast from winter 2024/2025 through winter 2030/2031", "irp", 8, "reflects approximately 8,200 MW of load"),
 ("load_basis", "What the load forecast includes", "large-load pipeline", "The forecast includes the Company's pipeline of potential and committed large-load customers", "irp", 8, "potential and committed large load customers"),
 ("load_summary", "Load growth, approval summary", "about 8,500 MW", "Load growth over the next six years, as stated in the summary issued after the plan's approval", "summary", 1, "approximately 8,500 megawatts (MW) of electrical load growth"),
 ("batt_ct", "Batteries and combustion turbines", "more than 2,065 MW", "Battery storage and combustion turbines combined, added by the end of 2027", "irp", 10, "more than 2,065 MW of battery energy storage systems"),
 ("batteries", "Planned company-owned batteries", "about 780 MW, including 500 MW certified in 2024", "Nameplate capacity of the seven planned battery projects in Attachment C.3, in service 2026-2027 (our sum of the table rows)", "irp", 135, "2023 IRP UPDATE – MCGRAU FORD PHASE 2"),
 ("ct", "New combustion turbines", "1,323 MW (three units of 441 MW)", "Plant Yates Units 8-10, company-owned gas/oil turbines, summer capacity, in service 12/2026-08/2027", "irp", 133, "YATES 10"),
 ("coal", "Coal units kept running", "about 1,100 MW", "Extended operation of coal units at Plants Scherer and Gaston", "irp", 9, "approximately 1,100 MW at Plants Scherer and Gaston"),
 ("rfp_all", "Capacity requests for proposals", "up to 9,500 MW", "Active requests for proposals for capacity of any fuel, by the end of 2030", "irp", 10, "RFPs for up to 9,500 MW of capacity"),
 ("renew_2030", "Renewables, active requests", "more than 3,500 MW", "Renewable resources in active requests for proposals, by the end of 2030", "irp", 10, "more than 3,500 MW of renewable energy resources"),
 ("renew_2035", "Renewables, new requests", "up to 4,000 MW", "New requests for proposals for energy from renewable resources, by 2035", "irp", 67, "up to 4,000 MW of renewable resources by 2035"),
 ("commit_q2", "Large-load commitments", "15,600 MW across 32 customers", "Customer commitments as of June 30, 2026, for load scheduled through the mid-2030s", "q2", 5, "reaching a total of 15,600 MW"),
 ("commit_2829", "Commitments due by winter 2028/2029", "8,700 MW", "The near-term part of those commitments: load scheduled by winter 2028/2029", "q2", 5, "load of 8,700 MW"),
 ("commit_base", "Commitments in October 2023", "3,600 MW", "Commitments at the October 2023 IRP Update filing, the baseline both 2026 reports compare against", "q2", 8, "from 3,600 MW to 15,600 MW"),
 ("pipeline", "Large-load pipeline", "84,800 MW", "Economic-development pipeline through the mid-2030s, including prospects without commitments", "q2", 5, "to 84,800 MW"),
]


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("–", "–")).strip()


def page_text(path, pg):
    return subprocess.run(["pdftotext", "-layout", "-f", str(pg), "-l", str(pg), path, "-"], capture_output=True, text=True, check=True).stdout


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        sys.exit("usage: build_georgia_irp_figures.py <YYYY-MM-DD>")
    out_dir = f"results/{sys.argv[1]}/georgia"; os.makedirs(out_dir, exist_ok=True)
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(Q2Z) as z:
        q2 = z.extract(Q2M, tmp)
    files = {"irp": IRP, "summary": SUM, "q2": q2}
    shown = {"irp": IRP, "summary": SUM, "q2": f"{Q2Z} > {os.path.basename(Q2M)}"}
    out = []
    for fid, item, value, measures, doc, pdf_pg, quote in ROWS:
        txt = page_text(files[doc], pdf_pg)
        if norm(quote) not in norm(txt):
            sys.exit(f"STOP: quote for {fid} not on {doc} PDF p. {pdf_pg}: {quote!r}")
        printed = pdf_pg - OFFSET[doc]
        if doc != "summary":      # the page's own footer number must match the convention
            foot = [l.strip() for l in txt.splitlines() if re.fullmatch(r"\s*\d{1,3}\s*", l)]
            if not foot or int(foot[-1]) != printed:
                sys.exit(f"STOP: {fid}: printed page {printed} not found as the footer of PDF p. {pdf_pg} (found {foot[-1:]})")
        if fid == "batteries":
            bess = [float(x) for x in re.findall(r"(?:2019 BESS DEMO|FORT STEWART 4 HR BESS|MCGRAU FORD 2 HR BATTERY|2023 IRP UPDATE – HAMMOND|2023 IRP UPDATE – MCGRAU FORD PHASE 2|2023 IRP UPDATE – MOODY AFB|2023 IRP UPDATE – ROBINS AFB)\s+([\d.]+)\s+100%", norm(txt))]
            cert = [float(x) for x in re.findall(r"2023 IRP UPDATE – (?:HAMMOND|MCGRAU FORD PHASE 2|MOODY AFB|ROBINS AFB)\s+([\d.]+)\s+100%", norm(txt))]
            if len(bess) != 7 or round(sum(bess)) != 780 or round(sum(cert)) != 500:
                sys.exit(f"STOP: battery rows {bess} sum {sum(bess)}, certified {sum(cert)}")
        if fid == "ct":
            u = [float(x) for x in re.findall(r"YATES (?:8|9|10)\s+([\d.]+)\s", norm(txt))]
            if len(u) != 3 or round(sum(u)) != 1323:
                sys.exit(f"STOP: Yates rows {u}")
        out.append(dict(id=fid, item=item, value=value, measures=measures, document=DOC[doc], file=shown[doc],
                        printed_page=printed, pdf_page=pdf_pg, cite=f"p. {printed} [PDF p. {pdf_pg}]", quote=quote, verified="yes"))
    with open(f"{out_dir}/irp_figures.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
    print(f"{len(out)} figures verified -> {out_dir}/irp_figures.csv")


if __name__ == "__main__":
    main()

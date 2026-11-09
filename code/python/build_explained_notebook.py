#!/usr/bin/env python3
"""Build, run and export the plain-English notebook.

Usage (from the project root):
    python3 code/python/build_explained_notebook.py <YYYY-MM-DD>

1. Writes notebooks/ECON499R_explained.ipynb from code/python/explained_cells.txt
   (cells separated by lines that read "%%code").
2. Runs it top to bottom in a fresh kernel (nbconvert --execute), which writes
   results/<date>/explained/number_check.csv.
3. Exports it with code hidden (nbconvert --no-input) to outputs/ECON499R_Explained_<date>.html.
4. Prints that HTML to outputs/ECON499R_Explained_<date>.pdf with headless Chrome via Playwright,
   after MathJax has rendered the equations (Letter, about 0.5 in margins).
5. Checks every logged number appears in the exported text, and reports untraced decimals.
"""
import json, os, re, subprocess, sys, html as _html
import nbformat

ROOT = os.getcwd()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def build(nb_path, src):
    cells = [c.strip("\n") for c in open(src).read().split("%%code\n") if c.strip()]
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(c) for c in cells]
    nb.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                   "language_info": {"name": "python"}}
    nbformat.write(nb, nb_path)
    return len(cells)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-4000:]}")
    return r


def pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True)
        pg = b.new_page()
        pg.goto("file://" + os.path.abspath(html_path), wait_until="networkidle", timeout=120000)
        pg.wait_for_function("window.MathJax !== undefined", timeout=60000)
        pg.evaluate("""() => new Promise(res => {
            if (window.MathJax && MathJax.Hub && MathJax.Hub.Queue) { MathJax.Hub.Queue(res); }
            else if (window.MathJax && MathJax.typesetPromise) { MathJax.typesetPromise().then(res); }
            else { res(); } })""")
        pg.wait_for_timeout(1500)
        pg.emulate_media(media="print")
        pg.pdf(path=pdf_path, format="Letter", print_background=True,
               margin=dict(top="0.5in", bottom="0.55in", left="0.55in", right="0.55in"),
               display_header_footer=True, header_template="<span></span>",
               footer_template='<div style="font-size:8pt;color:#52514e;width:100%;text-align:center;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
        b.close()


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        sys.exit("usage: build_explained_notebook.py <YYYY-MM-DD>")
    date = sys.argv[1]
    nb_path = "notebooks/ECON499R_explained.ipynb"
    n = build(nb_path, "code/python/explained_cells.txt")
    print(f"notebook: {nb_path}, {n} cells")
    run(["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace",
         "--ExecutePreprocessor.timeout=600", "--ExecutePreprocessor.kernel_name=python3", nb_path])
    os.makedirs("outputs", exist_ok=True)
    base = f"ECON499R_Explained_{date}"
    run(["jupyter", "nbconvert", "--to", "html", "--no-input", "--no-prompt", "--output-dir", "outputs", "--output", base, nb_path])
    html_path, pdf_path = f"outputs/{base}.html", f"outputs/{base}.pdf"
    pdf(html_path, pdf_path)

    # numbers vs the exported text
    import pandas as pd
    ck_path = f"results/{date}/explained/number_check.csv"
    ck = pd.read_csv(ck_path, dtype=str)
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", open(html_path).read(), flags=re.S)
    text = _html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text)
    sys.path.insert(0, "code/python")
    from explained_helpers import deexpand
    text = deexpand(text)
    ck["in_exported_html"] = ["yes" if x in text else "NO" for x in ck.number]
    ck.loc[ck.in_exported_html == "NO", "status"] = "FAILED"
    ck.to_csv(ck_path, index=False)
    unl = pd.read_csv(f"results/{date}/explained/number_check_unlogged.csv")
    info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
    pages = re.search(r"Pages:\s+(\d+)", info).group(1)
    fonts = subprocess.run(["pdffonts", pdf_path], capture_output=True, text=True).stdout
    print(f"html: {html_path} ({os.path.getsize(html_path)/1e6:.1f} MB)")
    print(f"pdf: {pdf_path} ({os.path.getsize(pdf_path)/1e6:.1f} MB), {pages} pages")
    print(f"traced numbers: {len(ck)}; status ok: {(ck.status == 'ok').sum()}; FAILED: {(ck.status != 'ok').sum()}; untraced decimals: {len(unl)}")
    if len(unl):
        print(unl.to_string()[:3000])
    bad = ck[ck.status != "ok"]
    if len(bad):
        print(bad[["section", "number", "source_file", "column", "match", "in_notebook_text", "in_exported_html"]].to_string()[:3000])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download NSF National Patterns of R&D Resources Table 10 (R&D by state), 2017-2023.

Usage: download_nsf_tab10.py <raw_nsf_dir>

One edition per data year. Existing files are left alone. A file is kept only if it
is an xlsx (a zip). Prints size and sha256 for the receipt.
"""
import hashlib, os, subprocess, sys

EDITIONS = {2023: "nsf26313", 2022: "nsf25326", 2021: "nsf24318", 2020: "nsf23321",
            2019: "nsf22320", 2018: "nsf21325", 2017: "nsf20307"}
URL = "https://ncses.nsf.gov/pubs/{p}/assets/data-tables/tables/{p}-tab010.xlsx"


def main(out):
    os.makedirs(out, exist_ok=True)
    for year, pub in sorted(EDITIONS.items()):
        path = os.path.join(out, f"{pub}-tab010.xlsx")
        if os.path.exists(path):
            print(year, pub, "exists")
        else:
            tmp = path + ".part"
            r = subprocess.run(["curl", "-sSL", "--max-time", "90", "--retry", "2", "-A",
                                "Mozilla/5.0 (ECON499R research data pull)", "-w", "%{http_code}",
                                "-o", tmp, URL.format(p=pub)], capture_output=True, text=True)
            ok = r.stdout.strip() == "200" and os.path.exists(tmp) and open(tmp, "rb").read(2) == b"PK"
            if not ok:
                print(year, pub, "FAILED http", r.stdout.strip(), r.stderr.strip()[:200])
                if os.path.exists(tmp):
                    os.remove(tmp)
                continue
            os.replace(tmp, path)
        data = open(path, "rb").read()
        print(year, pub, len(data), hashlib.sha256(data).hexdigest(), URL.format(p=pub))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

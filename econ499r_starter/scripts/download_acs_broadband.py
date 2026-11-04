#!/usr/bin/env python3
"""Pull ACS 1-year S2801 household broadband for states, 2015-2024.

Usage: download_acs_broadband.py <env_file> <raw_acs_dir> <out_csv> <spot_check_csv>

The key is read only from <env_file> (CENSUS_KEY=...). It is sent as a request
parameter and is never printed or stored; responses are saved without it, and all
error text is scrubbed. The variable code is resolved each year from the Census
label because it changes: 2015 uses S2801_C02_012E ("With broadband subscription"),
where S2801_C02_014E means mobile broadband. There is no 2020 1-year release, so
2020 stays as NA rows with a reason.
"""
import json, os, re, sys
import pandas as pd
import requests

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
BASE = "https://api.census.gov/data/{y}/acs/acs1"
FIPS = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","11":"DC","12":"FL","13":"GA",
        "15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA",
        "26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY",
        "37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX",
        "49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY"}


def load_key(path):
    for line in open(path):
        m = re.match(r"\s*CENSUS_KEY\s*=\s*(.*?)\s*$", line)
        if m and m.group(1).strip("\"'"):
            return m.group(1).strip("\"'")
    sys.exit("CENSUS_KEY not set in env file")


def scrub(text, key):
    return str(text).replace(key, "<REDACTED>")


def get_json(url, params, key):
    try:
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # Exception text can contain the full URL, so only a scrubbed version is shown.
        sys.exit(f"request failed: {type(e).__name__}: {scrub(e, key)}")


def resolve_s2801(year, key):
    v = get_json(BASE.format(y=year) + "/subject/groups/S2801.json", {}, key)["variables"]
    want = {}
    for code, meta in v.items():
        lab = meta["label"]
        tail = lab.split("!!")[-1].rstrip(":")
        if "!!With an Internet subscription" in lab and tail in ("Broadband of any type", "With broadband subscription"):
            if code.endswith("E") and "C02" in code:
                want["pct"] = code; want["label"] = lab
            if code.endswith("E") and "C01" in code:
                want["count"] = code
        if tail == "Total households" and code.endswith("E") and "C01" in code:
            want["total"] = code
    if not {"pct", "count", "total"} <= set(want):
        sys.exit(f"could not resolve S2801 codes for {year}: {want}")
    want["moe"] = want["pct"][:-1] + "M"
    return want


def main(env_file, raw_dir, out_csv, spot_csv):
    key = load_key(env_file)
    os.makedirs(raw_dir, exist_ok=True)
    rows, codes = [], []
    for y in YEARS:
        if y == 2020:
            for st in FIPS.values():
                rows.append(dict(state=st, year=y, note="no 2020 ACS 1-year release"))
            codes.append(dict(year=y, code="none", label="no 2020 ACS 1-year release"))
            continue
        c = resolve_s2801(y, key)
        codes.append(dict(year=y, code=c["pct"], label=c["label"]))
        get = ",".join(["NAME", c["pct"], c["moe"], c["count"], c["total"]])
        data = get_json(BASE.format(y=y) + "/subject", {"get": get, "for": "state:*", "key": key}, key)
        json.dump(data, open(os.path.join(raw_dir, f"s2801_{y}.json"), "w"))
        h = data[0]
        for rec in data[1:]:
            d = dict(zip(h, rec))
            st = FIPS.get(d["state"])
            if st is None:  # Puerto Rico
                continue
            rows.append(dict(state=st, year=y, broadband_pct=float(d[c["pct"]]), broadband_pct_moe=float(d[c["moe"]]),
                             broadband_households=float(d[c["count"]]), total_households=float(d[c["total"]]),
                             census_var=c["pct"], note="2015 question wording differs; see receipt" if y == 2015 else ""))
        print(y, c["pct"], "|", c["label"][-70:], "| states", sum(1 for r in rows if r["year"] == y))
    df = pd.DataFrame(rows).sort_values(["state", "year"])
    df.to_csv(out_csv, index=False)
    pd.DataFrame(codes).to_csv(os.path.join(raw_dir, "s2801_variable_codes.csv"), index=False)
    print("wrote", out_csv, df.shape)

    # Spot check S2801 against the separate detailed table B28002, using one definition for
    # every year: (with a subscription - dial-up only) / total. Labels are verified first.
    chk = []
    for y in (2015, 2019, 2024):
        v = get_json(BASE.format(y=y) + "/groups/B28002.json", {}, key)["variables"]
        if not (v["B28002_002E"]["label"].endswith("With an Internet subscription") and "Dial-up" in v["B28002_003E"]["label"]):
            sys.exit(f"B28002 labels changed in {y}")
        d = get_json(BASE.format(y=y), {"get": "NAME,B28002_001E,B28002_002E,B28002_003E", "for": "state:13,51,56", "key": key}, key)
        for rec in d[1:]:
            r = dict(zip(d[0], rec)); st = FIPS[r["state"]]
            pub = float(df[(df.state == st) & (df.year == y)].broadband_pct.iloc[0])
            chk.append(dict(state=st, year=y, s2801_pct=pub,
                            b28002_pct=round(100 * (float(r["B28002_002E"]) - float(r["B28002_003E"])) / float(r["B28002_001E"]), 1)))
    pd.DataFrame(chk).to_csv(spot_csv, index=False)
    print(pd.DataFrame(chk).to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])

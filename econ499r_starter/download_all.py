"""Download every scriptable data file for the ECON 499R state panel.

Usage:
    python download_all.py                 # core panel + financials + stretch files
    python download_all.py --core-only     # only what build_panel.py needs
    python download_all.py --with-eia-forms  # also EIA-860/860M/923/861 plant- and utility-level zips (~80 MB)

Environment variables (optional):
    SEC_USER_AGENT   e.g. "Shunji Lewandowski your.email@emory.edu"  (SEC asks for a name and email)
    CENSUS_KEY       free key from https://api.census.gov/data/key_signup.html (broadband table)

Files land in ./raw/ in the layout scripts/build_panel.py and scripts/ferc_fin.py expect.
Files that need a browser (LBNL RPS spreadsheet, Georgia PSC docket filings) are listed in data_links.md.
"""
import argparse
import os
import sys
import time
import urllib.request
import zipfile

UA = 'Mozilla/5.0 (ECON499R student research)'
RAW = 'raw'
YEARS_QCEW = range(2014, 2026)

EIA_STATE = 'https://www.eia.gov/electricity/data/state/'
CORE = [
    (EIA_STATE + 'annual_generation_state.xlsx', 'eia/annual_generation_state.xlsx'),
    (EIA_STATE + 'existcapacity_annual.xlsx', 'eia/existcapacity_annual.xlsx'),
    (EIA_STATE + 'plancapacity_annual.xlsx', 'eia/plancapacity_annual.xlsx'),
    (EIA_STATE + 'annual_consumption_state.xlsx', 'eia/annual_consumption_state.xlsx'),
    (EIA_STATE + 'emission_annual.xlsx', 'eia/emission_annual.xlsx'),
    (EIA_STATE + 'xls/861/HS861%202010-.xlsx', 'eia/HS861_2010-.xlsx'),
    ('https://www.eia.gov/state/seds/sep_use/total/csv/use_all_btu.csv', 'eia/seds/use_all_btu.csv'),
    ('https://apps.bea.gov/regional/zip/SAGDP.zip', 'bea/SAGDP.zip'),
    ('https://apps.bea.gov/regional/zip/SAINC.zip', 'bea/SAINC.zip'),
    ('https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip', 'census/gaz_counties.zip'),
    ('https://www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2023.txt', 'census/county_adj.txt'),
]
for y in YEARS_QCEW:
    for code in ('518210', '5415', '10'):
        CORE.append((f'https://data.bls.gov/cew/data/api/{y}/a/industry/{code}.csv', f'bls/qcew_{y}_{code}.csv'))

PUDL = 'https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/stable/'
PUDL_TABLES = ['out_ferc1__yearly_income_statements_sched114', 'out_ferc1__yearly_plant_in_service_sched204',
               'out_ferc1__yearly_all_plants', 'out_ferc1__yearly_steam_plants_fuel_by_plant_sched402',
               'out_ferc1__yearly_utility_plant_summary_sched200', 'out_ferc1__yearly_rate_base',
               'out_ferc1__yearly_operating_revenues_sched300', 'out_eia__yearly_utilities', 'out_eia__yearly_plants',
               'out_rus12__yearly_statement_of_operations', 'out_rus7__yearly_statement_of_operations']
FIN = [(PUDL + t + '.parquet', f'pudl/{t}.parquet') for t in PUDL_TABLES]

GEORGIA = [
    ('https://www.selc.org/wp-content/uploads/2025/03/2025-IRP-Main-Document.pdf', 'georgia/2025_IRP_Main_Document.pdf'),
    ('https://www.selc.org/wp-content/uploads/2025/02/2025-IRP-TOC.pdf', 'georgia/2025_IRP_TOC.pdf'),
    ('https://www.georgiapower.com/content/dam/georgia-power/pdfs/about/2025-irp-one-page-summary.pdf', 'georgia/2025_IRP_one_page_summary.pdf'),
    ('https://georgiapower.com/content/dam/georgia-power/pdfs/company-pdfs/2023-irp-update-main-document.pdf', 'georgia/2023_IRP_Update_Main_Document.pdf'),
    ('https://services.psc.ga.gov/api/v1/External/Public/Get/Document/DownloadFile/226607/107887', 'georgia/LargeLoad_Report_Q1_2026.pdf'),
    ('https://www.lazard.com/media/kcfconhf/lazards-lcoeplus_vf.pdf', 'costs/Lazard_LCOEplus_2026.pdf'),
]

NSF_TAB10 = {2017: 'nsf20307', 2018: 'nsf21325', 2019: 'nsf22320', 2020: 'nsf23321', 2021: 'nsf24318', 2022: 'nsf25326', 2023: 'nsf26313'}
STRETCH = [(f'https://ncses.nsf.gov/pubs/{p}/assets/data-tables/tables/{p}-tab010.xlsx', f'nsf/state_rd_{y}_{p}_tab010.xlsx') for y, p in NSF_TAB10.items()]
STRETCH.append(('https://epoch.ai/data/data_centers/data_centers.csv', 'datacenters/epoch_frontier_data_centers.csv'))
# NOAA Climate at a Glance statewide codes: 1-48 = contiguous states in alphabetical order (degree days exist only for these)
NOAA_STATES = ['AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
               'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
               'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
NOAA = 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/{code}/{var}/12/12/2010-2025.csv'
for i, st in enumerate(NOAA_STATES, 1):
    for var in ('hdd', 'cdd'):
        STRETCH.append((NOAA.format(code=i, var=var), f'noaa/{st}_{var}.csv'))
# Alaska (code 50) has temperature but no degree-day series; Hawaii is not covered.

EIA_FORMS = [
    ('https://www.eia.gov/electricity/data/eia860/xls/eia8602025.zip', 'eia_forms/eia8602025.zip'),
    ('https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx', 'eia_forms/september_generator2026.xlsx'),
    ('https://www.eia.gov/electricity/data/eia923/xls/f923_2025.zip', 'eia_forms/f923_2025.zip'),
    ('https://www.eia.gov/electricity/data/eia861/zip/f8612025.zip', 'eia_forms/f8612025.zip'),
]


def fetch(url, rel, ua=UA, retries=3):
    path = os.path.join(RAW, rel)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return 'cached'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': ua})
            with urllib.request.urlopen(req, timeout=180) as r, open(path + '.part', 'wb') as f:
                f.write(r.read())
            os.replace(path + '.part', path)
            return 'ok'
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(2 * (attempt + 1))
    return f'FAILED ({err})'


def census_broadband(key):
    """ACS 1-year subject table S2801, percent of households with broadband of any type.
    The variable code changes across years; check https://api.census.gov/data/<year>/acs/acs1/subject/variables.html
    and edit VARS if a year fails. 2020 1-year standard estimates were not released."""
    VARS = {y: 'S2801_C02_014E' for y in (2017, 2018, 2019, 2021, 2022, 2023, 2024)}
    VARS.update({2015: 'S2801_C02_014E', 2016: 'S2801_C02_014E'})
    out = []
    for y, v in sorted(VARS.items()):
        url = f'https://api.census.gov/data/{y}/acs/acs1/subject?get=NAME,{v}&for=state:*&key={key}'
        out.append((y, fetch(url, f'census/acs_s2801_{y}.json')))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--core-only', action='store_true')
    ap.add_argument('--with-eia-forms', action='store_true')
    a = ap.parse_args()
    groups = [('core panel', CORE)]
    if not a.core_only:
        groups += [('utility financials (PUDL / FERC Form 1)', FIN), ('Georgia and cost documents', GEORGIA), ('stretch variables', STRETCH)]
    if a.with_eia_forms:
        groups.append(('EIA forms', EIA_FORMS))
    failed = []
    for name, items in groups:
        print(f'== {name}: {len(items)} files')
        for url, rel in items:
            s = fetch(url, rel)
            if s.startswith('FAILED'):
                failed.append((url, s))
            print(f'  {s:8s} {rel}')
    # unzip what build_panel.py reads
    for z, d in [('bea/SAGDP.zip', 'bea/sagdp'), ('bea/SAINC.zip', 'bea/sainc'), ('census/gaz_counties.zip', 'census')]:
        zp = os.path.join(RAW, z)
        if os.path.exists(zp):
            with zipfile.ZipFile(zp) as zf:
                zf.extractall(os.path.join(RAW, d))
    if os.environ.get('CENSUS_KEY') and not a.core_only:
        print('== Census ACS broadband'); print(census_broadband(os.environ['CENSUS_KEY']))
    print('\nSEC company financials: run  python scripts/sec_fin.py raw/sec/cache out/sec_company_financials.csv')
    print('(set SEC_USER_AGENT to "Your Name your@email" first; SEC asks for a contact)')
    if failed:
        print('\nFAILED downloads (open these in a browser):')
        for u, s in failed:
            print(' ', u, s)
        sys.exit(1)
    print('\nAll downloads done.')


if __name__ == '__main__':
    main()

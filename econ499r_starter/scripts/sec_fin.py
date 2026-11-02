"""Pull annual financials from SEC XBRL companyfacts for a list of power, utility, clean and fossil companies.
Usage: python3 -I sec_fin.py <cache_dir> <out_csv>
"""
import sys, os, json, time, subprocess
import pandas as pd

CACHE, OUT = sys.argv[1], sys.argv[2]
UA = os.environ.get('SEC_USER_AGENT', 'ECON499R student research (set SEC_USER_AGENT to "Name email")')
# (ticker, cik, group, note)
CO = [
 ('SO', 92122, 'Regulated utility (Georgia)', 'Parent of Georgia Power'),
 ('GA Power', 41091, 'Regulated utility (Georgia)', 'Georgia Power Co (Southern Co subsidiary, files its own 10-K)'),
 ('OPC', 788816, 'Regulated utility (Georgia)', 'Oglethorpe Power, Georgia generation co-op (bonds, no stock)'),
 ('NEE', 753308, 'Regulated utility + renewables developer', 'FPL plus NextEra Energy Resources'),
 ('DUK', 1326160, 'Regulated utility', ''), ('D', 715957, 'Regulated utility', ''), ('AEP', 4904, 'Regulated utility', ''),
 ('XEL', 72903, 'Regulated utility', ''), ('ETR', 65984, 'Regulated utility', ''), ('EXC', 1109357, 'Regulated utility', 'Wires only since 2022'),
 ('PCG', 1004980, 'Regulated utility', ''), ('EIX', 827052, 'Regulated utility', ''), ('FE', 1031296, 'Regulated utility', ''),
 ('PPL', 922224, 'Regulated utility', ''), ('AEE', 1002910, 'Regulated utility', ''), ('CMS', 811156, 'Regulated utility', ''),
 ('WEC', 783325, 'Regulated utility', ''), ('ES', 72741, 'Regulated utility', ''), ('ED', 1047862, 'Regulated utility', ''),
 ('DTE', 936340, 'Regulated utility', ''), ('EVRG', 1711269, 'Regulated utility', ''), ('PNW', 764622, 'Regulated utility', ''),
 ('SRE', 1032208, 'Regulated utility', ''), ('CNP', 1130310, 'Regulated utility', ''), ('NI', 1111711, 'Regulated utility', ''),
 ('LNT', 352541, 'Regulated utility', ''), ('OGE', 1021635, 'Regulated utility', ''), ('IDA', 1057877, 'Regulated utility', ''),
 ('AES', 874761, 'Renewables developer / yieldco', 'Large renewables arm plus utilities'),
 ('CWEN', 1567683, 'Renewables developer / yieldco', ''), ('ORA', 1296445, 'Renewables developer / yieldco', 'Geothermal'),
 ('XIFR', 1603145, 'Renewables developer / yieldco', 'Formerly NextEra Energy Partners (NEP)'),
 ('HASI', 1561894, 'Renewables developer / yieldco', 'Climate infrastructure investor'),
 ('FSLR', 1274494, 'Clean-tech equipment', 'Solar modules'), ('ENPH', 1463101, 'Clean-tech equipment', 'Solar inverters'),
 ('RUN', 1469367, 'Clean-tech equipment', 'Residential solar'), ('SEDG', 1419612, 'Clean-tech equipment', 'Solar inverters'),
 ('NXT', 1852131, 'Clean-tech equipment', 'Solar trackers'), ('ARRY', 1820721, 'Clean-tech equipment', 'Solar trackers'),
 ('FLNC', 1868941, 'Clean-tech equipment', 'Battery storage'),
 ('CEG', 1868275, 'Independent power producer', 'Mostly nuclear'), ('VST', 1692819, 'Independent power producer', 'Gas, coal, nuclear'),
 ('NRG', 1013871, 'Independent power producer', 'Gas, coal'), ('TLN', 1622536, 'Independent power producer', 'Nuclear, gas'),
 ('BTU', 1064728, 'Fossil fuel: coal', ''), ('CNR', 1710366, 'Fossil fuel: coal', 'CONSOL + Arch merger, 2025'),
 ('ARLP', 1086600, 'Fossil fuel: coal', ''), ('HCC', 1691303, 'Fossil fuel: coal', 'Metallurgical coal'),
 ('EQT', 33213, 'Fossil fuel: natural gas', ''), ('CTRA', 858470, 'Fossil fuel: natural gas', ''),
 ('AR', 1433270, 'Fossil fuel: natural gas', ''), ('RRC', 315852, 'Fossil fuel: natural gas', ''),
 ('EXE', 895126, 'Fossil fuel: natural gas', 'Formerly Chesapeake'),
 ('XOM', 34088, 'Fossil fuel: oil and gas', ''), ('CVX', 93410, 'Fossil fuel: oil and gas', ''),
 ('COP', 1163165, 'Fossil fuel: oil and gas', ''), ('OXY', 797468, 'Fossil fuel: oil and gas', ''),
 ('KMI', 1506307, 'Fossil fuel: pipelines', ''), ('WMB', 107263, 'Fossil fuel: pipelines', ''),
]
# concept -> list of XBRL tags tried in order; flows use CYyyyy frames, stocks use CYyyyyQ4I
FLOW = {
 'revenue': ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'RegulatedAndUnregulatedOperatingRevenue',
             'ElectricUtilityRevenue', 'RevenueFromContractWithCustomerIncludingAssessedTax', 'SalesRevenueNet'],
 'operating_income': ['OperatingIncomeLoss'],
 'net_income': ['NetIncomeLoss', 'ProfitLoss', 'NetIncomeLossAvailableToCommonStockholdersBasic'],
 'capex': ['PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets', 'PaymentsForCapitalImprovements',
           'PaymentsToAcquireOtherPropertyPlantAndEquipment'],
 'depreciation': ['DepreciationDepletionAndAmortization', 'DepreciationAndAmortization', 'Depreciation'],
 'operating_cash_flow': ['NetCashProvidedByUsedInOperatingActivities'],
}
STOCK = {
 'total_assets': ['Assets'],
 'ppe_net': ['PropertyPlantAndEquipmentNet', 'PublicUtilitiesPropertyPlantAndEquipmentNet'],
 'long_term_debt': ['LongTermDebtNoncurrent', 'LongTermDebt', 'LongTermDebtAndCapitalLeaseObligations'],
 'equity': ['StockholdersEquity', 'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest', 'PartnersCapital', 'MembersEquity'],
}
YEARS = range(2015, 2026)
os.makedirs(CACHE, exist_ok=True)
rows = []
for tk, cik, grp, note in CO:
    fp = f'{CACHE}/CIK{cik:010d}.json'
    if not os.path.exists(fp) or os.path.getsize(fp) < 1000:
        subprocess.run(['curl', '-s', '-m', '90', '-A', UA, '-o', fp, f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json'])
        time.sleep(0.25)
    try:
        j = json.load(open(fp))
    except Exception:
        print('FAILED', tk, cik); continue
    facts = j.get('facts', {}).get('us-gaap', {})
    def get(tags, instant):
        out, src = {}, {}
        for tag in tags:
            units = facts.get(tag, {}).get('units', {}).get('USD', [])
            for u in units:
                fr = u.get('frame', '')
                if instant and fr.endswith('Q4I') and len(fr) == 9:
                    y = int(fr[2:6])
                elif (not instant) and len(fr) == 6 and fr.startswith('CY'):
                    y = int(fr[2:6])
                else:
                    continue
                if y in YEARS and y not in out:
                    out[y] = u['val']; src[y] = tag
        return out, src
    vals = {}
    for k, tags in FLOW.items():
        vals[k] = get(tags, False)
    for k, tags in STOCK.items():
        vals[k] = get(tags, True)
    for y in YEARS:
        r = {'ticker': tk, 'cik': cik, 'company': j.get('entityName'), 'group': grp, 'note': note, 'year': y}
        any_val = False
        for k, (v, s) in vals.items():
            r[k + '_musd'] = round(v[y] / 1e6, 1) if y in v else None
            any_val |= y in v
        r['revenue_tag'] = vals['revenue'][1].get(y)
        if any_val:
            rows.append(r)
    print(tk, j.get('entityName'), sum(1 for r in rows if r['ticker'] == tk), 'years')
df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(df.shape)

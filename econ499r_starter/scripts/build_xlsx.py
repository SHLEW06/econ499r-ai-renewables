"""Assemble the ECON 499R data workbook. Usage: python3 -I build_xlsx.py <out_dir> <xlsx_path>"""
import sys
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment

OUT, XL = sys.argv[1], sys.argv[2]
F = 'Arial'
HDR = Font(name=F, bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='1F3864')
BODY = Font(name=F, size=10); BLUE = Font(name=F, size=10, color='0000FF'); BOLD = Font(name=F, size=10, bold=True)
TITLE = Font(name=F, size=14, bold=True)

panel = pd.read_csv(f'{OUT}/state_panel_2015_2025.csv')
ferc_u = pd.read_csv(f'{OUT}/ferc1_utility_financials.csv')
ferc_t = pd.read_csv(f'{OUT}/ferc1_cost_by_technology.csv')
ferc_p = pd.read_csv(f'{OUT}/ferc1_plant_costs.csv')
sec = pd.read_csv(f'{OUT}/sec_company_financials.csv')
pre = pd.read_csv(f'{OUT}/prelim_step1_slx.csv')
mor = pd.read_csv(f'{OUT}/prelim_morans_i.csv')
Wd = pd.read_csv(f'{OUT}/W_inverse_distance_rowstd.csv', index_col=0)
Wb = pd.read_csv(f'{OUT}/W_border_binary.csv', index_col=0)

wb = Workbook()

def header(ws, cols, row=1):
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=j, value=c)
        cell.font = HDR; cell.fill = HFILL; cell.alignment = Alignment(wrap_text=True, vertical='center')
    ws.freeze_panes = ws.cell(row=row + 1, column=3 if len(cols) > 6 else 1)

def write_df(ws, df, fmt=None, start=1, width=14):
    header(ws, list(df.columns), start)
    for i, rec in enumerate(df.itertuples(index=False), start + 1):
        for j, v in enumerate(rec, 1):
            if isinstance(v, float) and pd.isna(v):
                v = None
            c = ws.cell(row=i, column=j, value=v); c.font = BODY
            if fmt and df.columns[j - 1] in fmt:
                c.number_format = fmt[df.columns[j - 1]]
    for j, col in enumerate(df.columns, 1):
        ws.column_dimensions[get_column_letter(j)].width = max(10, min(width, len(str(col)) + 2)) if j > 2 else 16
    ws.auto_filter.ref = f'A{start}:{get_column_letter(len(df.columns))}{start + len(df)}'

# ---------------- README ----------------
ws = wb.active; ws.title = 'README'
lines = [
 ('ECON 499R starter data: U.S. state panel and power-sector financials', TITLE),
 ('Built Oct 30, 2026 for Shunji Lewandowski and Alexander Hendricks (Prof. Fohlin). All data public; downloaded Oct 30, 2026.', BODY),
 ('', BODY),
 ('Tabs', BOLD),
 ('Core Panel: 50 states + DC, 2015-2025. The Methods Memo variables. Blue = downloaded values; black = formulas you can audit.', BODY),
 ('Full Panel: same rows, every built variable (generation and capacity by fuel, sales by sector, CO2, SEDS, QCEW, BEA). Values only; also in state_panel_2015_2025.csv for R.', BODY),
 ('Codebook: definition, unit and source for every Full Panel column.', BODY),
 ('Prelim Results: first-pass Step 1 (two-way FE), SLX neighbor test, Step 2b and Moran\'s I, run in Python (pyfixest). Re-run in R before reporting.', BODY),
 ('FERC1 Utilities: income statement and plant in service by type (steam, nuclear, hydro, other, solar, wind, storage) for every FERC Form 1 filer, 2015-2025.', BODY),
 ('FERC1 Cost by Tech: book capital cost per kW, fuel and non-fuel cost per MWh, capacity factor, by technology and year (utility-owned plants only).', BODY),
 ('FERC1 Plants: the plant-level rows behind that summary.', BODY),
 ('SEC Companies: revenue, income, capex, assets, debt and equity for 58 SEC filers: power, utility, clean-energy and fossil-fuel companies (SEC XBRL, calendar-year frames).', BODY),
 ('W Inverse Distance / W Border: 50 x 50 spatial weight matrices for H3 (row-standardized inverse distance; binary shared border).', BODY),
 ('Sources: every file used, with links.', BODY),
 ('', BODY),
 ('Caveats', BOLD),
 ('1. NAICS 518210 (the AI measure) is "Computing infrastructure providers, data processing, web hosting." It counts all data processing and hosting jobs, not only AI data centers. Georgia ranks 2nd in 2025 (5.0 per 1,000), ahead of Virginia, so check which Georgia employers drive the count.', BODY),
 ('2. BLS suppresses 518210 for AK, ND, SD and WY in 2025; those cells are blank in dc_jobs and dc_wages_usd, not zero, with dc_suppressed = 1.', BODY),
 ('3. EIA generation is utility-scale only (1 MW and up); rooftop solar is not in renew_share. CO2 ends 2024; SEDS ends 2024.', BODY),
 ('4. FERC Form 1 covers investor-owned utilities only (Georgia Power yes; EMCs and MEAG no). Solar, wind and storage plant accounts exist only from the XBRL years (2021+); before that they sit in "other production."', BODY),
 ('5. SEC values are SEC-deduplicated calendar-year frames. NEE, DTE and HASI capex are blank because they use company-specific tags. Georgia Power has no standalone XBRL facts (it files inside Southern Co\'s 10-K); use FERC1 for Georgia Power.', BODY),
]
for i, (t, f) in enumerate(lines, 1):
    c = ws.cell(row=i, column=1, value=t); c.font = f
ws.column_dimensions['A'].width = 150

# ---------------- Core Panel with formulas ----------------
ws = wb.create_sheet('Core Panel')
raw = ['state', 'year', 'population', 'sales_mwh', 'revenue_kusd', 'gdp_real_musd2017', 'gdp_nom_musd', 'gdp_farm_musd',
       'gdp_manuf_musd', 'gen_total_mwh', 'gen_renew_mwh', 'gen_fossil_mwh', 'gen_solar_mwh', 'cap_renew_mw', 'dc_jobs',
       'tech5415_jobs', 'total_jobs', 'land_sqmi', 'ai_dc_per1000_lag1']
der = [('sales_mwh_pc', '=D{r}/C{r}', '0.00'), ('ln_ec', '=LN(T{r})', '0.000'),
       ('ee_usd_per_mwh', '=F{r}*1000000/D{r}', '#,##0'), ('ln_ee', '=LN(V{r})', '0.000'),
       ('renew_share', '=K{r}/J{r}', '0.0%'), ('solar_share', '=M{r}/J{r}', '0.0%'),
       ('fossil_to_renew', '=IF(K{r}>0,L{r}/K{r},"")', '0.00'),
       ('ai_dc_per1000', '=IF(O{r}="","",1000*O{r}/Q{r})', '0.000'),
       ('tech_share', '=IF(P{r}="","",P{r}/Q{r})', '0.00%'),
       ('price_c_kwh', '=100*E{r}/D{r}', '0.00'),
       ('ln_gdp_pc', '=LN(F{r}*1000000/C{r})', '0.000'),
       ('manuf_share', '=I{r}/G{r}', '0.0%'),
       ('ea_nonfarm_gdp_per_sqmi', '=(G{r}-H{r})*1000000/R{r}', '#,##0')]
cols = raw + [d[0] for d in der]
header(ws, cols)
for i, rec in enumerate(panel[raw].itertuples(index=False), 2):
    for j, v in enumerate(rec, 1):
        if isinstance(v, float) and pd.isna(v):
            v = None
        c = ws.cell(row=i, column=j, value=v)
        c.font = BLUE if j > 2 else BODY
        if j > 2:
            c.number_format = '#,##0' if raw[j - 1] != 'ai_dc_per1000_lag1' else '0.000'
    for k, (name, f, nf) in enumerate(der):
        c = ws.cell(row=i, column=len(raw) + 1 + k, value=f.format(r=i)); c.font = BODY; c.number_format = nf
for j, col in enumerate(cols, 1):
    ws.column_dimensions[get_column_letter(j)].width = 8 if j <= 2 else 15
ws['S1'].comment = Comment('Last year\'s data-center jobs per 1,000 workers, computed in Python from the prior-year QCEW file (2015 uses 2014 QCEW). Values, not a formula, because 2014 is not in this sheet.', 'Claude')
ws['O1'].comment = Comment('QCEW NAICS 518210, private ownership, annual average employment. Blank = suppressed by BLS.', 'Claude')
ws.auto_filter.ref = f'A1:{get_column_letter(len(cols))}{len(panel) + 1}'

# ---------------- Full Panel ----------------
ws = wb.create_sheet('Full Panel')
write_df(ws, panel)

# ---------------- Codebook ----------------
cb = {
 'state': ('Two-letter state code (50 states + DC)', '', ''),
 'year': ('Calendar year', '', ''),
 'gen_total_mwh': ('Net generation, all sources, Total Electric Power Industry', 'MWh', 'EIA annual_generation_state.xlsx'),
 'gen_renew_mwh': ('Hydro + wind + solar + geothermal + wood + other biomass generation (memo definition)', 'MWh', 'EIA annual_generation_state.xlsx'),
 'gen_fossil_mwh': ('Coal + natural gas + petroleum + other gases generation', 'MWh', 'EIA annual_generation_state.xlsx'),
 'renew_share': ('H1 energy-structure outcome: gen_renew_mwh / gen_total_mwh', 'share', 'derived'),
 'solar_share': ('Solar generation / total generation', 'share', 'derived'),
 'wind_share': ('Wind generation / total generation', 'share', 'derived'),
 'clean_share': ('(Renewables + nuclear) / total generation', 'share', 'derived'),
 'fossil_to_renew': ('Paper-matching check: fossil MWh / renewable MWh (lower = cleaner)', 'ratio', 'derived'),
 'cap_renew_mw': ('Nameplate capacity of renewable sources in service', 'MW', 'EIA existcapacity_annual.xlsx'),
 'new_renew_mw': ('Renewable build-out check: change in cap_renew_mw from prior year (can be negative after retirements)', 'MW', 'derived'),
 'new_solar_mw': ('Change in solar nameplate capacity from prior year', 'MW', 'derived'),
 'new_wind_mw': ('Change in wind nameplate capacity from prior year', 'MW', 'derived'),
 'sales_mwh': ('Retail electricity sales, all sectors', 'MWh', 'EIA HS861 2010-.xlsx'),
 'sales_res_mwh': ('Residential retail sales', 'MWh', 'EIA HS861'), 'sales_com_mwh': ('Commercial retail sales (data centers mostly here)', 'MWh', 'EIA HS861'),
 'sales_ind_mwh': ('Industrial retail sales', 'MWh', 'EIA HS861'),
 'revenue_kusd': ('Retail electricity revenue, all sectors', 'thousand $', 'EIA HS861'),
 'price_c_kwh': ('Control: average retail price = revenue / sales', 'cents/kWh', 'derived'),
 'price_com_c_kwh': ('Commercial average price', 'cents/kWh', 'derived'),
 'co2_power_t': ('CO2 from the electric power industry', 'metric tons', 'EIA emission_annual.xlsx (ends 2024)'),
 'co2_per_mwh_t': ('CO2 per MWh generated', 't/MWh', 'derived'),
 'seds_total_energy_bbtu': ('Total energy consumption, all fuels (SEDS series TETCB)', 'billion Btu', 'EIA SEDS use_all_btu.csv (ends 2024)'),
 'seds_mmbtu_pc': ('Paper-matching consumption check: SEDS total energy per person', 'MMBtu/person', 'derived'),
 'dc_jobs': ('NAICS 518210 annual average employment, private only. Government rows exist and are excluded; see data/ai_allown_518210.csv', 'jobs', 'BLS QCEW industry file 518210'),
 'dc_suppressed': ('1 if BLS suppressed 518210 for the state-year', '0/1', 'BLS QCEW'),
 'dc_wages_usd': ('NAICS 518210 total annual wages, private. Blank where dc_suppressed = 1', '$', 'BLS QCEW'),
 'tech5415_jobs': ('NAICS 5415 computer systems design employment, private', 'jobs', 'BLS QCEW industry file 5415'),
 'tech5415_suppressed': ('1 if BLS suppressed 5415', '0/1', 'BLS QCEW'),
 'total_jobs': ('All-industry employment, total covered (industry 10, own 0)', 'jobs', 'BLS QCEW industry file 10'),
 'ai_dc_per1000': ('Cause: private data-center jobs per 1,000 workers = 1,000 x dc_jobs / total_jobs (memo Section 3; private only by team decision)', 'per 1,000 workers', 'derived'),
 'ai_dc_per1000_lag1': ('Cause, lagged one year (enters Step 1): private data-center jobs per 1,000 workers', 'per 1,000 workers', 'derived'),
 'tech_share': ('hum for HMA, or the H2a mediator directly: tech5415_jobs / total_jobs', 'share', 'derived'),
 'gdp_nom_musd': ('GDP, all industries, current dollars', '$ million', 'BEA SAGDP2 line 1'),
 'gdp_farm_musd': ('GDP, farms', '$ million', 'BEA SAGDP2 line 4'),
 'gdp_manuf_musd': ('GDP, manufacturing', '$ million', 'BEA SAGDP2 line 12'),
 'gdp_real_musd2017': ('Real GDP, chained 2017 dollars', '$ million (2017)', 'BEA SAGDP9 line 1'),
 'population': ('Resident population', 'persons', 'BEA SAINC1 line 2'),
 'land_sqmi': ('Land area (sum of 2020 county land areas)', 'sq mi', 'Census 2020 county Gazetteer'),
 'sales_mwh_pc': ('MWh sold per person', 'MWh/person', 'derived'),
 'ln_ec': ('H1 consumption outcome: ln(sales_mwh_pc)', 'log', 'derived'),
 'ee_usd_per_mwh': ('Real GDP per MWh sold', '2017 $/MWh', 'derived'),
 'ln_ee': ('H1 efficiency outcome: ln(ee_usd_per_mwh)', 'log', 'derived'),
 'ln_gdp_pc': ('Control: ln real GDP per person', 'log', 'derived'),
 'manuf_share': ('Control: manufacturing share of nominal GDP', 'share', 'derived'),
 'pop_growth': ('Control: population growth from prior year', 'share', 'derived'),
 'ea_nonfarm_gdp_per_sqmi': ('H2b mediator: nonfarm nominal GDP / land area', '$/sq mi', 'derived'),
 'ln_ea': ('ln of ea_nonfarm_gdp_per_sqmi', 'log', 'derived'),
 'energy_equity': ('Stretch threshold variable: state share of U.S. GDP / state share of U.S. retail MWh', 'ratio', 'derived'),
 'hma': ('Paper eq. 2 coupling index of range-standardized AI and tech_share (0 to 1)', 'index', 'derived'),
 'contig48': ('1 if in the contiguous 48 (+DC)', '0/1', ''), 'is_dc': ('1 for District of Columbia (drop for the 50-state sample)', '0/1', ''),
}
rows = []
for c in panel.columns:
    if c in cb:
        d, u, s = cb[c]
    elif c.startswith('gen_'):
        d, u, s = (f'Net generation from {c[4:-4]}', 'MWh', 'EIA annual_generation_state.xlsx')
    elif c.startswith('cap_'):
        d, u, s = (f'Nameplate capacity, {c[4:-3]}', 'MW', 'EIA existcapacity_annual.xlsx')
    else:
        d, u, s = ('', '', '')
    rows.append({'variable': c, 'definition': d, 'unit': u, 'source': s, 'non-missing 2015-2025': int(panel[c].notna().sum())})
ws = wb.create_sheet('Codebook')
cbd = pd.DataFrame(rows)
write_df(ws, cbd)
ws.column_dimensions['A'].width = 26; ws.column_dimensions['B'].width = 90; ws.column_dimensions['C'].width = 16; ws.column_dimensions['D'].width = 40

# ---------------- Prelim Results ----------------
ws = wb.create_sheet('Prelim Results')
ws['A1'] = 'First-pass results (Python pyfixest, run Oct 30, 2026). 50 states, 2015-2025, N = 550. State and year fixed effects; SEs clustered by state; outcomes and AI winsorized at 1st/99th percentiles.'
ws['A1'].font = BOLD
ws['A2'] = 'Controls: ln GDP per person, manufacturing share, average electricity price, population growth. AI = last year\'s data-center jobs per 1,000 workers. SLX adds the inverse-distance-weighted average of neighbors\' lagged AI (theta).'
ws['A2'].font = BODY
pre2 = pre.copy()
write_df(ws, pre2.round(4), start=4, width=18)
r0 = 4 + len(pre2) + 3
ws.cell(row=r0 - 1, column=1, value="Moran's I (inverse-distance W, 999 permutations; p = share of permutations at least as large)").font = BOLD
for j, c in enumerate(mor.columns, 1):
    cell = ws.cell(row=r0, column=j, value=c); cell.font = HDR; cell.fill = HFILL
for i, rec in enumerate(mor.itertuples(index=False), r0 + 1):
    for j, v in enumerate(rec, 1):
        ws.cell(row=i, column=j, value=v).font = BODY
r1 = r0 + len(mor) + 3
ws.cell(row=r1, column=1, value='Step 2b (H2a): tech_share (pct points) on lagged AI with the same controls and FE: b = -0.0165, SE 0.0208, p = 0.43. AI does not move the tech-worker share within states.').font = BODY
ws.freeze_panes = None

# ---------------- FERC sheets ----------------
ws = wb.create_sheet('FERC1 Utilities'); write_df(ws, ferc_u, fmt={c: '#,##0.0' for c in ferc_u.columns if c.endswith('_musd')})
ws.column_dimensions['C'].width = 40
ws = wb.create_sheet('FERC1 Cost by Tech'); write_df(ws, ferc_t, fmt={'capacity_mw': '#,##0', 'net_generation_mwh': '#,##0', 'book_capex_usd_per_kw': '#,##0', 'nonfuel_opex_usd_per_mwh': '0.00', 'fuel_usd_per_mwh': '0.00', 'total_opex_usd_per_mwh': '0.00', 'capacity_factor': '0.0%'}, width=18)
ws.column_dimensions['A'].width = 30
ws = wb.create_sheet('FERC1 Plants'); write_df(ws, ferc_p)
ws = wb.create_sheet('SEC Companies'); write_df(ws, sec, fmt={c: '#,##0.0' for c in sec.columns if c.endswith('_musd')})
ws.column_dimensions['C'].width = 36; ws.column_dimensions['D'].width = 34

# ---------------- W matrices ----------------
for name, M, nf in [('W Inverse Distance', Wd, '0.0000'), ('W Border', Wb, '0')]:
    ws = wb.create_sheet(name)
    ws.cell(row=1, column=1, value='state').font = HDR; ws.cell(row=1, column=1).fill = HFILL
    for j, c in enumerate(M.columns, 2):
        cell = ws.cell(row=1, column=j, value=c); cell.font = HDR; cell.fill = HFILL
    for i, (idx, rec) in enumerate(M.iterrows(), 2):
        ws.cell(row=i, column=1, value=idx).font = BOLD
        for j, v in enumerate(rec.values, 2):
            c = ws.cell(row=i, column=j, value=float(v)); c.font = BODY; c.number_format = nf
    ws.freeze_panes = 'B2'
    for j in range(1, len(M.columns) + 2):
        ws.column_dimensions[get_column_letter(j)].width = 7

# ---------------- Sources ----------------
src = [
 ('EIA state electricity data (generation, capacity, sales/revenue, emissions)', 'https://www.eia.gov/electricity/data/state/', 'annual_generation_state.xlsx, existcapacity_annual.xlsx, HS861 2010-.xlsx, emission_annual.xlsx'),
 ('EIA SEDS consumption', 'https://www.eia.gov/state/seds/sep_use/total/csv/use_all_btu.csv', 'Series TETCB'),
 ('BLS QCEW annual industry files', 'https://data.bls.gov/cew/data/api/2025/a/industry/518210.csv', 'Same pattern for 5415 and 10, years 2014-2025'),
 ('BEA state GDP (SAGDP) and income/population (SAINC)', 'https://apps.bea.gov/regional/zip/SAGDP.zip', 'SAGDP2, SAGDP9; SAINC.zip for SAINC1'),
 ('Census 2020 county Gazetteer (land area, centroids)', 'https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip', 'State land = sum of counties; centroid = land-weighted'),
 ('Census county adjacency 2023 (border matrix)', 'https://www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2023.txt', ''),
 ('FERC Form 1 via Catalyst Cooperative PUDL (stable release, Oct 14, 2026)', 'https://data.catalyst.coop/', 'out_ferc1__yearly_income_statements_sched114, _plant_in_service_sched204, _all_plants, _steam_plants_fuel_by_plant_sched402; out_eia__yearly_utilities'),
 ('SEC XBRL company facts API', 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000092122.json', 'One JSON per CIK (Southern Co shown)'),
]
ws = wb.create_sheet('Sources')
write_df(ws, pd.DataFrame(src, columns=['dataset', 'url', 'files / notes']), width=60)
ws.column_dimensions['A'].width = 60; ws.column_dimensions['B'].width = 90; ws.column_dimensions['C'].width = 90

for s in wb.worksheets:
    s.sheet_view.zoomScale = 90
wb.save(XL)
print('saved', XL)

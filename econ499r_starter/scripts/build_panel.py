"""Build the ECON 499R state-year panel (50 states + DC, 2015-2025) from raw federal files.
Usage: python3 -I build_panel.py <raw_dir> <out_dir>
"""
import sys, os, math
import numpy as np
import pandas as pd

RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
Y0, Y1 = 2010, 2025          # build from 2010 so lags and growth exist for 2015
STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA',
          'MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX',
          'UT','VT','VA','WA','WV','WI','WY']
FIPS = {'AL':'01','AK':'02','AZ':'04','AR':'05','CA':'06','CO':'08','CT':'09','DE':'10','DC':'11','FL':'12','GA':'13',
        'HI':'15','ID':'16','IL':'17','IN':'18','IA':'19','KS':'20','KY':'21','LA':'22','ME':'23','MD':'24','MA':'25',
        'MI':'26','MN':'27','MS':'28','MO':'29','MT':'30','NE':'31','NV':'32','NH':'33','NJ':'34','NM':'35','NY':'36',
        'NC':'37','ND':'38','OH':'39','OK':'40','OR':'41','PA':'42','RI':'44','SC':'45','SD':'46','TN':'47','TX':'48',
        'UT':'49','VT':'50','VA':'51','WA':'53','WV':'54','WI':'55','WY':'56'}
FIPS2ST = {v: k for k, v in FIPS.items()}
idx = pd.MultiIndex.from_product([STATES, range(Y0, Y1 + 1)], names=['state', 'year'])
P = pd.DataFrame(index=idx)

# ---------- EIA net generation ----------
g = pd.read_excel(f'{RAW}/eia/annual_generation_state.xlsx', header=1)
g.columns = ['year', 'state', 'producer', 'source', 'mwh']
g['state'] = g['state'].str.strip().str.upper()
g = g[(g.producer == 'Total Electric Power Industry') & g.state.isin(STATES) & g.year.between(Y0, Y1)]
gp = g.pivot_table(index=['state', 'year'], columns='source', values='mwh', aggfunc='sum').fillna(0)
gmap = {'Total': 'gen_total_mwh', 'Coal': 'gen_coal_mwh', 'Natural Gas': 'gen_gas_mwh', 'Petroleum': 'gen_petroleum_mwh',
        'Other Gases': 'gen_othergas_mwh', 'Nuclear': 'gen_nuclear_mwh', 'Hydroelectric Conventional': 'gen_hydro_mwh',
        'Wind': 'gen_wind_mwh', 'Solar Thermal and Photovoltaic': 'gen_solar_mwh', 'Geothermal': 'gen_geothermal_mwh',
        'Wood and Wood Derived Fuels': 'gen_wood_mwh', 'Other Biomass': 'gen_otherbio_mwh',
        'Pumped Storage': 'gen_pumpedstorage_mwh', 'Other': 'gen_other_mwh'}
gp = gp.rename(columns=gmap)[[v for v in gmap.values() if v in gp.rename(columns=gmap).columns]]
P = P.join(gp)
P['gen_renew_mwh'] = P[['gen_hydro_mwh', 'gen_wind_mwh', 'gen_solar_mwh', 'gen_geothermal_mwh', 'gen_wood_mwh', 'gen_otherbio_mwh']].sum(axis=1)
P['gen_fossil_mwh'] = P[['gen_coal_mwh', 'gen_gas_mwh', 'gen_petroleum_mwh', 'gen_othergas_mwh']].sum(axis=1)
P['renew_share'] = P.gen_renew_mwh / P.gen_total_mwh
P['solar_share'] = P.gen_solar_mwh / P.gen_total_mwh
P['wind_share'] = P.gen_wind_mwh / P.gen_total_mwh
P['clean_share'] = (P.gen_renew_mwh + P.gen_nuclear_mwh) / P.gen_total_mwh
P['fossil_to_renew'] = P.gen_fossil_mwh / P.gen_renew_mwh.replace(0, np.nan)

# ---------- EIA capacity ----------
c = pd.read_excel(f'{RAW}/eia/existcapacity_annual.xlsx', header=1)
c.columns = ['year', 'state', 'producer', 'source', 'generators', 'facilities', 'nameplate_mw', 'summer_mw']
c['state'] = c['state'].astype(str).str.strip().str.upper()
c = c[(c.producer == 'Total Electric Power Industry') & c.state.isin(STATES) & c.year.between(Y0, Y1)]
c['nameplate_mw'] = pd.to_numeric(c.nameplate_mw, errors='coerce')
cp = c.pivot_table(index=['state', 'year'], columns='source', values='nameplate_mw', aggfunc='sum').fillna(0)
cmap = {'All Sources': 'cap_total_mw', 'Coal': 'cap_coal_mw', 'Natural Gas': 'cap_gas_mw', 'Petroleum': 'cap_petroleum_mw',
        'Nuclear': 'cap_nuclear_mw', 'Hydroelectric': 'cap_hydro_mw', 'Wind': 'cap_wind_mw',
        'Solar Thermal and Photovoltaic': 'cap_solar_mw', 'Geothermal': 'cap_geothermal_mw',
        'Wood and Wood Derived Fuels': 'cap_wood_mw', 'Other Biomass': 'cap_otherbio_mw', 'Other': 'cap_other_mw',
        'Pumped Storage': 'cap_pumpedstorage_mw', 'Other Gases': 'cap_othergas_mw'}
cp = cp.rename(columns=cmap)[[v for v in cmap.values() if v in cp.rename(columns=cmap).columns]]
P = P.join(cp)
P['cap_renew_mw'] = P[['cap_hydro_mw', 'cap_wind_mw', 'cap_solar_mw', 'cap_geothermal_mw', 'cap_wood_mw', 'cap_otherbio_mw']].sum(axis=1)
P['new_renew_mw'] = P.groupby(level='state').cap_renew_mw.diff()
P['new_solar_mw'] = P.groupby(level='state').cap_solar_mw.diff()
P['new_wind_mw'] = P.groupby(level='state').cap_wind_mw.diff()

# ---------- EIA retail sales, revenue, price (HS861) ----------
s = pd.read_excel(f'{RAW}/eia/HS861_2010-.xlsx', header=None, skiprows=3)
s = s.iloc[:, :22]
s.columns = ['year', 'state'] + [f'{sec}_{v}' for sec in ['res', 'com', 'ind', 'trans', 'tot'] for v in ['rev_k', 'sales_mwh', 'cust', 'price']]
s = s[pd.to_numeric(s.year, errors='coerce').notna()]
s['year'] = s.year.astype(int); s['state'] = s.state.astype(str).str.strip().str.upper()
s = s[s.state.isin(STATES) & s.year.between(Y0, Y1)]
for col in s.columns[2:]:
    s[col] = pd.to_numeric(s[col], errors='coerce')
s = s.groupby(['state', 'year']).sum(numeric_only=True)
P['sales_mwh'] = s.tot_sales_mwh
P['sales_res_mwh'] = s.res_sales_mwh
P['sales_com_mwh'] = s.com_sales_mwh
P['sales_ind_mwh'] = s.ind_sales_mwh
P['revenue_kusd'] = s.tot_rev_k
P['price_c_kwh'] = 100 * (s.tot_rev_k * 1000) / (s.tot_sales_mwh * 1000)   # cents per kWh = revenue/sales
P['price_com_c_kwh'] = 100 * (s.com_rev_k * 1000) / (s.com_sales_mwh * 1000)

# ---------- EIA CO2 from electricity ----------
e = pd.read_excel(f'{RAW}/eia/emission_annual.xlsx', header=0)
e.columns = ['year', 'state', 'producer', 'source', 'co2_t', 'so2_t', 'nox_t']
e['state'] = e.state.astype(str).str.strip().str.upper()
e = e[(e.producer.str.contains('Total Electric Power Industry')) & (e.source == 'All Sources') & e.state.isin(STATES) & e.year.between(Y0, Y1)]
P['co2_power_t'] = e.groupby(['state', 'year']).co2_t.sum()
P['co2_per_mwh_t'] = P.co2_power_t / P.gen_total_mwh

# ---------- EIA SEDS total energy consumption (paper-matching check) ----------
sd = pd.read_csv(f'{RAW}/eia/seds/use_all_btu.csv')
sd = sd[(sd.MSN == 'TETCB') & sd.State.isin(STATES)]
sd = sd.melt(id_vars=['Data_Status', 'State', 'MSN'], var_name='year', value_name='v')
sd['year'] = pd.to_numeric(sd.year, errors='coerce'); sd = sd[sd.year.between(Y0, Y1)]
P['seds_total_energy_bbtu'] = sd.set_index(['State', 'year']).v.rename_axis(['state', 'year'])

# ---------- BLS QCEW ----------
rows = []
for y in range(2014, Y1 + 1):
    def rd(code):
        q = pd.read_csv(f'{RAW}/bls/qcew_{y}_{code}.csv', dtype={'area_fips': str, 'disclosure_code': str}, low_memory=False)
        q = q[q.area_fips.str.endswith('000') & q.area_fips.str[:2].isin(FIPS2ST.keys())]
        q['state'] = q.area_fips.str[:2].map(FIPS2ST)
        return q
    dc = rd('518210'); dc = dc[(dc.own_code == 5) & (dc.agglvl_code == 58)]
    it = rd('5415'); it = it[(it.own_code == 5) & (it.agglvl_code == 56)]
    tt = rd('10'); tt = tt[(tt.own_code == 0) & (tt.agglvl_code == 50)]
    for st in STATES:
        d = dc[dc.state == st]; i = it[it.state == st]; t = tt[tt.state == st]
        rows.append({'state': st, 'year': y,
                     'dc_jobs': d.annual_avg_emplvl.iloc[0] if len(d) else np.nan,
                     'dc_suppressed': int(len(d) == 0 or str(d.disclosure_code.iloc[0]) == 'N'),
                     'dc_wages_usd': d.total_annual_wages.iloc[0] if len(d) else np.nan,
                     'tech5415_jobs': i.annual_avg_emplvl.iloc[0] if len(i) else np.nan,
                     'tech5415_suppressed': int(len(i) == 0 or str(i.disclosure_code.iloc[0]) == 'N'),
                     'total_jobs': t.annual_avg_emplvl.iloc[0] if len(t) else np.nan})
q = pd.DataFrame(rows).set_index(['state', 'year'])
q.loc[q.dc_suppressed == 1, 'dc_jobs'] = np.nan
q.loc[q.tech5415_suppressed == 1, 'tech5415_jobs'] = np.nan
P = P.join(q)
P['ai_dc_per1000'] = 1000 * P.dc_jobs / P.total_jobs
P['tech_share'] = P.tech5415_jobs / P.total_jobs

# ---------- BEA GDP and population ----------
def bea(table, line, start):
    d = pd.read_csv(f'{RAW}/bea/sagdp/{table}__ALL_AREAS_{start}_2025.csv', encoding='latin1', low_memory=False, dtype={'GeoFIPS': str})
    d['GeoFIPS'] = d.GeoFIPS.str.strip().str.strip('"').str.strip()
    d = d[(pd.to_numeric(d.LineCode, errors='coerce') == line) & d.GeoFIPS.str[:2].isin(FIPS2ST.keys()) & d.GeoFIPS.str.endswith('000')]
    d['state'] = d.GeoFIPS.str[:2].map(FIPS2ST)
    yrs = [str(y) for y in range(Y0, Y1 + 1)]
    d = d.melt(id_vars=['state'], value_vars=yrs, var_name='year', value_name='v')
    d['year'] = d.year.astype(int); d['v'] = pd.to_numeric(d.v, errors='coerce')
    return d.set_index(['state', 'year']).v
P['gdp_nom_musd'] = bea('SAGDP2', 1, 1997)
P['gdp_farm_musd'] = bea('SAGDP2', 4, 1997)
P['gdp_manuf_musd'] = bea('SAGDP2', 12, 1997)
P['gdp_real_musd2017'] = bea('SAGDP9', 1, 1997)
pi = pd.read_csv(f'{RAW}/bea/sainc/SAINC1__ALL_AREAS_1929_2025.csv', encoding='latin1', low_memory=False, dtype={'GeoFIPS': str})
pi['GeoFIPS'] = pi.GeoFIPS.str.strip().str.strip('"').str.strip()
pi = pi[(pd.to_numeric(pi.LineCode, errors='coerce') == 2) & pi.GeoFIPS.str[:2].isin(FIPS2ST.keys()) & pi.GeoFIPS.str.endswith('000')]
pi['state'] = pi.GeoFIPS.str[:2].map(FIPS2ST)
pi = pi.melt(id_vars=['state'], value_vars=[str(y) for y in range(Y0, Y1 + 1)], var_name='year', value_name='v')
pi['year'] = pi.year.astype(int)
P['population'] = pd.to_numeric(pi.set_index(['state', 'year']).v, errors='coerce')

# ---------- Census land area and centroids (from 2020 county gazetteer) ----------
gz = pd.read_csv(f'{RAW}/census/2020_Gaz_counties_national.txt', sep='\t', dtype={'GEOID': str})
gz.columns = [x.strip() for x in gz.columns]
gz = gz[gz.USPS.isin(STATES)]
land = gz.groupby('USPS').ALAND_SQMI.sum()
cen = gz.groupby('USPS').apply(lambda d: pd.Series({'lat': np.average(d.INTPTLAT, weights=d.ALAND_SQMI),
                                                    'lon': np.average(d.INTPTLONG, weights=d.ALAND_SQMI)}), include_groups=False)
P = P.reset_index()
P['land_sqmi'] = P.state.map(land)

# ---------- Derived variables (memo definitions) ----------
P['sales_mwh_pc'] = P.sales_mwh / P.population
P['ln_ec'] = np.log(P.sales_mwh_pc)                                   # H1 consumption
P['ee_usd_per_mwh'] = P.gdp_real_musd2017 * 1e6 / P.sales_mwh         # real 2017 $ of GDP per MWh sold
P['ln_ee'] = np.log(P.ee_usd_per_mwh)                                 # H1 efficiency
P['seds_mmbtu_pc'] = P.seds_total_energy_bbtu * 1000 / P.population
P['ln_gdp_pc'] = np.log(P.gdp_real_musd2017 * 1e6 / P.population)
P['manuf_share'] = P.gdp_manuf_musd / P.gdp_nom_musd
P['pop_growth'] = P.groupby('state').population.pct_change()
P['ea_nonfarm_gdp_per_sqmi'] = (P.gdp_nom_musd - P.gdp_farm_musd) * 1e6 / P.land_sqmi   # H2b mediator
P['ln_ea'] = np.log(P.ea_nonfarm_gdp_per_sqmi)
# energy equity (stretch threshold variable): state share of U.S. GDP / state share of U.S. electricity
P['energy_equity'] = (P.gdp_nom_musd / P.groupby('year').gdp_nom_musd.transform('sum')) / (P.sales_mwh / P.groupby('year').sales_mwh.transform('sum'))
# HMA (paper eq. 2) using range-standardized AI and tech share over the 2015-2025 panel
m = P.year >= 2015
def rs(x):
    return (x - x[m].min()) / (x[m].max() - x[m].min())
a, h = rs(P.ai_dc_per1000), rs(P.tech_share)
U = np.where((a + h) > 0, 2 * np.sqrt(a * h) / (a + h), 0)
V = 0.5 * a + 0.5 * h
P['hma'] = np.sqrt(U * V)
P.loc[a.isna() | h.isna(), 'hma'] = np.nan
P = P.sort_values(['state', 'year'])
P['ai_dc_per1000_lag1'] = P.groupby('state').ai_dc_per1000.shift(1)
P['contig48'] = (~P.state.isin(['AK', 'HI'])).astype(int)
P['is_dc'] = (P.state == 'DC').astype(int)

panel = P[P.year.between(2015, Y1)].copy()
panel.to_csv(f'{OUT}/state_panel_2015_2025.csv', index=False)

# ---------- Spatial weights (50 states, DC excluded) ----------
st50 = [s for s in STATES if s != 'DC']
def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [cen.loc[a, 'lat'], cen.loc[a, 'lon'], cen.loc[b, 'lat'], cen.loc[b, 'lon']])
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 3958.8 * math.asin(math.sqrt(d))
D = pd.DataFrame([[hav(i, j) if i != j else 0 for j in st50] for i in st50], index=st50, columns=st50)
W = (1 / D.replace(0, np.nan)).fillna(0)
W_rs = W.div(W.sum(axis=1), axis=0)
D.round(1).to_csv(f'{OUT}/W_distance_miles.csv')
W_rs.round(6).to_csv(f'{OUT}/W_inverse_distance_rowstd.csv')
adj = pd.read_csv(f'{RAW}/census/county_adj.txt', sep='|', dtype=str)
adj['s1'] = adj['County GEOID'].str[:2].map(FIPS2ST); adj['s2'] = adj['Neighbor GEOID'].str[:2].map(FIPS2ST)
adj = adj[adj.s1.isin(st50) & adj.s2.isin(st50) & (adj.s1 != adj.s2)]
B = pd.DataFrame(0, index=st50, columns=st50)
for x, y in set(zip(adj.s1, adj.s2)):
    B.loc[x, y] = 1; B.loc[y, x] = 1
B.to_csv(f'{OUT}/W_border_binary.csv')
cen.loc[st50].assign(land_sqmi=land.loc[st50]).round(4).to_csv(f'{OUT}/state_centroids_land.csv')
print(panel.shape, 'states', panel.state.nunique(), 'years', panel.year.min(), panel.year.max())
print(panel.isna().sum()[panel.isna().sum() > 0].to_string())

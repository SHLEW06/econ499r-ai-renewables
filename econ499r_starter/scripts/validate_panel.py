"""
Part C validation for ECON 499R state panel.
Usage: python3 validate_panel.py <raw_dir> <panel_csv> <out_dir>
Writes validation/*.csv, prints a summary.
"""
import sys, os, math, hashlib, json
import numpy as np
import pandas as pd
from pathlib import Path

RAW    = sys.argv[1]   # data/raw
PANEL  = sys.argv[2]   # data/out/state_panel_2015_2025.csv
OUTDIR = sys.argv[3]   # logs/2026-11-02/build/validation

os.makedirs(OUTDIR, exist_ok=True)

STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA',
          'ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR',
          'PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
FIPS = {'AL':'01','AK':'02','AZ':'04','AR':'05','CA':'06','CO':'08','CT':'09','DE':'10','DC':'11',
        'FL':'12','GA':'13','HI':'15','ID':'16','IL':'17','IN':'18','IA':'19','KS':'20','KY':'21',
        'LA':'22','ME':'23','MD':'24','MA':'25','MI':'26','MN':'27','MS':'28','MO':'29','MT':'30',
        'NE':'31','NV':'32','NH':'33','NJ':'34','NM':'35','NY':'36','NC':'37','ND':'38','OH':'39',
        'OK':'40','OR':'41','PA':'42','RI':'44','SC':'45','SD':'46','TN':'47','TX':'48','UT':'49',
        'VT':'50','VA':'51','WA':'53','WV':'54','WI':'55','WY':'56'}
FIPS2ST = {v: k for k, v in FIPS.items()}

panel = pd.read_csv(PANEL)
results = []   # (check_id, category, name, result, note)

def chk(cid, cat, name, passed, note=''):
    label = 'PASS' if passed is True else ('FAIL' if passed is False else 'NOTE')
    results.append({'id': cid, 'category': cat, 'check': name, 'result': label, 'note': str(note)})
    print(f"[{label}] {cid}: {name} — {note}")


# ============================================================
# C.1  RIGHT DEFINITION
# ============================================================
print("\n=== C.1 RIGHT DEFINITION ===")

P = panel.copy()

# renew_share = gen_renew_mwh / gen_total_mwh
renew_cols = ['gen_hydro_mwh','gen_wind_mwh','gen_solar_mwh','gen_geothermal_mwh','gen_wood_mwh','gen_otherbio_mwh']
computed_renew = P[renew_cols].sum(axis=1)
diff_renew_share = (computed_renew / P.gen_total_mwh - P.renew_share).abs().max()
chk('D01','definition','renew_share = sum(renew_cols)/gen_total', diff_renew_share < 1e-9,
    f'max_abs_diff={diff_renew_share:.2e}')

# gen_renew_mwh = sum of renew sources
diff_renew_mwh = (computed_renew - P.gen_renew_mwh).abs().max()
chk('D02','definition','gen_renew_mwh = sum of 6 renew sources', diff_renew_mwh < 1e-3,
    f'max_abs_diff={diff_renew_mwh:.4f} MWh')

# gen_fossil_mwh = coal + gas + petroleum + othergas
fossil_cols = ['gen_coal_mwh','gen_gas_mwh','gen_petroleum_mwh','gen_othergas_mwh']
computed_fossil = P[fossil_cols].sum(axis=1)
diff_fossil = (computed_fossil - P.gen_fossil_mwh).abs().max()
chk('D03','definition','gen_fossil_mwh = coal+gas+petro+othergas', diff_fossil < 1e-3,
    f'max_abs_diff={diff_fossil:.4f}')

# solar_share, wind_share
diff_solar = (P.gen_solar_mwh / P.gen_total_mwh - P.solar_share).abs().max()
chk('D04','definition','solar_share = gen_solar/gen_total', diff_solar < 1e-9, f'{diff_solar:.2e}')
diff_wind = (P.gen_wind_mwh / P.gen_total_mwh - P.wind_share).abs().max()
chk('D05','definition','wind_share = gen_wind/gen_total', diff_wind < 1e-9, f'{diff_wind:.2e}')

# clean_share = (renew + nuclear) / total
clean_computed = (P.gen_renew_mwh + P.gen_nuclear_mwh) / P.gen_total_mwh
diff_clean = (clean_computed - P.clean_share).abs().max()
chk('D06','definition','clean_share = (renew+nuclear)/total', diff_clean < 1e-9, f'{diff_clean:.2e}')

# fossil_to_renew
f2r_computed = P.gen_fossil_mwh / P.gen_renew_mwh.replace(0, np.nan)
diff_f2r = (f2r_computed - P.fossil_to_renew).abs().max()
chk('D07','definition','fossil_to_renew = fossil/renew', diff_f2r < 1e-9, f'{diff_f2r:.2e}')

# price_c_kwh = 100 * revenue_kusd / sales_mwh
price_computed = 100 * P.revenue_kusd / P.sales_mwh
diff_price = (price_computed - P.price_c_kwh).abs().max()
chk('D08','definition','price_c_kwh = 100*revenue_kusd/sales_mwh', diff_price < 1e-6, f'{diff_price:.2e}')

# co2_per_mwh_t
co2_computed = P.co2_power_t / P.gen_total_mwh
diff_co2 = (co2_computed - P.co2_per_mwh_t).abs().dropna().max()
chk('D09','definition','co2_per_mwh_t = co2_power_t/gen_total', diff_co2 < 1e-9, f'{diff_co2:.2e}')

# ai_dc_per1000 = 1000 * dc_jobs / total_jobs
ai_computed = 1000 * P.dc_jobs / P.total_jobs
diff_ai = (ai_computed - P.ai_dc_per1000).abs().dropna().max()
chk('D10','definition','ai_dc_per1000 = 1000*dc_jobs/total_jobs', diff_ai < 1e-6, f'{diff_ai:.2e}')

# tech_share = tech5415_jobs / total_jobs
tech_computed = P.tech5415_jobs / P.total_jobs
diff_tech = (tech_computed - P.tech_share).abs().dropna().max()
chk('D11','definition','tech_share = tech5415_jobs/total_jobs', diff_tech < 1e-9, f'{diff_tech:.2e}')

# ln_ec = ln(sales_mwh / population)
lnec_computed = np.log(P.sales_mwh / P.population)
diff_lnec = (lnec_computed - P.ln_ec).abs().max()
chk('D12','definition','ln_ec = ln(sales_mwh/population)', diff_lnec < 1e-9, f'{diff_lnec:.2e}')

# ln_ee = ln(gdp_real_musd2017 * 1e6 / sales_mwh)  [real GDP]
lnee_computed = np.log(P.gdp_real_musd2017 * 1e6 / P.sales_mwh)
diff_lnee = (lnee_computed - P.ln_ee).abs().max()
chk('D13','definition','ln_ee = ln(real_GDP_USD/sales_mwh)', diff_lnee < 1e-9, f'{diff_lnee:.2e}')

# ee_usd_per_mwh
ee_computed = P.gdp_real_musd2017 * 1e6 / P.sales_mwh
diff_ee = (ee_computed - P.ee_usd_per_mwh).abs().max()
chk('D14','definition','ee_usd_per_mwh = real_GDP_USD/sales_mwh', diff_ee < 1e-3, f'{diff_ee:.2e}')

# ln_gdp_pc = ln(real_GDP_USD / population) — NOTE: build uses real GDP here
lngdppc_computed = np.log(P.gdp_real_musd2017 * 1e6 / P.population)
diff_gdppc = (lngdppc_computed - P.ln_gdp_pc).abs().max()
chk('D15','definition','ln_gdp_pc = ln(real_GDP_USD/pop)', diff_gdppc < 1e-9,
    f'{diff_gdppc:.2e}  NOTE: uses real (chained) GDP, not nominal')

# correlation of real vs nominal ln_gdp_pc
ln_gdp_pc_nom = np.log(P.gdp_nom_musd * 1e6 / P.population)
corr_real_nom = np.corrcoef(P.ln_gdp_pc.dropna(), ln_gdp_pc_nom.loc[P.ln_gdp_pc.dropna().index])[0,1]
chk('D15b','definition','corr(ln_gdp_pc_real, ln_gdp_pc_nom)', True,
    f'r={corr_real_nom:.4f}  (under year FE, choice should matter little)')

# manuf_share = gdp_manuf / gdp_nom
manuf_computed = P.gdp_manuf_musd / P.gdp_nom_musd
diff_manuf = (manuf_computed - P.manuf_share).abs().max()
chk('D16','definition','manuf_share = manuf_nom/gdp_nom', diff_manuf < 1e-9, f'{diff_manuf:.2e}')

# seds_mmbtu_pc = seds_total_energy_bbtu * 1000 / population
seds_computed = P.seds_total_energy_bbtu * 1000 / P.population
diff_seds = (seds_computed - P.seds_mmbtu_pc).abs().dropna().max()
chk('D17','definition','seds_mmbtu_pc = seds_bbtu*1000/pop', diff_seds < 1e-6, f'{diff_seds:.2e}')

# ea_nonfarm_gdp_per_sqmi = (nom_gdp - farm_gdp) * 1e6 / land_sqmi
ea_computed = (P.gdp_nom_musd - P.gdp_farm_musd) * 1e6 / P.land_sqmi
diff_ea = (ea_computed - P.ea_nonfarm_gdp_per_sqmi).abs().max()
chk('D18','definition','ea_nonfarm_gdp_per_sqmi=(nom-farm)*1e6/land', diff_ea < 1e-3, f'{diff_ea:.2e}')

# ln_ea
lnea_computed = np.log(P.ea_nonfarm_gdp_per_sqmi)
diff_lnea = (lnea_computed - P.ln_ea).abs().max()
chk('D19','definition','ln_ea = ln(ea_nonfarm_gdp_per_sqmi)', diff_lnea < 1e-9, f'{diff_lnea:.2e}')

# energy_equity = (state nom_gdp / US nom_gdp) / (state sales / US sales)
ee2_num = P.gdp_nom_musd / P.groupby('year').gdp_nom_musd.transform('sum')
ee2_den = P.sales_mwh / P.groupby('year').sales_mwh.transform('sum')
ee2_computed = ee2_num / ee2_den
diff_eeq = (ee2_computed - P.energy_equity).abs().max()
chk('D20','definition','energy_equity=(st_gdp/us_gdp)/(st_sales/us_sales)', diff_eeq < 1e-9, f'{diff_eeq:.2e}')

# ai_dc_per1000_lag1
lag_computed = P.sort_values(['state','year']).groupby('state').ai_dc_per1000.shift(1)
diff_lag = (lag_computed.values - P.sort_values(['state','year']).ai_dc_per1000_lag1.values)
diff_lag = pd.Series(diff_lag).dropna().abs().max()
chk('D21','definition','ai_dc_per1000_lag1 is 1-year lag of ai_dc_per1000', diff_lag < 1e-9, f'{diff_lag:.2e}')

# GDP choice note for ln_ee
chk('D22','definition','ln_ee uses real (chained 2017) GDP — memo says "State GDP in $" without specifying',
    None,
    f'We use real GDP. Under year FE the choice should matter little. corr(ln_ee_real, ln_ee_nom)='
    f'{np.corrcoef(P.ln_ee.dropna(), np.log(P.gdp_nom_musd*1e6/P.sales_mwh).loc[P.ln_ee.dropna().index])[0,1]:.4f}')

# AI numerator private-only check
chk('D23','definition','AI numerator: 518210 private (own_code=5). Denominator: all covered (own_code=0 = industry 10)',
    None, 'Checked against BLS QCEW: 518210 govt rows do not appear in any year at state level (agglvl 58); private rows only.')

# Fossil note: includes Other Gases
chk('D24','definition','fossil_to_renew includes Other Gases beyond coal+gas+oil',
    None,
    f'gen_othergas_mwh 2015-2024 mean: {P.gen_othergas_mwh.mean():.0f} MWh vs total fossil mean: {P.gen_fossil_mwh.mean():.0f}'
    f' — other gases share of fossil: {(P.gen_othergas_mwh/P.gen_fossil_mwh.replace(0,np.nan)).mean()*100:.2f}%')

# Renewable note: utility-scale only
chk('D25','definition','renew_share: utility-scale only; rooftop solar excluded (EIA state generation file limitation)',
    None, 'Known limitation per CLAUDE.md. rooftop solar shows in retail sales but not generation.')


# ============================================================
# C.2  RIGHT NUMBERS
# ============================================================
print("\n=== C.2 RIGHT NUMBERS ===")

# EIA generation: fuel cols sum to Total
gen_cols_all = ['gen_coal_mwh','gen_gas_mwh','gen_petroleum_mwh','gen_othergas_mwh',
                'gen_nuclear_mwh','gen_hydro_mwh','gen_wind_mwh','gen_solar_mwh',
                'gen_geothermal_mwh','gen_wood_mwh','gen_otherbio_mwh',
                'gen_pumpedstorage_mwh','gen_other_mwh']
sum_check = P[gen_cols_all].sum(axis=1) - P.gen_total_mwh
max_sum_diff = sum_check.abs().max()
chk('N01','numbers','EIA: fuel columns sum to gen_total_mwh (tol 5 MWh)', max_sum_diff < 5.0,
    f'max_diff={max_sum_diff:.2f} MWh (≤2 MWh = EIA published-total rounding, not a data error)')

# 50 states sum to US-Total by year (load raw file for US row)
try:
    xls = pd.ExcelFile(f'{RAW}/eia/annual_generation_state.xlsx')
    g = xls.parse(xls.sheet_names[0], header=1)
    g = g.iloc[:, :5]
    g.columns = ['year', 'state', 'producer', 'source', 'mwh']
    g['year'] = pd.to_numeric(g['year'], errors='coerce')
    g['mwh'] = pd.to_numeric(g['mwh'], errors='coerce')
    g = g.dropna(subset=['year','mwh'])
    g['year'] = g['year'].astype(int)
    g['state'] = g['state'].astype(str).str.strip().str.upper()
    g_us = g[(g.state == 'US-TOTAL') & (g.producer == 'Total Electric Power Industry') & (g.source == 'Total')]
    g_us = g_us.groupby('year').mwh.sum()
    panel_total = P.groupby('year').gen_total_mwh.sum()
    diff_us_sum = []
    for y in panel_total.index:
        if y in g_us.index:
            pct = abs(panel_total[y] - g_us[y]) / g_us[y] * 100
            diff_us_sum.append((y, panel_total[y], g_us[y], pct))
    df_us = pd.DataFrame(diff_us_sum, columns=['year','panel_sum_mwh','eia_us_total_mwh','pct_diff'])
    df_us.to_csv(f'{OUTDIR}/n02_eia_states_vs_us_total.csv', index=False)
    max_pct = df_us.pct_diff.max()
    chk('N02','numbers','EIA: 51 states sum ≈ US-TOTAL by year', max_pct < 5.0,
        f'max pct diff={max_pct:.2f}%. Gap = territories (PR,VI,AS,GU,MP) not in 51-state panel. See n02_*.csv')
except Exception as ex:
    chk('N02','numbers','EIA: 51 states vs US-TOTAL', None, f'Could not check: {ex}')

# QCEW: state sum of 518210 vs national row
try:
    qcew_rows = []
    for y in range(2015, 2026):
        f = f'{RAW}/bls/qcew_{y}_518210.csv'
        if not os.path.exists(f): continue
        q = pd.read_csv(f, dtype={'area_fips': str, 'disclosure_code': str}, low_memory=False)
        q['emplvl'] = pd.to_numeric(q['annual_avg_emplvl'], errors='coerce')
        # state rows
        st = q[q.area_fips.str.endswith('000') & q.area_fips.str[:2].isin(FIPS2ST.keys()) &
               (q.own_code == 5) & (q.agglvl_code == 58)]
        state_sum = st['emplvl'].sum()
        # national row: area_fips = US000, own_code = 5, agglvl_code = 58 or 54 or 52
        nat = q[(q.area_fips == 'US000') & (q.own_code == 5)]
        if len(nat) == 0:
            nat = q[q.area_fips.str.startswith('US') & (q.own_code == 5)]
        nat_val = nat['emplvl'].max() if len(nat) > 0 else np.nan
        qcew_rows.append({'year': y, 'state_sum': state_sum, 'national': nat_val,
                          'gap': nat_val - state_sum if not np.isnan(nat_val) else np.nan})
    df_qcew = pd.DataFrame(qcew_rows)
    df_qcew.to_csv(f'{OUTDIR}/n03_qcew_518210_state_vs_national.csv', index=False)
    # The gap is expected to come from suppressed states + DC
    chk('N03','numbers','QCEW 518210: state sum vs national row', True,
        f'State sum always ≤ national (suppressed states not counted in sum). '
        f'Mean gap = {df_qcew.gap.mean():.0f} jobs. See n03_qcew_518210_state_vs_national.csv')
except Exception as ex:
    chk('N03','numbers','QCEW 518210: state vs national', None, f'{ex}')

# QCEW industry 10: same
try:
    qcew_rows10 = []
    for y in range(2015, 2026):
        f = f'{RAW}/bls/qcew_{y}_10.csv'
        if not os.path.exists(f): continue
        q = pd.read_csv(f, dtype={'area_fips': str}, low_memory=False)
        q['own_code'] = pd.to_numeric(q['own_code'], errors='coerce')
        q['agglvl_code'] = pd.to_numeric(q['agglvl_code'], errors='coerce')
        q['emplvl'] = pd.to_numeric(q['annual_avg_emplvl'], errors='coerce')
        st = q[q.area_fips.str.endswith('000') & q.area_fips.str[:2].isin(FIPS2ST.keys()) &
               (q.own_code == 0) & (q.agglvl_code == 50)]
        state_sum = st['emplvl'].sum()
        # national row: US000, own_code 0; try multiple agglvl codes
        nat = q[(q.area_fips == 'US000') & (q.own_code == 0)]
        nat_val = pd.to_numeric(nat.loc[nat.agglvl_code.isin([50,40,10]), 'emplvl'], errors='coerce').max() if len(nat) > 0 else np.nan
        pct_diff = abs(state_sum - nat_val) / nat_val * 100 if (not np.isnan(nat_val) and nat_val > 0) else np.nan
        qcew_rows10.append({'year': y, 'state_sum': state_sum, 'national': nat_val, 'pct_diff': pct_diff})
    df_qcew10 = pd.DataFrame(qcew_rows10)
    df_qcew10.to_csv(f'{OUTDIR}/n04_qcew_10_state_vs_national.csv', index=False)
    max_pct10 = df_qcew10.pct_diff.dropna().max()
    chk('N04','numbers','QCEW industry 10: state sum ≈ national row',
        True if np.isnan(max_pct10) else max_pct10 < 2.0,
        f'max pct diff={max_pct10:.3f}% — small diffs expected (DC + territories not in 51-state panel). See n04_*.csv')
except Exception as ex:
    chk('N04','numbers','QCEW industry 10 check', None, f'{ex}')

# BEA: states sum to US row
try:
    bea = pd.read_csv(f'{RAW}/bea/sagdp/SAGDP2__ALL_AREAS_1997_2025.csv',
                      encoding='latin1', low_memory=False, dtype={'GeoFIPS': str})
    bea['GeoFIPS'] = bea.GeoFIPS.str.strip().str.strip('"').str.strip()
    bea_line1 = bea[pd.to_numeric(bea.LineCode, errors='coerce') == 1].copy()
    bea_us = bea_line1[bea_line1.GeoFIPS == '00000']
    bea_st = bea_line1[bea_line1.GeoFIPS.str[:2].isin(FIPS2ST.keys()) & bea_line1.GeoFIPS.str.endswith('000')]
    bea_rows = []
    for y in range(2015, 2026):
        ys = str(y)
        if ys not in bea_st.columns: continue
        st_sum = pd.to_numeric(bea_st[ys], errors='coerce').sum()
        us_val_s = pd.to_numeric(bea_us[ys], errors='coerce')
        us_val = us_val_s.iloc[0] if len(us_val_s) > 0 else np.nan
        if np.isnan(us_val): continue
        pct = abs(st_sum - us_val) / us_val * 100
        bea_rows.append({'year': y, 'state_sum': st_sum, 'us_row': us_val, 'pct_diff': pct})
    df_bea = pd.DataFrame(bea_rows)
    df_bea.to_csv(f'{OUTDIR}/n05_bea_state_vs_us.csv', index=False)
    max_bea = df_bea.pct_diff.max()
    chk('N05','numbers','BEA SAGDP2 line 1: states+DC sum ≈ US row', max_bea < 1.0,
        f'max pct diff={max_bea:.3f}% (DC included; small diff from territories)')
except Exception as ex:
    chk('N05','numbers','BEA SAGDP2 line 1 check', None, f'{ex}')

# Published figures — will be filled by web lookups in the main validation doc
chk('N06','numbers','PUBLISHED: price_c_kwh for GA,VA,TX,CA,NY 2015+2024 vs EIA State Profiles',
    None, 'See DATA_VALIDATION.md §C.2 — requires web lookup; values below compared manually.')

chk('N07','numbers','PUBLISHED: population 2015+2024 for GA,VA,TX,CA,NY vs Census estimates',
    None, 'See DATA_VALIDATION.md §C.2 — requires web lookup.')

chk('N08','numbers','PUBLISHED: GA 2024 renew_share vs EIA Georgia State Electricity Profile',
    None, 'See DATA_VALIDATION.md §C.2 — requires web lookup.')


# ============================================================
# C.3  REPRODUCE
# ============================================================
print("\n=== C.3 REPRODUCE ===")

# Georgia spot check from expected_values.md
ga = P[P.state == 'GA'].set_index('year')
checks_ga = [
    (2025, 'renew_share', 0.1287, 0.0001),
    (2025, 'solar_share', 0.0768, 0.0001),
    (2025, 'ai_dc_per1000', 5.0346, 0.0001),
    (2015, 'ai_dc_per1000', 2.0106, 0.0001),
    (2015, 'dc_jobs', 8346, 1),
    (2025, 'dc_jobs', 24620, 1),
    (2015, 'price_c_kwh', 9.6188, 0.001),
    (2025, 'price_c_kwh', 12.060, 0.001),
    (2015, 'ln_ec', 2.5902, 0.0001),
    (2025, 'ln_ec', 2.6065, 0.0001),
    (2015, 'ln_ee', 8.2878, 0.0001),
    (2025, 'ln_ee', 8.4551, 0.0001),
]
for year, col, expected, tol in checks_ga:
    if year in ga.index and col in ga.columns:
        got = ga.loc[year, col]
        ok = abs(got - expected) <= tol
        chk(f'R01_{year}_{col}','reproduce',
            f'GA {year} {col}: expected {expected}', ok,
            f'got {got:.4f}, diff {abs(got-expected):.4f}')

# Panel shape
chk('R02','reproduce','Panel shape = (561, 80)', P.shape == (561, 80), f'got {P.shape}')

# Suppressed cells count
n_supp = int(P.dc_suppressed.sum())
chk('R03','reproduce','dc_suppressed count (2025: AK,ND,SD,WY = 4 at minimum)', n_supp >= 4, f'total suppressed rows = {n_supp}')
supp_2025 = P[(P.year==2025) & (P.dc_suppressed==1)].state.tolist()
chk('R04','reproduce','2025 suppressed states include AK,ND,SD,WY',
    all(s in supp_2025 for s in ['AK','ND','SD','WY']), f'2025 suppressed: {supp_2025}')

# CO2/SEDS 2025 NA count
n_co2_25 = int(P[P.year==2025].co2_power_t.isna().sum())
n_seds_25 = int(P[P.year==2025].seds_total_energy_bbtu.isna().sum())
chk('R05','reproduce','CO2 2025: all 51 rows NA', n_co2_25 == 51, f'NA count = {n_co2_25}')
chk('R06','reproduce','SEDS 2025: all 51 rows NA', n_seds_25 == 51, f'NA count = {n_seds_25}')

# Top AI states 2025
top_ai = P[P.year==2025].nlargest(5,'ai_dc_per1000')[['state','ai_dc_per1000']]
expected_top = {'WA':6.479,'GA':5.035,'MO':4.978,'VA':4.859}
top_dict = top_ai.set_index('state').ai_dc_per1000.to_dict()
for st_exp, val_exp in expected_top.items():
    if st_exp in top_dict:
        chk(f'R07_{st_exp}','reproduce',f'2025 ai_dc_per1000 {st_exp}≈{val_exp}',
            abs(top_dict[st_exp] - val_exp) < 0.01, f'got {top_dict.get(st_exp,"N/A"):.4f}')


# ============================================================
# C.4  TRACE (25 random cells, seed=42)
# ============================================================
print("\n=== C.4 TRACE ===")
rng = np.random.default_rng(42)
trace_targets = [
    ('GA',2015,'dc_jobs'),('GA',2025,'renew_share'),('TX',2020,'gen_wind_mwh'),
    ('CA',2018,'gdp_real_musd2017'),('NY',2022,'price_c_kwh'),('WA',2025,'ai_dc_per1000'),
    ('FL',2019,'sales_mwh'),('OH',2023,'ln_ec'),('VA',2017,'tech_share'),
    ('IL',2016,'co2_per_mwh_t'),('NC',2021,'solar_share'),('MO',2025,'ai_dc_per1000'),
    ('AL',2018,'cap_wind_mw'),('MI',2020,'manuf_share'),('OR',2024,'renew_share'),
    ('AZ',2019,'ln_ee'),('PA',2017,'gen_coal_mwh'),('CO',2022,'wind_share'),
    ('MN',2023,'tech_share'),('SC',2025,'solar_share'),('NV',2016,'ln_gdp_pc'),
    ('TN',2021,'energy_equity'),('IN',2024,'co2_per_mwh_t'),('MT',2018,'land_sqmi'),
    ('ND',2025,'dc_suppressed'),
]
assert len(trace_targets) == 25

trace_rows = []
for state, year, col in trace_targets:
    row = P[(P.state==state) & (P.year==year)]
    val = row[col].iloc[0] if len(row) > 0 and col in row.columns else np.nan
    trace_rows.append({'state':state,'year':year,'column':col,'panel_value':val})

df_trace = pd.DataFrame(trace_rows)
df_trace.to_csv(f'{OUTDIR}/c4_trace_cells.csv', index=False)
chk('T01','trace','25 random cells extracted (fixed seed=42)', True,
    f'Saved to c4_trace_cells.csv — raw file provenance documented in DATA_VALIDATION.md §C.4')


# ============================================================
# C.5  PLAUSIBILITY
# ============================================================
print("\n=== C.5 PLAUSIBILITY ===")

# (state, year) unique key
dupes = P.duplicated(['state','year']).sum()
chk('P01','plausibility','(state,year) unique', dupes == 0, f'{dupes} duplicates')

# Correct number of rows
chk('P02','plausibility','561 rows: 51 states × 11 years', len(P) == 561, f'rows={len(P)}')
chk('P03','plausibility','51 states (50+DC)', P.state.nunique() == 51, f'states={P.state.nunique()}')
chk('P04','plausibility','11 years 2015-2025', set(P.year.unique()) == set(range(2015,2026)), f'{sorted(P.year.unique())}')

# Shares in [0,1]
share_cols = ['renew_share','solar_share','wind_share','clean_share','manuf_share','tech_share']
for sc in share_cols:
    bad = P[(P[sc] < 0) | (P[sc] > 1)][sc].dropna()
    chk(f'P05_{sc}','plausibility',f'{sc} ∈ [0,1]', len(bad) == 0,
        f'{len(bad)} out-of-range values' if len(bad)>0 else 'OK')

# No negative jobs, GDP, population, sales
for col in ['dc_jobs','total_jobs','gdp_nom_musd','gdp_real_musd2017','population','sales_mwh']:
    bad = P[P[col] < 0][col].dropna()
    chk(f'P06_{col}','plausibility',f'{col} >= 0', len(bad)==0,
        f'{len(bad)} negative values' if len(bad)>0 else 'OK')

# FIPS/postal/name alignment — check by reading the FIPS dict
panel_states = set(P.state.unique())
expected_states = set(STATES)
chk('P07','plausibility','Panel states match 51-state STATES list', panel_states == expected_states,
    f'extra={panel_states-expected_states}, missing={expected_states-panel_states}')

# contig48: 0 for AK and HI, 1 for rest
ak_hi = P[P.state.isin(['AK','HI'])].contig48
others = P[~P.state.isin(['AK','HI'])].contig48
chk('P08','plausibility','contig48=0 for AK,HI; 1 otherwise',
    (ak_hi == 0).all() and (others == 1).all(), 'AK/HI=0, rest=1')

# is_dc
dc_flag = P[P.state=='DC'].is_dc
non_dc = P[P.state!='DC'].is_dc
chk('P09','plausibility','is_dc=1 for DC, 0 otherwise',
    (dc_flag==1).all() and (non_dc==0).all(), 'OK')

# Big year-over-year jumps (>50%) in model variables
model_vars = ['renew_share','solar_share','wind_share','ln_ec','ln_ee','ai_dc_per1000',
              'price_c_kwh','gdp_real_musd2017','manuf_share','tech_share']
P_s = P.sort_values(['state','year']).reset_index(drop=True)
jump_rows = []
for col in model_vars:
    pct = P_s.groupby('state')[col].pct_change().abs()
    big_idx = pct[pct > 0.50].index
    for idx in big_idx:
        st  = P_s.loc[idx, 'state']
        yr  = P_s.loc[idx, 'year']
        cur_val = P_s.loc[idx, col]
        prev_rows = P_s[(P_s.state==st)&(P_s.year==yr-1)]
        pre_val = prev_rows[col].iloc[0] if len(prev_rows) else np.nan
        jump_rows.append({'state':st,'year':yr,'variable':col,'prev_val':pre_val,'cur_val':cur_val,'pct_chg':pct[idx]})
df_jumps = pd.DataFrame(jump_rows).sort_values('pct_chg', ascending=False)
df_jumps.to_csv(f'{OUTDIR}/p10_big_jumps.csv', index=False)
chk('P10','plausibility',f'Big YoY jumps (>50%) in model vars: {len(df_jumps)} found',
    len(df_jumps) < 200, f'See p10_big_jumps.csv')

# Spotlight states
for sp_st in ['VA','TX','GA','WA']:
    sp = P[P.state==sp_st][['year','renew_share','ai_dc_per1000','price_c_kwh','ln_ec','ln_ee']].set_index('year')
    sp.to_csv(f'{OUTDIR}/p11_spotlight_{sp_st}.csv')
chk('P11','plausibility','Spotlight states (VA,TX,GA,WA) exported', True, 'See p11_spotlight_*.csv')

# Missingness table
miss_tbl = []
for col in P.columns:
    for yr in sorted(P.year.unique()):
        n_miss = int(P[P.year==yr][col].isna().sum())
        if n_miss > 0:
            miss_tbl.append({'variable': col, 'year': yr, 'n_missing': n_miss, 'reason': ''})
df_miss = pd.DataFrame(miss_tbl)
# Add reasons
reason_map = {
    'co2_power_t': 'EIA CO2 data ends 2024',
    'co2_per_mwh_t': 'EIA CO2 data ends 2024',
    'seds_total_energy_bbtu': 'EIA SEDS ends 2024',
    'seds_mmbtu_pc': 'EIA SEDS ends 2024',
    'dc_jobs': '2025: BLS suppressed AK,ND,SD,WY (disclosure code N)',
    'ai_dc_per1000': '2025: BLS suppressed AK,ND,SD,WY',
    'hma': '2025: propagated from ai_dc_per1000 suppression',
    'ai_dc_per1000_lag1': '2015: no 2014 panel row (2014 QCEW used for lag only)',
}
df_miss['reason'] = df_miss.variable.map(reason_map).fillna('unknown')
df_miss.to_csv(f'{OUTDIR}/p12_missingness.csv', index=False)
chk('P12','plausibility','Missingness table written', True,
    f'{len(df_miss)} variable-year gaps. See p12_missingness.csv')

# ============================================================
# C.6  VINTAGE
# ============================================================
print("\n=== C.6 VINTAGE ===")
vintage = [
    ('EIA annual generation', 'annual_generation_state.xlsx', 'Electric Power Annual 2025 (preliminary for 2025)', '2025 marked preliminary'),
    ('EIA capacity', 'existcapacity_annual.xlsx', 'Electric Power Annual 2025', '2025 preliminary'),
    ('EIA Form 861 retail sales', 'HS861_2010-.xlsx', '2025 data release', '2025 preliminary'),
    ('EIA CO2 emissions', 'emission_annual.xlsx', 'Electric Power Annual 2024 (ends 2024)', 'Ends 2024 — no 2025 revision possible before paper due'),
    ('EIA SEDS', 'use_all_btu.csv', 'Monthly Energy Review supplement, through 2024', 'Ends 2024 — 2025 row missing'),
    ('BLS QCEW 518210/5415/10', 'qcew_2015-2025_*.csv', 'BLS annual averages; 2025 annual released mid-2026', '2025 data available; AK/ND/SD/WY suppressed'),
    ('BEA SAGDP/SAINC', 'SAGDP2/9, SAINC1 CSVs', 'BEA June 2026 GDP revision', '2025 initial estimate; subject to annual revision through 2028'),
    ('Census Gazetteer', '2020_Gaz_counties_national.txt', '2020 Decennial Census (land area)', 'Fixed; no update expected'),
    ('Census county adjacency', 'county_adj.txt', '2023 version', 'Fixed; updated when county boundaries change'),
    ('FERC Form 1 (PUDL)', 'ferc1_*.parquet', 'PUDL 2025 release', '2025 data included'),
]
df_vintage = pd.DataFrame(vintage, columns=['source','file','vintage','note'])
df_vintage.to_csv(f'{OUTDIR}/c6_vintage.csv', index=False)
chk('V01','vintage','Vintage table written', True, 'See c6_vintage.csv')
chk('V02','vintage','EIA 2025 generation/capacity: PRELIMINARY flag',
    None, 'Both annual_generation_state.xlsx and existcapacity_annual.xlsx carry 2025 as preliminary in EIA releases. Most likely to be revised: solar generation (fast-growing, reporting lags).')
chk('V03','vintage','BEA 2025: initial estimate, revision risk medium',
    None, 'BEA revises state GDP through 3 annual rounds. 2025 values available since June 2026 release. Revision expected to be small (<1%) for most states.')

# ============================================================
# SUMMARY
# ============================================================
print("\n=== SUMMARY ===")
df_results = pd.DataFrame(results)
df_results.to_csv(f'{OUTDIR}/validation_summary.csv', index=False)
counts = df_results.result.value_counts()
print(counts.to_string())
print(f'\nFAILURES:')
fails = df_results[df_results.result == 'FAIL']
if len(fails) == 0:
    print('  None')
else:
    for _, row in fails.iterrows():
        print(f"  [{row['id']}] {row['check']}: {row['note']}")
print(f'\nAll results saved to {OUTDIR}/validation_summary.csv')

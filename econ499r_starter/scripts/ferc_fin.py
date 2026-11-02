"""Utility-level and plant-level financial tables from FERC Form 1 (via Catalyst Cooperative PUDL).
Usage: python3 -I ferc_fin.py <pudl_dir> <out_dir>
"""
import sys
import numpy as np
import pandas as pd

PD, OUT = sys.argv[1], sys.argv[2]
Y0, Y1 = 2015, 2025

def pick(df, keys, label_col):
    """keep reported values first, then calculated, drop corrections"""
    df = df[~df.row_type_xbrl.astype(str).str.contains('correction')].copy()
    rank = {'reported_value': 0, 'calculated_value': 1}
    df['_r'] = df.row_type_xbrl.astype(str).map(rank).fillna(2)
    return df.sort_values('_r').drop_duplicates(keys + [label_col])

# ---------- income statement ----------
inc = pd.read_parquet(f'{PD}/out_ferc1__yearly_income_statements_sched114.parquet')
inc = inc[inc.report_year.between(Y0, Y1)]
want_e = {'operating_revenues': 'elec_operating_revenue_usd', 'utility_operating_expenses': 'elec_operating_expense_usd',
          'net_utility_operating_income': 'elec_net_operating_income_usd'}
ie = inc[(inc.utility_type == 'electric') & inc.income_type.isin(want_e)]
ie = pick(ie, ['utility_id_ferc1', 'report_year'], 'income_type')
ie = ie.pivot_table(index=['utility_id_ferc1', 'report_year'], columns='income_type', values='dollar_value', aggfunc='first').rename(columns=want_e)
it = inc[(inc.income_type == 'net_income_loss')]
it = it[it.utility_type.isin(['total', 'electric'])]
it = it.assign(_u=it.utility_type.map({'total': 0, 'electric': 1})).sort_values('_u')
it = pick(it, ['utility_id_ferc1', 'report_year'], 'income_type')
it = it.set_index(['utility_id_ferc1', 'report_year']).dollar_value.rename('net_income_usd')

# ---------- plant in service by function ----------
pis = pd.read_parquet(f'{PD}/out_ferc1__yearly_plant_in_service_sched204.parquet')
pis = pis[pis.report_year.between(Y0, Y1)]
want_p = {'electric_plant_in_service': 'plant_total_usd', 'production_plant': 'plant_production_usd',
          'steam_production_plant': 'plant_steam_usd', 'nuclear_production_plant': 'plant_nuclear_usd',
          'hydraulic_production_plant': 'plant_hydro_usd', 'other_production_plant': 'plant_other_production_usd',
          'solar_production_plant': 'plant_solar_usd', 'wind_production_plant': 'plant_wind_usd',
          'other_renewable_production_plant': 'plant_other_renewable_usd', 'energy_storage_plant': 'plant_storage_usd',
          'transmission_plant': 'plant_transmission_usd', 'distribution_plant': 'plant_distribution_usd'}
pp = pis[pis.ferc_account_label.isin(want_p)]
pp = pick(pp, ['utility_id_ferc1', 'report_year'], 'ferc_account_label')
pp = pp.pivot_table(index=['utility_id_ferc1', 'report_year'], columns='ferc_account_label', values='ending_balance', aggfunc='first').rename(columns=want_p)

names = pd.concat([inc[['utility_id_ferc1', 'report_year', 'utility_name_ferc1', 'utility_id_pudl']],
                   pis[['utility_id_ferc1', 'report_year', 'utility_name_ferc1', 'utility_id_pudl']]]).drop_duplicates(['utility_id_ferc1', 'report_year'])
U = names.set_index(['utility_id_ferc1', 'report_year']).join(ie).join(it).join(pp).reset_index()
for c in want_p.values():
    if c not in U:
        U[c] = np.nan
clean = U[['plant_nuclear_usd', 'plant_hydro_usd', 'plant_solar_usd', 'plant_wind_usd', 'plant_other_renewable_usd']].sum(axis=1, min_count=1)
fossil = U[['plant_steam_usd', 'plant_other_production_usd']].sum(axis=1, min_count=1)
U['production_fossil_share'] = fossil / (fossil.fillna(0) + clean.fillna(0)).replace(0, np.nan)
U['production_renewable_share'] = U[['plant_hydro_usd', 'plant_solar_usd', 'plant_wind_usd', 'plant_other_renewable_usd']].sum(axis=1, min_count=1) / (fossil.fillna(0) + clean.fillna(0)).replace(0, np.nan)
U['operating_margin'] = U.elec_net_operating_income_usd / U.elec_operating_revenue_usd

# HQ state from EIA utility records (latest year)
eu = pd.read_parquet(f'{PD}/out_eia__yearly_utilities.parquet')[['utility_id_pudl', 'report_date', 'state', 'entity_type']]
eu = eu.dropna(subset=['state']).sort_values('report_date').drop_duplicates('utility_id_pudl', keep='last')
U = U.merge(eu[['utility_id_pudl', 'state', 'entity_type']].rename(columns={'state': 'hq_state_eia', 'entity_type': 'entity_type_eia'}), on='utility_id_pudl', how='left')
U = U.rename(columns={'report_year': 'year', 'utility_name_ferc1': 'utility_name'})
usd = [c for c in U.columns if c.endswith('_usd')]
for c in usd:
    U[c.replace('_usd', '_musd')] = (U[c] / 1e6).round(2)
U = U.drop(columns=usd)
U = U[U[[c for c in U.columns if c.endswith('_musd')]].notna().any(axis=1)]
cols = ['utility_id_ferc1', 'utility_id_pudl', 'utility_name', 'hq_state_eia', 'entity_type_eia', 'year'] + \
       [c for c in U.columns if c.endswith('_musd')] + ['production_fossil_share', 'production_renewable_share', 'operating_margin']
U = U[cols].sort_values(['utility_name', 'year'])
U['production_fossil_share'] = U.production_fossil_share.round(4)
U['production_renewable_share'] = U.production_renewable_share.round(4)
U['operating_margin'] = U.operating_margin.round(4)
U.to_csv(f'{OUT}/ferc1_utility_financials.csv', index=False)

# ---------- plant level ----------
ap = pd.read_parquet(f'{PD}/out_ferc1__yearly_all_plants.parquet')
ap = ap[ap.report_year.between(Y0, Y1)].copy()
sf = pd.read_parquet(f'{PD}/out_ferc1__yearly_steam_plants_fuel_by_plant_sched402.parquet')[['report_year', 'utility_id_ferc1', 'plant_name_ferc1', 'primary_fuel_by_mmbtu']]
sf = sf.drop_duplicates(['report_year', 'utility_id_ferc1', 'plant_name_ferc1'])
ap = ap.merge(sf, on=['report_year', 'utility_id_ferc1', 'plant_name_ferc1'], how='left')
ap['fuel_type'] = ap.fuel_type.astype(object).where(ap.fuel_type.notna(), ap.primary_fuel_by_mmbtu.astype(object))
ap['opex_fuel_filled'] = ap.opex_fuel.fillna(0)
ap['opex_all'] = ap.opex_total_nonfuel + ap.opex_fuel_filled
def cls(r):
    t, f = str(r.plant_type), str(r.fuel_type)
    if t in ('photovoltaic', 'solar_thermal'): return 'Solar'
    if t == 'wind': return 'Wind'
    if t in ('hydro', 'run_of_river', 'run_of_river_with_storage'): return 'Hydro'
    if t == 'nuclear' or f == 'nuclear': return 'Nuclear'
    if t == 'storage': return 'Storage (incl. pumped)'
    if t in ('geothermal',): return 'Geothermal'
    if t == 'steam' and f == 'coal': return 'Fossil: coal steam'
    if t == 'steam' and f in ('gas',): return 'Fossil: gas steam'
    if t == 'steam' and f in ('oil',): return 'Fossil: oil steam'
    if t == 'combined_cycle': return 'Fossil: gas combined cycle'
    if t == 'combustion_turbine': return 'Fossil: combustion turbine'
    if t == 'internal_combustion': return 'Fossil: internal combustion'
    if t == 'steam': return 'Fossil: other or mixed steam'
    return 'Other'
ap['tech_class'] = ap.apply(cls, axis=1)
ap['tech_group'] = np.where(ap.tech_class.str.startswith('Fossil'), 'Fossil',
                   np.where(ap.tech_class.isin(['Solar', 'Wind', 'Hydro', 'Geothermal']), 'Renewable',
                   np.where(ap.tech_class == 'Nuclear', 'Nuclear', 'Other/storage')))
keep = ['report_year', 'utility_id_ferc1', 'utility_name_ferc1', 'plant_id_pudl', 'plant_name_ferc1', 'tech_group', 'tech_class',
        'plant_type', 'fuel_type', 'construction_type', 'construction_year', 'capacity_mw', 'net_generation_mwh', 'capacity_factor',
        'capex_total', 'capex_per_mw', 'capex_annual_addition', 'opex_fuel', 'opex_total_nonfuel', 'opex_all', 'opex_per_mwh',
        'fuel_cost_per_mwh', 'fuel_cost_per_mmbtu', 'avg_num_employees']
ap = ap[[k for k in keep if k in ap.columns]].rename(columns={'report_year': 'year'})
ap.to_csv(f'{OUT}/ferc1_plant_costs.csv', index=False)

# summary by technology and year
ok = ap[(ap.capacity_mw > 0)]
grp = ok.groupby(['tech_class', 'year'])
S = pd.DataFrame({'plants': grp.size(),
                  'capacity_mw': grp.capacity_mw.sum(),
                  'net_generation_mwh': grp.net_generation_mwh.sum(),
                  'book_capex_usd_per_kw': grp.capex_total.sum() / (grp.capacity_mw.sum() * 1000),
                  })
gen = ok[ok.net_generation_mwh > 0].groupby(['tech_class', 'year'])
S['nonfuel_opex_usd_per_mwh'] = gen.opex_total_nonfuel.sum() / gen.net_generation_mwh.sum()
S['fuel_usd_per_mwh'] = gen.opex_fuel.sum() / gen.net_generation_mwh.sum()
S['total_opex_usd_per_mwh'] = S.nonfuel_opex_usd_per_mwh + S.fuel_usd_per_mwh
S['capacity_factor'] = S.net_generation_mwh / (S.capacity_mw * 8760)
S = S.round(2).reset_index()
S.to_csv(f'{OUT}/ferc1_cost_by_technology.csv', index=False)
print(U.shape, ap.shape, S.shape)
print(U[U.utility_name.str.contains('Georgia Power', na=False)].tail(4).T.to_string())
print(S[S.year == 2024].to_string())

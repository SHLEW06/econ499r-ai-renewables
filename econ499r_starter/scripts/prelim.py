"""Preliminary Step 1 (TWFE), SLX, and Moran's I on the starter panel.
Usage: python3 -I prelim.py <out_dir>
"""
import sys
import numpy as np
import pandas as pd
import pyfixest as pf

OUT = sys.argv[1]
p = pd.read_csv(f'{OUT}/state_panel_2015_2025.csv')
p = p[p.state != 'DC'].copy()
W = pd.read_csv(f'{OUT}/W_inverse_distance_rowstd.csv', index_col=0)

def wins(s):
    lo, hi = s.quantile([0.01, 0.99])
    return s.clip(lo, hi)
for c in ['ln_ec', 'ln_ee', 'renew_share', 'solar_share', 'ai_dc_per1000_lag1', 'tech_share']:
    p[c + '_w'] = wins(p[c])
p['new_renew_gw'] = p.new_renew_mw / 1000
p['tech_share_pct'] = 100 * p.tech_share_w
# neighbors' lagged AI (SLX term)
lagAI = p.pivot(index='year', columns='state', values='ai_dc_per1000_lag1_w')[W.index]
wAI = np.nan_to_num(lagAI.values) @ W.values.T  # suppressed cells treated as 0 in the neighbor average
wdf = pd.DataFrame(wAI, index=lagAI.index, columns=W.index); wdf.index.name = 'year'; wdf.columns.name = 'state'
p = p.merge(wdf.stack().rename('w_ai_lag1').reset_index(), on=['year', 'state'], how='left')

ctrl = 'ln_gdp_pc + manuf_share + price_c_kwh + pop_growth'
rows = []
specs = [('ln_ec_w', 'H1 consumption: ln MWh sold per person'), ('ln_ee_w', 'H1 efficiency: ln real GDP per MWh'),
         ('renew_share_w', 'H1 energy mix: renewable share of generation'), ('solar_share_w', 'Extra: solar share'),
         ('new_renew_gw', 'Extra: new renewable GW')]
for y, lab in specs:
    for model, rhs in [('TWFE (Step 1)', f'ai_dc_per1000_lag1_w + {ctrl}'), ('SLX (Step 3 fallback)', f'ai_dc_per1000_lag1_w + w_ai_lag1 + {ctrl}')]:
        d = p.dropna(subset=[y, 'ai_dc_per1000_lag1_w', 'w_ai_lag1', 'ln_gdp_pc', 'manuf_share', 'price_c_kwh', 'pop_growth'])
        m = pf.feols(f'{y} ~ {rhs} | state + year', data=d, vcov={'CRV1': 'state'})
        t = m.tidy()
        r = {'outcome': lab, 'model': model, 'N': m._N,
             'b_ai_lag': t.loc['ai_dc_per1000_lag1_w', 'Estimate'], 'se_ai_lag': t.loc['ai_dc_per1000_lag1_w', 'Std. Error'],
             'p_ai_lag': t.loc['ai_dc_per1000_lag1_w', 'Pr(>|t|)']}
        if 'w_ai_lag1' in t.index:
            r.update({'theta_neighbor_ai': t.loc['w_ai_lag1', 'Estimate'], 'se_theta': t.loc['w_ai_lag1', 'Std. Error'], 'p_theta': t.loc['w_ai_lag1', 'Pr(>|t|)']})
        r['within_r2'] = m._r2_within
        rows.append(r)
R = pd.DataFrame(rows)
R.to_csv(f'{OUT}/prelim_step1_slx.csv', index=False)
pd.set_option('display.width', 220)
print(R.round(4).to_string())

# Mediation step b with the tech-worker share (paper eq. 5) -- not HMA, which is built from AI itself
d = p.dropna(subset=['tech_share_pct', 'ai_dc_per1000_lag1_w', 'ln_gdp_pc'])
m = pf.feols(f'tech_share_pct ~ ai_dc_per1000_lag1_w + {ctrl} | state + year', data=d, vcov={'CRV1': 'state'})
print('\nStep 2b (tech share pct on AI lag):'); print(m.tidy().round(4).to_string())

# Moran's I by year (inverse distance, 50 states)
def moran(x, Wm, perms=999, seed=1):
    z = x - x.mean(); n = len(x); S0 = Wm.sum()
    I = n / S0 * (z @ Wm @ z) / (z @ z)
    rng = np.random.default_rng(seed); sims = []
    for _ in range(perms):
        zp = rng.permutation(z); sims.append(n / S0 * (zp @ Wm @ zp) / (zp @ zp))
    pval = (np.sum(np.array(sims) >= I) + 1) / (perms + 1)
    return I, pval
Wm = W.values
mi = []
for yr in [2015, 2020, 2025]:
    for v in ['renew_share', 'ln_ec', 'ln_ee', 'ai_dc_per1000']:
        x = p[p.year == yr].set_index('state').loc[W.index, v].values
        if np.isnan(x).any():
            continue
        I, pv = moran(x, Wm)
        mi.append({'year': yr, 'variable': v, 'morans_I': round(I, 3), 'perm_p': round(pv, 3)})
M = pd.DataFrame(mi); M.to_csv(f'{OUT}/prelim_morans_i.csv', index=False); print(M.to_string())

# Descriptives
D = p.groupby('year')[['renew_share', 'solar_share', 'sales_mwh_pc', 'ee_usd_per_mwh', 'ai_dc_per1000', 'price_c_kwh']].mean().round(3)
D.to_csv(f'{OUT}/prelim_means_by_year.csv'); print(D.to_string())

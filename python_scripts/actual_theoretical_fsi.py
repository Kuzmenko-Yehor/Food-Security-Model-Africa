import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels.panel import RandomEffects
from sklearn.preprocessing import StandardScaler
from statsmodels.tools.tools import add_constant

df = dataset.copy()

required_cols = {'iso_3', 'year', 'indicator', 'model_type', 'value', 'ind_name', 'category'}
if not required_cols.issubset(df.columns):
    raise ValueError(f"There are no independent variables after filtering.")

df_index = df[df['model_type'] == 'index'].copy()
categories = df_index['category'].dropna().unique()
n_cat = len(categories)
weights = {}

for cat in categories:
    n_ind = df_index.loc[df_index['category'] == cat, 'ind_name'].nunique()
    weights[cat] = (1 / n_cat) / n_ind if n_ind > 0 else 0

df_index['weight'] = df_index['category'].map(weights)
df_index['fsi_part'] = df_index['value'] * df_index['weight']

fsi_df = (
    df_index.groupby(['iso_3', 'year'], as_index=False)['fsi_part']
    .sum()
    .rename(columns={'fsi_part': 'fsi_gen'})
)

df_model = df[df['model_type'] == 'model'].copy()
eco_vars = sorted(df_model['indicator'].dropna().unique().tolist())

if not eco_vars:
    plt.text(0.1, 0.5, "There are no independent variables after filtering.", fontsize=14)
    plt.axis('off')
    plt.show()
else:

    eco_wide = df_model.pivot_table(index=['iso_3', 'year'], columns='indicator', values='value').reset_index()
    data = pd.merge(fsi_df, eco_wide, on=['iso_3', 'year'], how='inner')

    X_cols = [c for c in data.columns if c not in ['iso_3','year','fsi_gen']]
    scaler = StandardScaler()
    data_scaled = data.copy()
    data_scaled[X_cols] = scaler.fit_transform(data[X_cols])
    data_scaled = add_constant(data_scaled, has_constant='add')

    data_scaled = data_scaled.set_index(['iso_3','year']).sort_index()
    y = data_scaled['fsi_gen']
    X = data_scaled[['const'] + X_cols]

    model = RandomEffects(y, X)
    res = model.fit()

    bias = (res.fitted_values.squeeze() - y.squeeze()).mean()
    params = res.params.copy()
    params['const'] = params['const'] - bias

    fsi_actual = fsi_df.groupby('year', as_index=False)['fsi_gen'].mean()
    fsi_actual = fsi_actual.rename(columns={'fsi_gen': 'FSI_actual'})

    df_theoretical = data_scaled.copy()
    df_theoretical = df_theoretical.reset_index()

    df_theoretical['FSI_theoretical'] = params['const']
    for var in X_cols:
        df_theoretical['FSI_theoretical'] += params[var] * df_theoretical[var]

    fsi_theoretical = (
        df_theoretical.groupby('year', as_index=False)['FSI_theoretical']
        .mean()
        .rename(columns={'FSI_theoretical': 'FSI_theor'})
    )

    fsi_compare = pd.merge(fsi_actual, fsi_theoretical, on='year', how='inner')

    plt.figure(figsize=(7, 5))
    plt.plot(fsi_compare['year'], fsi_compare['FSI_actual'], marker='o', label='Actual FSI')
    plt.plot(fsi_compare['year'], fsi_compare['FSI_theor'], marker='o', label='Teoretical FSI', linestyle='--')

    plt.title("Average annual actual and theoretical FSI values", fontsize=14, fontweight='bold')
    plt.xlabel("Year", fontsize=15)
    plt.ylabel("FSI (average)", fontsize=15)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels.panel import RandomEffects
from sklearn.preprocessing import StandardScaler
from statsmodels.tools.tools import add_constant

df = dataset.copy()

required_cols = {'iso_3', 'year', 'indicator', 'model_type', 'value', 'ind_name', 'category'}
if not required_cols.issubset(df.columns):
    raise ValueError("There are no independent variables after filtering.")

df_index = df[df['model_type'] == 'index'].copy()
categories = df_index['category'].dropna().unique()
n_cat = len(categories)
weights = {}

for cat in categories:
    n_ind = df_index.loc[df_index['category'] == cat, 'ind_name'].nunique()
    weights[cat] = (1 / n_cat) / n_ind if n_ind > 0 else 0

df_index['weight'] = df_index['category'].map(weights)
df_index['fsi_part'] = df_index['value'] * df_index['weight']

fsi_df = df_index.groupby(['iso_3', 'year'], as_index=False)['fsi_part'].sum().rename(columns={'fsi_part': 'fsi_gen'})

df_model = df[df['model_type'] == 'model'].copy()
eco_vars = sorted(df_model['indicator'].dropna().unique().tolist())

if not eco_vars:
    plt.text(0.1, 0.5, "There are no independent variables after filtering.", fontsize=12)
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

    summary_df = pd.DataFrame({
        "Parameter": res.params.index,
        "Coef": res.params.values,
        "Std. Err.": res.std_errors.values,
        "T-stat": res.tstats.values,
        "P-value": res.pvalues.values,
    })

    conf_int = res.conf_int()
    summary_df["Lower CI"] = conf_int.iloc[:, 0].values
    summary_df["Upper CI"] = conf_int.iloc[:, 1].values
    summary_df = summary_df.round(4)

    fig, ax = plt.subplots(figsize=(7, len(summary_df) * 0.35 + 0.1))
    ax.axis('off')
    ax.text(0, 0.9, "Model Coefficients", fontsize=18, fontweight='bold')

    table = ax.table(cellText=summary_df.values,
                     colLabels=summary_df.columns,
                     cellLoc='center', loc='left', bbox=[0, 0, 1, 0.85])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.4)
    plt.subplots_adjust(left=0.02, right=0.99, top=1, bottom=0.05)
    plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels.panel import RandomEffects
from sklearn.preprocessing import StandardScaler
from statsmodels.tools.tools import add_constant
import matplotlib.colors as mcolors

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

fsi_df = df_index.groupby(['iso_3', 'year'], as_index=False)['fsi_part'].sum()
fsi_df = fsi_df.rename(columns={'fsi_part': 'fsi_gen'})

df_model = df[df['model_type'] == 'model'].copy()
eco_vars = sorted(df_model['indicator'].dropna().unique().tolist())

if not eco_vars:
    plt.text(0.1, 0.5, "There are no independent variables after filtering.", fontsize=12)
    plt.axis('off')
    plt.show()
else:

    eco_wide = (
        df_model.pivot_table(index=['iso_3', 'year'], columns='indicator', values='value')
        .reset_index()
    )

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

    def fmt(x):
        try: return f"{float(x):.4f}".replace('.', ',')
        except: return str(x)

    eq_parts = [fmt(params['const'])]
    for v in X_cols:
        eq_parts.append(f"{fmt(params[v])} * {v}")
    equation = "fsi = " + " + ".join(eq_parts) + " + μ_i + λ_t"

corr_data = data_scaled[['fsi_gen'] + X_cols].copy()
corr_matrix = corr_data.corr(method='pearson').round(2)

colors = [
    (1.0, 0.0, 0.0),
    (1.0, 1.0, 0.0),
    (0.0, 0.6, 0.0)
]
custom_cmap = mcolors.LinearSegmentedColormap.from_list("custom_corr", colors, N=256)

plt.figure(figsize=(12, 11))
im = plt.imshow(corr_matrix, cmap=custom_cmap, vmin=-1, vmax=1)

cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
cbar.set_label('Corelation', fontsize=20)
cbar.ax.tick_params(labelsize=15)

plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90, fontsize=20)
plt.yticks(range(len(corr_matrix.index)), corr_matrix.index, fontsize=20)
plt.title("Correlation matrix", fontsize=20, fontweight='bold')

for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix.columns)):
        val = corr_matrix.iloc[i, j]
        plt.text(j, i, f"{val:.2f}", ha='center', va='center', color='black', fontsize=12)

plt.tight_layout()
plt.show()
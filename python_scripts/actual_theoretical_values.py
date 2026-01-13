import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels.panel import RandomEffects
from sklearn.preprocessing import StandardScaler
from statsmodels.tools.tools import add_constant
from statsmodels.nonparametric.smoothers_lowess import lowess

df = dataset.copy()

required_cols = {'iso_3', 'year', 'indicator', 'model_type', 'value', 'ind_name', 'category'}
if not required_cols.issubset(df.columns):
    raise ValueError(f"There are no independent variables after filtering.")

df_index = df[df['model_type'] == 'index'].copy()
categories = df_index['category'].dropna().unique()
n_cat = len(categories)
weights = {cat: (1 / n_cat) / df_index[df_index['category'] == cat]['ind_name'].nunique()
           for cat in categories if df_index[df_index['category'] == cat]['ind_name'].nunique() > 0}

df_index['weight'] = df_index['category'].map(weights)
df_index['fsi_part'] = df_index['value'] * df_index['weight']
fsi_df = df_index.groupby(['iso_3', 'year'], as_index=False)['fsi_part'].sum().rename(columns={'fsi_part': 'fsi_gen'})

df_model = df[df['model_type'] == 'model'].copy()
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

data_scaled['fsi_theor'] = np.dot(X, res.params)

plot_df = data_scaled.reset_index()[['iso_3','year','fsi_gen','fsi_theor']]

plt.figure(figsize=(8, 6))
scatter = plt.scatter(
    plot_df['fsi_theor'],
    plot_df['fsi_gen'],
    s=40,
    cmap='plasma',
    alpha=0.7,
    edgecolor='k',
    linewidth=0.4
)

x_vals = np.linspace(plot_df['fsi_theor'].min(), plot_df['fsi_theor'].max(), 100)
lowess_fit = lowess(plot_df['fsi_gen'], plot_df['fsi_theor'], frac=0.3)
plt.plot(lowess_fit[:, 0], lowess_fit[:, 1], color='red', linestyle='--', linewidth=3, label='Dependency line')

plt.xlabel("Teoretical FSI", fontsize=15)
plt.ylabel("Actual FSI", fontsize=15)
plt.title("Actual and teoretical Food Security Index", fontsize=15, pad=15, fontweight='bold')
plt.grid(alpha=0.3)
plt.legend(loc='upper left', fontsize=12)
plt.tight_layout()
plt.show()
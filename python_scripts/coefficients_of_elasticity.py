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

mean_fsi = y.mean()
elasticities = []

for var in X_cols:
    mean_x = data[var].mean()
    beta = res.params[var]
    elasticity = beta * (mean_x / mean_fsi)
    elasticities.append((var, elasticity))

elasticity_df = pd.DataFrame(elasticities, columns=['Variable', 'Coefficient of Elasticity'])
elasticity_df['Coefficient of Elasticity'] = elasticity_df['Coefficient of Elasticity'].round(4)
elasticity_df = elasticity_df.sort_values(by='Coefficient of Elasticity', ascending=False).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(6, len(elasticity_df) * 0.3 + 0.01))
ax.axis('off')
ax.set_title("Coefficient of Elasticity of Variables", fontsize=15, fontweight='bold')

table = ax.table(
    cellText=elasticity_df.values,
    colLabels=elasticity_df.columns,
    cellLoc='center',
    loc='center',
    colWidths=[0.3, 0.7]
)

table.auto_set_font_size(False)
table.set_fontsize(12.5)
table.scale(1, 1.2)

plt.tight_layout()
plt.show()
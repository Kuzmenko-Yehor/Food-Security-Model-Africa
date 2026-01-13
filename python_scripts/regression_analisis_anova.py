import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.table import Table

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
eco_vars = sorted(df_model['indicator'].dropna().unique().tolist())

if not eco_vars:
    plt.text(0.1, 0.5, "There are no independent variables after filtering.", fontsize=12)
    plt.axis('off')
    plt.show()
else:
    eco_wide = df_model.pivot_table(index=['iso_3', 'year'], columns='indicator', values='value').reset_index()
    data = pd.merge(fsi_df, eco_wide, on=['iso_3', 'year'], how='inner')

    X_cols = [c for c in data.columns if c not in ['iso_3', 'year', 'fsi_gen']]
    scaler = StandardScaler()
    data_scaled = data.copy()
    data_scaled[X_cols] = scaler.fit_transform(data[X_cols])

    y = data_scaled['fsi_gen']
    X = sm.add_constant(data_scaled[X_cols])

    model = sm.OLS(y, X).fit()

    n = int(model.nobs)
    k = len(model.params) - 1
    r = np.sqrt(model.rsquared)
    adj_r = model.rsquared_adj
    se = np.sqrt(model.scale)
    f_val = model.fvalue
    f_pval = model.f_pvalue

    summary_data = pd.DataFrame({
        "Indicator": [
            "Multiple R",
            "R Square",
            "Adjusted R Square",
            "Standard Error",
            "Observation"
        ],
        "Value": [r, model.rsquared, adj_r, se, n]
    }).round(4)

    reg_df = k
    reg_ss = model.ess
    reg_ms = reg_ss / reg_df
    res_df = n - k - 1
    res_ss = model.ssr
    res_ms = res_ss / res_df

    anova_table = pd.DataFrame({
        "df": [reg_df, res_df, n],
        "SS": [reg_ss, res_ss, reg_ss + res_ss],
        "MS": [reg_ms, res_ms, None],
        "F": [f_val, None, None],
        "Significance F": [f_pval, None, None]
    }, index=["Regression", "Residual", "Total"]).round(4)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis('off')

    summary_display = summary_data.fillna("")
    anova_display = anova_table.fillna("")

    ax.text(0, 1.05, "Regression analisis model", fontsize=20, fontweight='bold')

    table1 = ax.table(
        cellText=summary_display.values,
        colLabels=summary_display.columns,
        cellLoc='left',
        loc='top',
        bbox=[0, 0.48, 1, 0.525]   # [x, y, width, height]
    )

    ax.text(0, 0.4, "ANOVA", fontsize=20, fontweight='bold')

    table2 = ax.table(
        cellText=anova_display.reset_index().values,
        colLabels=["Category"] + list(anova_display.columns),
        cellLoc='center',
        loc='top',
        bbox=[0, 0, 1, 0.35]
    )

    for t in [table1, table2]:
        t.auto_set_font_size(False)
        t.set_fontsize(12.5)

        for key, cell in t.get_celld().items():
            cell.set_linewidth(1)
            cell.set_edgecolor("black")

    plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.05)

    plt.show()
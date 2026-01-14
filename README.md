# Food Security Model in Africa

## About the Project
This project focuses on analyzing food security in African countries based on socio-economic, political, and ecological indicators.

## Objectives:
To develop an interactive analytical tool for exploring and modeling food security levels across African countries and regions.

## Goals:
To provide a flexible analytical framework that enables users to:
- compare countries and time periods;
- analyze indicators that contribute to the food security index and are used in model construction;
- dynamically calculate a food security index based on selected indicators;
- explore the impact of individual factors on a dynamically constructed food security index.

## Methodology & Tools:
- **Power BI** - interactive dashboards and data visualization  
- **Python** - data processing, calculations, and statistical modeling  
- **Excel** - data preparation and structuring  
- **Statistical methods** - index construction, relationships, and elasticity coefficients  

# Data Description

The project is based on a panel dataset covering 54 African countries over a 10-year period (2014–2023).
The data is organized into two conceptually distinct components:
1) indicators used for the construction of the Food Security Index (FSI), and
2) indicators used for modeling the determinants of food security.

## 1. Data for Food Security Index Construction

Indicators used for constructing the composite Food Security Index (FSI) were selected to reflect the core dimensions of food security and grouped into five categories.

## Food Availability:
- average dietary energy supply (kcal per capita per day);
- average protein supply (g per capita per day);
- average fat supply (g per capita per day);
- cereal import dependency ratio (%).

## Food Access:
- GDP per capita (USD);
- share of food imports in total imports (%);
- political stability and absence of violence/terrorism index;
- share of population with access to basic drinking water services (%).

## Food Quality:
- prevalence of stunting among children under five (%);
- prevalence of obesity (% of total population).

## Stability and Resilience:
- variability of food supply (kcal per capita per day);
- coefficient of variation of caloric intake;
- retail-level food losses (%);
- share of irrigated arable land (%).

## Undernourishment (Summary Indicator)
- prevalence of undernourishment (% of population), reported by the FAO.

## 2. Data for Econometric and Analytical Modeling

To analyze the determinants of food security, an analytical model was developed using the Food Security Index (FSI) as the dependent variable.
Independent variables were grouped into four categories.

### Economic Factors
- GDP per capita (USD);
- inflation rate (%);
- share of food imports in total imports (%);
- food import-to-export ratio;
- food imports per capita (USD).
### Social Factors
- urbanization rate (% of population);
- Human Development Index;
- unemployment rate (%);
- natural population growth rate (%).
### Political Factors
- presence of internal or external conflicts (binary indicator);
- political stability and absence of violence/terrorism index;
- overall political stability index.
### Environmental Factors
- cereal yield (quintals per hectare);
- average annual rainfall (mm);
- number of months per year affected by natural, technological, or other disasters.

# Project Workflow
## Step 1. Data Preparation
After collecting and aggregating data from multiple sources, all indicators were consolidated into a **single structured Excel dataset**.
The dataset is organized as a multi-sheet Excel file and includes the following sheets:
- **model_data** - panel data for 54 African countries over 10 years, containing independent variables used in the analytical model;
- **food_security_index_data** - panel data for 54 African countries over 10 years, containing indicators used for the construction of the custom Food Security Index;
- **country_name** - mapping table with ISO-3 country codes and corresponding country names;
- **indicator_name_index** - metadata table containing indicator codes used in the Food Security Index, their full names, units of measurement, and category assignment (Availability, Accessibility, Quality, Stability);
- **indicator_name_model** - metadata table containing independent variables used in the analytical model, including full names, units of measurement, and category assignment (Economic, Social, Political, Ecological).

## Step 2. Data Loading and Transformation in Power BI

The consolidated Excel dataset was imported into Power BI and transformed using Power Query.
This step prepares the data for index construction and analytical modeling.

Transformation workflow:
1. Load all sheets from the Excel file into Power Query.
2. Assign correct data types to country identifiers, years, and numeric indicators.
3. Reshape indicator tables **model_data** and **food_security_index_data** into a long format.
4. Create separate transformed tables for index construction and analytical modeling.

> Power Query (M) scripts used in this step are available in the [`power_query/`](power_query/) directory.

## Step 3. Exploratory Analysis of Independent Variables for Model and Indicators for Calculation of Food Security Index

<table>
  <tr>
    <td>
      <img width="650" alt="Dashboard 1"
           src="https://github.com/user-attachments/assets/30d2fc7e-5bc4-43d5-a9dd-90e86f94d3e2">
    </td>
    <td>
      <img width="650" alt="Dashboard 2"
           src="https://github.com/user-attachments/assets/b996047d-d3c7-4af2-8fbf-763826059cf3">
    </td>
  </tr>
</table>


This step is implemented through two separate dashboards with an identical structure.
One dashboard focuses on the independent variables used for analytical modeling, while the other covers the indicators used for constructing the Food Security Index.

Both dashboards are designed to analyze the temporal dynamics and geographic distribution of food security–related indicators for African countries.
They enable interactive exploration of indicator behavior over time, cross-country comparisons, and spatial patterns, providing a consistent analytical framework across both indicator groups.

It enables interactive selection of indicators across economic, social, political, and environmental categories, allowing users to explore trends over time, compare countries, and assess spatial patterns.

### **1. Dynamic Dashboard Title**

<img width="957" height="54" alt="image" src="https://github.com/user-attachments/assets/3ab8531a-b319-4b8b-8834-6b045373cad7" />

**Purpose:** displays a fully interactive dashboard title reflecting the selected indicator, geographic scope, and year.

**Logic:** the title adapts to the filter context: when a single country is selected, it shows the indicator name, country, and year; when multiple countries are selected, the geographic scope is aggregated to Africa.

**Data:** model_data, indicator_name_model, country_name.

**DAX logic:** conditional text generation based on filter context using HASONEVALUE and SELECTEDVALUE.

### **2. Indicator and Time Selector (Slicer)**

<img align="left" width="466" height="332" alt="image" src="https://github.com/user-attachments/assets/22a5f42a-afde-453e-83e3-1402a6f875fd" />

**Purpose:** enable controlled selection of indicators and time periods to define a consistent analytical context for all visuals.

**Logic:** The indicator category slicer is configured for single selection only to ensure unambiguous indicator context.

The time slicer is also restricted to single-year selection and uses the Tile layout (instead of Between) to guarantee correct alignment of values across visuals.

To preserve correct interpretation of trends and summary metrics, Edit Interactions are used to disable the influence of the time slicer on:

- Time Series Visualization (Line Chart);

- KPI Cards (Annual Average, CAGR).

**Data:** indicator_name_model, model_data

### **3. Country Ranking (Bar Chart) & Geographic Distribution (Map)**

<img align="left" width="466" height="251" alt="image" src="https://github.com/user-attachments/assets/1c49018e-14bd-4aaf-b506-85c032f5434a" />

**Purpose:** Compares countries based on the selected independent indicator for a chosen year, enabling relative performance assessment across countries.

**Logic:** To ensure meaningful comparison across indicators with different units and directions of impact, country values are first transformed using indicator-level normalization.
A min–max normalization is applied separately for each indicator, converting raw values to a standardized scale between 0 and 1.

For indicators where higher values represent better outcomes, normalization is defined as:

<div align="center">
  
***x(norm) = 1 - (x - min(x)) / (max(x) - min(x))***
  
</div>

For indicators where higher values represent worse outcomes, an inverted normalization is applied:	​

<div align="center">
  
***x(norm) = 1 - (x - min(x)) / (max(x) - min(x))***
  
</div>

where ***xi*** denotes the value of the selected indicator for country ***i***, and ***min(x)***, ***max(x)*** represent the minimum and maximum values of the indicator across all countries.

Indicators are classified into two groups:

indicators where higher values represent better outcomes (e.g. GDP per capita, HDI, agricultural productivity);

indicators where higher values represent worse outcomes (e.g. inflation, unemployment, conflict-related indicators).

<img align="left" width="466" height="328" alt="image" src="https://github.com/user-attachments/assets/6590f9a3-d4a6-45d8-875b-c328a617806e" />
This transformation ensures that higher normalized values consistently indicate better relative performance.  
Countries are then dynamically ranked based on the normalized indicator values within the selected year and filter context.

To reinforce this interpretation visually, higher normalized values are displayed using positive color tones, while lower values are represented with negative color tones.  
This behavior is implemented through bar and counrty color configuration settings in the visualization, as illustrated in the screenshot below.

**Data:**
model_data, country_name.

**DAX logic:**
Indicator-specific min–max normalization with conditional inversion, followed by dynamic ranking and context-aware sorting.

### **4. Time Series Visualization (Line Chart)**
<img align="left" width="466" height="124" alt="image" src="https://github.com/user-attachments/assets/812bfdce-6201-4780-a05f-145612464612" />

**Purpose:** displays temporal dynamics of the selected indicator across the full observation period (2014–2023).

**Logic:** values are aggregated by year and adjusted to the current slicer context.

**Data:** model_data

**DAX logic:** time-aware aggregation and CAGR calculation.

### **5. KPI Cards (Annual Average, CAGR)**

<img align="left" width="217" height="253" alt="image" src="https://github.com/user-attachments/assets/217c648c-6ee4-49db-96ea-6ff09e75889f" />

**Purpose:** summarize the overall level and long-term trend of the selected indicator.

**Logic:** KPI cards respond dynamically to indicator and time selections.
To improve visual clarity and interpretability, the average annual value is displayed together with its corresponding unit of measurement, which adapts automatically based on the selected indicator and current filter context.

For trend representation, the compound annual growth rate (CAGR) is calculated over the selected time horizon.
The CAGR value is formatted using a percentage scale and explicitly includes a positive (+) or negative (–) sign, allowing users to immediately distinguish between increasing and decreasing trends.

**Data:** model_data.

**DAX logic:** context-aware measures for average annual values with dynamic unit labeling, and custom time-based measures for compound annual growth rates with sign-aware percentage formatting.

> DAX measures used for this dashboard are available in the [`dax/`](dax/) directory.

## Step 4. Interactive Food Security Index Construction

<img width="1279" height="715" alt="image" src="https://github.com/user-attachments/assets/5b77784b-28d5-4d83-8ee5-9bb7e250fe05" />

This step introduces a dedicated interactive dashboard for constructing a custom Food Security Index (FSI).
The dashboard follows the same structural design as the exploratory dashboards in Step 3, ensuring consistency in visual interpretation and user experience.

Unlike predefined composite indices, the Food Security Index in this project is fully user-driven.
Users can interactively define which indicators and dimensions are included in the index calculation, allowing flexible analytical scenarios and sensitivity analysis.

### **Dashboard structure and interaction logic**

The dashboard consists of the following key components:

- Indicator selection slicer

  A multi-select slicer allows users to choose which indicators are included in the index calculation.
Indicators are organized by food security dimensions, enabling transparent and controlled model specification.

- Geographic visualization (Map)

  Displays the resulting Food Security Index across African countries, allowing spatial comparison and identification of regional patterns.

- Time series visualization (Line Chart)

    Shows the evolution of the constructed index over time for selected countries or aggregated regions.

- KPI cards

  Summarize the overall level and long-term trend of the constructed index using average values and compound annual growth rates (CAGR).

All visuals update dynamically based on indicator selection, country filters, and time context.

### **Index construction methodology**

The Food Security Index is computed based on three core methodological principles:

**1. Indicator normalization**

  All indicators included in the index are normalized to a common scale [0,1] prior to aggregation.

  This ensures comparability across indicators with different units of measurement and different directional effects.

  Indicators with a positive contribution to food security are scaled directly, while indicators with a negative contribution are inverted so that higher normalized values always represent better outcomes.

**2. Dimensional structure**

Indicators are grouped into four conceptual food security dimensions:

- Availability - physical supply of food;

- Accessibility - economic and institutional access to food;

- Quality - nutritional outcomes and dietary adequacy;

- Stability - resilience of food systems over time.

This structure aligns the index with widely accepted food security frameworks and ensures interpretability of results.

**3. Adaptive weighting scheme**

The weighting system is dynamic and selection-dependent, rather than fixed.

- Each selected food security dimension receives equal total weight.

- Within each dimension, the total weight is evenly distributed among the selected indicators belonging to that dimension.

- The final weight of each indicator therefore depends on:

  - the number of selected dimensions;

  - the number of indicators selected within each dimension.

This approach prevents dominance of dimensions with many indicators and allows users to explore alternative index specifications transparently.

### **General index formulation**

The Food Security Index for country i at time t is calculated as a weighted sum of normalized indicators:

<div align="center">
  
***FSI(i, t) = Σ_c Σ_j∈c [ (1 / (C × N(c) )) × x_norm(i, t, j) ]***
  
</div>

where:

***x_norm(i, t, j)*** is the normalized value of indicator ***j*** for country ***i*** at time ***t***;

***w(c, j) = 1 / (C × N_c)*** is the weight assigned to indicator ***j*** in category ***c***;

***C*** is the number of selected categories;

***N_c*** is the number of selected indicators within category c.

This formulation guarantees:
- equal contribution of each selected food security dimension;

- flexibility with respect to indicator selection;

- transparency and reproducibility of index results.

**Analytical advantages of the approach**

The interactive construction of the Food Security Index enables:

- sensitivity analysis with respect to indicator inclusion;

- comparison of alternative index specifications;

- transparent assessment of how individual indicators and dimensions influence overall food security outcomes;

- alignment between exploratory analysis (Step 3) and modeling stages (Step 5).

### Implementation note

The index calculation logic is implemented using custom DAX measures that respond dynamically to filter context and slicer selections and available in the [`dax/`](dax/) directory.

The methodological description above reflects the conceptual logic of the index, independent of its technical implementation.

## Step 5. Data Preparation for Regression Analysis
This step focuses on preparing a unified and consistent dataset for subsequent regression and econometric analysis.

All transformations are performed within Power BI using calculated tables to ensure full integration with the interactive analytical workflow. DAX formulas for calculated table are lockated in the [`dax/`](dax/) directory 

### Purpose:

The goal of this step is to construct a model-ready dataset that combines:

- independent variables used as explanatory factors in the model;

- the Food Security Index, used as the dependent variable.

This step is required because the Python visual used in subsequent analysis does not correctly respond to filter context when data originates from multiple tables, even if those tables are related or combined through the data model.

To ensure that all filters (indicator selection, country, and time) are consistently applied within the Python visual, all relevant variables must be explicitly consolidated into a single analytical table.

This structure enables a seamless and technically robust transition from exploratory analysis to statistical modeling.

### Logic:

**1. Unified analytical dataset**

A single analytical table is created by merging two data sources:

- model input variables from model_data;

- normalized Food Security Index values from food_security_index_data.

Both sources are aligned by country (ISO-3 code) and year, and combined into a long-format table.

An additional field (model_type) is used to distinguish between:

- model - independent variables;

- index - the Food Security Index used as the dependent variable.

To ensure numerical stability and comparability across indicators, selected variables are rescaled during the transformation process (e.g. percentage-based indicators and large-magnitude variables).

**2. Indicator directory for model control**

A separate indicator directory table is created to support interactive control of model specification.

This table consolidates:

- independent variables used for model construction;

- indicators used to calculate the Food Security Index.

Each indicator is labeled with:

- its readable name;

- thematic category;

- source type (model factor vs. index component).

This structure allows the same slicer logic to be used consistently across:

- model variable selection;

- index-based dependent variable selection.

### Output:

As a result of this step:

- a clean, unified panel dataset is produced for regression analysis;

- indicators are fully traceable by category and role in the model;

- the dataset is ready for use in downstream modeling, including elasticity estimation and scenario analysis.

### Implementation note: 

The transformations described above are implemented using calculated tables and conditional logic.
The conceptual structure of the prepared dataset is independent of the specific implementation syntax and can be reproduced in other analytical environments.



## Step 6. Panel Data Modeling with Country and Time Effects
<img width="1278" height="718" alt="image" src="https://github.com/user-attachments/assets/93c09d1f-db02-417f-9ef8-9918970045ad" />

This step implements an econometric panel data model to quantify the relationship between the constructed Food Security Index and selected socio-economic, political, and environmental factors.

The analysis is performed using a Random Effects panel model with country-specific and time-specific effects, allowing the model to capture unobserved heterogeneity across countries and common shocks across years.

### Model logic and data flow

The modeling process follows a structured sequence of data preparation and estimation steps:

### 1. Input data validation and filtering

The model operates on a single unified dataset prepared in Step 5.

Before estimation, the script verifies that all required variables are present and that at least one independent variable remains after interactive filtering.

Two data streams are then separated:
- Dependent variable: dynamically constructed Food Security Index (fsi_gen);
- Independent variables: selected model factors (model_type = "model").

This design ensures that the panel model fully respects the interactive selection logic defined earlier in the dashboard.
  
```python
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
```

  ### 2. Dynamic construction of the dependent variable

The Food Security Index used in the panel model is reconstructed inside the Python visual using the same logic as in Step 4.

Indicators are:
- grouped by food security dimension;
- equally weighted across dimensions;
- evenly distributed within each dimension.

The weighted and normalized indicator values are aggregated at the country–year level, producing a consistent dependent variable (fsi_gen) that is fully synchronized with user selections.

This guarantees alignment between:
- the index used for visualization;
- the index used for panel data estimation.

```python
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
```

### 3. Reshaping independent variables

Selected independent variables are transformed from a long format into a wide panel structure, where:
- each row represents a country–year observation;
- each column represents a model factor.

This structure is required for panel data estimation and ensures proper alignment with the dependent variable.

```python
eco_vars = sorted(df_model['indicator'].dropna().unique().tolist())

if not eco_vars:
    plt.text(0.1, 0.5, "There are no independent variables after filtering.", fontsize=15)
    plt.axis('off')
    plt.show()
else:
    eco_wide = (
        df_model.pivot_table(index=['iso_3', 'year'], columns='indicator', values='value')
        .reset_index()
    )

    data = pd.merge(fsi_df, eco_wide, on=['iso_3', 'year'], how='inner')
```

### 4. Standardization of regressors

All independent variables are standardized using z-score normalization prior to estimation.

This step serves two purposes:
- improves numerical stability of the panel model;
- allows coefficients to be interpreted on a comparable scale, facilitating elasticity-style interpretation.

A constant term is explicitly added to capture the baseline level of food security.

```python
    X_cols = [c for c in data.columns if c not in ['iso_3','year','fsi_gen']]
    scaler = StandardScaler()
    data_scaled = data.copy()
    data_scaled[X_cols] = scaler.fit_transform(data[X_cols])
    data_scaled = add_constant(data_scaled, has_constant='add')

    data_scaled = data_scaled.set_index(['iso_3','year']).sort_index()
    y = data_scaled['fsi_gen']
    X = data_scaled[['const'] + X_cols]
```

### 5. Panel model specification

The model is specified as a Random Effects panel data model with country and time effects:
- country-level random effects capture unobserved, time-invariant heterogeneity across countries;
- time effects capture common shocks affecting all countries in a given year.

Conceptually, the model can be written as:
<div align="center">
  
***FSI(i, t) = β₀ + Σ β_k X_kit + μ_i + λ_t + ε_it***
  
</div>

where:

- ***FSI(i, t)*** is the Food Security Index for country ***i*** in year ***t***;

- ***X(k, i, t)*** are standardized independent variables;

- ***μ(i)*** represents country-specific effects;

- ***λ(t)*** represents year effects;

- ***ε(i, t)*** is the idiosyncratic error term.

```python
model = RandomEffects(y, X)
```
### 6. Estimation and intercept adjustment

After model estimation:

- fitted values are compared with observed values;

- a small adjustment is applied to the intercept to align predicted and observed index levels.

This step improves interpretability of the estimated equation without affecting slope coefficients or relative effect sizes.

```python
res = model.fit()

    bias = (res.fitted_values.squeeze() - y.squeeze()).mean()
    params = res.params.copy()
    params['const'] = params['const'] - bias

    def fmt(x):
        try: return f"{float(x):.4f}".replace('.', ',')
        except: return str(x)

    eq_parts = [fmt(params['const'])]
```

## Step 7. Model Analysis

### Regression Equation Construction

<img width="1254" height="105" alt="image" src="https://github.com/user-attachments/assets/2694c9e6-af78-44f8-ba95-8ae76e1459a7" />

**Purpose:**

Construct and visualize the analytical form of the estimated panel data model, reflecting the relationship between the Food Security Index and selected independent variables.

**Logic:**

1. Input data validation and separation

The script operates on the unified dataset prepared in the previous step and verifies that all required fields are present before proceeding.

```python
required_cols = {'iso_3', 'year', 'indicator', 'model_type', 'value', 'ind_name', 'category'}
if not required_cols.issubset(df.columns):
    raise ValueError("There are no independent variables after filtering.")
```

The data is then split into:

- index components (**model_type == "index"**), used to reconstruct the dependent variable;

- model factors (**model_type == "model"**), used as regressors.

```python
df_index = df[df['model_type'] == 'index'].copy()
df_model = df[df['model_type'] == 'model'].copy()
```

2. Dynamic reconstruction of the dependent variable

The Food Security Index (fsi_gen) is reconstructed inside the Python visual using the same category-based weighting logic applied earlier in the project.

Category weights are computed dynamically:

```python
weights[cat] = (1 / n_cat) / n_ind
```

Weighted indicator contributions are aggregated at the country–year level:

```python
fsi_df = df_index.groupby(['iso_3', 'year'])['fsi_part'].sum()
```

This ensures that the dependent variable used in the model is fully synchronized with user selections.

3. Preparation of independent variables

Selected independent variables are reshaped from long to wide format to form a panel-compatible design matrix.

```python
eco_wide = df_model.pivot_table(
    index=['iso_3', 'year'],
    columns='indicator',
    values='value'
)
```

The reconstructed index and regressors are merged into a single modeling dataset:

```python
data = pd.merge(fsi_df, eco_wide, on=['iso_3', 'year'], how='inner')
```

4. Standardization and model matrix construction

All independent variables are standardized using z-score normalization to ensure numerical stability and coefficient comparability.

```python
scaler = StandardScaler()
data_scaled[X_cols] = scaler.fit_transform(data[X_cols])
```

A constant term is explicitly added:

```python
data_scaled = add_constant(data_scaled, has_constant='add')
```

The dataset is then indexed by country and year, forming a proper panel structure.

5. Panel model estimation

The model is estimated as a Random Effects panel model with country-specific effects.

```python
model = RandomEffects(y, X)
res = model.fit()
```

This specification captures unobserved, time-invariant heterogeneity across countries while exploiting both cross-sectional and temporal variation in the data.

6. Intercept alignment

After estimation, the average difference between fitted and observed values is computed and used to adjust the intercept.

```python
bias = (res.fitted_values.squeeze() - y.squeeze()).mean()
params['const'] = params['const'] - bias
```

This adjustment improves alignment between predicted and observed index levels without affecting slope coefficients.

7. Dynamic equation assembly and visualization

The estimated coefficients are formatted and assembled into a readable analytical equation.

```python
eq_parts = [fmt(params['const'])]
for v in X_cols:
    eq_parts.append(f"{fmt(params[v])} * {v}")
```

The final equation explicitly includes country-specific effects and is rendered directly on the dashboard:

```python
equation = "fsi = " + " + ".join(eq_parts) + " + μ_i + λ_t"
```

The equation updates dynamically in response to changes in indicator selection and filtering.

### Correlation Matrix Construction

<img  align="left" width="466" height="501" alt="image" src="https://github.com/user-attachments/assets/2975f77d-0866-4be6-b5c1-08b6b21b2016" />

**Purpose:**

Analyze linear relationships between the dynamically constructed Food Security Index and selected independent variables within a consistent modeling context.

**Logic:**

1. Reuse of model-ready data

The correlation matrix is built using the same unified and filtered dataset that is prepared for panel modeling.

This ensures full consistency between correlation analysis and subsequent econometric estimation.

```python
df = dataset.copy()
```

2. Dynamic reconstruction of the Food Security Index

The Food Security Index is reconstructed inside the Python visual using the same category-based weighting logic applied in the index construction step.

```python
df_index = df[df['model_type'] == 'index'].copy()
```

Category-level weights are computed dynamically based on the number of selected categories and indicators:

```python
weights[cat] = (1 / n_cat) / n_ind
```

Weighted indicator contributions are aggregated at the country–year level:

```python
fsi_df = df_index.groupby(['iso_3', 'year'])['fsi_part'].sum()
```

3. Preparation of independent variables

Selected model factors are reshaped from long format into a wide panel structure and merged with the Food Security Index:

```python
eco_wide = df_model.pivot_table(
    index=['iso_3', 'year'],
    columns='indicator',
    values='value'
)
data = pd.merge(fsi_df, eco_wide, on=['iso_3', 'year'], how='inner')
```

4. Standardization prior to correlation analysis

All independent variables are standardized using z-score normalization to prevent scale effects from influencing correlation coefficients:

```python
scaler = StandardScaler()
data_scaled[X_cols] = scaler.fit_transform(data[X_cols])
```

5. Correlation matrix computation

Pearson correlation coefficients are calculated for the Food Security Index and all selected independent variables:

```python
corr_data = data_scaled[['fsi_gen'] + X_cols]
corr_matrix = corr_data.corr(method='pearson').round(2)
```

6. Visualization logic

The correlation matrix is visualized using a custom diverging color scale, where:
- red tones indicate negative correlations,
- green tones indicate positive correlations,
- neutral colors represent weak or near-zero relationships.

```python
custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom_corr",
    [(1, 0, 0), (1, 1, 0), (0, 0.6, 0)]
)
```
Numeric correlation values are displayed directly within each matrix cell to support precise interpretation.

### Actual vs Theoretical Food Security Index Dynamics

<img  align="left" width="466" height="504" alt="image" src="https://github.com/user-attachments/assets/539f7f73-f991-4682-80a9-d1ff23a08a61" />


**Purpose:**

Compare the temporal dynamics of the observed (actual) Food Security Index with the model-implied (theoretical) index to assess how well the estimated panel model reproduces long-term food security trends.

**Logic:**

1. Reconstruction of the actual Food Security Index

The observed Food Security Index is reconstructed dynamically using normalized index components and category-based weights, consistent with previous steps.

```python
df_index = df[df['model_type'] == 'index'].copy()
```

Category weights are computed based on the number of selected dimensions and indicators:

```python
weights[cat] = (1 / n_cat) / n_ind
```

Weighted indicator values are aggregated at the country–year level:

```python
fsi_df = (
    df_index.groupby(['iso_3', 'year'])['fsi_part']
    .sum()
    .rename(columns={'fsi_part': 'fsi_gen'})
)
```

To obtain a global trend, the index is averaged across countries for each year:

```python
fsi_actual = fsi_df.groupby('year')['fsi_gen'].mean()
```

2. Estimation of the panel data model

Independent variables are reshaped into a wide panel format, standardized, and combined with the reconstructed index.

```python
eco_wide = df_model.pivot_table(
    index=['iso_3', 'year'],
    columns='indicator',
    values='value'
)
```

The model is estimated as a Random Effects panel model with country-specific effects:

```python
model = RandomEffects(y, X)
res = model.fit()
```

An intercept adjustment is applied to improve alignment between fitted and observed index levels:

```python
params['const'] = params['const'] - bias
```

3. Construction of the theoretical Food Security Index

Using the estimated model parameters, a theoretical Food Security Index is computed for each country–year observation.

The theoretical index is defined as the linear combination of standardized regressors and estimated coefficients:

```python
df_theoretical['FSI_theoretical'] = params['const']
for var in X_cols:
    df_theoretical['FSI_theoretical'] += params[var] * df_theoretical[var]
```

To ensure comparability with the observed index, theoretical values are averaged across countries for each year:

```python
fsi_theoretical = df_theoretical.groupby('year')['FSI_theoretical'].mean()
```

4. Temporal comparison and visualization

Observed and theoretical indices are merged by year and visualized jointly to compare their dynamics over time:

```python
fsi_compare = pd.merge(fsi_actual, fsi_theoretical, on='year')
```

The resulting line chart highlights:

the empirical trajectory of food security (Actual FSI);

the trajectory implied by the estimated model (Theoretical FSI).

This comparison allows for an intuitive assessment of model performance in capturing long-term trends rather than individual country-level fluctuations.

### Regression Analysis and ANOVA
<img align="left" width="466" height="442" alt="image" src="https://github.com/user-attachments/assets/8b84c3af-460c-4249-ae14-84bb989cf085" />

**Purpose:**

Evaluate the overall explanatory power of the selected independent variables and assess the statistical significance of the constructed model using classical regression diagnostics and ANOVA decomposition.

**Logic:**

1. Preparation of the dependent variable

The Food Security Index (fsi_gen) is reconstructed dynamically using normalized index components and category-based weights, consistent with the index construction logic applied in previous steps.

```python
df_index = df[df['model_type'] == 'index'].copy()
```

Category-level weights are computed based on the number of selected dimensions and indicators:

```python
weights = {cat: (1 / n_cat) / df_index[df_index['category'] == cat]['ind_name'].nunique()}
```

Weighted indicator contributions are aggregated at the country–year level:

```python
fsi_df = df_index.groupby(['iso_3', 'year'])['fsi_part'].sum()
```

2. Preparation of independent variables

Selected model factors are reshaped from long to wide format and merged with the reconstructed Food Security Index:

```python
eco_wide = df_model.pivot_table(
    index=['iso_3', 'year'],
    columns='indicator',
    values='value'
)
data = pd.merge(fsi_df, eco_wide, on=['iso_3', 'year'], how='inner')
```

All independent variables are standardized using z-score normalization to ensure comparability of coefficients:

```python
scaler = StandardScaler()
data_scaled[X_cols] = scaler.fit_transform(data[X_cols])
```

3. Ordinary Least Squares (OLS) regression

A classical Ordinary Least Squares (OLS) regression is estimated using the standardized independent variables and the reconstructed Food Security Index as the dependent variable:

```python
model = sm.OLS(y, X).fit()
```

This regression serves as a global explanatory benchmark, complementing the panel data model by focusing on overall fit and variance decomposition.

4. Model performance metrics

Key goodness-of-fit and diagnostic statistics are extracted from the fitted model, including:

```python
model.rsquared
model.rsquared_adj
model.fvalue
model.f_pvalue
```

These metrics summarize:

- the proportion of variance explained by the model;

- the adjusted explanatory power accounting for model complexity;

- the overall statistical significance of the regression.

5. ANOVA decomposition

An Analysis of Variance (ANOVA) table is constructed to decompose total variation in the Food Security Index into:

- variation explained by the regression model;

- unexplained (residual) variation.

```python
anova_table = pd.DataFrame({
    "SS": [reg_ss, res_ss, reg_ss + res_ss],
    "F": [f_val, None, None]
})
```

This decomposition provides a clear statistical assessment of whether the selected factors jointly explain a significant share of variation in food security outcomes.

6. Tabular visualization

Regression summary statistics and the ANOVA table are rendered as formatted tables directly within the dashboard:

```python
ax.table(...)
```

This presentation enables users to:

inspect model quality at a glance;

compare explained vs. unexplained variance;

assess overall model significance without leaving the analytical interface.





# Data Sources
The indicators used in this project were collected from internationally recognized and publicly available data sources.
Each source was selected based on data coverage, methodological transparency, and relevance to food security analysis.

## [FAO — FAOSTAT: Suite of Food Security Indicators](https://www.fao.org/faostat/en/#data/FS)

Indicators used (Food Security Index construction):
- Average dietary energy supply (kcal per capita per day);
- Average protein supply (g per capita per day);
- Average fat supply (g per capita per day);
- Cereal import dependency ratio (%);
- Variability of food supply (kcal per capita per day);
- Coefficient of variation of dietary energy supply;
- Retail-level food losses (%);
- Share of irrigated arable land (%);
- Prevalence of undernourishment (% of population);
- Prevalence of stunting among children under five (%);
- Prevalence of obesity (% of total population).

## [International Trade Centre — Trade Map](https://www.trademap.org/Index.aspx)

Indicators used (economic and trade-related factors):
- Share of food imports in total imports (%);
- Ratio of food imports to food exports;
- Food imports per capita (USD).

## [Observatory of Economic Complexity](https://oec.world/en)

Indicators used (trade structure and dependency):
- Share of food imports in total imports (%);
- Ratio of food imports to food exports;
- Food imports per capita (USD).

## [Our World in Data](https://ourworldindata.org/grapher/average–precipitation–per–year)

Indicators used (political and environmental factors):
- Presence of internal or external conflicts;
- Political stability and absence of violence/terrorism index;
- Overall political stability index;
- Cereal yield (quintals per hectare);
- Average annual precipitation (mm);
- Number of months per year affected by natural, technological, or other disasters.

## [World Bank](https://www.worldbank.org/ext/en/who–we–are)

Indicators used (economic and social factors):
- GDP per capita (USD);
- Inflation rate (%);
- Urbanization rate (% of population living in urban areas);
- Unemployment rate (%);
- Natural population growth rate (%);
- Food imports per capita (USD).

Notes:
- Indicators obtained from multiple sources were cross-validated to ensure consistency.
- All data were harmonized across countries and years prior to index construction and modeling.
- Raw datasets are not included in the repository and are used exclusively for analytical processing.

# Food Security Model in Africa

## Introduction

### About the Project
This project focuses on analyzing food security in African countries based on socio-economic, political, and ecological indicators.

### Objectives:
To develop an interactive analytical tool for exploring and modeling food security levels across African countries and regions.

### Goals:
To provide a flexible analytical framework that enables users to:
- compare countries and time periods;
- analyze indicators that contribute to the food security index and are used in model construction;
- dynamically calculate a food security index based on selected indicators;
- explore the impact of individual factors on a dynamically constructed food security index.

### Methodology & Tools:
- **Power BI** - interactive dashboards and data visualization  
- **Python** - data processing, calculations, and statistical modeling  
- **Excel** - data preparation and structuring  
- **Statistical methods** - index construction, relationships, and elasticity coefficients  

## Data Description

The project is based on a panel dataset covering 54 African countries over a 10-year period (2014–2023).
The data is organized into two conceptually distinct components:
1) indicators used for the construction of the Food Security Index (FSI), and
2) indicators used for modeling the determinants of food security.

### 1. Data for Food Security Index Construction

Indicators used for constructing the composite Food Security Index (FSI) were selected to reflect the core dimensions of food security and grouped into five categories.

### Food Availability:
- average dietary energy supply (kcal per capita per day);
- average protein supply (g per capita per day);
- average fat supply (g per capita per day);
- cereal import dependency ratio (%).

### Food Access:
- GDP per capita (USD);
- share of food imports in total imports (%);
- political stability and absence of violence/terrorism index;
- share of population with access to basic drinking water services (%).

### Food Quality:
- prevalence of stunting among children under five (%);
- prevalence of obesity (% of total population).

### Stability and Resilience:
- variability of food supply (kcal per capita per day);
- coefficient of variation of caloric intake;
- retail-level food losses (%);
- share of irrigated arable land (%).

### Undernourishment (Summary Indicator)
- prevalence of undernourishment (% of population), reported by the FAO.

### 2. Data for Econometric and Analytical Modeling

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

## Project Workflow
### Step 1. Data Preparation
After collecting and aggregating data from multiple sources, all indicators were consolidated into a **single structured Excel dataset**.
The dataset is organized as a multi-sheet Excel file and includes the following sheets:
- **model_data** - panel data for 54 African countries over 10 years, containing independent variables used in the analytical model;
- **food_security_index_data** - panel data for 54 African countries over 10 years, containing indicators used for the construction of the custom Food Security Index;
- **country_name** - mapping table with ISO-3 country codes and corresponding country names;
- **indicator_name_index** - metadata table containing indicator codes used in the Food Security Index, their full names, units of measurement, and category assignment (Availability, Accessibility, Quality, Stability);
- **indicator_name_model** - metadata table containing independent variables used in the analytical model, including full names, units of measurement, and category assignment (Economic, Social, Political, Ecological).

### Step 2. Data Loading and Transformation in Power BI

The consolidated Excel dataset was imported into Power BI and transformed using Power Query.
This step prepares the data for index construction and analytical modeling.

Transformation workflow:
1. Load all sheets from the Excel file into Power Query.
2. Assign correct data types to country identifiers, years, and numeric indicators.
3. Reshape indicator tables **model_data** and **food_security_index_data** into a long format.
4. Create separate transformed tables for index construction and analytical modeling.

> Power Query (M) scripts used in this step are available in the [`power_query/`](power_query/) directory.

### Step 3. Exploratory Analysis of Independent Variables for Model and Indicators for Calculation of Food Security Index

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

**1. Dynamic Dashboard Title**

<img width="957" height="54" alt="image" src="https://github.com/user-attachments/assets/3ab8531a-b319-4b8b-8834-6b045373cad7" />

**Purpose:** displays a fully interactive dashboard title reflecting the selected indicator, geographic scope, and year.

**Logic:** the title adapts to the filter context: when a single country is selected, it shows the indicator name, country, and year; when multiple countries are selected, the geographic scope is aggregated to Africa.

**Data:** model_data, indicator_name_model, country_name.

**DAX logic:** conditional text generation based on filter context using HASONEVALUE and SELECTEDVALUE.

**2. Indicator and Time Selector (Slicer)**

<img align="left" width="466" height="332" alt="image" src="https://github.com/user-attachments/assets/22a5f42a-afde-453e-83e3-1402a6f875fd" />

**Purpose:** enable controlled selection of indicators and time periods to define a consistent analytical context for all visuals.

**Logic:** The indicator category slicer is configured for single selection only to ensure unambiguous indicator context.

The time slicer is also restricted to single-year selection and uses the Tile layout (instead of Between) to guarantee correct alignment of values across visuals.

To preserve correct interpretation of trends and summary metrics, Edit Interactions are used to disable the influence of the time slicer on:

- Time Series Visualization (Line Chart);

- KPI Cards (Annual Average, CAGR).

**Data:** indicator_name_model, model_data

**3. Country Ranking (Bar Chart) & Geographic Distribution (Map)**

<img align="left" width="466" height="251" alt="image" src="https://github.com/user-attachments/assets/1c49018e-14bd-4aaf-b506-85c032f5434a" />

**Purpose:** Compares countries based on the selected independent indicator for a chosen year, enabling relative performance assessment across countries.

**Logic:** To ensure meaningful comparison across indicators with different units and directions of impact, country values are first transformed using indicator-level normalization.
A min–max normalization is applied separately for each indicator, converting raw values to a standardized scale between 0 and 1.

For indicators where higher values represent better outcomes, normalization is defined as:

<div align="center">
  
***x_norm = 1 - (x - min(x)) / (max(x) - min(x))***
  
</div>

For indicators where higher values represent worse outcomes, an inverted normalization is applied:	​

<div align="center">
  
***x_norm = 1 - (x - min(x)) / (max(x) - min(x))***
  
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

4. Time Series Visualization (Line Chart)
<img align="left" width="466" height="124" alt="image" src="https://github.com/user-attachments/assets/812bfdce-6201-4780-a05f-145612464612" />

**Purpose:** displays temporal dynamics of the selected indicator across the full observation period (2014–2023).

**Logic:** values are aggregated by year and adjusted to the current slicer context.

**Data:** model_data

**DAX logic:** time-aware aggregation and CAGR calculation.

5. KPI Cards (Annual Average, CAGR)

<img align="left" width="217" height="253" alt="image" src="https://github.com/user-attachments/assets/217c648c-6ee4-49db-96ea-6ff09e75889f" />

**Purpose:** summarize the overall level and long-term trend of the selected indicator.

**Logic:** KPI cards respond dynamically to indicator and time selections.
To improve visual clarity and interpretability, the average annual value is displayed together with its corresponding unit of measurement, which adapts automatically based on the selected indicator and current filter context.

For trend representation, the compound annual growth rate (CAGR) is calculated over the selected time horizon.
The CAGR value is formatted using a percentage scale and explicitly includes a positive (+) or negative (–) sign, allowing users to immediately distinguish between increasing and decreasing trends.

**Data:** model_data.

**DAX logic:** context-aware measures for average annual values with dynamic unit labeling, and custom time-based measures for compound annual growth rates with sign-aware percentage formatting.

> DAX measures used for this dashboard are available in the [`dax/`](dax/) directory.

### Step 4. Interactive Food Security Index Construction

<img width="1279" height="715" alt="image" src="https://github.com/user-attachments/assets/5b77784b-28d5-4d83-8ee5-9bb7e250fe05" />

This step introduces a dedicated interactive dashboard for constructing a custom Food Security Index (FSI).
The dashboard follows the same structural design as the exploratory dashboards in Step 3, ensuring consistency in visual interpretation and user experience.

Unlike predefined composite indices, the Food Security Index in this project is fully user-driven.
Users can interactively define which indicators and dimensions are included in the index calculation, allowing flexible analytical scenarios and sensitivity analysis.

**Dashboard structure and interaction logic**

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

**Index construction methodology**

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

**General index formulation**

The Food Security Index for country i at time t is calculated as a weighted sum of normalized indicators:

<div align="center">
  
***FSI(i, t) = Σ_c Σ_j∈c [ (1 / (C × N_c)) × x_norm(i, t, j) ]***
  
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

Implementation note

The index calculation logic is implemented using custom DAX measures that respond dynamically to filter context and slicer selections and available in the [`dax/`](dax/) directory..

The methodological description above reflects the conceptual logic of the index, independent of its technical implementation.

### Step 5. Interactive Food Security Index Construction




## Data Sources
The indicators used in this project were collected from internationally recognized and publicly available data sources.
Each source was selected based on data coverage, methodological transparency, and relevance to food security analysis.

### [FAO — FAOSTAT: Suite of Food Security Indicators](https://www.fao.org/faostat/en/#data/FS)

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

### [International Trade Centre — Trade Map](https://www.trademap.org/Index.aspx)

Indicators used (economic and trade-related factors):
- Share of food imports in total imports (%);
- Ratio of food imports to food exports;
- Food imports per capita (USD).

### [Observatory of Economic Complexity](https://oec.world/en)

Indicators used (trade structure and dependency):
- Share of food imports in total imports (%);
- Ratio of food imports to food exports;
- Food imports per capita (USD).

### [Our World in Data](https://ourworldindata.org/grapher/average–precipitation–per–year)

Indicators used (political and environmental factors):
- Presence of internal or external conflicts;
- Political stability and absence of violence/terrorism index;
- Overall political stability index;
- Cereal yield (quintals per hectare);
- Average annual precipitation (mm);
- Number of months per year affected by natural, technological, or other disasters.

### [World Bank](https://www.worldbank.org/ext/en/who–we–are)

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

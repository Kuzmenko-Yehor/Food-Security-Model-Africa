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

### Step 3. Exploratory Analysis of Independent Variables
<img width="1324" height="741" alt="image" src="https://github.com/user-attachments/assets/30d2fc7e-5bc4-43d5-a9dd-90e86f94d3e2" />
This dashboard is designed to analyze the temporal dynamics and geographic distribution of independent variables used in the food security modeling framework for African countries.

It enables interactive selection of indicators across economic, social, political, and environmental categories, allowing users to explore trends over time, compare countries, and assess spatial patterns.

**1. Dynamic Dashboard Title**

<img width="957" height="54" alt="image" src="https://github.com/user-attachments/assets/3ab8531a-b319-4b8b-8834-6b045373cad7" />

**Purpose:** displays a fully interactive dashboard title reflecting the selected indicator, geographic scope, and year.

**Logic:** the title adapts to the filter context: when a single country is selected, it shows the indicator name, country, and year; when multiple countries are selected, the geographic scope is aggregated to Africa.

**Data:** model_data, indicator_name_model, country_name.

**DAX logic:** conditional text generation based on filter context using HASONEVALUE and SELECTEDVALUE.

**2. Indicator Selector (Slicer)**

**Purpose:** enables dynamic selection of independent variables by category (Economic, Social, Political, Ecological).

**Logic:** slicers filter the fact table and dynamically change the context for all dependent visuals.

**Data:** indicator_name_model.

**3. Country Ranking (Bar Chart)**

<img align="left" width="284" height="292" alt="image" src="https://github.com/user-attachments/assets/db9b0ae4-f716-446f-992b-9fa07e4dd57f" />

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

This transformation ensures that higher normalized values consistently indicate better relative performance.
Countries are then dynamically ranked based on the normalized indicator values within the selected year and filter context.

**Data:**
model_data, country_name.

**DAX logic:**
Indicator-specific min–max normalization with conditional inversion, followed by dynamic ranking and context-aware sorting.

4. Geographic Distribution (Map)

- Purpose: visualizes the spatial distribution of the selected indicator across African countries.
- Logic: country-level values are mapped using ISO-3 country codes.
- Data: model_data, country_name.
- DAX logic: aggregation at country level with geographic binding.


4. Time Series Visualization (Line Chart)

Purpose: displays temporal dynamics of the selected indicator across the full observation period (2014–2023).

Logic: values are aggregated by year and adjusted to the current slicer context.

Data: model_data, Date/Year dimension.

DAX logic: time-aware aggregation and CAGR calculation.


5. KPI Cards (Annual Average, CAGR)

- Purpose: summarize the overall level and long-term trend of the selected indicator.
- Logic: KPIs respond dynamically to indicator and time selections.
- Data: model_data.
- DAX logic: custom measures for averages and compound annual growth rates.


> DAX measures used for this dashboard are available in the [`dax/`](dax/) directory.








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

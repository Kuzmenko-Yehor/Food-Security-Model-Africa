model_data_cagr = 
VAR StartYear = MIN('model_data'[year])
VAR EndYear   = MAX('model_data'[year])
VAR NumYears  = EndYear - StartYear
VAR StartValue = CALCULATE(
    AVERAGE('model_data'[value]),
    'model_data'[year] = StartYear
)
VAR EndValue = CALCULATE(
    AVERAGE('model_data'[value]),
    'model_data'[year] = EndYear
)
VAR Val = IF(
    NumYears > 0,
    DIVIDE(EndValue - StartValue, ABS(StartValue) * NumYears),
    BLANK()
)
RETURN
IF(Val < 0,
 FORMAT(Val*100, "0.00") & "%",
"+" & FORMAT(Val*100, "0.00") & "%"
)
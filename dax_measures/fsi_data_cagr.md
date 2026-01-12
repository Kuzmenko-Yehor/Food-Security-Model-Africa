fsi_data_cagr = 
VAR StartYear = MIN('food_security_index_data'[year])
VAR EndYear   = MAX('food_security_index_data'[year])
VAR NumYears  = EndYear - StartYear
VAR StartValue = CALCULATE(
    AVERAGE('food_security_index_data'[value]),
    'food_security_index_data'[year] = StartYear
)
VAR EndValue = CALCULATE(
    AVERAGE('food_security_index_data'[value]),
    'food_security_index_data'[year] = EndYear
)
VAR Val = IF(
    NumYears  0,
    DIVIDE(EndValue - StartValue, ABS(StartValue)  NumYears),
    BLANK()
)
RETURN
IF(Val  0,
 FORMAT(Val100, 0.00) & %,
+ & FORMAT(Val100, 0.00) & %
)
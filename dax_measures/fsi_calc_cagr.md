fsi_calc_cagr = 
VAR SelectedCategories = 
    CALCULATE(
        COUNTROWS(
            VALUES(indicator_name_index[category])
        )
    )
VAR AvailWeight = 
    DIVIDE(
        1SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Availability)
            )
        )
    )
VAR AccessWeight = 
    DIVIDE(
        1SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Accessibility)
            )
        )
    )
VAR QualityWeight = 
    DIVIDE(
        1SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Quality)
            )
        )
    )
VAR StabWeight = 
    DIVIDE(
        1SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Stability)
            )
        )
    )

VAR fsi = SUMX('food_security_index_data', 
    VAR Category = RELATED(indicator_name_index[category])
    VAR Weigh = 
        SWITCH(
            TRUE(),
            Category = Availability, AvailWeight,
            Category = Accessibility, AccessWeight,
            Category = Quality, QualityWeight,
            Category = Stability, StabWeight
        )
    RETURN 'food_security_index_data'[normalized_index_value]  Weigh)
VAR StartYear = MIN('food_security_index_data'[year])
VAR EndYear   = MAX('food_security_index_data'[year])
VAR NumYears  = EndYear - StartYear

VAR StartValue = CALCULATE(
        [fsi],
        'food_security_index_data'[year] = StartYear
    )

VAR EndValue = CALCULATE(
        [fsi],
        'food_security_index_data'[year] = EndYear
    )
VAR Val = DIVIDE(EndValue - StartValue, ABS(StartValue)  NumYears)

RETURN IF(Val  0,
 FORMAT(Val100, 0.00) & %,
+ & FORMAT(Val100, 0.00) & %
)
fsi = 
VAR SelectedCategories = 
    CALCULATE(
        COUNTROWS(
            VALUES(indicator_name_index[category])
        )
    )
VAR AvailWeight = 
    DIVIDE(
        1/SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = "Availability")
            )
        )
    )
VAR AccessWeight = 
    DIVIDE(
        1/SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = "Accessibility")
            )
        )
    )
VAR QualityWeight = 
    DIVIDE(
        1/SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = "Quality")
            )
        )
    )
VAR StabWeight = 
    DIVIDE(
        1/SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = "Stability")
            )
        )
    )

RETURN SUMX('food_security_index_data', 
    VAR Category = RELATED(indicator_name_index[category])
    VAR Weigh = 
        SWITCH(
            TRUE(),
            Category = "Availability", AvailWeight,
            Category = "Accessibility", AccessWeight,
            Category = "Quality", QualityWeight,
            Category = "Stability", StabWeight
        )
    RETURN 'food_security_index_data'[normalized_index_value] * Weigh)
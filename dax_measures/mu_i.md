mu_i = 
VAR SelectedCats =
    VALUES('indicator_directory'[category])

VAR AvailableCats =
    CALCULATETABLE(
        VALUES('indicator_name_index'[category]),
        TREATAS(SelectedCats, 'indicator_name_index'[category])
    )

VAR SelectedCategories = COUNTROWS(AvailableCats)
VAR AvailWeight =
    DIVIDE(
        1  SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Availability)
            )
        )
    )
VAR AccessWeight =
    DIVIDE(
        1  SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Accessibility)
            )
        )
    )
VAR QualityWeight =
    DIVIDE(
        1  SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Quality)
            )
        )
    )
VAR StabWeight =
    DIVIDE(
        1  SelectedCategories,
        CALCULATE(
            COUNTROWS(
                FILTER('indicator_name_index', 'indicator_name_index'[category] = Stability)
            )
        )
    )

VAR fsi =
    SUMX(
        'food_security_index_data',
        VAR Category = RELATED(indicator_name_index[category])
        VAR Weigh =
            SWITCH(
                TRUE(),
                Category = Availability, AvailWeight,
                Category = Accessibility, AccessWeight,
                Category = Quality, QualityWeight,
                Category = Stability, StabWeight
            )
        RETURN 'food_security_index_data'[normalized_index_value]  Weigh
    )

VAR fsi_country =
    AVERAGEX(
        VALUES(food_security_index_data[year]),
        [fsi]
    )

VAR total_fsi =
    CALCULATE(
        [fsi],
        ALL('food_security_index_data')
    )

VAR n_obs =
    CALCULATE(
        DISTINCTCOUNT('food_security_index_data'[country_year]),
        ALL('food_security_index_data')
    )

VAR global_fsi = DIVIDE(total_fsi, n_obs)

RETURN  fsi_country - global_fsi
fsi_data_avg_value&name = FORMAT(
    CALCULATE(
        AVERAGE(food_security_index_data[value]),
        'food_security_index_data'[indicator] = SELECTEDVALUE(food_security_index_data[indicator]),
        REMOVEFILTERS(food_security_index_data[year])
    ),
    0.00) &   & MAX('indicator_name_index'[dimension])
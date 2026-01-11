model_data_avg_value&name = FORMAT(
    CALCULATE(
        AVERAGE(model_data[value]),
        'model_data'[indicator] = SELECTEDVALUE(model_data[indicator]),
        REMOVEFILTERS(model_data[year])
    ),
    "0.00") & " " & MAX('indicator_name_model'[dimension])
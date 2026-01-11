normalized_model_value = 
VAR currentIndicator = 'model_data'[indicator]
VAR currentValue = 'model_data'[value]
VAR minValue = 
    CALCULATE(
        MIN('model_data'[value]),
        ALLEXCEPT('model_data', 'model_data'[indicator])
    )
VAR maxValue =
    CALCULATE(
        MAX('model_data'[value]),
        ALLEXCEPT('model_data', 'model_data'[indicator])
    )
RETURN 
SWITCH(
    TRUE(),
    'model_data'[indicator] IN {gdp, urb, hdi, pst, psi, pop, yld, rfl, ukrfim, fsi}, DIVIDE('model_data'[value] - minValue, MaxValue - minValue), 
    'model_data'[indicator] IN {inf, ffim, ier, fpc, une, war, dis, ukrdst}, 1 - DIVIDE('model_data'[value] - minValue, MaxValue - minValue)
)
normalized_index_value = 
VAR currentIndicator = 'food_security_index_data'[indicator]
VAR currentValue = 'food_security_index_data'[value]
VAR minValue = 
    CALCULATE(
        MIN('food_security_index_data'[value]),
        ALLEXCEPT('food_security_index_data', 'food_security_index_data'[indicator])
    )
VAR maxValue =
    CALCULATE(
        MAX('food_security_index_data'[value]),
        ALLEXCEPT('food_security_index_data', 'food_security_index_data'[indicator])
    )
RETURN 
SWITCH(
    TRUE(),
    'food_security_index_data'[indicator] IN {csa, api, afi, ali, gdpc, psvi, wat}, DIVIDE('food_security_index_data'[value] - minValue, MaxValue - minValue), 
    'food_security_index_data'[indicator] IN {cic, fim, stu, obe, fsv, cvc, cll, pun}, 1 - DIVIDE('food_security_index_data'[value] - minValue, MaxValue - minValue)
)
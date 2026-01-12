fsi_calc_dashboard_name = 
IF(HASONEVALUE(country_name[name]),
    Calculation of the Food Security Index for  & SELECTEDVALUE('country_name'[name]) &  in  & SELECTEDVALUE('food_security_index_data'[year]),
    Calculation of the Food Security Index for all African countries in  & SELECTEDVALUE('food_security_index_data'[year])
) 
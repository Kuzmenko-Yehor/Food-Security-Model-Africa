fsi_data_dashboard_name = 
IF(HASONEVALUE(country_name[name]),
    SELECTEDVALUE('indicator_name_index'[ind_name]) &  of  & SELECTEDVALUE('country_name'[name]) &  in  & SELECTEDVALUE('food_security_index_data'[year]),
    General  & SELECTEDVALUE('indicator_name_index'[ind_name]) &  of Africa in  & SELECTEDVALUE('food_security_index_data'[year])
) 
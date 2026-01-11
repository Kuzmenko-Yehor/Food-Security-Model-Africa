model_data_dashboard_name = 
IF(HASONEVALUE(country_name[name]),
    SELECTEDVALUE('indicator_name_model'[ind_name]) &  of  & SELECTEDVALUE('country_name'[name]) &  in  & SELECTEDVALUE('model_data'[year]),
    General  & SELECTEDVALUE('indicator_name_model'[ind_name]) &  of Africa in  & SELECTEDVALUE('model_data'[year])
) 
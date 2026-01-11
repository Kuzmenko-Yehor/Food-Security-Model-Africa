let
    Source = Excel.Workbook(File.Contents("D:\food_security_model_africa\panel_model_africa\data\data_food_security_model_africa.xlsx"), null, true),
    food_security_index_data_Sheet = Source{[Item="indicator_name_index",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(food_security_index_data_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"indicator", type text}, {"ind_name", type text}, {"dimension", type text}, {"category", type text}})
in
    #"Changed Type"
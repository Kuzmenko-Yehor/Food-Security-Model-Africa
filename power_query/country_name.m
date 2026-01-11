let
    Source = Excel.Workbook(File.Contents("D:\food_security_model_africa\panel_model_africa\data\data_food_security_model_africa.xlsx"), null, true),
    food_security_index_data_Sheet = Source{[Item="country_name",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(food_security_index_data_Sheet,{{"Column1", type text}, {"Column2", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true])
in
    #"Promoted Headers"
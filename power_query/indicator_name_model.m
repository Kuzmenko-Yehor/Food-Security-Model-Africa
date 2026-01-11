let
    Source = Excel.Workbook(File.Contents("D:\food_security_model_africa\panel_model_africa\data\data_food_security_model_africa.xlsx"), null, true),
    indicator_name_model_Sheet = Source{[Item="indicator_name_model",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(indicator_name_model_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"indicator", type text}, {"ind_name", type text}, {"dimension", type text}, {"category", type text}})
in
    #"Changed Type"
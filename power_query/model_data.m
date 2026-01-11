let
    Source = Excel.Workbook(File.Contents("D:\food_security_model_africa\panel_model_africa\data\data_food_security_model_africa.xlsx"), null, true),
    food_security_index_data_Sheet = Source{[Item="model_data",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(food_security_index_data_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"iso_3", type text}, {"year", Int64.Type}, {"gdp", type number}, {"inf", type number}, {"ier", type number}, {"fpc", type number}, {"urb", type number}, {"hdi", type number}, {"une", type number}, {"pop", type number}, {"war", Int64.Type}, {"pst", type number}, {"psi", type number}, {"yld", type number}, {"rfl", type number}, {"dis", Int64.Type}}),
    #"Unpivoted Only Selected Columns" = Table.Unpivot(#"Changed Type", {"gdp", "inf", "ier", "fpc", "urb", "hdi", "une", "pop", "war", "pst", "psi", "yld", "rfl", "dis"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Only Selected Columns",{{"Value", "value"}, {"Attribute", "indicator"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", each [iso_3] & " " & Text.From([year])),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"Custom", type text}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type1",{{"Custom", "country_year"}})
in
    #"Renamed Columns1"
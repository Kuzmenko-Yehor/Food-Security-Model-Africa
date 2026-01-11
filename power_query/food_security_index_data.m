let
    Source = Excel.Workbook(File.Contents("D:\food_security_model_africa\panel_model_africa\data\data_food_security_model_africa.xlsx"), null, true),
    food_security_index_data_Sheet = Source{[Item="food_security_index_data",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(food_security_index_data_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"iso_3", type text}, {"year", Int64.Type}, {"csa", type number}, {"api ", type number}, {"afi", type number}, {"cic", type number}, {"ali", type number}, {"gdpc", type number}, {"fim", type number}, {"wat", type number}, {"stu", type number}, {"obe", type number}, {"fsv", type number}, {"cvc", type number}, {"cll", type number}, {"pun", type number}}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"iso_3", "year"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Columns",{{"Attribute", "indicator"}, {"Value", "value"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", each [iso_3] & " " & Text.From([year])),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"Custom", type text}}),
    #"Renamed Columns2" = Table.RenameColumns(#"Changed Type1",{{"Custom", "country_year"}})
in
    #"Renamed Columns2"
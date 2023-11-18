import pandas as pd

from map_nl.map.chloropleth import ChloroplethMapNL

# Example usage
df = pd.read_csv("data/woz-pc4.csv")
m = ChloroplethMapNL(geojson_simplify_tolerance=0.0001).plot(
    df, pc4_column_name="pc4", value_column_name="WOZ", legend_name="Average WOZ Value"
)
m.save("map.html")
import pandas as pd

from map_nl.map import MapNL

# Example usage
df = pd.read_csv("data/woz-pc4.csv")
netherlands_map = MapNL(geojson_simplify_tolerance=0.0001)
m = netherlands_map.plot(df, pc4_column_name="pc4", value_column_name="WOZ")
m.save("map.html")

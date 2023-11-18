import pandas as pd

from map_nl.map.map import MapNL


def get_color(value):
    if not value:
        return "grey"
    if value > 500:
        return "green"
    else:
        return "blue"


def style(feature):
    return {"fillColor": get_color(feature.get("properties").get("WOZ"))}


# Example usage
df = pd.read_csv("data/woz-pc4.csv")
netherlands_map = MapNL(geojson_simplify_tolerance=0.0001)
m = netherlands_map.plot(df, pc4_column_name="pc4", value_column_name="WOZ", style_function=style, name="WOZ value")
m.save("map.html")

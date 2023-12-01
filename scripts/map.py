from __future__ import annotations

import pandas as pd

from map_nl import MapNL


def get_color(value):
    if not value:
        return "grey"
    if value > 500:
        return "green"
    else:
        return "blue"


def style(feature):
    return {"fillColor": get_color(feature.get("properties").get("WOZ"))}


df = pd.read_csv("data/woz-pc4.csv")
m = MapNL(geojson_simplify_tolerance=0.0001).plot(
    df, pc4_column_name="pc4", value_column_name="WOZ", style_function=style, name="WOZ value"
)
m.save("map.html")

from __future__ import annotations

import pandas as pd

from map_nl import ChoroplethMapNL

df = pd.read_csv("data/woz-pc4.csv")
m = ChoroplethMapNL(geojson_simplify_tolerance=0.0001).plot(
    df, pc4_column_name="pc4", value_column_name="WOZ", legend_name="Average WOZ Value", fill_color="OrRd"
)
m.save("map.html")

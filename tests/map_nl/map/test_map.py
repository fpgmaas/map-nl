from __future__ import annotations

import pandas as pd

from map_nl import MapNL
from tests.utils import run_within_dir


def test_plot(tmp_path, nl_pc4_geojson_sample):
    with run_within_dir(tmp_path):

        def get_color(value):
            if not value:
                return "grey"
            if value > 150:
                return "green"
            else:
                return "blue"

        def style(feature):
            return {"fillColor": get_color(feature.get("properties").get("WOZ"))}

        # Example usage
        df = pd.DataFrame({"pc4": ["3297", "3352"], "WOZ": [100, 200]})

        m = MapNL(geojson_simplify_tolerance=0.0001).plot(
            df, pc4_column_name="pc4", value_column_name="WOZ", style_function=style, name="WOZ value"
        )
        m.save("map.html")

from __future__ import annotations

import pandas as pd

from map_nl import ChoroplethMapNL
from tests.utils import run_within_dir


def test_choropleth(tmp_path, nl_pc4_geojson_sample):
    with run_within_dir(tmp_path):
        # Example usage
        df = pd.DataFrame({"pc4": ["3297", "3352"], "WOZ": [100, 200]})
        m = ChoroplethMapNL(geojson_simplify_tolerance=0.0001).plot(
            df, pc4_column_name="pc4", value_column_name="WOZ", legend_name="Average WOZ Value"
        )
        m.save("map.html")
        assert m

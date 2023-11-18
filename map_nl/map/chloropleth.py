from pathlib import Path

import folium
import pandas as pd

from map_nl.geojson.getter import GeoJsonGetter

GEO_JSON_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-netherlands-postcode-pc4/exports/geojson?lang=en&timezone=Europe%2FBerlin"
DATA_DIR = ".map_nl"


class ChloroplethMapNL:
    def __init__(self, geojson_simplify_tolerance: float | None = None):
        self.geojson_simplify_tolerance = geojson_simplify_tolerance
        self.geojson_path = Path(DATA_DIR) / "nl-pc4-map.geojson"
        # Coordinates roughly at the center of the Netherlands
        self.map_center = [52.1326, 5.2913]
        self.map_zoom_start = 8  # Initial zoom level

    def plot(self, df: pd.DataFrame, value_column_name: str, pc4_column_name: str, **kwargs):
        """Create a Chloropleth map with Folium."""

        pc4_geojson = self._get_geojson()

        # Initialize the map
        m = folium.Map(location=self.map_center, zoom_start=self.map_zoom_start)

        default_args = {
            "geo_data": pc4_geojson,
            "name": "choropleth",
            "data": df,
            "columns": [pc4_column_name, value_column_name],
            "key_on": "feature.properties.pc4_code",
            "fill_color": "YlGn",
            "fill_opacity": 0.7,
            "line_opacity": 0.1,
        }
        choropleth_args = {**default_args, **kwargs}

        # Add GeoJSON layer
        folium.Choropleth(**choropleth_args).add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)

        return m

    def _get_geojson(self):
        return GeoJsonGetter(
            url=GEO_JSON_URL, geojson_path=self.geojson_path, geojson_simplify_tolerance=self.geojson_simplify_tolerance
        ).get()

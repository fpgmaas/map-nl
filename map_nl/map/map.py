from pathlib import Path

import folium
import geopandas as gpd
import pandas as pd

from map_nl.geojson.getter import GeoJsonGetter

GEO_JSON_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-netherlands-postcode-pc4/exports/geojson?lang=en&timezone=Europe%2FBerlin"
DATA_DIR = ".map_nl"


class MapNL:
    def __init__(self, geojson_simplify_tolerance: float | None = None):
        self.geojson_simplify_tolerance = geojson_simplify_tolerance
        self.geojson_path = Path(DATA_DIR) / "nl-pc4-map.geojson"
        # Coordinates roughly at the center of the Netherlands
        self.map_center = [52.1326, 5.2913]
        self.map_zoom_start = 8  # Initial zoom level

    def plot(self, df: pd.DataFrame, value_column_name: str, pc4_column_name: str, **kwargs):
        """Create a Folium map."""

        df = self._prepare_input_data(df, pc4_column_name, value_column_name)
        pc4_geojson = self._get_geojson()
        pc4_geojson = self._add_values_to_geojson(pc4_geojson, df)

        # Initialize the map
        m = folium.Map(location=self.map_center, zoom_start=self.map_zoom_start)

        default_args = {"weight": 1, "opacity": 1, "color": "black", "dashArray": "3", "fillOpacity": 0.7}
        plot_args = {**default_args, **kwargs}

        # Add GeoJSON layer
        folium.GeoJson(pc4_geojson, **plot_args).add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)

        return m

    @staticmethod
    def _prepare_input_data(df: pd.DataFrame, pc4_column_name: str, value_column_name: str):
        df.rename(columns={pc4_column_name: "pc4_code"}, inplace=True)
        df["pc4_code"] = df["pc4_code"].astype("str")
        return df

    def _get_geojson(self):
        return GeoJsonGetter(
            url=GEO_JSON_URL, geojson_path=self.geojson_path, geojson_simplify_tolerance=self.geojson_simplify_tolerance
        ).get()

    @staticmethod
    def _add_values_to_geojson(geojson, df):
        gdf = gpd.GeoDataFrame.from_features(geojson["features"])
        merged_gdf = gdf.merge(df, on="pc4_code", how="left")
        return merged_gdf.to_json()

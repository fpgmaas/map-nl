from __future__ import annotations

import folium  # type: ignore
import geopandas as gpd  # type: ignore
import pandas as pd

from map_nl.map.base import BaseMapNL


class MapNL(BaseMapNL):
    """A class for creating custom PC4 maps of the Netherlands using `folium.GeoJson`."""

    def plot(self, df: pd.DataFrame, value_column_name: str, pc4_column_name: str, **kwargs) -> folium.Map:  # type: ignore
        """Creates and adds a custom map layer to the Folium map instance.

        This method processes the input DataFrame and GeoJSON data to create a
        Folium GeoJson layer, which is then added to the map.

        You can also pass any arguments to this function that are accepted by `folium.GeoJson`. For example,
        to add custom fill colors to the plot based on the column 'my_feature' in the DataFrame `df`, do the following:

        ```
        def get_color(value):
            if not value:
                return "grey"
            if value > 500:
                return "green"
            else:
                return "blue"

        def style(feature):
            return {"fillColor": get_color(feature.get("properties").get("my_feature"))}

        m = MapNL(geojson_simplify_tolerance=0.0001).plot(
            df, pc4_column_name="pc4", value_column_name="my_feature", style_function=style
        )
        ```

        Args:
            df (pd.DataFrame): DataFrame containing the data for the map.
            value_column_name (str): Name of the column in df that contains the values to be visualized.
            pc4_column_name (str): Name of the column in df that contains the PC4 area codes.
            **kwargs: Additional keyword arguments to customize the GeoJson layer.

        Returns:
            folium.Map: The Folium Map object with the custom layer added.
        """

        df = self._prepare_input_data(df, pc4_column_name)
        pc4_geojson = self._get_geojson()
        pc4_geojson = self._add_values_to_geojson(pc4_geojson, df)
        tooltip = self._get_default_tooltip(value_column_name)

        default_args = {
            "weight": 1,
            "opacity": 1,
            "color": "black",
            "dashArray": "3",
            "fillOpacity": 0.7,
            "tooltip": tooltip,
        }

        plot_args = {**default_args, **kwargs}
        folium.GeoJson(pc4_geojson, **plot_args).add_to(self.m)

        folium.LayerControl().add_to(self.m)

        return self.m

    @staticmethod
    def _prepare_input_data(df: pd.DataFrame, pc4_column_name: str) -> pd.DataFrame:
        df.rename(columns={pc4_column_name: "pc4_code"}, inplace=True)
        df["pc4_code"] = df["pc4_code"].astype("str")
        return df

    @staticmethod
    def _add_values_to_geojson(geojson: dict, df: pd.DataFrame) -> dict:
        gdf = gpd.GeoDataFrame.from_features(geojson["features"])
        merged_gdf = gdf.merge(df, on="pc4_code", how="left")
        return merged_gdf.to_json()

    @staticmethod
    def _get_default_tooltip(value_column_name: str) -> folium.GeoJsonTooltip:
        return folium.GeoJsonTooltip(
            fields=["pc4_code", "gem_name", value_column_name],
            aliases=["PC4:", "Gemeente:", f"{value_column_name}:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )

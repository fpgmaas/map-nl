from __future__ import annotations

import folium  # type: ignore
import pandas as pd

from map_nl.map.base import BaseMapNL


class ChoroplethMapNL(BaseMapNL):
    """A class for creating Choropleth maps of the Netherlands using `folium.Choropleth`."""

    def plot(  # type: ignore
        self, df: pd.DataFrame, value_column_name: str, pc4_column_name: str, tooltip: bool = True, **kwargs
    ) -> folium.Map:
        """This method takes a pandas DataFrame with PC4-data and plots a Choropleth map based on these data.
        Any **kwargs are passed on to `folium.Choropleth`. For example, to change the fill color, run

        ```
        m = ChoroplethMapNL(...).plot(..., fill_opacity=1)
        ```

        Args:
            df (pd.DataFrame): DataFrame containing the data for the Choropleth map.
            value_column_name (str): Name of the column in df that contains the values to be visualized.
            pc4_column_name (str): Name of the column in df that contains the postal code (PC4) information.
            tooltip (bool): Add a simple tooltip.
            **kwargs: Additional arguments that are passed to `folium.Choropleth`.

        Returns:
            folium.Map: The Folium Map object with the Choropleth layer added.
        """

        pc4_geojson = self._get_geojson()

        default_args = {
            "geo_data": pc4_geojson,
            "name": "choropleth",
            "data": df,
            "columns": [pc4_column_name, value_column_name],
            "key_on": "feature.properties.pc4_code",
            "fill_color": "Blues",
            "fill_opacity": 0.8,
            "line_opacity": 0.2,
            "nan_fill_color": "white",
        }
        choropleth_args = {**default_args, **kwargs}

        choropleth = folium.Choropleth(**choropleth_args).add_to(self.m)

        if tooltip:
            self._add_tooltip(choropleth, df, pc4_column_name, value_column_name)

        folium.LayerControl().add_to(self.m)

        return self.m

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

    def _add_tooltip(
        self, choropleth: folium.Choropleth, df: pd.DataFrame, pc4_column_name: str, value_column_name: str
    ) -> None:
        df_indexed = df.set_index(pc4_column_name)
        for s in choropleth.geojson.data["features"]:
            pc4_code = int(s.get("properties")["pc4_code"])
            if pc4_code in df_indexed.index:
                s["properties"][value_column_name] = str(df_indexed.loc[pc4_code, value_column_name])
            else:
                s["properties"][value_column_name] = None
        tooltip = self._get_default_tooltip(value_column_name)
        tooltip.add_to(choropleth.geojson)

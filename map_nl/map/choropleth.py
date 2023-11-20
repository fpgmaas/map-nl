import folium
import pandas as pd

from map_nl.map.base import BaseMapNL


class ChoroplethMapNL(BaseMapNL):
    """A class for creating Choropleth maps of the Netherlands using `folium.Choropleth`."""

    def plot(self, df: pd.DataFrame, value_column_name: str, pc4_column_name: str, **kwargs) -> folium.Map:
        """This method takes a pandas DataFrame with PC4-data and plots a Choropleth map based on these data.
        Any **kwargs are passed on to `folium.Choropleth`. For example, to change the fill color, run

        ```
        m = ChloroplethMapNL(...).plot(..., fill_opacity=1)
        ```

        Args:
            df (pd.DataFrame): DataFrame containing the data for the Choropleth map.
            value_column_name (str): Name of the column in df that contains the values to be visualized.
            pc4_column_name (str): Name of the column in df that contains the postal code (PC4) information.
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
            "fill_color": "YlGn",
            "fill_opacity": 0.7,
            "line_opacity": 0.1,
        }
        choropleth_args = {**default_args, **kwargs}

        # Add GeoJSON layer
        folium.Choropleth(**choropleth_args).add_to(self.m)

        # Add layer control
        folium.LayerControl().add_to(self.m)

        return self.m

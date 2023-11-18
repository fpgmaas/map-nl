import json
from pathlib import Path

import folium

from map_nl.utils.file_downloader import FileDownloader

GEO_JSON_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-netherlands-postcode-pc4/exports/geojson?lang=en&timezone=Europe%2FBerlin"
DATA_DIR = ".map_nl"


class MapNL:
    def __init__(self):
        self.geojson_path = Path(DATA_DIR) / "nl-pc4-map.geojson"
        # Coordinates roughly at the center of the Netherlands
        self.map_center = [52.1326, 5.2913]
        self.map_zoom_start = 8  # Initial zoom level

    def _download_geojson_if_not_exists(self):
        if not self.geojson_path.exists():
            FileDownloader(url=GEO_JSON_URL, file_path=self.geojson_path).download()

    def create(self):
        """Create a Folium map using the provided GeoJSON file."""

        self._download_geojson_if_not_exists()

        # Initialize the map
        m = folium.Map(location=self.map_center, zoom_start=self.map_zoom_start)

        with Path(self.geojson_path).open("r") as f:
            pc4_geojson = json.load(f)

        # Add GeoJSON layer
        folium.GeoJson(pc4_geojson, name="Postal Code 4 Map").add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)

        return m

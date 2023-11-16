import json
from pathlib import Path

import folium


class MapNL:
    def __init__(self, geojson_path):
        self.geojson_path = Path(geojson_path)
        self.map = None

        # Coordinates roughly at the center of the Netherlands
        self.map_center = [52.1326, 5.2913]
        self.map_zoom_start = 8  # Initial zoom level

    def create_map(self):
        """Create a Folium map using the provided GeoJSON file."""
        if not self.geojson_path.exists():
            return

        # Initialize the map
        self.map = folium.Map(location=self.map_center, zoom_start=self.map_zoom_start)

        with Path(self.geojson_path).open("r"):
            pc4_geojson = json.load()

        # Add GeoJSON layer
        folium.GeoJson(pc4_geojson, name="Postal Code 4 Map").add_to(self.map)

        # Add layer control
        folium.LayerControl().add_to(self.map)

    def show(self):
        """Display the map if it has been created."""
        if self.map is not None:
            return self.map
        else:
            pass

    def save(self, filename):
        """Save the map to an HTML file."""
        if self.map is not None:
            self.map.save(filename)
        else:
            pass

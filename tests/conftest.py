import json

import pytest


# Fixture to create a GeoJSON file
@pytest.fixture()
def geojson_file(tmp_path):
    # Create a GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]},
                "properties": {"name": "Sample Point"},
            }
        ],
    }

    # Define file path
    geojson_file = tmp_path / "example.geojson"

    # Write the GeoJSON to a file
    with open(geojson_file, "w") as f:
        json.dump(geojson, f)

    # Yield the path to the file for the test
    return geojson_file

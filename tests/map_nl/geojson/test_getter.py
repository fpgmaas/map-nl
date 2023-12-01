import json
import os

import pytest

from map_nl.geojson.getter import GeoJsonGetter
from tests.utils import run_within_dir


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


def test_skip_download_when_file_exists(tmp_path, geojson_file):
    with run_within_dir(tmp_path):
        getter = GeoJsonGetter("http://example.com/geojson", geojson_file)
        geojson = getter.get()
        assert geojson["type"] == "FeatureCollection"


def test_skip_download_and_simplify(tmp_path, geojson_file):
    """
    Assert that the file is not downloaded, it is loaded from disk, and then it is simplified and stored to disk with a new name.
    """
    with run_within_dir(tmp_path):
        getter = GeoJsonGetter("http://example.com/geojson", geojson_file, 0.1)
        getter.get()
        assert "example-simplified-0.1.geojson" in os.listdir(tmp_path)

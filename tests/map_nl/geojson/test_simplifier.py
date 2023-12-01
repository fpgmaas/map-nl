import os

from map_nl.geojson.simplifier import GeoJsonSimplifier
from tests.utils import run_within_dir


def test_simplifier(tmp_path, geojson_file):
    with run_within_dir(tmp_path):
        GeoJsonSimplifier(input_file_path=geojson_file, output_file_path="simplified.geojson", tolerance=0.1).simplify()
        assert "simplified.geojson" in os.listdir(tmp_path)

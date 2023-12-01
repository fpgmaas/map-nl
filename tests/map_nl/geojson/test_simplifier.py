from __future__ import annotations

import os

from map_nl.geojson.simplifier import GeoJsonSimplifier
from tests.utils import run_within_dir


def test_simplifier(tmp_path, nl_pc4_geojson_sample):
    with run_within_dir(tmp_path):
        GeoJsonSimplifier(
            input_file_path=nl_pc4_geojson_sample, output_file_path="simplified.geojson", tolerance=0.1
        ).simplify()
        assert "simplified.geojson" in os.listdir(tmp_path)
        size_file_original = os.path.getsize(nl_pc4_geojson_sample)
        size_file_simplified = os.path.getsize("simplified.geojson")
        assert size_file_simplified < size_file_original

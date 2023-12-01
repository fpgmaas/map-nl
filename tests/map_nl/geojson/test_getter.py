from __future__ import annotations

import os

from map_nl.geojson.getter import GeoJsonGetter
from tests.utils import run_within_dir


def test_skip_download_when_file_exists(tmp_path, nl_pc4_geojson_sample):
    with run_within_dir(tmp_path):
        getter = GeoJsonGetter("http://example.com/geojson", nl_pc4_geojson_sample)
        geojson = getter.get()
        assert geojson["type"] == "FeatureCollection"


def test_skip_download_and_simplify(tmp_path, nl_pc4_geojson_sample):
    """
    Assert that the file is not downloaded, it is loaded from disk, and then it is simplified and stored to disk with a new name.
    """
    with run_within_dir(tmp_path):
        getter = GeoJsonGetter("http://example.com/geojson", nl_pc4_geojson_sample, 0.1)
        getter.get()
        assert "nl-pc4-map-simplified-0.1.geojson" in os.listdir(tmp_path / ".map_nl")

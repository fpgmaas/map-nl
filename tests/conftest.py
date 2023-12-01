from __future__ import annotations

import shutil
from pathlib import Path

import pytest


# Fixture to provide the file '.map_nl/nl-pc4-map.geojson' within the temporary directory.
# It contains geojson for two PC4's.
@pytest.fixture()
def nl_pc4_geojson_sample(tmp_path: Path) -> Path:
    source_file = "tests/data/nl-pc4-map.geojson"
    dest_dir = tmp_path / ".map_nl"
    dest_dir.mkdir(parents=True)
    shutil.copy(source_file, dest_dir)
    return Path(dest_dir) / "nl-pc4-map.geojson"

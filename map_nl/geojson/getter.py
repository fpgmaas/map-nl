import json
from dataclasses import dataclass
from pathlib import Path

from map_nl.geojson.simplifier import GeoJsonSimplifier
from map_nl.utils.file_downloader import FileDownloader


@dataclass
class GeoJsonGetter:
    def __init__(self, url: str, geojson_path: Path, geojson_simplify_tolerance: float | None = None):
        self.geojson_simplify_tolerance = geojson_simplify_tolerance
        self.geojson_path = geojson_path
        self.url = url

    def get(self):
        if not self.geojson_path.exists():
            FileDownloader(url=self.url, file_path=self.geojson_path).download()

        if not self.geojson_simplify_tolerance:
            with Path(self.geojson_path).open("r") as f:
                return json.load(f)
        else:
            return self._simplify()

    def _get_simplified_geojson_name(self):
        file_name, file_ext = self.geojson_path.stem, self.geojson_path.suffix
        new_file_name = f"{file_name}-simplified-{self.geojson_simplify_tolerance}{file_ext}"
        return self.geojson_path.with_name(new_file_name)

    def _simplify(self):
        simplified_json_path = self._get_simplified_geojson_name()

        if not simplified_json_path.exists():
            GeoJsonSimplifier(
                input_file_path=self.geojson_path,
                output_file_path=simplified_json_path,
                tolerance=self.geojson_simplify_tolerance,
            ).simplify()

        with Path(simplified_json_path).open("r") as f:
            return json.load(f)

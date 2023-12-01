from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from map_nl.geojson.simplifier import GeoJsonSimplifier
from map_nl.utils.file_downloader import FileDownloader

logger = logging.getLogger(__name__)


@dataclass
class GeoJsonGetter:
    """Handles the retrieval and optional simplification of GeoJSON files.

    This class provides functionality to download a GeoJSON file from a specified
    URL if it does not exist locally and optionally simplify the file based on a given tolerance.
    """

    def __init__(self, url: str, geojson_path: Path, geojson_simplify_tolerance: float | None = None) -> None:
        """Initializes the GeoJsonGetter with the specified URL, local path, and optional simplification tolerance.

        Args:
            url (str): URL from where the GeoJSON file should be downloaded.
            geojson_path (Path): Local file path for the GeoJSON file.
            geojson_simplify_tolerance (float | None, optional): Tolerance level for GeoJSON simplification.
                Defaults to None, which means no simplification is performed.
        """
        self.geojson_simplify_tolerance = geojson_simplify_tolerance
        self.geojson_path = geojson_path
        self.url = url

    def get(self) -> dict:
        """Downloads the GeoJSON file if it does not exist locally. If simplification tolerance is provided,
        the file is simplified accordingly.

        Returns:
            dict: The contents of the GeoJSON file, either in its original or simplified form.
        """

        if not self.geojson_path.exists():
            FileDownloader(url=self.url, file_path=self.geojson_path).download()
        logging.debug(f"File {self.geojson_path} already exists, so skipping download.")

        if not self.geojson_simplify_tolerance:
            with Path(self.geojson_path).open("r") as f:
                return json.load(f)
        else:
            return self._simplify()

    def _get_simplified_geojson_name(self) -> Path:
        """
        Generates the name for the simplified GeoJSON file based on the original file name and simplification tolerance.
        The new file name will be `<existing-file-name>-simplified-<tolerance>.<extension>`.
        """
        file_name, file_ext = self.geojson_path.stem, self.geojson_path.suffix
        new_file_name = f"{file_name}-simplified-{self.geojson_simplify_tolerance}{file_ext}"
        return self.geojson_path.with_name(new_file_name)

    def _simplify(self) -> dict:
        """Simplifies the GeoJSON file based on the specified tolerance.

        If a simplified file already exists, it returns the content of that file.
        Otherwise, it performs the simplification process and then returns the content.

        Returns:
            dict: The contents of the simplified GeoJSON file.
        """
        simplified_json_path = self._get_simplified_geojson_name()

        if not simplified_json_path.exists():
            GeoJsonSimplifier(
                input_file_path=self.geojson_path,
                output_file_path=simplified_json_path,
                tolerance=self.geojson_simplify_tolerance,  # type: ignore
            ).simplify()
        logging.debug(
            f"File {simplified_json_path} already exists, so skipping simplification and returning the contents of that"
            " file instead."
        )

        with Path(simplified_json_path).open("r") as f:
            return json.load(f)

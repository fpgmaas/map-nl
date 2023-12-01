from __future__ import annotations

import logging
from pathlib import Path

import geopandas as gpd  # type: ignore
import topojson as tp  # type: ignore

logger = logging.getLogger(__name__)


class GeoJsonSimplifier:
    """A utility class for simplifying GeoJSON files.

    This class uses TopoJSON and GeoPandas to simplify the geometry of a GeoJSON file,
    which can be useful for reducing file size and complexity.
    """

    def __init__(
        self,
        input_file_path: str | Path,
        output_file_path: str | Path,
        tolerance: float = 0.01,  # Default tolerance value
    ):
        """Initializes the GeoJsonSimplifier with input and output file paths and an optional tolerance level.

        Args:
            input_file_path (str | Path): The file path to the input GeoJSON file.
            output_file_path (str | Path): The file path where the simplified GeoJSON will be saved.
            tolerance (float, optional): The tolerance level for simplification.
                Lower values preserve more detail. Defaults to 0.01.
        """
        self.input_file_path = Path(input_file_path)
        self.output_file_path = Path(output_file_path)
        self.tolerance = tolerance

    def simplify(self) -> None:
        """Performs the simplification process on the input GeoJSON file.

        Reads the input GeoJSON file, simplifies it using the specified tolerance,
        and saves the simplified GeoJSON to the output file path.
        """
        logging.debug("Simplifying the GeoJSON to reduce its size.")

        gdf = gpd.read_file(self.input_file_path)
        topology = tp.Topology(gdf, prequantize=False)
        simplified_topology = topology.toposimplify(self.tolerance)
        simplified_topology.to_gdf().to_file(self.output_file_path, driver="GeoJSON")

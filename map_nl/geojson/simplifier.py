import logging
from pathlib import Path

import geopandas as gpd
import topojson as tp

logger = logging.getLogger(__name__)


class GeoJsonSimplifier:
    def __init__(
        self,
        input_file_path: str | Path,
        output_file_path: str | Path,
        tolerance: float = 0.01,  # Default tolerance value
    ):
        self.input_file_path = Path(input_file_path)
        self.output_file_path = Path(output_file_path)
        self.tolerance = tolerance

    def simplify(self):
        # Load the GeoJSON file
        gdf = gpd.read_file(self.input_file_path)

        # Create a TopoJSON object
        topology = tp.Topology(gdf, prequantize=False)

        # Topology-aware simplification
        simplified_topology = topology.toposimplify(self.tolerance)

        # Save the simplified GeoJSON
        simplified_topology.to_gdf().to_file(self.output_file_path, driver="GeoJSON")

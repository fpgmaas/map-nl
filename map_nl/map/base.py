from abc import ABC, abstractmethod
from pathlib import Path

import folium

from map_nl.geojson.getter import GeoJsonGetter

GEO_JSON_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-netherlands-postcode-pc4/exports/geojson?lang=en&timezone=Europe%2FBerlin"
DATA_DIR = ".map_nl"
DEFAULT_MAP_ARGS = {"location": [52.1326, 5.2913], "zoom_start": 8, "tiles": "cartodb positron"}


class BaseMapNL(ABC):
    """Abstract base class for creating maps of the Netherlands using Folium.

    This class provides basic functionalities for downloading and handling GeoJSON data,
    initializing a Folium map, and defining an abstract method for plotting.
    """

    def __init__(
        self,
        url: str = GEO_JSON_URL,
        data_dir: str = DATA_DIR,
        geojson_simplify_tolerance: float | None = None,
        **kwargs,
    ):
        """
        Args:
            url (str, optional): URL to download the GeoJSON file. Defaults to a file from https://public.opendatasoft.com.
            data_dir (str, optional): Directory to save the downloaded GeoJSON file. Defaults to `.map_nl`.
            geojson_simplify_tolerance (float | None, optional): Tolerance level for GeoJSON simplification.
                If None, no simplification is performed. Lower values lead to simpler maps. Sensible values for
                coordinates stored in degrees are in the range of 0.0001 to 10. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the folium.Map() function. By default, only `location`
                and `zoom_start` are passed with default values.
        """
        self.geojson_simplify_tolerance = geojson_simplify_tolerance
        self.geojson_path = Path(data_dir) / "nl-pc4-map.geojson"
        self.url = url

        map_args = {**DEFAULT_MAP_ARGS, **kwargs}
        self.m = folium.Map(**map_args)

    @abstractmethod
    def plot(self):
        raise NotImplementedError()

    def _get_geojson(self) -> dict:
        """Retrieves the GeoJSON data for the map.

        Downloads the GeoJSON file if it does not exist locally and optionally simplifies it.

        Returns:
            dict: The contents of the GeoJSON file, either in its original or simplified form.
        """
        return GeoJsonGetter(
            url=GEO_JSON_URL, geojson_path=self.geojson_path, geojson_simplify_tolerance=self.geojson_simplify_tolerance
        ).get()

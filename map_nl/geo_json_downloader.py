import os
import requests
from pathlib import Path

from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)

class GeoJsonDownloader:

    def __init__(self):
        self.url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-netherlands-postcode-pc4/exports/geojson?lang=en&timezone=Europe%2FBerlin"
        self.directory = ".map-nl"
        self.file_name = "nl-pc4-map.geojson"
        self.file_path = Path(self.directory) / self.file_name

    def download(self):
        if not self.file_path.exists():
            Path(self.directory).mkdir(parents=True, exist_ok=True)
            self._download_file()
        else:
            print("File already exists.")

    def _download_file(self):
        print(f"Downloading file from {self.url}...")
        response = requests.get(self.url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(self.file_path, 'wb') as file, tqdm(
                desc=self.file_path.name,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)
            print(f"File downloaded and saved as {self.file_path}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")



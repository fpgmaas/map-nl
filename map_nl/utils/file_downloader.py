import logging
from pathlib import Path

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)


class FileDownloader:
    def __init__(
        self,
        url: str,
        file_path: str | Path,
    ):
        self.url = url
        self.file_path = Path(file_path)

    def download(self):
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(self.url, stream=True, timeout=5)
        if response.status_code == 200:
            total_size = int(response.headers.get("content-length", 0))
            with open(self.file_path, "wb") as file, tqdm(
                desc=self.file_path.name, total=total_size, unit="iB", unit_scale=True, unit_divisor=1024
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

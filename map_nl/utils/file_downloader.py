from __future__ import annotations

import logging
from pathlib import Path

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)


class FileDownloader:
    """A utility class for downloading files from a given URL."""

    def __init__(
        self,
        url: str,
        file_path: str | Path,
    ) -> None:
        """
        Args:
            url (str): The URL from where the file will be downloaded.
            file_path (str | Path): The local path where the downloaded file will be saved.
        """
        self.url = url
        self.file_path = Path(file_path)

    def download(self) -> None:
        try:
            response = requests.get(self.url, stream=True, timeout=5)
            response.raise_for_status()  # This will raise an HTTPError if the status is 4xx or 5xx

            total_size = int(response.headers.get("content-length", 0))
            with open(self.file_path, "wb") as file, tqdm(
                desc=self.file_path.name, total=total_size, unit="iB", unit_scale=True, unit_divisor=1024
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            logger.info("Download successful.")

        except requests.HTTPError as e:
            logger.error(f"Failed to download {self.url}. Status code: {e.response.status_code}")  # type: ignore
            raise Exception(f"Error downloading {self.url}: {e}") from None

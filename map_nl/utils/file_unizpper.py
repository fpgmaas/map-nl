from __future__ import annotations

import logging
from pathlib import Path
from zipfile import ZipFile

from tqdm import tqdm

logger = logging.getLogger(__name__)


class FileUnzipper:
    def __init__(self, zip_file_name: str, extract_to: str, directory: str = ".map-nl") -> None:
        self.zip_file_path = Path(directory) / zip_file_name
        self.extract_to_path = Path(directory) / extract_to

    def unzip(self) -> None:
        with ZipFile(self.zip_file_path, "r") as zip_ref:
            # List of file names in zip
            zip_files = zip_ref.namelist()
            for file in tqdm(zip_files, desc="Extracting files"):
                zip_ref.extract(member=file, path=self.extract_to_path)

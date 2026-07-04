from enum import Enum

from common.metaData import MetaData
from sources.mangaDex import mangaDexCoverDownloader


class CoverSourcesFactory(Enum):
    MANGADEX = "mangaDex"

    @classmethod
    def from_source_name(cls, source_name: str) -> "CoverSourcesFactory":
        for source in cls:
            if source.value == source_name:
                return source
        raise ValueError(f"Unknown cover source: {source_name}")

    def download(self, metaData: MetaData, folder_path: str):
        if self is CoverSourcesFactory.MANGADEX:
            return mangaDexCoverDownloader.download_manga_covers(
                folder_path,
                metaData.mangadex_manga_code,
            )
        else:
            raise ValueError(f"Unknown cover source: {self.value}")

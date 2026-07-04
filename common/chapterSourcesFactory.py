from enum import Enum

from common.metaData import MetaData
from sources.mangaDex import mangaDexMangaDownloader
from sources.mangaPill import mangaPillMangaDownloader


class ChapterSourcesFactory(Enum):
    MANGADEX = "mangaDex"
    MANGAPILL = "mangapill"

    @classmethod
    def from_source_name(cls, source_name: str) -> "ChapterSourcesFactory":
        for source in cls:
            if source.value == source_name:
                return source
        raise ValueError(f"Unknown chapter source: {source_name}")

    def download(self, metaData: MetaData, folder_path: str):
        if self is ChapterSourcesFactory.MANGADEX:
            return mangaDexMangaDownloader.download_manga(
                folder_path,
                metaData.mangadex_manga_code,
                metaData.translated_language,
                metaData.group_id,
            )

        if self is ChapterSourcesFactory.MANGAPILL:
            return mangaPillMangaDownloader.download_manga(
                folder_path,
                metaData.chapter_per_volumes,
                metaData.mangapill_manga_code,
                metaData.mangapill_manga_name,
            )

        raise ValueError(f"Unknown chapter source: {self.value}")

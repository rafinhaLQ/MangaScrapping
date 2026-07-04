import json
import logging
import time

import config.loggerFactory as loggerFactory
from common.chapterSourcesFactory import ChapterSourcesFactory
from common.coverSourcesFactory import CoverSourcesFactory
from common.metaData import MetaData

logger = loggerFactory.get_logger(__name__, logging.INFO)


def extract_metadata_from_json() -> MetaData:
    with open("metadata.json", "r") as file:
        data = json.load(file)

    metaData = MetaData()
    metaData.manga_name = data.get("manga_name")
    metaData.cover_source = data.get("cover_source")
    metaData.chapter_source = data.get("chapter_source")
    metaData.mangadex_manga_code = data.get("mangadex_manga_code")
    metaData.translated_language = data.get("translated_language")
    metaData.group_id = data.get("group_id")
    metaData.chapter_per_volumes = {
        int(volume): tuple(chapter_range)
        for volume, chapter_range in data.get("chapter_per_volumes", {}).items()
    }
    metaData.mangapill_manga_code = data.get("mangapill_manga_code")
    metaData.mangapill_manga_name = data.get("mangapill_manga_name")

    return metaData


def get_cover_source(metaData: MetaData):
    coverSource = CoverSourcesFactory.from_source_name(metaData.cover_source)
    logger.info("Downloading manga covers from %s", coverSource.value)
    coverSource.download(metaData, get_folder_path(metaData.manga_name))


def get_chapter_source(metaData: MetaData):
    chapterSource = ChapterSourcesFactory.from_source_name(metaData.chapter_source)
    logger.info("Downloading manga chapters from %s", chapterSource.value)
    chapterSource.download(metaData, get_folder_path(metaData.manga_name))


def get_folder_path(manga_name: str) -> str:
    return f"{manga_name}-Scrapping/{manga_name} Vol."


if __name__ == "__main__":
    metaData = extract_metadata_from_json()

    start_time = time.time()

    logger.info("Starting download for %s", metaData.manga_name)

    get_cover_source(metaData)
    logger.info("Manga covers download complete.")

    get_chapter_source(metaData)
    logger.info("Manga chapters download complete.")

    end_time = time.time()
    elapsed = end_time - start_time
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    logger.info(
        "Total download time: %dh %dm %ds", int(hours), int(minutes), int(seconds)
    )
    logger.info("Download complete.")

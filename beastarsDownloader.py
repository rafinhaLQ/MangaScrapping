import time
import mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import mangaDex.mangaDexMangaDownloader as mangaDexMangaDownloader
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO)

manga_name = "Beastars"
mangaDex_code = "f5e3baad-3cd4-427c-a2ec-ad7d776b370d"
translated_language = "pt-br"
group_id = "ba83b2a6-7b2f-431b-9cae-4436cd8cce42"

default_folder_path = f"{manga_name}-Scrapping/{manga_name} Vol."


def download_covers():
    logger.info("Downloading manga covers")
    mangaDexCoverDownloader.download_manga_covers(default_folder_path, mangaDex_code)
    logger.info("Manga covers download complete.")


def download_manga_chapters():
    logger.info("Starting download of manga chapters")
    mangaDexMangaDownloader.download_manga(
        default_folder_path, mangaDex_code, translated_language, group_id
    )
    logger.info("Manga chapters download complete.")


if __name__ == "__main__":
    start_time = time.time()

    logger.info("Starting download for %s", manga_name)

    download_covers()

    download_manga_chapters()

    end_time = time.time()
    elapsed = end_time - start_time
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    logger.info(
        "Total download time: %dh %dm %ds", int(hours), int(minutes), int(seconds)
    )
    logger.info("Download complete.")

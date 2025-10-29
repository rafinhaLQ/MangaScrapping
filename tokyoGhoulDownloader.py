import time
import mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import mangaDex.mangaDexMangaDownloader as mangaDexMangaDownloader
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO)

manga_name = "Tokyo Ghoul"
mangaDex_code = "6a1d1cb1-ecd5-40d9-89ff-9d88e40b136b"
translated_language = "pt-br"
group_id = "d2394014-12a5-467f-ab8c-3317013ce9c8"

default_folder_path = f"Tokyo Ghoul-Scrapping/Tokyo Ghoul Vol."


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

import time
import mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import mangaPill.mangaPillMangaDownloader as mangaPillMangaDownloader
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO)

mangaDex_code = "ac54cf12-1d69-4bcc-8d14-eaec4b4da6b1"
mangaPill_code = "2687"
mangaPill_manga_name = "magi-sinbad-no-bouken"

default_folder_path = f"Magi-Sinbad-no-Bouken-Scrapping/Magi The Adventures of Sinbad Vol."

# volumes and chapters definition
volumes_dict = {
    1: (0, 10),
    2: (10, 16),
    3: (16, 22),
    4: (22, 28),
    5: (28, 37),
    6: (37, 48),
    7: (48, 59),
    8: (59, 70),
    9: (70, 81),
    10: (81, 92),
    11: (92, 103),
    12: (103, 114),
    13: (114, 125),
    14: (125, 136),
    15: (136, 147),
    16: (147, 158),
    17: (158, 168),
    18: (168, 178),
    19: (178, 183)
}
volumes = [list(range(start, end)) for start, end in volumes_dict.values()]

def download_covers():
    logger.info("Downloading manga covers")
    mangaDexCoverDownloader.download_manga_covers(default_folder_path, mangaDex_code)
    logger.info("Manga covers download complete.")

def download_manga_chapters():
    logger.info("Starting download of manga chapters")
    for volume_index, (start, end) in volumes_dict.items():
        logger.info(f"Processing Volume {volume_index}")
        for chapter_index in range(start, end):
            logger.info(f"Processing Chapter {chapter_index}")
            total_number_of_pages, image_format = (
                mangaPillMangaDownloader.fetch_number_of_total_pages(
                    mangaPill_code, mangaPill_manga_name, chapter_index
                )
            )
            logger.debug(f"Chapter {chapter_index} has {total_number_of_pages} pages:")
            if total_number_of_pages is not None:
                for page in range(1, total_number_of_pages + 1):
                    mangaPillMangaDownloader.download_chapter_pages(
                        default_folder_path,
                        mangaPill_code,
                        chapter_index,
                        page,
                        volume_index,
                        image_format,
                    )
        logger.info(f"Completed Volume {volume_index}.")

if __name__ == "__main__":
    start_time = time.time()

    logger.info(f"Starting download for Magi: The Adventures of Sinbad")

    download_covers()

    download_manga_chapters()

    end_time = time.time()
    elapsed = end_time - start_time
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    logger.info(f"Total download time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    logger.info("Download complete.")

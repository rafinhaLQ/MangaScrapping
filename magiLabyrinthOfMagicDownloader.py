import time
import mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import mangaPill.mangaPillMangaDownloader as mangaPillMangaDownloader
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO)

mangaDex_code = "ce63e6b8-fad8-48bc-a2aa-d801fb8d5d43"
mangaPill_code = "2686"
mangaPill_manga_name = "magi-labyrinth-of-magic"

default_folder_path = f"Magi-Labyrinth-of-Magic-Scrapping/Magi Labyrinth of Magic Vol."

# volumes and chapters definition
volumes_dict = {
    1: (1, 8),
    2: (8, 18),
    3: (18, 28),
    4: (28, 38),
    5: (38, 49),
    6: (49, 59),
    7: (59, 69),
    8: (69, 79),
    9: (79, 89),
    10: (89, 99),
    11: (99, 109),
    12: (109, 119),
    13: (119, 129),
    14: (129, 139),
    15: (139, 149),
    16: (149, 159),
    17: (159, 169),
    18: (169, 179),
    19: (179, 189),
    20: (189, 199),
    21: (199, 209),
    22: (209, 219),
    23: (219, 229),
    24: (229, 239),
    25: (239, 249),
    26: (249, 259),
    27: (259, 269),
    28: (269, 279),
    29: (279, 289),
    30: (289, 299),
    31: (299, 309),
    32: (309, 319),
    33: (319, 329),
    34: (329, 339),
    35: (339, 350),
    36: (350, 360),
    37: (360, 370)
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

    logger.info(f"Starting download for Magi: Labyrinth of Magic")

    download_covers()

    download_manga_chapters()

    end_time = time.time()
    elapsed = end_time - start_time
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    logger.info(f"Total download time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    logger.info("Download complete.")

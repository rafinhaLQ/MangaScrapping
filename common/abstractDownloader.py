from abc import ABC, abstractmethod
import time
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO)

class AbstractDownloader(ABC):
    def __init__(self, manga_name: str, logger: logging.Logger = None):
        self.manga_name = manga_name
        self.logger = logger or logging.getLogger(__name__)

    def download(self):
        start_time = time.time()

        self.logger.info("Starting download for %s", self.manga_name)

        self.logger.info("Downloading manga covers")
        self.download_covers()
        self.logger.info("Manga covers download complete.")

        self.logger.info("Starting download of manga chapters")
        self.download_chapters()
        self.logger.info("Manga chapters download complete.")

        end_time = time.time()
        elapsed = end_time - start_time
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        self.logger.info(
            "Total download time: %dh %dm %ds", int(hours), int(minutes), int(seconds)
        )
        self.logger.info("Download complete.")

    @abstractmethod
    def download_covers(self):
        raise NotImplementedError()

    @abstractmethod
    def download_chapters(self):
        raise NotImplementedError()
    
    def get_folder_path(self) -> str:
        return f"{self.manga_name}-Scrapping/{self.manga_name} Vol."

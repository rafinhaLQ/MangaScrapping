from common.abstractDownloader import AbstractDownloader
import sources.mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import sources.mangaDex.mangaDexMangaDownloader as mangaDexMangaDownloader


class TokyoGhoulDownloader(AbstractDownloader):
    def download_covers(self):
        mangaDexCoverDownloader.download_manga_covers(
            self.get_folder_path(),
            mangadex_manga_code="6a1d1cb1-ecd5-40d9-89ff-9d88e40b136b",
        )

    def download_chapters(self):
        mangaDexMangaDownloader.download_manga(
            self.get_folder_path(),
            mangadex_manga_code="6a1d1cb1-ecd5-40d9-89ff-9d88e40b136b",
            translated_language="pt-br",
            group_id="d2394014-12a5-467f-ab8c-3317013ce9c8",
        )


if __name__ == "__main__":
    downloader = TokyoGhoulDownloader("Tokyo Ghoul")
    downloader.download()

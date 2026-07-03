from common.abstractDownloader import AbstractDownloader
import sources.mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import sources.mangaDex.mangaDexMangaDownloader as mangaDexMangaDownloader


class SunKenRockDownloader(AbstractDownloader):
    def download_covers(self):
        mangaDexCoverDownloader.download_manga_covers(
            self.get_folder_path(),
            mangadex_manga_code="d8de5f5f-692d-4d8f-9275-2d8cb98b702b",
        )

    def download_chapters(self):
        mangaDexMangaDownloader.download_manga(
            self.get_folder_path(),
            mangadex_manga_code="d8de5f5f-692d-4d8f-9275-2d8cb98b702b",
            translated_language="pt-br",
        )


if __name__ == "__main__":
    downloader = SunKenRockDownloader("Sun Ken Rock")
    downloader.download()

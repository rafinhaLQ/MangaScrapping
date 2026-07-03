from common.abstractDownloader import AbstractDownloader
import sources.mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import sources.mangaDex.mangaDexMangaDownloader as mangaDexMangaDownloader


class BibliomaniaDownloader(AbstractDownloader):
    def download_covers(self):
        mangaDexCoverDownloader.download_manga_covers(
            self.get_folder_path(),
            mangadex_manga_code="d22ae7a1-cfae-475a-a8fc-589ef85eece4",
        )

    def download_chapters(self):
        mangaDexMangaDownloader.download_manga(
            self.get_folder_path(),
            mangadex_manga_code="d22ae7a1-cfae-475a-a8fc-589ef85eece4",
            translated_language="en",
            group_id="a9ffebfc-f58b-467f-9506-15f87ffad6fc",
        )


if __name__ == "__main__":
    downloader = BibliomaniaDownloader("Bibliomania")
    downloader.download()

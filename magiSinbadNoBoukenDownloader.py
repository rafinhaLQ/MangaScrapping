from common.abstractDownloader import AbstractDownloader
import sources.mangaDex.mangaDexCoverDownloader as mangaDexCoverDownloader
import sources.mangaPill.mangaPillMangaDownloader as mangaPillMangaDownloader


class MagiSinbadNoBoukenDownloader(AbstractDownloader):
    def download_covers(self):
        mangaDexCoverDownloader.download_manga_covers(
            self.get_folder_path(),
            mangadex_manga_code="ac54cf12-1d69-4bcc-8d14-eaec4b4da6b1",
        )

    def download_chapters(self):
        chapter_per_volumes = {
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
            19: (178, 183),
        }

        mangaPillMangaDownloader.download_manga(
            self.get_folder_path(),
            chapter_per_volumes,
            mangapill_manga_code="2687",
            mangapill_manga_name="magi-sinbad-no-bouken",
        )


if __name__ == "__main__":
    downloader = MagiSinbadNoBoukenDownloader("Magi Sinbad no Bouken")
    downloader.download()

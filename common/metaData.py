from typing import Optional


class MetaData:
    manga_name: str
    cover_source: str
    chapter_source: str

    # MangaDex
    mangadex_manga_code: str
    translated_language: str
    group_id: Optional[str] = None

    # mangapill
    mangapill_manga_code: str
    mangapill_manga_name: str
    chapter_per_volumes: dict[int, tuple[int, int]]

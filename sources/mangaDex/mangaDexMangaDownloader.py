import os
import config.retryableHttpSession as retryableHttpSession
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO, log_to_file=True)

request = retryableHttpSession.create_retryable_session()


def __fetch_chapters_by_group(
    manga_code: str, translated_language: str, group_id: str | None
) -> list[tuple[int, float, str]]:

    params = {"translatedLanguage[]": translated_language}
    if group_id:
        params["groups[]"] = group_id

    response = request.get(
        f"https://api.mangadex.org/manga/{manga_code}/aggregate", params=params
    )
    volumes = response.json().get("volumes", {})

    volume_chapter_id_list = [
        (vol, chap, chap_data["id"])
        for vol, vol_data in volumes.items()
        for chap, chap_data in vol_data["chapters"].items()
    ]

    volume_chapter_id_list.sort(key=lambda x: float(x[1]))
    return volume_chapter_id_list


def __fetch_chapter_images(chapter_id: str) -> list[str]:
    response = request.get(f"https://api.mangadex.org/at-home/server/{chapter_id}")
    base_url = response.json().get("baseUrl", "")
    chapter_data = response.json().get("chapter", {})
    hash = chapter_data.get("hash", "")
    image_paths = chapter_data.get("data", [])
    image_urls = [f"{base_url}/data/{hash}/{path}" for path in image_paths]
    return image_urls


def __format_chapter(chapter):
    if float(chapter).is_integer():
        return f"{int(chapter)}"
    else:
        return f"{float(chapter):.1f}"


def __download_chapter_pages(
    default_folder_path: str, volume: int, chapter: float, chapter_id: str
):
    image_urls = __fetch_chapter_images(chapter_id)
    for page, image_url in enumerate(image_urls, start=1):
        response = request.get(image_url)
        if response.status_code != 200:
            logger.error(
                "Failed to download chapter %.1f. Status code: %d",
                float(chapter),
                response.status_code,
            )
        else:
            logger.info(
                "Successfully downloaded chapter %.1f page %d", float(chapter), page
            )

        chapter_str = __format_chapter(chapter)
        folder_path = f"{default_folder_path}{int(volume):02d}/Chapter {chapter_str}"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(
            folder_path, f"chapter_{chapter_str}_page_{page:03d}.jpg"
        )
        with open(file_path, "wb") as file:
            file.write(response.content)
    return True


def download_manga(
    default_folder_path: str,
    mangadex_manga_code: str,
    translated_language: str,
    group_id: str | None,
):
    volume_chapter_id_list = __fetch_chapters_by_group(
        mangadex_manga_code, translated_language, group_id
    )
    for volume, chapter, chapter_id in volume_chapter_id_list:
        __download_chapter_pages(default_folder_path, volume, chapter, chapter_id)

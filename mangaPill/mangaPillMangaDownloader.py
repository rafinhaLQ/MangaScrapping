from bs4 import BeautifulSoup
import os
import time
import config.retryableHttpSession as retryableHttpSession
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.INFO, log_to_file=True)

request = retryableHttpSession.create_retryable_session()

def fetch_number_of_total_pages(
    manga_code: str, manga_name: str, chapter: int
) -> tuple[int, str] | None:
    response = request.get(
        f"https://mangapill.com/chapters/{manga_code}-10{chapter:03d}000/{manga_name}-chapter-{chapter}"
    )
    if response.status_code != 200:
        logger.error(
            f"Failed to fetch chapter {chapter}. Status code: {response.status_code}"
        )
        return None
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    summary_div = soup.find("div", attrs={"data-summary": True})
    if summary_div:
        page_counter = summary_div.find("div", class_="text-sm")
        if page_counter:
            _, total_pages = page_counter.text.strip("page ").split("/")
            jpeg_count = html.count(".jpeg")
            if jpeg_count >= int(total_pages):
                return int(total_pages), "jpeg"
            else:
                return int(total_pages), "jpg"
        else:
            logger.error("Page counter not found inside summary div.")
            return None
    else:
        logger.error("Summary div not found.")
        return None


def download_chapter_pages(
    default_folder_path: str, manga_code: str, chapter: int, page: int, volume: int, image_format: str
) -> bool:
    headers = {"Referer": "https://mangapill.com/"}
    response = request.get(
        f"https://cdn.readdetectiveconan.com/file/mangap/{manga_code}/10{chapter:03d}000/{page}.{image_format}",
        headers=headers,
    )
    if response.status_code != 200:
        logger.error(
            f"Failed to download chapter {chapter}. Status code: {response.status_code}"
        )
        return False
    else:
        logger.info(f"Successfully downloaded chapter {chapter} page {page}")
    folder_path = f"{default_folder_path}{volume:02d}/Chapter {chapter:03d}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"chapter_{chapter:03d}_page_{page:03d}.jpg")
    with open(file_path, "wb") as file:
        file.write(response.content)
    return True

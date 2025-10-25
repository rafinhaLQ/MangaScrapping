import json
from typing import Dict, Any, Union
import config.retryableHttpSession as retryableHttpSession
import config.loggerFactory as loggerFactory
import logging
import os

logger = loggerFactory.get_logger(__name__, logging.INFO)

request = retryableHttpSession.create_retryable_session()


def fetch_manga_dex_covers_list(manga_code: str):
    resp = request.get(
        f"https://api.mangadex.org/cover?order[volume]=asc&manga[]={manga_code}&limit=100&offset=0"
    )
    if resp.status_code != 200:
        logger.error(
            f"Failed to fetch covers for manga {manga_code}. Status code: {resp.status_code}"
        )

    try:
        data = resp.json()
    except ValueError:
        logger.error("Response was not valid JSON")

    return parse_cover_collection(data)


def parse_cover_collection(response_json: Union[str, Dict[str, Any]]) -> Dict[str, str]:
    if isinstance(response_json, str):
        try:
            response_json = json.loads(response_json)
        except json.JSONDecodeError:
            return {}

    result: Dict[str, str] = {}

    for item in (
        response_json.get("data", []) if isinstance(response_json, dict) else []
    ):
        if not isinstance(item, dict):
            continue
        attributes = item.get("attributes", {}) or {}
        if not isinstance(attributes, dict):
            continue

        volume = attributes.get("volume")
        if volume is None:
            continue
        else:
            volume_key = str(volume).zfill(2)

        file_name = attributes.get("fileName") or attributes.get("filename")
        if not file_name:
            continue

        if volume_key in result:
            continue

        result[volume_key] = file_name

    return result


def download_manga_covers(default_folder_path: str, manga_code: str):
    volume_to_filename = fetch_manga_dex_covers_list(manga_code)
    if not volume_to_filename:
        logger.error("No covers found to download.")
        return False

    errors = {}
    for volume, file_name in volume_to_filename.items():
        folder_path = f"{default_folder_path}{volume}"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{volume}.cover.jpg")
        try:
            resp = request.get(f"https://mangadex.org/covers/{manga_code}/{file_name}")
            if resp.status_code != 200:
                errors[volume] = (
                    f"Error {resp.status_code} - Could not download {file_name}"
                )
                continue
            with open(file_path, "wb") as f:
                f.write(resp.content)
            logger.info(f"Saved cover for volume {volume} as {file_path}")
        except Exception as exc:
            logger.error(f"Exception downloading cover for volume {volume}: {exc}")
            errors[volume] = str(exc)
    if errors:
        logger.error("Errors:")
        for volume, err in errors.items():
            logger.error(f"Volume {volume}: {err}")
    return True

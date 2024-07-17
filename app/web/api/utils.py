import os
import uuid

import aiofiles
from fastapi import UploadFile

from app.core.logger import logger
from app.core.paths import IMAGES_DIR
from app.web.api.validators import check_file_format


async def save_image(image: UploadFile) -> str:
    """Функция сохранения изображения"""
    try:
        _, ext = os.path.splitext(image.filename)
        check_file_format(image.content_type)
        file_name = f"{uuid.uuid4().hex}{ext}"
        os.makedirs(IMAGES_DIR, exist_ok=True)

        async with aiofiles.open(
            f"{IMAGES_DIR}/{file_name}", mode="wb"
        ) as out_file:
            content = await image.read()
            await out_file.write(content)
        return file_name

    except Exception as e:
        logger.error(f"Failed to saved file: {e}")
        raise e

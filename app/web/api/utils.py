import os
import uuid
from typing import Any, Dict

import aiofiles
from fastapi import Request, UploadFile

from app.core.logger import logger
from app.core.paths import IMAGES_DIR
from app.web.api.validators import check_file_format, check_required_field


async def save_image(image: UploadFile) -> str:
    """Функция сохранения изображения"""
    try:
        _, ext = os.path.splitext(image.filename)
        check_file_format(image.content_type)
        file_name = f"{uuid.uuid4().hex[:6]}{ext}"
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


async def process_form(
    request: Request, required_fields: list
) -> Dict[str, Any]:
    """Функция обработки данных формы"""
    form_data = await request.form()

    form_dict = {key: form_data.get(key) for key in required_fields}
    check_required_field(form_dict)  # проверяем заполнение обязательных полей

    image: UploadFile = form_data.get("image")
    if image and image.filename:
        file_name = await save_image(image)  # сохраняем изображение
        form_dict["image_name"] = file_name

    return form_dict


async def process_poll_form(request: Request) -> Dict[str, Any]:
    required_fields = ["name", "description", "poll_type"]
    return await process_form(request, required_fields)


async def process_question_form(request: Request) -> Dict[str, Any]:
    required_fields = ["title", "description", "text_ask", "options_type"]
    return await process_form(request, required_fields)

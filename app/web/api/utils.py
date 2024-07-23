import os
import uuid
from typing import Dict, Any

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


async def process_poll_form(request: Request) -> Dict[str, Any]:
    form_data = await request.form()

    poll_dict = {
        key: form_data.get(key)
        for key in ["name", "description", "poll_type", "slug"]
    }

    check_required_field(poll_dict)  # проверяем заполнение обязательных полей

    image: UploadFile = form_data.get("image")
    if image and image.filename:
        file_name = await save_image(image)  # сохраняем изображение
        poll_dict["image_name"] = file_name

    return poll_dict


async def process_question_form(request: Request) -> Dict[str, Any]:
    form_data = await request.form()
    question_dict = {
        key: form_data.get(key)
        for key in ["title", "description", "text_ask", "options_type"]
    }
    check_required_field(
        question_dict
    )  # проверяем заполнение обязательных полей

    image: UploadFile = form_data.get("image")
    if image and image.filename:
        file_name = await save_image(image)  # сохраняем изображение
        question_dict["image_name"] = file_name

    return question_dict

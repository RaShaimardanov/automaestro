from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.paths import TEMPLATES_FOLDER


main_router = APIRouter(prefix=settings.API_PREFIX)
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


@main_router.get(path="/", response_class=HTMLResponse)
async def main_page(request: Request):
    """Функция для обработки запроса главной страницы."""
    return templates.TemplateResponse(request=request, name="index.html")

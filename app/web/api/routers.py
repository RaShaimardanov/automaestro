from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.paths import TEMPLATES_FOLDER
from app.web.api.endpoints.admin.main import router as admin_router

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


@router.get(path="/", response_class=HTMLResponse)
async def main_page(request: Request):
    """Функция для обработки запроса главной страницы."""
    return templates.TemplateResponse(request=request, name="index.html")


router.include_router(admin_router)

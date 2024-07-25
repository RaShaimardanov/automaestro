from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.paths import TEMPLATES_FOLDER
from app.database.repo.requests import RequestsRepo
from app.database.setup import get_repo
from app.web.api.endpoints.admin.poll import router as poll_router

router = APIRouter(prefix="/admin")
router.include_router(poll_router)
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


@router.get(path="/", response_class=HTMLResponse)
async def main_page_admin(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
):
    polls = await repo.polls.get_all()
    users = await repo.users.get_all()
    employees = await repo.employees.get_all()

    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={"polls": polls, "users": users, "employees": employees},
    )

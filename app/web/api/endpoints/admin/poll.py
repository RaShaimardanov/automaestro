from fastapi import APIRouter, Request, Depends, status, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.logger import logger
from app.database.setup import get_repo
from app.database.repo.requests import RequestsRepo
from app.core.paths import TEMPLATES_FOLDER

router = APIRouter(prefix="/poll")
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


@router.get(path="/add", response_class=HTMLResponse)
async def get_add_poll_template(request: Request):
    return templates.TemplateResponse(
        request=request, name="admin/add-poll.html"
    )


@router.post(path="/add", response_class=HTMLResponse)
async def add_poll(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
):

    try:
        form_data = await request.form()
        poll_dict = {
            key: form_data.get(key) for key in ["name", "description", "slug"]
        }
        poll = await repo.polls.create(poll_dict)

        return RedirectResponse(
            url=f"{poll.id}",
            status_code=status.HTTP_302_FOUND,
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e


@router.get(path="/{poll_id}", response_class=HTMLResponse)
async def poll_detail(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    poll = await repo.polls.get(poll_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/poll-detail.html",
        context={"poll": poll},
    )

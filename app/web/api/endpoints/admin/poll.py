from typing import Dict, Any

from fastapi import (
    APIRouter,
    Request,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.logger import logger
from app.database.setup import get_repo
from app.database.repo.requests import RequestsRepo
from app.core.paths import TEMPLATES_FOLDER
from app.utils.enums import OptionsType
from app.web.api.utils import save_image
from app.web.api.validators import check_required_field

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
            url=f"/admin/poll/{poll.id}",
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


@router.get(path="/{poll_id}/question", response_class=HTMLResponse)
async def poll_detail(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    poll = await repo.polls.get(poll_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/add-question.html",
        context={"poll": poll},
    )


@router.post(path="/{poll_id}/question", response_class=HTMLResponse)
async def add_question(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    form_data = await request.form()
    question_dict: Dict[str, Any] = {
        key: form_data.get(key) for key in ["title", "text", "options_type"]
    }

    check_required_field(question_dict)

    image = form_data.get("image")
    if image:
        file_name = await save_image(image)
        question_dict["image_name"] = file_name

    question_dict["poll_id"] = poll_id

    question = await repo.questions.create(question_dict)

    redirect_url = f"/admin/poll/{poll_id}"
    if question.options_type == OptionsType.custom:
        redirect_url = f"/admin/poll/{poll_id}/question/{question.id}"

    return RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_302_FOUND,
    )


@router.get(
    path="/{poll_id}/question/{question_id}", response_class=HTMLResponse
)
async def get_question(
    request: Request,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    question = await repo.questions.get(question_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/question-detail.html",
        context={"question": question},
    )


@router.post(
    path="/{poll_id}/question/{question_id}", response_class=HTMLResponse
)
async def add_option(
    request: Request,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    form_data = await request.form()
    title = form_data.get("title")
    try:
        await repo.options.create(dict(value=title, question_id=question_id))
        question = await repo.questions.get(question_id)
        return templates.TemplateResponse(
            request=request,
            name="admin/question-detail.html",
            context={"question": question},
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create option",
        )


@router.get(
    path="/{poll_id}/question/{question_id}/options",
    response_class=HTMLResponse,
)
async def get_option_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/add-option.html",
    )

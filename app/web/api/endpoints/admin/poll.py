from typing import Dict, Any

from fastapi import (
    APIRouter,
    Request,
    Depends,
    status,
    HTTPException,
    UploadFile,
)
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.logger import logger
from app.core.paths import TEMPLATES_FOLDER
from app.database.setup import get_repo
from app.database.repo.requests import RequestsRepo
from app.utils.enums import OptionsType
from app.web.api.utils import save_image
from app.web.api.validators import check_required_field

router = APIRouter(prefix="/poll")
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


@router.get(path="/", response_class=HTMLResponse)
async def get_add_poll_template(request: Request):
    return templates.TemplateResponse(
        request=request, name="admin/add-poll.html"
    )


@router.post(path="/", response_class=HTMLResponse)
async def add_poll(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
):
    try:
        form_data = await request.form()
        poll_dict = {
            key: form_data.get(key)
            for key in ["name", "description", "poll_type", "slug"]
        }
        check_required_field(poll_dict)

        image: UploadFile = form_data.get("image")

        if image and image.filename:
            file_name = await save_image(image)
            poll_dict["image_name"] = file_name

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


@router.get(path="/{poll_id}/update", response_class=HTMLResponse)
async def poll_update(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    poll = await repo.polls.get(poll_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/poll/update.html",
        context={"poll": poll},
    )


@router.delete(path="/{poll_id}", response_class=HTMLResponse)
async def poll_delete(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    answers = await repo.answers.get_answers_by_poll_id(poll_id)

    if answers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This poll has answers",
        )

    poll = await repo.polls.get(poll_id)

    if poll:
        await repo.polls.remove(poll)

    return RedirectResponse(
        url=f"/admin",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(path="/{poll_id}/question", response_class=HTMLResponse)
async def get_add_question_template(
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
        key: form_data.get(key)
        for key in ["title", "description", "text_ask", "options_type"]
    }

    check_required_field(question_dict)

    image: UploadFile = form_data.get("image")

    if image and image.filename:
        file_name = await save_image(image)
        question_dict["image_name"] = file_name

    question_dict["poll_id"] = poll_id

    question = await repo.questions.create(question_dict)

    redirect_url = f"/admin/poll/{poll_id}"
    if question.options_type == OptionsType.CUSTOM:
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
    value = form_data.get("value")
    try:
        await repo.options.create(dict(value=value, question_id=question_id))
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


@router.delete(
    path="/{poll_id}/question/{question_id}", response_class=HTMLResponse
)
async def delete_question(
    request: Request,
    poll_id: int,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):

    answers = await repo.answers.get_answers_by_question_id(
        question_id=question_id
    )
    if answers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This question has answers",
        )

    question = await repo.questions.get(question_id)
    if question:
        await repo.questions.remove(question)

    return RedirectResponse(
        url=f"/admin/poll/{poll_id}",
        status_code=status.HTTP_303_SEE_OTHER,
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

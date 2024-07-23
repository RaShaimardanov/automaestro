from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.paths import TEMPLATES_FOLDER
from app.database.setup import get_repo
from app.database.repo.requests import RequestsRepo
from app.utils.enums import OptionsType
from app.web.api.utils import process_question_form, process_poll_form


router = APIRouter(prefix="/poll")
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


@router.post(path="/", response_class=HTMLResponse)
async def add_poll(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для добавления нового опроса"""
    poll_dict = await process_poll_form(request)
    poll = await repo.polls.create(poll_dict)

    return RedirectResponse(
        url=f"/admin/poll/{poll.id}",
        status_code=status.HTTP_302_FOUND,
    )


@router.get(path="/{poll_id}", response_class=HTMLResponse)
async def poll_detail(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для загрузки страницы с опросом"""
    print(request.cookies.get("telegram_id"))
    poll = await repo.polls.get(poll_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/poll/detail.html",
        context={"poll": poll},
    )


@router.patch(path="/{poll_id}", response_class=HTMLResponse)
async def poll_update(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для обновления данных опроса"""
    poll = await repo.polls.get(poll_id)

    poll_dict = await process_poll_form(request)

    poll = await repo.polls.update(obj=poll, update_data=poll_dict)

    return templates.TemplateResponse(
        request=request,
        name="admin/poll/detail.html",
        context={"poll": poll},
    )


@router.get(path="/{poll_id}/update", response_class=HTMLResponse)
async def poll_update(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт загрузки страницы с редактированием опроса"""
    poll = await repo.polls.get(poll_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/poll/update.html",
        context={"poll": poll},
    )


@router.delete(path="/{poll_id}", response_class=HTMLResponse)
async def poll_delete(
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт удаления опроса"""
    # проверяем наличие ответов
    answers = await repo.answers.get_answers_by_poll_id(poll_id)
    if answers:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This poll has answers",
        )

    poll = await repo.polls.get(poll_id)

    if poll:
        await repo.polls.remove(poll)

    return RedirectResponse(
        url=f"/admin",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    path="/{poll_id}/question/{question_id}", response_class=HTMLResponse
)
async def get_question(
    request: Request,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для загрузки страницы с вопросом"""
    question = await repo.questions.get(question_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/question/detail.html",
        context={"question": question},
    )


@router.post(path="/{poll_id}/question", response_class=HTMLResponse)
async def add_question(
    request: Request,
    poll_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для добавления вопроса"""
    question_dict = await process_question_form(request)
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
    path="/{poll_id}/question/{question_id}/update",
    response_class=HTMLResponse,
)
async def question_update_page(
    request: Request,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для загрузки страницы редактирования вопроса"""
    question = await repo.questions.get(question_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/question/update.html",
        context={"question": question},
    )


@router.patch(
    path="/{poll_id}/question/{question_id}",
    response_class=HTMLResponse,
)
async def update_question(
    request: Request,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт для обновления данных вопроса и вариантов ответа к нему"""
    form_data = await request.form()

    for key, value in form_data.items():
        # перебираем варианты ответов
        if key.startswith("option_"):
            _, option_id = key.split("_")  # получаем id варианта ответа
            option = await repo.options.get(int(option_id))
            # проверяем изменилось ли значение
            if option.value != value:
                await repo.options.update(option, {"value": value})

    question_dict = await process_question_form(request)

    question = await repo.questions.get(question_id)
    question = await repo.questions.update(question, question_dict)

    return templates.TemplateResponse(
        request=request,
        name="admin/question/detail.html",
        context={"question": question},
    )


@router.delete(
    path="/{poll_id}/question/{question_id}", response_class=HTMLResponse
)
async def delete_question(
    poll_id: int,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт удаления вопроса"""
    # проверяем наличие ответов
    answers = await repo.answers.get_answers_by_question_id(
        question_id=question_id
    )
    if answers:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This question has answers",
        )

    question = await repo.questions.get(question_id)
    if question:
        await repo.questions.remove(question)

    return RedirectResponse(
        url=f"/admin/poll/{poll_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post(
    path="/{poll_id}/question/{question_id}", response_class=HTMLResponse
)
async def add_option(
    request: Request,
    question_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт добавления нового варианты ответа к вопросу"""
    form_data = await request.form()
    value = form_data.get("value")

    await repo.options.create(dict(value=value, question_id=question_id))
    question = await repo.questions.get(question_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/question/detail.html",
        context={"question": question},
    )


@router.delete(
    path="/{poll_id}/question/{question_id}/{option_id}",
    response_class=HTMLResponse,
)
async def delete_option(
    request: Request,
    question_id: int,
    option_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    """Эндпоинт удаления варианты ответа"""
    option = await repo.options.get(option_id)
    if option:
        await repo.questions.remove(option)

    question = await repo.questions.get(question_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/question/update.html",
        context={"question": question},
    )

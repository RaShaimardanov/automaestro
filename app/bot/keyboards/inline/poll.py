from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.models import Question
from app.bot.utils.callback_data import PollCallback, AnswerCallback


def launch_poll_kb(poll_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Начать",
                    callback_data=PollCallback(poll_id=poll_id).pack(),
                )
            ]
        ],
    )


def get_options_kb(question: Question) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for option in question.options:
        builder.button(
            text=option.value,
            callback_data=AnswerCallback(
                question_id=question.id,
                option=option.value,
                poll_id=question.poll_id,
            ),
        )
    if not question.options_type.value:
        builder.adjust(1)
    return builder.as_markup()

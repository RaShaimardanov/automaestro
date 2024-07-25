from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.utils.callback_data import AnswerCallback, PollCallback
from app.database.models import Question
from app.utils.enums import OptionsType


def launch_poll_kb(
    poll_id: int, questions_quantity: int
) -> InlineKeyboardMarkup:
    """Клавиатура для запуска опроса"""
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Начать",
                    callback_data=PollCallback(
                        poll_id=poll_id, questions_quantity=questions_quantity
                    ).pack(),
                )
            ]
        ],
    )


def get_options_kb(
    question: Question, questions_quantity: int, question_number: int
) -> InlineKeyboardMarkup:
    """Клавиатура с вариантами ответов"""
    builder = InlineKeyboardBuilder()
    for option in question.options:
        builder.button(
            text=option.value,
            callback_data=AnswerCallback(
                question_id=question.id,
                option=option.value,
                poll_id=question.poll_id,
                question_number=question_number,
                questions_quantity=questions_quantity,
            ),
        )
    if question.options_type == OptionsType.CUSTOM:
        builder.adjust(1)
    return builder.as_markup()

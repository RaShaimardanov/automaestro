from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (MenuButtonDefault, MenuButtonWebApp, Message,
                           WebAppInfo)

from app.core.config import settings

router = Router()


@router.message(Command("admin"))
async def command_admin_handler(message: Message) -> None:
    """Установка кнопки Web App для администраторов"""
    if message.from_user.id in settings.ADMINS_IDS:
        await message.bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(
                text="Web App",
                web_app=WebAppInfo(url=f"{settings.WEB_APP_URL}"),
            ),
        )


@router.message(Command("clear"))
async def command_clear_handler(message: Message) -> None:
    await message.bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonDefault(),
    )

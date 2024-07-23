from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.scene import Scene, on

from app.bot.utils.enums import MenuOptions
from app.bot.utils.callback_data import MenuActionCallback


class MenuScene(Scene, callback_query_without_state=True):
    @on.callback_query(MenuActionCallback.filter())
    async def select_menu_item(
        self, callback_query: CallbackQuery, callback_data: MenuActionCallback
    ):
        await self.wizard.goto(
            MenuOptions[callback_data.action].scene,
            context=callback_data.context,
        )

    @on.callback_query(F.data == "update")
    async def get_update(self, callback_query: CallbackQuery):
        await self.wizard.retake()

    @on.callback_query(F.data == "back")
    async def get_back(self, callback_query: CallbackQuery):
        await self.wizard.back()

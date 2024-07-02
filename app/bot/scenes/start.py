from aiogram import F
from aiogram.types import Message
from aiogram.fsm.scene import Scene, on
from aiogram.filters import CommandStart, CommandObject
from fluentogram import TranslatorRunner

from app.bot.utils.enums import MenuOptions
from app.database.models import User
from app.database.repo.requests import RequestsRepo


class StartScene(
    Scene,
    reset_data_on_enter=True,
    reset_history_on_enter=True,
):

    @on.message(CommandStart(deep_link=True, magic=F.args.isdigit()))
    async def on_enter_deep_link(
        self,
        message: Message,
        command: CommandObject,
        user: User,
        repo: RequestsRepo,
    ):
        employee = await repo.employees.get_employee(
            telegram_id=int(command.args)
        )
        if not employee:
            await self.wizard.goto(MenuOptions.MAIN_MENU.scene)
            return

        visit = await repo.visits.get_current_visit(user_id=user.id)
        if not visit:
            await repo.visits.create_visit(
                user_id=user.id, employee_id=employee.id
            )
        await self.wizard.goto(
            MenuOptions.REGISTER.scene
            if not user.car
            else MenuOptions.MAIN_MENU.scene
        )

    @on.message(CommandStart)
    async def on_enter_start(self, message: Message):
        await self.wizard.goto(MenuOptions.MAIN_MENU.scene)

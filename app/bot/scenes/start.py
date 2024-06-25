from aiogram import F
from aiogram.types import Message
from aiogram.fsm.scene import Scene, on
from aiogram.filters import CommandStart, CommandObject
from fluentogram import TranslatorRunner

from app.database.models import User
from app.database.repo.requests import RequestsRepo
from app.bot.scenes.user import MainMenuUserScene
from app.bot.scenes.register import RegisterCarScene


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
        i18n: TranslatorRunner,
    ):
        employee = await repo.employees.get_employee(
            telegram_id=int(command.args)
        )
        if not employee:
            return await self.wizard.goto(MainMenuUserScene)

        visit = await repo.visits.get_current_visit(
            user_id=user.id, employee_id=employee.id
        )
        if not visit:
            await repo.visits.create_visit(
                user_id=user.id, employee_id=employee.id
            )

        await self.wizard.goto(
            RegisterCarScene if not user.car else MainMenuUserScene
        )

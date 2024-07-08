from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.scene import Scene, on
from aiogram.filters import CommandStart, CommandObject
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.user import csat_kb
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
        i18n: TranslatorRunner,
    ):
        employee = await repo.employees.get_employee(
            telegram_id=int(command.args)
        )
        if employee:

            visit = await repo.visits.get_current_visit(user_id=user.id)
            if not visit:
                await repo.visits.create_visit(
                    user_id=user.id, employee_id=employee.id
                )
        await message.answer(text=i18n.cmd.start.show(user=user.first_name))
        await self.wizard.goto(
            MenuOptions.REGISTER.scene
            if not user.car
            else MenuOptions.MAIN_MENU.scene
        )

    @on.message(CommandStart(deep_link=True, magic=F.args.contains("show")))
    async def on_enter_start(
        self, message: Message, user: User, i18n: TranslatorRunner
    ):
        await self.wizard.goto(MenuOptions.MAIN_MENU.scene)
        # new_user_storage_key = StorageKey(
        #     message.bot.id, chat_id=user.telegram_id, user_id=user.telegram_id
        # )
        # # state = await self.wizard.state.set_state(state="estimations")
        # await self.wizard.state.storage.set_state(
        #     key=new_user_storage_key, state="estimations"
        # )
        # await message.answer(
        #     text=i18n.rate.quality.service(),
        #     reply_markup=csat_kb(visit_id=4),
        # )
        # await message.answer(text=i18n.cmd.start.show(user=user.first_name))
        # await self.wizard.goto(MenuOptions.MAIN_MENU.scene)

    @on.message(CommandStart)
    async def on_enter_start(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        visit = await repo.visits.get(5)
        print(visit)
        visit_up = await repo.visits.update(
            visit, update_data={"comment": "test"}
        )
        print(visit_up)

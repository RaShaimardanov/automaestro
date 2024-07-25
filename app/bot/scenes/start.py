from aiogram import F
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.bot.bot import bot
from app.bot.keyboards.inline.employee import main_menu_employee_kb
from app.bot.utils.enums import MenuOptions
from app.database.models import User
from app.database.repo.requests import RequestsRepo
from app.services.tasks.messages import send_message_task


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
                user_storage_key = StorageKey(
                    bot_id=bot.id,
                    chat_id=employee.telegram_id,
                    user_id=employee.telegram_id,
                )
                data = await self.wizard.state.storage.get_data(
                    key=user_storage_key
                )

                visits = await repo.visits.get_current_visits_by_employee_id(
                    employee_id=employee.id
                )
                message_employee = await message.bot.send_message(
                    chat_id=employee.telegram_id,
                    text=i18n.employee.main.menu(total=len(visits)),
                    reply_markup=main_menu_employee_kb(visits),
                )

                prev_message = data.get("message")
                if prev_message:
                    await prev_message.delete()
                    await self.wizard.state.storage.set_data(
                        key=user_storage_key,
                        data={"message": message_employee},
                    )

        await message.answer(text=i18n.cmd.start.show(user=user.first_name))
        await self.wizard.goto(
            MenuOptions.REGISTER.scene
            if not user.car
            else MenuOptions.MAIN_MENU_USER.scene
        )

    @on.message(CommandStart(deep_link=True, magic=F.args.contains("show")))
    async def on_enter_start(
        self, message: Message, user: User, i18n: TranslatorRunner
    ):
        await self.wizard.goto(MenuOptions.MAIN_MENU_USER.scene)

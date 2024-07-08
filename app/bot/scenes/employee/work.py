from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.base import update_kb
from app.bot.keyboards.inline.employee import work_menu_kb, work_detail_menu_kb
from app.bot.keyboards.inline.user import csat_kb, accept_kb
from app.bot.scenes.mixins import MenuScene
from app.bot.utils.callback_data import ChangeStatusCallback
from app.bot.utils.enums import MenuOptions
from app.database.models import Employee
from app.database.repo.requests import RequestsRepo
from app.utils.enums import OrderStatus


class WorkEmployeeScene(MenuScene, state="work_employee"):
    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        visits = await repo.visits.get_current_visits_by_employee_id(
            employee_id=employee.id
        )
        await callback_query.message.edit_text(
            text="Автомобили в работе", reply_markup=work_menu_kb(visits)
        )


class WorkDetailEmployeeScene(MenuScene, state="work_detail_employee"):
    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
        context,
    ):
        visit = await repo.visits.get(int(context))
        await self.wizard.update_data(visit=visit)
        await callback_query.message.edit_text(
            text=i18n.employee.work.detail.info(
                license_plate_number=visit.user.car.license_plate_number,
                status=visit.status.value,
                first_name=visit.user.first_name,
                last_name=visit.user.last_name,
                notify_ready=visit.notify_ready,
            ),
            reply_markup=work_detail_menu_kb(visit=visit),
        )

    @on.callback_query(ChangeStatusCallback.filter())
    async def change_status(
        self,
        callback_query: CallbackQuery,
        callback_data: ChangeStatusCallback,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        visit = await repo.visits.get(int(callback_data.visit_id))
        await repo.visits.update(
            visit, update_data=dict(status=callback_data.status)
        )
        user_storage_key = StorageKey(
            callback_query.bot.id,
            chat_id=visit.user.telegram_id,
            user_id=visit.user.telegram_id,
        )
        data = await self.wizard.state.storage.get_data(key=user_storage_key)
        message = data.get("message")
        if message:
            await message.delete()

        if visit.notify_ready and (
            callback_data.status == OrderStatus.ready.name
        ):
            await callback_query.bot.send_message(
                chat_id=visit.user.telegram_id,
                text=i18n.car.ready.notify(
                    license_plate_number=visit.user.car.license_plate_number
                ),
                reply_markup=accept_kb(),
            )

        elif callback_data.status == OrderStatus.issued.name:
            await self.wizard.state.storage.set_state(
                key=user_storage_key, state="estimations"
            )
            await callback_query.bot.send_message(
                chat_id=visit.user.telegram_id,
                text=i18n.rate.quality.service(),
                reply_markup=csat_kb(visit_id=visit.id),
            )
        await self.wizard.goto(MenuOptions.MAIN_MENU_EMPLOYEE.scene)

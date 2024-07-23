from aiogram.filters import Command


from app.bot.scenes.employee.work import (
    WorkEmployeeScene,
    WorkDetailEmployeeScene,
)
from app.bot.scenes.poll import PollScene
from app.bot.scenes.start import StartScene
from app.bot.scenes.user.estimations import EstimationsScene
from app.bot.scenes.user.profile import ProfileScene
from app.bot.scenes.user.main_menu import MainMenuUserScene
from app.bot.scenes.user.send_vcard import SendVCardScene
from app.bot.scenes.user.register import RegisterCarScene
from app.bot.scenes.user.notifications import NotificationsScene
from app.bot.scenes.employee.main_menu import MainMenuEmployeeScene
from app.bot.scenes.employee.profile import ProfileEmployeeScene
from app.bot.scenes.employee.register import RegisterEmployeeScene

user_router = MainMenuUserScene.as_router(name=__name__)
employee_router = MainMenuEmployeeScene.as_router(name=__name__)

user_router.message.register(MainMenuUserScene.as_handler(), Command("menu"))
employee_router.message.register(
    MainMenuEmployeeScene.as_handler(), Command("master")
)

router_list = [user_router, employee_router]
scenes_list = [
    StartScene,
    PollScene,
    ProfileScene,
    SendVCardScene,
    RegisterCarScene,
    MainMenuUserScene,
    NotificationsScene,
    EstimationsScene,
    WorkEmployeeScene,
    ProfileEmployeeScene,
    RegisterEmployeeScene,
    MainMenuEmployeeScene,
    WorkDetailEmployeeScene,
]

__all__ = [
    "router_list",
    "scenes_list",
]

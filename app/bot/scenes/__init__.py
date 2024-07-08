from aiogram.filters import Command


from app.bot.scenes.employee.work import (
    WorkEmployeeScene,
    WorkDetailEmployeeScene,
)
from app.bot.scenes.poll import PollScene
from app.bot.scenes.start import StartScene
from app.bot.scenes.user.estimations import EstimationsScene
from app.bot.scenes.user.profile import ProfileScene
from app.bot.scenes.user.main import MainMenuUserScene
from app.bot.scenes.user.send_vcard import SendVCardScene
from app.bot.scenes.user.register import RegisterCarScene
from app.bot.scenes.user.notifications import NotificationsScene
from app.bot.scenes.employee.main import MainMenuEmployeeScene
from app.bot.scenes.employee.profile import ProfileEmployeeScene
from app.bot.scenes.employee.register import RegisterEmployeeScene

start_router = StartScene.as_router(name=__name__)
employee_router = MainMenuEmployeeScene.as_router(name=__name__)

# start_router.message.register(StartScene.as_handler(), Command("start"))
employee_router.message.register(
    MainMenuEmployeeScene.as_handler(), Command("master")
)

router_list = [employee_router]
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

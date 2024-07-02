from __future__ import annotations

from app.bot.scenes.poll import PollScene
from app.bot.scenes.start import StartScene
from app.bot.scenes.user.profile import ProfileScene
from app.bot.scenes.user.main import MainMenuUserScene
from app.bot.scenes.user.register import RegisterCarScene
from app.bot.scenes.user.notifications import NotificationsScene

scenes_list = [
    StartScene,
    PollScene,
    ProfileScene,
    RegisterCarScene,
    MainMenuUserScene,
    NotificationsScene,
]

__all__ = [
    "scenes_list",
]

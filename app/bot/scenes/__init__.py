from app.bot.scenes.start import StartScene
from app.bot.scenes.user import MainMenuUserScene
from app.bot.scenes.register import RegisterCarScene


scenes_list = [
    StartScene,
    RegisterCarScene,
    MainMenuUserScene,
]

__all__ = [
    "scenes_list",
]

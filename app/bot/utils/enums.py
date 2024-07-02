import importlib
from enum import Enum
from functools import lru_cache


class MenuOptions(Enum):
    """Класс для опций меню."""

    MAIN_MENU = (
        "Главное меню",
        "app.bot.scenes.user.main",
        "MainMenuUserScene",
    )
    POLL = (
        "Пройти опрос",
        "app.bot.scenes.poll",
        "PollScene",
    )
    PROFILE = (
        "Профиль",
        "app.bot.scenes.user.profile",
        "ProfileScene",
    )
    REGISTER = (
        "Изменить данные автомобиля",
        "app.bot.scenes.user.register",
        "RegisterCarScene",
    )
    NOTIFICATIONS = (
        "Настройка уведомлений",
        "app.bot.scenes.user.notifications",
        "NotificationsScene",
    )

    def __init__(self, text, module_name, class_name):
        self._text = text
        self._module_name = module_name
        self._class_name = class_name

    @property
    def text(self):
        """Возвращает текстовую метку опции меню."""
        return self._text

    @property
    @lru_cache(None)
    def scene(self):
        """Ленивая загрузка импортов и кэширование сцены."""
        module = importlib.import_module(self._module_name)
        return getattr(module, self._class_name)

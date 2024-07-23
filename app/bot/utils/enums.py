import importlib
from enum import Enum
from functools import lru_cache


class MenuOptions(Enum):

    # Пункты меню пользователя
    MAIN_MENU_USER = (
        "Главное меню",
        "app.bot.scenes.user.main_menu",
        "MainMenuUserScene",
    )
    PROFILE_USER = (
        "Профиль",
        "app.bot.scenes.user.profile",
        "ProfileScene",
    )
    POLL = (
        "Пройти опрос",
        "app.bot.scenes.poll",
        "PollScene",
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
    VISIT_CARD = (
        "Контакты мастера",
        "app.bot.scenes.user.send_vcard",
        "SendVCardScene",
    )

    # Пункты меню сотрудника
    MAIN_MENU_EMPLOYEE = (
        "Главное меню",
        "app.bot.scenes.employee.main_menu",
        "MainMenuEmployeeScene",
    )
    REGISTER_EMPLOYEE = (
        "Начать",
        "app.bot.scenes.employee.register",
        "RegisterEmployeeScene",
    )
    WORK_SCENE = (
        "Автомобили",
        "app.bot.scenes.employee.work",
        "WorkEmployeeScene",
    )
    WORK_DETAIL = (
        "Автомобили • Информация",
        "app.bot.scenes.employee.work",
        "WorkDetailEmployeeScene",
    )
    PROFILE_EMPLOYEE = (
        "Профиль",
        "app.bot.scenes.employee.profile",
        "ProfileEmployeeScene",
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


class EstimationsEnum(Enum):
    """Перечисление возможных оценок"""

    def __init__(self, score, smile):
        self.score = score
        self.smile = smile

    POOR = ("1", "😞")
    FAIR = ("2", "😕")
    AVERAGE = ("3", "😐")
    GOOD = ("4", "🙂")
    EXCELLENT = ("5", "😊")

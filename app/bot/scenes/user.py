from aiogram.types import Message
from aiogram.fsm.scene import Scene, on

from app.database.models import User


class MainMenuUserScene(
    Scene,
    state="main_menu_user",
):
    @on.message.enter()
    async def on_enter(self, message: Message, user: User):
        pass

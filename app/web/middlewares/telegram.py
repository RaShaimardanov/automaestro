from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class TelegramIDCheckingMiddleware(BaseHTTPMiddleware):
    EXCLUSIONS = ("/", "/static", "/docs", "/webhook")

    async def dispatch(self, request: Request, call_next):
        """
        Middleware для проверки наличия telegram_id в куках запроса.
        Проверяет принадлежность telegram_id к списку ADMINS_IDS.
        """
        if request.url.path in self.EXCLUSIONS:
            return await call_next(request)

        telegram_id = request.cookies.get("telegram_id")

        if request.url.path.startswith("/admin") and telegram_id:
            if int(telegram_id) in settings.ADMINS_IDS:
                return await call_next(request)

        return RedirectResponse("/")

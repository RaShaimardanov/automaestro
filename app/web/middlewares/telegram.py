from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class TelegramIDCheckingMiddleware(BaseHTTPMiddleware):
    EXCLUSIONS = ("/", "/static", "/docs", "/webhook")

    async def dispatch(self, request: Request, call_next):
        """
        Мидлварь для проверки наличия telegram_id в куках реквеста.
        Проверяет принадлежность telegram_id к списку ADMINS_IDS
        """

        if request.url.path in self.EXCLUSIONS:
            return await call_next(request)

        if (
            request.url.path not in self.EXCLUSIONS
            and "telegram_id" not in request.cookies
        ):
            return RedirectResponse("/")

        if request.cookies.get("telegram_id") not in settings.ADMINS_IDS:
            return RedirectResponse("/")

        response = await call_next(request)

        return response

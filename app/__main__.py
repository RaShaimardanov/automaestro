import uvicorn

from app.core.config import settings
from app.web.app import app

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.SERVER.SERVER_HOST,
        port=settings.SERVER.SERVER_PORT,
        forwarded_allow_ips=["*"],
        log_level="info",
    )

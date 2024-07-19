from celery import Celery

from app.core.config import settings

celery_app = Celery(
    main=settings.PROJECT_NAME,
    broker=settings.REDIS.REDIS_URL,
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks(["app.services.tasks.*"])

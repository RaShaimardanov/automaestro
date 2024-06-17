import logging
from logging import Logger
import sys

from app.core.config import settings


def configure_logging() -> Logger:
    """Настройка логгирования для приложения."""

    LOGGER_NAME = f"{settings.PROJECT_NAME} Logger"
    STREAM_LOG_LEVEL = logging.INFO
    FILE_LOG_LEVEL = logging.ERROR
    FILE_LOG_NAME = "log.log"

    STREAM_FORMAT = "%(levelname)s:     %(message)s [%(asctime)s]"
    STREAM_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    FILE_FORMAT = (
        "%(asctime)s [%(levelname)s]: "
        "%(module)s - %(funcName)s: %(lineno)d - %(message)s"
    )

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)  # Установка общего уровня логгирования

    # Настройка StreamHandler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(STREAM_LOG_LEVEL)
    stream_handler.setFormatter(
        logging.Formatter(fmt=STREAM_FORMAT, datefmt=STREAM_DATE_FORMAT)
    )

    # Настройка FileHandler
    file_handler = logging.FileHandler(FILE_LOG_NAME)
    file_handler.setLevel(FILE_LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(fmt=FILE_FORMAT))

    # Добавление обработчиков к логгеру
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


if not logging.getLogger().handlers:
    logger = configure_logging()
else:
    logger = logging.getLogger(__name__)

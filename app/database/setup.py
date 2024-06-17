from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from app.core.config import settings


def create_engine(
    url: str, echo: bool = False, pool_timeout: int = 1, pool_size: int = 10
) -> AsyncEngine:
    """
    Создает и возвращает асинхронный движок SQLAlchemy.

    :param url: URI для подключения к базе данных
    :param echo: Логирование запросов SQL
    :param pool_timeout: Время ожидания свободного подключения в пуле
    :param pool_size: Размер пула подключений
    :return: Асинхронный движок SQLAlchemy
    """
    return create_async_engine(
        url=url,
        echo=echo,
        future=True,
        pool_pre_ping=True,
        pool_timeout=pool_timeout,
        pool_size=pool_size,
    )


def get_async_session_maker(engine: AsyncEngine):
    """
    Создает и возвращает фабрику асинхронных сессий.

    :param engine: Асинхронный движок SQLAlchemy
    :return: Фабрика асинхронных сессий
    """
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )


# Инициализация движка и фабрики сессий
engine: AsyncEngine = create_engine(
    url=settings.POSTGRES_URI, echo=settings.POSTGRES_ECHO
)

async_session_pool = get_async_session_maker(engine)


async def get_async_session():
    """
    Контекстный менеджер для получения асинхронной сессии.
    """
    async with async_session_pool() as async_session:
        yield async_session

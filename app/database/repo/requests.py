from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repo.user import UserRepo


@dataclass
class RequestsRepo:
    """
    Хранилище для обработки операций с базами данных.
    Этот класс содержит все хранилища для моделей баз данных.
    Вы можете добавить дополнительные хранилища в качестве свойств к этому классу,
    чтобы они были легко доступны.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        return UserRepo(self.session)

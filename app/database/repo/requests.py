from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import (
    Car,
    Visit,
    User,
    Employee,
    Poll,
    Question,
    Option,
    Answer,
)
from app.database.repo.car import CarRepo
from app.database.repo.poll import (
    PollRepo,
    QuestionRepo,
    OptionRepo,
    AnswerRepo,
)
from app.database.repo.user import UserRepo
from app.database.repo.visit import VisitRepo
from app.database.repo.employee import EmployeeRepo


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
        return UserRepo(model=User, session=self.session)

    @property
    def employees(self) -> EmployeeRepo:
        return EmployeeRepo(model=Employee, session=self.session)

    @property
    def visits(self) -> VisitRepo:
        return VisitRepo(model=Visit, session=self.session)

    @property
    def cars(self) -> CarRepo:
        return CarRepo(model=Car, session=self.session)

    @property
    def polls(self) -> PollRepo:
        return PollRepo(model=Poll, session=self.session)

    @property
    def questions(self) -> QuestionRepo:
        return QuestionRepo(model=Question, session=self.session)

    @property
    def options(self) -> OptionRepo:
        return OptionRepo(model=Option, session=self.session)

    @property
    def answers(self) -> AnswerRepo:
        return AnswerRepo(model=Answer, session=self.session)

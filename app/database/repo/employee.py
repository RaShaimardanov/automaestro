from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.database.models import Employee
from app.database.repo.base import BaseRepo


class EmployeeRepo(BaseRepo):
    async def get_employee(self, telegram_id: int) -> Employee | None:
        """
        Ищет и возвращает экземпляр модели сотрудника по telegram_id, если такой есть в БД
        """
        insert_stmt = select(Employee).where(telegram_id == Employee.telegram_id)
        result = await self.session.execute(insert_stmt)

        return result.scalar_one_or_none()
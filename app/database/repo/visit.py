from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.dialects.postgresql import insert

from app.database.models import Visit
from app.database.repo.base import BaseRepo
from app.utils.enums import OrderStatus


class VisitRepo(BaseRepo):

    async def create_visit(self, user_id: int, employee_id: int) -> Visit:
        insert_stmt = (
            insert(Visit)
            .values(user_id=user_id, employee_id=employee_id)
            .returning(Visit)
        )
        result = await self.session.scalar(insert_stmt)
        await self.session.commit()
        return result

    async def get_last_visit_by_user_id(self, user_id: int) -> Optional[Visit]:
        stmt = (
            select(Visit)
            .where(and_(user_id == Visit.user_id))
            .order_by(Visit.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_current_visit(self, user_id: int) -> Optional[Visit]:
        stmt = select(Visit).where(
            and_(user_id == Visit.user_id, OrderStatus.issued != Visit.status)
        )
        result = await self.session.scalar(stmt)
        return result

    async def get_current_visits_by_employee_id(
        self, employee_id: int
    ) -> Optional[list[Visit]]:
        stmt = (
            select(Visit)
            .where(
                and_(
                    employee_id == Visit.employee_id,
                    OrderStatus.issued != Visit.status,
                )
            )
            .order_by(Visit.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

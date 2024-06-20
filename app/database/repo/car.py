from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.database.models import Car
from app.database.repo.base import BaseRepo


class CarRepo(BaseRepo):
    async def check_unique_number(
        self, license_plate_number: str
    ) -> Optional[Car]:
        stmt = select(Car).where(
            license_plate_number == Car.license_plate_number
        )
        result = await self.session.scalar(stmt)
        return result

    async def get_or_create_car(self, **kwargs) -> Optional[Car]:
        insert_stmt = (
            insert(Car)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=[Car.license_plate_number],
                set_=kwargs,
            )
            .returning(Car)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one_or_none()

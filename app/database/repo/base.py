from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


class BaseRepo:
    """
    A class representing a base repository for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.

    """

    def __init__(self, model, session):
        self.model = model
        self.session: AsyncSession = session

    async def create(self, data: dict, user: Optional[User] = None):
        if user is not None:
            data["user_id"] = user.id
        db_obj = self.model(**data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, obj, update_data: dict):
        obj_data = jsonable_encoder(obj)

        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def remove(self, obj):
        await self.session.delete(obj)
        await self.session.commit()
        return obj

from typing import Generic, Optional, Sequence, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_all(self, session: AsyncSession) -> Sequence[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_by_id(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in: BaseModel,
        session: AsyncSession
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: BaseModel,
        session: AsyncSession
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession
    ) -> ModelType:
        await session.delete(db_obj)
        return db_obj

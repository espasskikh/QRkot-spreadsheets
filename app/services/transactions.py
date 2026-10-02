from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import TransactionError


@asynccontextmanager
async def transaction(session: AsyncSession):
    """Сохраняет операцию в БД целиком или отменяет изменения при ошибке."""
    try:
        yield
        await session.commit()
    except SQLAlchemyError as error:
        await session.rollback()
        raise TransactionError from error

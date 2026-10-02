from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.repositories.base import BaseRepository


class CharityProjectRepository(BaseRepository[CharityProject]):

    async def get_open_oldest_projects(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        """Получить открытые проекты, начиная с самого старого."""
        db_objs = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date, CharityProject.id)
        )
        return db_objs.scalars().all()

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Найти ID проекта по его имени."""
        project_id = await session.execute(
            select(CharityProject.id)
            .where(CharityProject.name == project_name)
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        """Получить закрытые проекты."""
        db_objs = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(True))
        )
        return db_objs.scalars().all()


charity_project_repository = CharityProjectRepository(CharityProject)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.repositories.charity_project import charity_project_repository
from app.repositories.donation import donation_repository
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.services.investment import close_if_fully_invested, process_investment
from app.services.transactions import transaction
from app.services.validators import (
    check_full_amount,
    check_name_duplicate,
    check_project_can_be_deleted,
    check_project_exists,
    check_project_is_open
)


async def get_projects(session: AsyncSession) -> list[CharityProject]:
    """Получить все проекты."""
    return await charity_project_repository.get_all(session)


async def create_project(
    project_in: CharityProjectCreate,
    session: AsyncSession
) -> CharityProject:
    """Создать проект и переложить в него свободные пожертвования."""
    await check_name_duplicate(project_in.name, session)
    async with transaction(session):
        project = await charity_project_repository.create(project_in, session)
        await process_investment(
            project,
            donation_repository.find_open_donations,
            session
        )
    await session.refresh(project)
    return project


async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Изменить открытый проект."""
    project = await check_project_exists(project_id, session)
    check_project_is_open(project)
    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session, project_id)
    if project_in.full_amount is not None:
        check_full_amount(project, project_in.full_amount)

    async with transaction(session):
        project = await charity_project_repository.update(
            project,
            project_in,
            session,
        )
        close_if_fully_invested(project)
    await session.refresh(project)
    return project


async def delete_project(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Удалить открытый проект без вложенных средств."""
    project = await check_project_exists(project_id, session)
    check_project_can_be_deleted(project)
    async with transaction(session):
        await charity_project_repository.remove(project, session)
    return project

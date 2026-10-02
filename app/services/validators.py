from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.repositories.charity_project import charity_project_repository


async def check_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта с указанным ID."""
    project = await charity_project_repository.get_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден.'
        )
    return project


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
    project_id: Optional[int] = None
) -> None:
    """Отсутствие другого проекта с таким именем."""
    existing_id = await charity_project_repository.get_project_id_by_name(
        name,
        session
    )
    if existing_id is not None and existing_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует.'
        )


def check_project_is_open(project: CharityProject) -> None:
    """Проект не закрыт и его можно изменить."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя редактировать закрытый проект.'
        )


def check_full_amount(project: CharityProject, full_amount: int) -> None:
    """Новая сумма при изменении не меньше вложенной."""
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                'Нельзя установить значение full_amount '
                'меньше вложенной суммы.'
            )
        )


def check_project_can_be_deleted(project: CharityProject) -> None:
    """Проект открыт и в него не вложены средства."""
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить проект, средства уже внесены.'
        )

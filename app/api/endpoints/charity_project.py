from fastapi import APIRouter

from app.api.dependencies import SessionDep, SuperuserDep
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.charity_project import (
    create_project,
    delete_project,
    get_projects,
    update_project
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получить список проектов.'
)
async def get_all_charity_projects(
    session: SessionDep
) -> list[CharityProject]:
    return await get_projects(session)


@router.post(
    '/',
    dependencies=[SuperuserDep],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Создать новый проект.'
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: SessionDep
) -> CharityProject:
    return await create_project(project, session)


@router.patch(
    '/{project_id}',
    dependencies=[SuperuserDep],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Изменить проект.'
)
async def update_charity_project(
    project_id: int,
    project: CharityProjectUpdate,
    session: SessionDep
) -> CharityProject:
    return await update_project(project_id, project, session)


@router.delete(
    '/{project_id}',
    dependencies=[SuperuserDep],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Удалить открытый проект.'
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep
) -> CharityProject:
    return await delete_project(project_id, session)

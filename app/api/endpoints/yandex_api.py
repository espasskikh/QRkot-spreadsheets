from fastapi import APIRouter

from app.api.dependencies import SessionDep, SuperuserDep, YandexClientDep
from app.services.yandex_api import create_project_report


router = APIRouter()


@router.post(
    '/',
    dependencies=[SuperuserDep],
    response_model=str,
    summary='Создать отчёт о закрытых проектах.'
)
async def create_report(
    session: SessionDep,
    yandex_client: YandexClientDep
) -> str:
    return await create_project_report(session, yandex_client)

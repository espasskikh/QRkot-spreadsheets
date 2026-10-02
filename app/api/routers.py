from fastapi import APIRouter

from app.api.endpoints import (
    auth_router,
    charity_project_router,
    donation_router,
    register_router,
    users_router,
    yandex_router
)


main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity_projects']
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['donations']
)
main_router.include_router(
    auth_router,
    prefix='/auth/jwt',
    tags=['auth']
)
main_router.include_router(
    register_router,
    prefix='/auth',
    tags=['auth']
)
main_router.include_router(
    users_router,
    prefix='/users',
    tags=['users']
)
main_router.include_router(
    yandex_router,
    prefix='/yandex',
    tags=['Yandex Disk']
)

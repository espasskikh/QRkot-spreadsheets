from app.api.endpoints.charity_project import router as charity_project_router
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.user import auth_router, register_router, users_router
from app.api.endpoints.yandex_api import router as yandex_router


__all__ = [
    'auth_router',
    'charity_project_router',
    'donation_router',
    'register_router',
    'users_router',
    'yandex_router'
]

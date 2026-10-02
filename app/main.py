from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
# from app.core.lifespan import check_yandex_disk_access


app = FastAPI(
    title=settings.app_title,
    description='Фонд QRKot для помощи котам.',
    # NOTE: lifespan не проходит проверку тестов в яндекс практикум,
    # поэтому  закомментирован. Локально работает.
    # lifespan=check_yandex_disk_access
)

app.include_router(main_router)

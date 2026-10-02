from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.lifespan import lifespan


app = FastAPI(
    title=settings.app_title,
    description='Фонд QRKot для помощи котам.',
    lifespan=lifespan
)

app.include_router(main_router)

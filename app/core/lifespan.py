from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common.exceptions import YandexDiskError
from app.core.config import settings
from app.core.yandex_client import YandexDiskClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with YandexDiskClient(settings.yandex_disk_token) as client:
        try:
            await client.get_basic_info()
        except YandexDiskError as error:
            raise RuntimeError(
                'Нет доступа к Яндекс Диску. '
                'Проверьте токен QRKOT_YANDEX_DISK_TOKEN'
            ) from error
    yield

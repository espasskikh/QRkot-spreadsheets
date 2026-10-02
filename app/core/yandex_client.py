import json
from typing import Optional

import httpx
from fastapi import status

from app.common.exceptions import YandexDiskError
from app.core.config import settings


BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
RESOURCES_URL = f'{BASE_URL}/resources'
UPLOAD_URL = f'{RESOURCES_URL}/upload'
PUBLISH_URL = f'{RESOURCES_URL}/publish'
REQUEST_TIMEOUT = 30.0
XLSX_CONTENT_TYPE = (
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)


class YandexDiskClient:
    """Клиент для API Яндекс Диска."""

    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'OAuth {token}'}
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=REQUEST_TIMEOUT)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    @staticmethod
    def _parse_json(response: httpx.Response) -> dict:
        """Вернуть JSON ответ или вернуть исключение."""
        try:
            return response.json()
        except json.JSONDecodeError as error:
            raise YandexDiskError(
                detail='Ошибка преобразования ответа Яндекс Диска в JSON'
            ) from error

    async def create_excel_file(
        self, title: str, folder: Optional[str] = None
    ) -> tuple[str, str]:
        """Создать Excel и вернуть ссылку для загрузки и путь к файлу."""
        folder = folder or settings.reports_folder
        await self._create_folder(folder)

        file_path = f'disk:/{folder}/{title}.xlsx'

        try:
            response = await self._client.get(
                UPLOAD_URL,
                headers=self.headers,
                params={'path': file_path, 'overwrite': 'true'}
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise YandexDiskError(
                'Не удалось запросить ссылку для загрузки на Яндекс Диск'
            ) from error

        upload_url = self._parse_json(response).get('href')
        if not upload_url:
            raise YandexDiskError('Не удалось получить ссылку для загрузки')

        return upload_url, file_path

    async def upload_file(self, upload_url: str, content: bytes):
        """Загружает файл по полученной ссылке."""
        try:
            response = await self._client.put(
                upload_url,
                content=content,
                headers={'Content-Type': XLSX_CONTENT_TYPE}
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise YandexDiskError(
                'Не удалось загрузить файл на Яндекс Диск'
            ) from error

    async def publish_file(self, file_path: str) -> str:
        """Делает файл публичным и возвращает ссылку."""
        try:
            response = await self._client.put(
                PUBLISH_URL,
                headers=self.headers,
                params={'path': file_path}
            )
            response.raise_for_status()

            response = await self._client.get(
                RESOURCES_URL,
                headers=self.headers,
                params={'path': file_path}
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise YandexDiskError(
                'Не удалось опубликовать файл на Яндекс Диск'
            ) from error

        public_url = self._parse_json(response).get('public_url')
        if not public_url:
            raise YandexDiskError(
                'Ссылка не была получена со стороны Яндекс Диска'
            )

        return public_url

    async def _create_folder(self, folder: str) -> None:
        """Создаёт папку, если её нет."""
        try:
            response = await self._client.put(
                RESOURCES_URL,
                headers=self.headers,
                params={'path': f'disk:/{folder}'}
            )
            if response.status_code == status.HTTP_409_CONFLICT:
                return
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise YandexDiskError(
                'Не удалось создать папку на Яндекс Диске'
            ) from error

    async def get_basic_info(self) -> dict:
        """Получить общую информацию о Диске."""
        try:
            response = await self._client.get(
                BASE_URL,
                headers=self.headers
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise YandexDiskError(
                'Не удалось выполнить запрос к API Яндекс Диска'
            ) from error
        return self._parse_json(response)


async def get_yandex_client():
    """Dependency для получения клиента Яндекс Диска."""
    async with YandexDiskClient(settings.yandex_disk_token) as client:
        yield client

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Фонд помощи котам'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    yandex_disk_token: Optional[str] = None
    report_format: str = '%d.%m.%Y %H:%M:%S'
    reports_folder: str = 'QRKot Reports'

    model_config = SettingsConfigDict(env_file='.env', env_prefix='QRKOT_')


settings = Settings()

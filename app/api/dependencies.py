from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.core.yandex_client import YandexDiskClient, get_yandex_client
from app.models.user import User


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
SuperuserDep = Depends(current_superuser)
UserDep = Annotated[User, Depends(current_user)]
YandexClientDep = Annotated[YandexDiskClient, Depends(get_yandex_client)]

from fastapi import APIRouter

from app.api.dependencies import SessionDep, SuperuserDep, UserDep
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.donation import (
    create_donation,
    get_donations,
    get_user_donations
)


router = APIRouter()


@router.get(
    '/',
    dependencies=[SuperuserDep],
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    summary='Получить список пожертвований.'
)
async def get_all_donations(session: SessionDep) -> list[Donation]:
    return await get_donations(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    summary='Получить свои пожертвования.'
)
async def get_my_donations(
    session: SessionDep,
    user: UserDep
) -> list[Donation]:
    return await get_user_donations(user.id, session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary='Создать пожертвование.'
)
async def create_new_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: UserDep
) -> Donation:
    return await create_donation(donation, session, user.id)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.repositories.charity_project import charity_project_repository
from app.repositories.donation import donation_repository
from app.schemas.donation import DonationCreate
from app.services.investment import process_investment
from app.services.transactions import transaction


async def get_donations(session: AsyncSession) -> list[Donation]:
    """Получить все пожертвования."""
    return await donation_repository.get_all(session)


async def get_user_donations(
    user_id: int,
    session: AsyncSession
) -> list[Donation]:
    """Получить пожертвования пользователя."""
    return await donation_repository.get_by_user(user_id, session)


async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession,
    user_id: int
) -> Donation:
    """Создать пожертвование и распределить его по открытым проектам."""
    async with transaction(session):
        donation = await donation_repository.create_by_user(
            donation_in,
            user_id,
            session
        )
        await process_investment(
            donation,
            charity_project_repository.get_open_oldest_projects,
            session
        )
    await session.refresh(donation)
    return donation

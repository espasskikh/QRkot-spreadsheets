from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.repositories.base import BaseRepository
from app.schemas.donation import DonationCreate


class DonationRepository(BaseRepository[Donation]):

    async def find_open_donations(
        self,
        session: AsyncSession
    ):
        """Найти все нераспределенные пожертвования."""
        result = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
        )
        return result.scalars().all()

    async def create_by_user(
        self,
        obj_in: DonationCreate,
        user_id: int,
        session: AsyncSession
    ) -> Donation:
        """Создать пожертвование от имени пользователя."""
        donation = Donation(**obj_in.model_dump(), user_id=user_id)
        session.add(donation)
        await session.flush()
        return donation

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession
    ) -> list[Donation]:
        """Получить пожертвования пользователя."""
        result = await session.execute(
            select(Donation)
            .where(Donation.user_id == user_id)
        )
        return list(result.scalars().all())


donation_repository = DonationRepository(Donation)

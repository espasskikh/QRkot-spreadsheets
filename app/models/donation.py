from typing import Optional

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import FundingBase


class Donation(FundingBase):
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False
    )

    def __repr__(self) -> str:
        return f'Пожертвование на сумму {self.full_amount}'

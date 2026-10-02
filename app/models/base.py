from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.common.constants import DEFAULT_INVEST
from app.core.db import Base, CommonMixin


class FundingBase(CommonMixin, Base):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            f'full_amount > {DEFAULT_INVEST}',
            name='full_amount_positive'
        ),
        nullable=False
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            f'invested_amount >= {DEFAULT_INVEST}',
            name='invested_amount_nonnegative'
        ),
        default=DEFAULT_INVEST,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(),
        nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

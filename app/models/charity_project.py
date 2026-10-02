from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.common.constants import (
    MAX_LENGTH_NAME,
    MIN_LENGTH_DESCRIPTION,
    MIN_LENGTH_NAME
)
from app.models.base import FundingBase


class CharityProject(FundingBase):
    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_NAME),
        CheckConstraint(
            f'length(name) BETWEEN {MIN_LENGTH_NAME} AND {MAX_LENGTH_NAME}',
            name='charityproject_name_length'
        ),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        CheckConstraint(
            f'length(description) >= {MIN_LENGTH_DESCRIPTION}',
            name='charityproject_description_length'
        ),
        nullable=False
    )

    def __repr__(self) -> str:
        return (
            f'Проект {self.name} на сумму {self.full_amount}, '
            f'уже собрано {self.invested_amount}'
        )

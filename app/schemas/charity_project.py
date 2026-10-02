from datetime import datetime
from typing import Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    ValidationInfo,
    field_validator
)

from app.common.constants import (
    DEFAULT_INVEST,
    MAX_LENGTH_NAME,
    MIN_LENGTH_DESCRIPTION,
    MIN_LENGTH_NAME
)


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=MIN_LENGTH_NAME, max_length=MAX_LENGTH_NAME)
    description: str = Field(min_length=MIN_LENGTH_DESCRIPTION)
    full_amount: PositiveInt

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH_NAME,
        max_length=MAX_LENGTH_NAME
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH_DESCRIPTION)
    full_amount: Optional[int] = Field(None, gt=DEFAULT_INVEST)

    @field_validator('name', 'description', 'full_amount')
    @classmethod
    def fields_cannot_be_null(
        cls,
        value: Optional[Union[str, int]],
        info: ValidationInfo
    ) -> Union[str, int]:
        if value is None:
            raise ValueError(f'Поле {info.field_name} не может быть пустым.')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

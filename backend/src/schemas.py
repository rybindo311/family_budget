from datetime import date, datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator


class TransactionCategory(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    OTHER = "other"

class TransactionBase(BaseModel):
    sum: int = Field(..., description="Сумма в рублях")
    category: TransactionCategory
    
    @field_validator('sum')
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError('Сумма должна быть положительной')
        return value

class TransactionCreate(TransactionBase):

    model_config = ConfigDict(
        extra="forbid",  
        str_strip_whitespace=True,
    )

class Transaction(TransactionBase):
    id: int
    user_id: int
    date: datetime

class TransactionResponse(Transaction):


    model_config = ConfigDict(
        use_enum_values=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "sum": 1.000,
                "category": "food",
                "date": "2024-01-01T12:00:00",
            },
            "description": "Модель транзакции",
        }
    )

class DateRange (BaseModel):
    from_date: date
    to_date: date

    @field_validator('from_date')
    @classmethod
    def validate_from_date(cls, from_date: date) -> date:
        if from_date > datetime.now().date():
            raise ValueError('from_date не может быть в будущем')
        return from_date
    
    @model_validator(mode='after')
    def validate_dates_order(self) -> 'DateRange':
        if self.to_date < self.from_date:
            raise ValueError('to_date не может быть раньше from_date')
        return self


class StatsResponse(BaseModel):
    
    transactionsCount: int
    transactionsSum: int

class CategoryStatsResponse(StatsResponse):

    categories: dict[str, StatsResponse]

class FamilyStatsResponse(StatsResponse):

    members: dict[str, CategoryStatsResponse]

Stats = TypeVar("Stats", bound=StatsResponse)

class LimitedStatsResponse (BaseModel, Generic[Stats]):
    period: DateRange
    stats: Stats
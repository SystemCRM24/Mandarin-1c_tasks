"""Схемы для работы с данными из 1с"""
from pydantic import BaseModel, Field, field_validator
from math import ceil


class CalculationItemSchema(BaseModel):
    """Схема для исполнителей задач по заказу"""
    position: str = Field(alias="Должность")
    position_id: str = Field(alias="ДолжностьИдентификатор")
    time: int = Field(
        alias="Время", 
        description="Время в секундах которое предполагается затратить на производство задачи"
    )
    amount: float = Field(alias="Сумма")

    @field_validator('time', mode='before')
    @classmethod
    def validate_time(cls, minutes: float) -> int:
        """
        На вход подается время в минутах.
        Округляем вверх до кратного 5 минутам и возвращает в виде секунд.
        """
        return ceil(minutes / 5) * 5 * 60

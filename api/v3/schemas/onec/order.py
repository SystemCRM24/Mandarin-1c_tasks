"""Схемы для работы с данными из 1с"""
from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime
from ...constants import MOSCOW_TZ


from .calculation import CalculationItemSchema
from .file_item import FileItemSchema


class OrderSchema(BaseModel):
    """Схема заказа"""
    id: str = Field(alias="ИдентификаторЗаказа")
    name: str = Field(alias="НомерЗаказа")
    date: datetime = Field(
        alias="ДатаЗаказа", 
        description="Дата, когда был заведен заказ в 1с"
    )
    assigner: str = Field(alias="Исполнитель")
    counterparty: str = Field(alias="Контрагент")
    manager: str = Field(alias="Менеджер")
    completed: bool = Field(alias="Выполнен")
    deadline: datetime = Field(alias="РекоммендуемаяДатаСдачи")
    acceptance: datetime = Field(
        alias="ДатаПриема", 
        description="Дата, когда заказ должен поступить на производсто."
    )
    calculation: List[CalculationItemSchema] = Field(
        alias="Калькуляция", 
        description="Список позиций (должностей), на которые будут распределены задачи."
    )
    files: List[FileItemSchema] = Field(
        alias="ПрисоединенныеФайлы", 
        default_factory=list
    )

    @field_validator('date', 'deadline', 'acceptance', mode='after')
    @classmethod
    def validate_date(cls, value: datetime):
        # Все даты приходят в формате ISO, но без указания часового пояса. 
        # Соответственно, строка 2025-02-13T17:36:20 означает, что это 17:36 по Москве.
        if value.tzinfo is None:
            return value.replace(tzinfo=MOSCOW_TZ)
        return value

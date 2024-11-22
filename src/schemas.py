from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CalculationItem(BaseModel):
    """Схема для исполнителей задач по заказу"""
    position: str = Field(alias='Должность')
    position_id: str = Field(alias='ДолжностьИдентификатор')
    time: float = Field(alias='Время', description='Время в минутах')
    amount: float = Field(alias='Сумма')


class AttachedFilesItem(BaseModel):
    """Схема прилагаемых файлов"""
    name: str = Field(alias='Имя')
    binary: str = Field(alias='ДвоичныеДанные')


class OrderSchema(BaseModel):
    """Схема запроса для заказа"""
    id: str = Field(alias='ИдентификаторЗаказа')
    number: str = Field(alias='НомерЗаказа')
    date: datetime = Field(alias='ДатаЗаказа')
    executor: str = Field(alias='Исполнитель')
    completed: bool = Field(alias='Выполнен')
    completion_date: datetime = Field(alias='РекоммендуемаяДатаСдачи')
    acceptance_date: datetime = Field(alias='ДатаПриема')
    calculation: List[CalculationItem] = Field(alias='Калькуляция')
    attached_files: List[AttachedFilesItem] = Field(alias='ПрисоединенныеФайлы', default_factory=list)

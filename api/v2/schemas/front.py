"""Схемы для работы с данными для фронт-части приложения"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from api.v2.constants import MOSCOW_TZ


class IntervalSchema(BaseModel):
    """Схема Временного промежутка"""
    start: datetime
    end: datetime

    @field_validator('start', 'end', mode='before')
    @classmethod
    def validate_date(cls, value) -> datetime:
        if isinstance(value, int):
            return datetime.fromtimestamp(value, MOSCOW_TZ)
        return value


class ResourceSchema(BaseModel):
    """Схема ресурса"""
    id: str | int
    label: str
    department: str | int


class FromFrontTaskSchema(BaseModel):
    id: str
    label: str
    resourceId: str
    time: IntervalSchema
    deadline: int


class TaskSchema(BaseModel):
    """Схема задачи"""
    id: str | int
    label: str
    resourceId: str | int
    time: IntervalSchema
    deadline: datetime


class WebSocketDataSchema(BaseModel):
    """Схема ответа по WebSocket соединению"""
    now: datetime
    interval: IntervalSchema
    workIntervals: list[IntervalSchema]
    resources: list[ResourceSchema]
    tasks: list[TaskSchema]

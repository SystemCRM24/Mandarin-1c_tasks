"""Схемы для работы с данными для фронт-части приложения"""
from pydantic import BaseModel
from datetime import datetime
from .main import DepartmentSchema, UserSchema, TaskSchema


class UpdateTaskSchema(BaseModel):
    """Схема обновления задачи."""
    RESPONSIBLE_ID: str
    START_DATE_PLAN: str
    END_DATE_PLAN: str
    DEADLINE: str
    TIME_ESTIMATE: int


class IntervalSchema(BaseModel):
    """Схема Временного промежутка"""
    start: datetime
    end: datetime


class WebSocketSchema(BaseModel):
    """Схема ответа по вс соединению"""
    departments: dict[str: DepartmentSchema]
    staff: dict[str: UserSchema]
    tasks: dict[str: TaskSchema]
    interval: IntervalSchema
    workIntervals: list[IntervalSchema]

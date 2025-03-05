"""Схемы для работы с данными для фронт-части приложения"""
from pydantic import BaseModel
from datetime import datetime
from .main import DepartmentSchema, UserSchema, TaskSchema
from typing import Dict


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
    departments: Dict[str, DepartmentSchema]
    staff: Dict[str, UserSchema]
    tasks: Dict[str, TaskSchema]
    interval: IntervalSchema
    workIntervals: list[IntervalSchema]
    now: datetime

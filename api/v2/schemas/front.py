"""Схемы для работы с данными для фронт-части приложения"""
from pydantic import BaseModel
from datetime import datetime


class IntervalSchema(BaseModel):
    """Схема Временного промежутка"""
    start: datetime
    end: datetime


class ResourceSchema(BaseModel):
    """Схема ресурса"""
    id: str | int
    label: str
    department: str | int


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

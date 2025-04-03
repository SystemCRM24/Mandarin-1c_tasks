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


class FromFrontTaskSchema(BaseModel):
    id: str
    label: str
    resourceId: str
    time: IntervalSchema
    deadline: datetime


class TaskSchema(BaseModel):
    """Схема задачи"""
    id: str | int
    label: str
    resourceId: str | int
    time: IntervalSchema
    deadline: datetime


class WebSocketDataSchema(BaseModel):
    """Схема ответа по WebSocket соединению"""
    interval: IntervalSchema
    workIntervals: list[IntervalSchema]
    resources: list[ResourceSchema]
    tasks: list[TaskSchema]


class WebSocketMessageSchema(BaseModel):
    meta: str
    content: WebSocketDataSchema | bool

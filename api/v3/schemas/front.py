from pydantic import BaseModel
from datetime import datetime


class IntervalSchema(BaseModel):
    """Схема Временного промежутка"""
    start: datetime
    end: datetime


class TaskSchema(BaseModel):
    """Схема задачи"""
    id: str | int
    label: str
    resourceId: str | int
    time: IntervalSchema
    deadline: datetime


class ResourceSchema(BaseModel):
    """Схема ресурса"""
    id: str | int
    label: str
    department: str | int


class _DataSchema(BaseModel):
    interval: IntervalSchema
    workIntervals: list[IntervalSchema]
    resources: list[ResourceSchema]
    tasks: list[TaskSchema]

class DataSchema(BaseModel):
    meta: str = 'data'
    content: _DataSchema


class SyncSchema(BaseModel):
    meta: str = 'sync'
    content: bool

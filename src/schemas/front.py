"""Схемы для работы с данными для фронт-части приложения"""
from pydantic import BaseModel


class UpdateTaskSchema(BaseModel):
    """Схема обновления задачи."""
    RESPONSIBLE_ID: str
    START_DATE_PLAN: str
    END_DATE_PLAN: str
    DEADLINE: str
    TIME_ESTIMATE: int



# class WorkIntervalSchema(BaseModel):
#     start: datetime
#     end: datetime


# class ResultSchema(BaseModel):
#     departments: dict[str, DepartmentSchema]
#     staff: dict[str, StaffSchema]
#     tasks: dict[str, TaskSchema]
#     interval: dict[str, str] | list[dict]
#     workIntervals: List[WorkIntervalSchema] | None = None
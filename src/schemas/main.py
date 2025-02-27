"""Внутренние схемы приложения"""
from pydantic import BaseModel, computed_field, field_validator
from datetime import datetime
from zoneinfo import ZoneInfo


class DepartmentSchema(BaseModel):
    """Схема подразделения"""
    ID: str
    NAME: str
    PARENT: str | None = None
    UF_HEAD: str | None = None


class UserSchema(BaseModel):
    """Схема для персонала"""
    ID: str
    NAME: str
    LAST_NAME: str
    UF_DEPARTMENT: list[int] = []

    @computed_field
    @property
    def full_name(self) -> str:
        return self.NAME + ' ' + self.LAST_NAME 


class TaskSchema(BaseModel):
    id: str
    title: str
    description: str
    createdBy: str
    responsibleId: str
    groupId: str
    allowTimeTracking: str
    # Поля связанные с датами и временем
    dateStart: datetime
    deadline: datetime
    startDatePlan: datetime
    endDatePlan: datetime
    timeEstimate: int
    
    @field_validator('dateStart', 'deadline', 'startDatePlan', 'endDatePlan', mode='before')
    @classmethod
    def validate_datetime(cls, value: str) -> datetime:
        """Округляет время в потолок"""
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            value = datetime.now()
        return value.replace(tzinfo=ZoneInfo('Europe/Moscow'))



class TaskResponseSchema(BaseModel):
    """Схема ответа по постановке/обновлении задачи"""
    position: str
    user: str = ''
    user_id: str = ''
    message: str = 'ok'

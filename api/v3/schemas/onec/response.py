from pydantic import BaseModel


class TaskItemSchema(BaseModel):
    """Схема ответа по задаче"""
    position: str
    id: str = ''
    message: str = ''


class ResponseSchema(BaseModel):
    """Схема ответа"""
    order: str
    tasks: list[TaskItemSchema]

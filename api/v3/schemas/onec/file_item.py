"""Схемы для работы с данными из 1с"""
from pydantic import BaseModel, Field, field_validator
from urllib.parse import unquote


class FileItemSchema(BaseModel):
    """Схема прилагаемых файлов"""
    name: str = Field(alias="Имя")
    binary: str = Field(alias="ДвоичныеДанные")

    @field_validator('binary', mode='after')
    @classmethod
    def validate_binary(cls, value: str):
        return unquote(value)

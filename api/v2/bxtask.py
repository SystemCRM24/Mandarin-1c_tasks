from typing import Self
from datetime import datetime
import asyncio

from .constants import MOSCOW_TZ, ONEC_GROUP_ID, DIRECTOR_ID


class BXTask:
    """Интерфейс для работы с задачами"""

    __slots__ = (
        '_updated',
        'id', 
        'group_id',
        'allow_time_tracking',
        'assigner_id',
        'responsible_id',
        'title',
        'description',
        'date_start',
        'deadline',
        'start_date_plan',
        'end_date_plan',
        'time_estimate',
        'webdav_files'
    )

    @staticmethod
    def parse_bitrix_date(datestring: str) -> datetime:
        """Парсит дату из битрикса. Принудительно заменяет часовой пояс на московский."""
        if datestring is None or not datestring:
            return None
        return datetime.fromisoformat(datestring).replace(tzinfo=MOSCOW_TZ)

    @classmethod
    def from_bitrix(cls, task_response: dict) -> Self:
        bxtask = cls()
        bxtask.id = task_response.get('id', None)
        bxtask.group_id = task_response.get('groupId', None)
        bxtask.allow_time_tracking = task_response.get('allowTimeTracking', None)
        bxtask.assigner_id = task_response.get('createdBy', None)
        bxtask.responsible_id = task_response.get('responsibleId', None)
        bxtask.title = task_response.get('title', None)
        bxtask.description = task_response.get('description', None)
        date_start = task_response.get('dateStart', None)
        bxtask.date_start = cls.parse_bitrix_date(date_start)
        deadline = task_response.get('deadline', None)
        bxtask.deadline = cls.parse_bitrix_date(deadline)
        start_date_plan = task_response.get('startDatePlan', None)
        bxtask.start_date_plan = cls.parse_bitrix_date(start_date_plan)
        end_date_plan = task_response.get('endDatePlan', None)
        bxtask.end_date_plan = cls.parse_bitrix_date(end_date_plan)
        bxtask.time_estimate = int(task_response.get('timeEstimate', 0))
        bxtask.webdav_files = task_response.get('ufTaskWebdavFiles', None)
        bxtask._updated.clear()
        return bxtask

    def __init__(self):
        self._updated = set()
        # Метаинформация по задаче
        self.id = None
        self.group_id = ONEC_GROUP_ID
        self.allow_time_tracking = 'Y'
        # Персонал задачи
        self.assigner_id = DIRECTOR_ID
        self.responsible_id = DIRECTOR_ID
        # Текстовая информация задачи
        self.title = None
        self.description = None
        # Временные метки
        self.date_start = None
        self.deadline = None
        self.start_date_plan = None
        self.end_date_plan = None
        self.time_estimate = None   # Время в секундах
        # Прикрепленные файлы
        self.webdav_files = None
        # Чистим множество после инициализации
        self._updated.clear()
    
    def is_valid(self) -> bool:
        """Проверяет задачу на валидность."""
        return all((
            self.group_id,
            self.assigner_id,
            self.responsible_id,
            self.title,
            self.start_date_plan,
            self.end_date_plan
        ))
    
    def __setattr__(self, name, value):
        old_value = getattr(self, name, None)
        super().__setattr__(name, value)
        if name != '_updated' and old_value != value:
            self._updated.add(name)

    def __str__(self):
        gen = (f'{attr}={getattr(self, attr)}' for attr in self.__slots__[1:])
        return f'{self.__class__.__name__}({", ".join(gen)})'
    
    async def create(self):
        pass

    async def update(self):
        pass

    async def execute(self):
        """Отправляет запрос на выполнение задачи"""
        pass
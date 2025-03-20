from typing import Self
from datetime import datetime
from . import requests

from ..constants import MOSCOW_TZ, TIMEZONE_COMPENSATION, DIRECTOR_ID


class BXTask:
    """Интерфейс для работы с задачами"""

    PARAM_BY_ATTR = {
        'group_id': "GROUP_ID",
        'allow_time_tracking': 'ALLOW_TIME_TRACKING',
        'assigner_id': 'CREATED_BY',
        'responsible_id': 'RESPONSIBLE_ID',
        'title': 'TITLE',
        'description': 'DESCRIPTION',
        'created_date': 'CREATED_DATE',
        'deadline': 'DEADLINE',
        'start_date_plan': 'START_DATE_PLAN',
        'end_date_plan': 'END_DATE_PLAN',
        'time_estimate': 'TIME_ESTIMATE',
        'webdav_files': 'UF_TASK_WEBDAV_FILES',
    }

    __slots__ = (
        '_updated',
        'id',
        'group_id',
        'allow_time_tracking',
        'assigner_id',
        'responsible_id',
        'title',
        'description',
        'created_date',
        'deadline',
        'start_date_plan',
        'end_date_plan',
        'time_estimate',
        'webdav_files',
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
        created_date = task_response.get('created_date', None)
        bxtask.created_date = cls.parse_bitrix_date(created_date)
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
        # Метаинформация по задаче
        self.id = None
        self.group_id = None
        self.allow_time_tracking = None
        # Персонал задачи
        self.assigner_id = None
        self.responsible_id = None
        # Текстовая информация задачи
        self.title = None
        self.description = None
        # Временные метки
        self.created_date = None
        self.deadline = None
        self.start_date_plan = None
        self.end_date_plan = None
        self.time_estimate = None   # Время в секундах
        # Прикрепленные файлы
        self.webdav_files = None
        # Чистим множество после инициализации
        self._updated = set()
    
    def is_valid(self) -> bool:
        """Проверяет задачу на валидность."""
        return all((
            self.group_id,
            self.assigner_id,
            self.responsible_id != DIRECTOR_ID,
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
    
    def get_bx_request(self) -> dict:
        plan_attr = ('start_date_plan', 'end_date_plan')
        if plan_attr[0] in self._updated:
            self._updated.add(plan_attr[1])
        if plan_attr[1] in self._updated:
            self._updated.add(plan_attr[0])
        request = {}
        for attr in self._updated:
            param = self.PARAM_BY_ATTR.get(attr, None)
            if param is None:
                continue
            value = getattr(self, attr)
            if attr == 'webdav_files':
                value = [f'n{file_id}' for file_id in value]
            if isinstance(value, datetime):
                if TIMEZONE_COMPENSATION:
                    value += MOSCOW_TZ.utcoffset(value)
                value = value.isoformat()
            request[param] = value
        return request

    async def create(self):
        request = self.get_bx_request()
        self._updated.clear()
        response = await requests.create_task(request)
        return response.get('id', '-1')

    async def update(self):
        if self._updated:
            # self.recalculate_total_duration()
            request = self.get_bx_request()
            await requests.update_task(self.id, request)
        self._updated.clear()
        return self.id

    async def execute(self):
        """Отправляет запрос на выполнение задачи"""
        await requests.execute_task(self.id)
        return self.id

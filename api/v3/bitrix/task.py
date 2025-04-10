from typing import Self
from datetime import datetime

from api.v3 import constants
from api.v3.bitrix import requests


class BXTask:
    """Объект для представления задач в битриксе"""

    __slots__ = (
        'id',
        'onec_id',
        'status',
        'group_id',
        'allow_time_tracking',
        'last_update',
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
        '_buffer'
    )

    PARAM_BY_ATTR = {
        'id': 'ID',
        'onec_id': 'UF_AUTO_151992241453',
        'status': 'STATUS',
        'group_id': 'GROUP_ID',
        'allow_time_tracking': 'ALLOW_TIME_TRACKING',
        'last_update': 'UF_AUTO_261370983936',
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
    
    def __init__(self):
        # Идешники задачи
        self.id = None          # Из битры
        self.onec_id = None     # Из 1c
        # Метаинформация по задаче
        self.status = None
        self.group_id = None
        self.allow_time_tracking = None
        self.last_update = None
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
        # Множество для отслеживания изменения атрибутов
        self._buffer = set()
    
    def __setattr__(self, name, value):
        old_value = getattr(self, name, None)
        super().__setattr__(name, value)
        if name != '_updated' and old_value != value:
            self._buffer.add(name)
    
    def __str__(self):
        gen = (f'{attr}={repr(getattr(self, attr))}' for attr in self.PARAM_BY_ATTR)
        return f'{self.__class__.__name__}({", ".join(gen)})'

    @staticmethod
    def parse_bitrix_date(datestring: str) -> datetime | None:
        """Парсит датестринг из запроса. Насильно прикручивает временную зону Москвы"""
        if datestring is None and not datestring:
            return None
        return datetime.fromisoformat(datestring).replace(tzinfo=constants.MOSCOW_TZ)

    @classmethod
    async def from_bitrix(cls, task_id: str) -> Self:
        """Создает объект на основе информации из битрикса"""
        task_dct = await requests.get_task_info(task_id, cls.PARAM_BY_ATTR.values())
        return cls.from_bitrix_response(task_dct)

    @classmethod
    def from_bitrix_response(cls, response: dict) -> Self:
        """Создает объект на основе переданного response"""
        if response is None:
            return None
        task = cls()
        task.id = response.get('id', None)
        task.onec_id = response.get('ufAuto151992241453', None)
        task.status = response.get('status', None)
        task.group_id = response.get('groupId', None)
        task.allow_time_tracking = response.get('allowTimeTracking', None)
        last_update: str = response.get('ufAuto261370983936', '')
        task.last_update = int(last_update) if last_update.isdigit() else None
        task.assigner_id = response.get('createdBy', None)
        task.responsible_id = response.get('responsibleId', None)
        task.title = response.get('title', None)
        task.description = response.get('description', None)
        created_date = response.get('created_date', None)
        task.created_date = cls.parse_bitrix_date(created_date)
        deadline = response.get('deadline', None)
        task.deadline = cls.parse_bitrix_date(deadline)
        start_date_plan = response.get('startDatePlan', None)
        task.start_date_plan = cls.parse_bitrix_date(start_date_plan)
        end_date_plan = response.get('endDatePlan', None)
        task.end_date_plan = cls.parse_bitrix_date(end_date_plan)
        task.time_estimate = int(response.get('timeEstimate', 0))
        task.webdav_files = response.get('ufTaskWebdavFiles', None)
        task._buffer.clear()
        return task
    
    def is_valid(self) -> bool:
        """Валидация задачи"""
        return all(self._is_valid())

    def _is_valid(self):
        yield bool(self.onec_id)
        yield self.group_id == constants.ONEC_GROUP_ID
        yield self.allow_time_tracking == 'Y'
        yield isinstance(self.last_update, int)
        yield isinstance(self.deadline, datetime)
        yield isinstance(self.start_date_plan, datetime)
        yield isinstance(self.end_date_plan, datetime)
        yield isinstance(self.time_estimate, int)

    def get_request(self) -> dict | None:
        """Выдает словарь готового запроса по измененным атрибутам. Чистит буфер."""
        if not self._buffer:
            return None
        plan_attrs = ('start_date_plan', 'end_date_plan')
        for index, plan_attr in enumerate(plan_attrs):
            if plan_attr in self._buffer:
                self._buffer.add(plan_attrs[not index])
        request = {}
        for attr in self._buffer:
            param = self.PARAM_BY_ATTR.get(attr, None)
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.isoformat()
            if attr == 'webdav_files':
                value = [f'n{file_id}' for file_id in value]
            request[param] = value
        self._buffer.clear()
        return request

    def get_create_batch(self) -> str:
        """Выдает батч на создание задачи"""

    def get_update_batch(self) -> str | None:
        """Выдает батч на обновление задачи"""
        if self._buffer:
            timestamp = datetime.now(constants.MOSCOW_TZ).timestamp()
            self.last_update = int(timestamp)
        request = self.get_request()
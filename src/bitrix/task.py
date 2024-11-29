import schemas
from . import requests
from .file import Files

from datetime import datetime, date, timezone, timedelta
import math


MOSCOW_TIMEZONE = timezone(timedelta(hours=3), 'ETC')


class UpdateTaskException(Exception):
    """Исключение при обновлении задачи"""


class Task:
    """Класс - интерфейс для работы с задачами"""

    def __init__(
            self,
            order: schemas.OrderSchema, 
            calculation: schemas.CalculationItem,
            files: Files
        ):
        self.order = order
        self.calculation = calculation
        self.files = files
        # Технические переменные
        self.staff: list = None
        self.staff_tasks: list = None
        # Переменные для запроса
        self.task_name: str = None
        self.victim: dict = None
        self.victim_last_deadline: datetime = None

    async def put_task(self):
        """Ставит задачу"""
        self._preprocessing()
        department_id = await requests.get_department_id_from_name(self.calculation.position)
        self.staff = await requests.get_staff_from_department_id(department_id)
        self.staff_tasks = await requests.get_staff_tasks(self.staff)
        handler = self._get_handler()
        request_data = await self._get_request()
        await handler(request_data)
    
    def _preprocessing(self):
        """Различная подготовка объекта перед выполнением запросов"""
        # Формируем название заказа
        self.task_name = f'{self.calculation.position}: {self.order.number}'
        # Округляем время в потолок. Переводим в секунды
        self.calculation.time = math.ceil(self.calculation.time * 60)
    
    def _get_handler(self):
        """Возвращает обработчик, который будет ставить или обновлять задачи."""
        for i in range(len(self.staff)):
            victim = self.staff[i]
            victim_tasks = self.staff_tasks[i]
            if not victim_tasks:
                self.victim_last_deadline = datetime.now(MOSCOW_TIMEZONE)
                self.victim = victim 
                break
            for task in victim_tasks:
                if task['title'] == self.task_name:     # В случае обновления задачи
                    self.victim_last_deadline = datetime.fromisoformat(task['createdDate'])
                    self.victim = victim
                    return self._update_task_wrapper(task['id'])
                current_deadline = datetime.fromisoformat(task['deadline'])
                if self.victim_last_deadline is None or current_deadline < self.victim_last_deadline:
                    self.victim_last_deadline = current_deadline
                    self.victim = self.staff[i]
        return requests.create_task

    @staticmethod
    def _update_task_wrapper(task_id: int | str):
        """Обертка для обновления задачи"""
        async def wrapper(request_data: dict):
            try:
                await requests.update_task(task_id, request_data)
            except:
                raise UpdateTaskException('Ошибка обновления задачи')
        return wrapper

    async def _get_request(self) -> dict:
        """Формирует ответ для постановки или обновления задачи. Записываем под формат битрикса"""
        return {
            'TITLE': self.task_name,
            'RESPONSIBLE_ID': self.victim['ID'],
            'DESCRIPTION': self._get_task_description(),
            'DATE_START': self.victim_last_deadline,
            'DEADLINE': await self._get_deadline_date(),
            'TIME_ESTIMATE': self.calculation.time,
            'UF_TASK_WEBDAV_FILES': await self.files.get_request(),
            'MATCH_WORK_TIME': 'Y',
            'ALLOW_TIME_TRACKING': 'Y'
        }

    def _get_task_description(self) -> str:
        """Возвращает описание задачи"""
        string = (
            f'Сумма: {self.calculation.amount}',
            f'Рекомендуемая дата сдачи: {self.order.completion_date}'
        )
        return '\n'.join(string)

    async def _get_deadline_date(self) -> date:
        """Возвращает deadline date. Подсчет ведется от переданной base"""
        work_schedule: dict = await requests.get_work_schedule()
        try:
            shifts = work_schedule['SHIFTS'][0]
            work_time_start = shifts['WORK_TIME_START']
            work_time_end = shifts['WORK_TIME_END']
        except:
            work_time_start = 32400
            work_time_end = 64800
        work_time_start = timedelta(seconds=work_time_start)
        work_time_end = timedelta(seconds=work_time_end)
        deadline = self.victim_last_deadline
        workday_duration = work_time_end - work_time_start
        task_duration = timedelta(seconds=self.calculation.time)
        while task_duration > workday_duration:
            deadline += timedelta(days=1)
            task_duration -= workday_duration
        deadline += task_duration
        # Проверка того, чтобы остаток не попал на время после окончания рабочего дня
        remains = timedelta(hours=deadline.hour, minutes=deadline.minute, seconds=deadline.second)
        if remains > work_time_end:
            deadline += timedelta(days=1) - workday_duration
        return deadline

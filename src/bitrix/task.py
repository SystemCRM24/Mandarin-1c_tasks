import schemas
from . import requests
from .file import Files

from typing import Coroutine
from datetime import datetime, date
import math


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
        self.victim_last_deadline: float = None

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
        # Переводим время в секунды. 
        self.calculation.time = math.ceil(self.calculation.time * 60)
    
    def _get_handler(self):
        """Возвращает обработчик, который будет ставить или обновлять задачи."""
        for i in range(len(self.staff)):
            victim = self.staff[i]
            victim_tasks = self.staff_tasks[i]
            if not victim_tasks:
                self.victim_last_deadline = datetime.now().timestamp()
                self.victim = victim 
                break
            for task in victim_tasks:
                if task['title'] == self.task_name:     # В случае обновления задачи
                    self.victim_last_deadline = datetime.fromisoformat(task['createdDate']).timestamp()
                    self.victim = victim
                    return self._update_task_wrapper(task['id'])
                current_deadline = datetime.fromisoformat(task['deadline']).timestamp()
                if self.victim_last_deadline is None or current_deadline < self.victim_last_deadline:
                    self.victim_last_deadline = current_deadline
                    self.victim = self.staff[i]
        return requests.create_task

    @staticmethod
    def _update_task_wrapper(task_id):
        """Обертка для обновления задачи"""
        async def wrapper(request_data):
            await requests.update_task(task_id, request_data)
        return wrapper

    async def _get_request(self) -> dict:
        """Формирует ответ для постановки или обновления задачи. Записываем под формат битрикса"""
        return {
            'TITLE': self.task_name,
            'RESPONSIBLE_ID': self.victim['ID'],
            'DESCRIPTION': self._get_task_description(),
            'DATE_START': date.fromtimestamp(self.victim_last_deadline),
            'DEADLINE': await self._get_deadline_date(self.victim_last_deadline),
            'TIME_ESTIMATE': self.calculation.time,
            'UF_TASK_WEBDAV_FILES': await self.files.get_request()
        }

    def _get_task_description(self) -> str:
        """Возвращает описание задачи"""
        string = (
            f'Сумма: {self.calculation.amount}',
            f'Рекомендуемая дата сдачи: {self.order.completion_date}'
        )
        return '\n'.join(string)

    async def _get_deadline_date(self, base: float) -> date:
        """Возвращает deadline date. Подсчет ведется от переданной base"""
        return date.fromtimestamp(base + self.calculation.time)

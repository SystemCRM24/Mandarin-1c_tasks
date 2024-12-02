import schemas
from . import requests
from .file import Files
from .bx_calendar import Calendar

from datetime import datetime, timezone, timedelta
import math
import asyncio


CORRECTION = timedelta(hours=3)
MOSCOW_TIME_ZONE = timezone(CORRECTION, 'ETC')
UTC = timezone(timedelta(hours=0), 'utc')


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
        self.staff_calendar = Calendar(calculation.position)
        # Переменные для запроса
        self.task_name: str = None
        self.rapist_id: int = 1
        self.victim: dict = None
        self.victim_last_deadline: datetime = None

    async def put_task(self):
        """Ставит задачу"""
        self._preprocessing()
        await asyncio.gather(
            self.files.atask,
            self.staff_calendar.update(),
            self._update_staff_info(), 
            self._select_rapist(),
        )
        handler = self._select_victim()
        await handler(self._get_request())
    
    def _preprocessing(self):
        """Различная подготовка объекта перед выполнением запросов"""
        # Формируем название заказа
        self.task_name = f'{self.calculation.position}: {self.order.number}'
        # Округляем время в потолок. Переводим в секунды
        self.calculation.time = math.ceil(self.calculation.time * 60)
    
    async def _update_staff_info(self):
        """Обновляет информацию по подразделению и сотрудникам"""
        department_id = await requests.get_department_id_from_name(self.calculation.position)
        self.staff = await requests.get_staff_from_department_id(department_id)
        self.staff_tasks = await requests.get_staff_tasks(self.staff)
    
    async def _select_rapist(self):
        """Устанавливает постановщика задачи"""
        self.rapist_id = await requests.get_department_head_from_name(self.order.executor)

    def _select_victim(self):
        """
        Определяет человека, которому будет поставлена задача 
        и время последней задачи, по которой будет производиться подсчет
        Возвращает обработчик, который будет ставить новую или обновлять старую задачу.
        Все в куче в одной функции, но зато одним циклом.
        """
        for i in range(len(self.staff)):
            victim = self.staff[i]
            victim_tasks = self.staff_tasks[i]
            if not victim_tasks:
                self.victim_last_deadline = datetime.now(UTC)
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

    def _get_request(self) -> dict:
        """Формирует ответ для постановки или обновления задачи. Записываем под формат битрикса"""
        return {
            'TITLE': self.task_name,
            'CREATED_BY': self.rapist_id,
            'RESPONSIBLE_ID': self.victim['ID'],
            'DESCRIPTION': self._get_task_description(),
            'DATE_START': self.victim_last_deadline,
            'DEADLINE': self._get_deadline_date(),
            'START_DATE_PLAN': self.order.acceptance_date,
            'END_DATE_PLAN': self.order.completion_date,
            'TIME_ESTIMATE': self.calculation.time,
            'UF_TASK_WEBDAV_FILES': self.files.request,
            'ALLOW_TIME_TRACKING': 'Y'
        }

    def _get_task_description(self) -> str:
        """Возвращает описание задачи"""
        string = (
            f'Сумма: {self.calculation.amount}',
            f'Рекомендуемая дата сдачи: {self.order.completion_date}'
        )
        return '\n'.join(string)

    def _get_deadline_date(self) -> datetime:
        """
        Возвращает deadline datetime
        При отправке битриксу даты нужно явно указывать часовой пояс даты. 
        Иначе битрикс будет ее интерпретировать по своему. Не смотря на то, что сам битрикс отдает дату в utc.
        В случае заказчика, это было важно, так как учитывалось рабочее время сотрудника.
        """
        deadline = self.victim_last_deadline.replace(tzinfo=MOSCOW_TIME_ZONE).astimezone()
        task_duration = timedelta(seconds=self.calculation.time)
        # Прибавляем дни по рабочим часам
        while task_duration > self.staff_calendar.work_day_duration:
            deadline += timedelta(days=1)
            task_duration -= self.staff_calendar.work_day_duration
            while not self.staff_calendar.is_working_day(deadline):
                deadline += timedelta(days=1)
        # Проверка того, чтобы остаток не попал на время после окончания рабочего дня
        deadline += task_duration + CORRECTION
        remains = timedelta(hours=deadline.hour, minutes=deadline.minute, seconds=deadline.second)
        if remains > self.staff_calendar.work_time_end:
            deadline += timedelta(days=1) - self.staff_calendar.work_day_duration
        # Проверка на выходные, праздники и тп.
        while not self.staff_calendar.is_working_day(deadline):
            deadline += timedelta(days=1)
        return deadline.replace(tzinfo=MOSCOW_TIME_ZONE)

import asyncio
from os import environ
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.schemas.one_ass import OrderSchema, CalculationItem
from src.schemas.main import TaskResponseSchema, DepartmentSchema, UserSchema
from .schedule import BXSchedule
from .file import FileUploader
from . import requests


DIRECTOR_ID = environ.get('DIRECTOR_ID')
MOSCOW_TIME_ZONE = ZoneInfo('Europe/Moscow')
CORRECTION = timedelta(hours=3)


class TaskException(Exception):
    pass


class Task:
    """Класс - интерфейс для работы с задачами"""

    def __init__(self, order: OrderSchema, calculation: CalculationItem, files: FileUploader):
        # Сохраняем в объекте съемы
        self.order = order
        self.calculation = calculation
        self.files = files
        # Технические переменные
        self.department: DepartmentSchema = None
        self.staff: list = None
        self.staff_tasks: list = None
        self.staff_calendar = BXSchedule()
        # Переменные для запроса
        self.task_name = f"{self.calculation.position}: {self.order.number}"
        self.assigner_id: int = None
        self.performer: UserSchema = None
        self.performers_last_deadline: datetime = None
        # Переменная для ответа
        self.response = TaskResponseSchema(position=calculation.position)

    async def put(self):
        """Ставит задачу"""
        await asyncio.gather(
            self.files._upload_event.wait(),
            self.staff_calendar.update_from_bxschedule(),
            self._update_staff_info(),
        )
        self._select_assigner()
        handler = self._select_performer()
        await handler(self._get_request())
        self.response.user = self.performer.full_name
        self.response.user_id = self.performer.ID
        return self.response

    async def _update_staff_info(self):
        """Обновляет информацию по подразделению и сотрудникам"""
        try:
            self.department = await self._get_department()
            self.staff = await self._get_staff(self.department.ID)
            self.staff_tasks = await requests.get_staff_tasks(self.staff)
        except TaskException:
            self.response.message = str(TaskException)
            self.staff = [await requests.get_user_from_id(DIRECTOR_ID)]
            self.staff_tasks = []
    
    async def _get_department(self) -> DepartmentSchema:
        """Получает подразделение для объекта"""
        departments: list[DepartmentSchema] = await requests.get_departments_info()
        for item in departments:
            if item.NAME == self.calculation.position:
                return item
        raise TaskException(f'Нет подразделения с именем {self.calculation.position}. Задачи ставяться на пользователя с ид: {DIRECTOR_ID}')
    
    async def _get_staff(self, department_id: str | int) -> list[UserSchema]:
        """Возвращает персонал подразделения"""
        staff = await requests.get_staff_from_department_id(department_id)
        if not staff:
            raise TaskException(f'В подразделении {self.calculation.position} нет ни одного сотрудника. Задачи ставяться на пользователя с ид: {DIRECTOR_ID}')
        return staff

    def _select_assigner(self):
        """Устанавливает постановщика задачи"""
        if self.department is not None and self.department.UF_HEAD is not None:
            self.assigner_id = self.department.UF_HEAD
        else:
            self.assigner_id = DIRECTOR_ID
            self.response.message = f'В подразделении {self.calculation.position} нет руководителя. Используется постановщик по умолчанию: {DIRECTOR_ID}'

    def _select_performer(self):
        """
        Определяет человека, которому будет поставлена задача и 
        время последней задачи, по которой будет производиться подсчет.
        Возвращает обработчик, который будет ставить новую или обновлять старую задачу.
        Все в куче в одной функции, но зато одним циклом.
        """
        now = datetime.now(MOSCOW_TIME_ZONE)
        for i in range(len(self.staff)):
            performer = self.staff[i]
            performer_tasks = self.staff_tasks[i]
            print(performer, performer_tasks)
            if not performer_tasks:
                self.performer = performer
                break
            for task in performer_tasks:
                if task.title == self.task_name:  # В случае обновления задачи
                    self.performer = performer
                    self.performers_last_deadline = task.dateStart
                    return self._update_task_wrapper(task.id)
                if self.performers_last_deadline is None or task.deadline < self.performers_last_deadline:
                    self.performer = self.staff[i]
                    self.performers_last_deadline = task.deadline
        if self.performers_last_deadline is None or now > self.performers_last_deadline:
            self.performers_last_deadline = now
        return requests.create_task

    @staticmethod
    def _update_task_wrapper(task_id: int | str):
        """Обертка для обновления задачи"""
        async def wrapper(request_data: dict):
            try:
                await requests.update_task(task_id, request_data)
            except:
                raise TaskException("Ошибка обновления задачи")
        return wrapper

    def _get_request(self) -> dict:
        """Формирует ответ для постановки или обновления задачи. Записываем под формат битрикса"""
        deadline = self._get_deadline_date()
        scum = True
        now = datetime.now(MOSCOW_TIME_ZONE)
        request =  {
            "TITLE": self.task_name,
            "GROUP_ID": 1,  # задачи из 1с
            "CREATED_BY": self.assigner_id,
            "CREATED_DATE": (now + CORRECTION) if scum else now,
            "RESPONSIBLE_ID": self.performer.ID,
            "DESCRIPTION": self._get_task_description(),
            "DATE_START": (self.performers_last_deadline + CORRECTION) if scum else self.performers_last_deadline,
            "DEADLINE": (deadline + CORRECTION) if scum else deadline,
            "START_DATE_PLAN": (self.performers_last_deadline + CORRECTION) if scum else self.performers_last_deadline,
            "END_DATE_PLAN": (deadline + CORRECTION) if scum else deadline,
            "TIME_ESTIMATE": self.calculation.time,
            "UF_TASK_WEBDAV_FILES": self.files.uploaded_files,
            "ALLOW_TIME_TRACKING": "Y",
        }
        return request

    def _get_task_description(self) -> str:
        """Возвращает описание задачи"""
        string = (
            f"Сумма: {self.calculation.amount}", 
            f"Рекомендуемая дата сдачи: {self.order.completion_date}"
        )
        return "\n".join(string)

    def _get_deadline_date(self) -> datetime:
        """
        Возвращает deadline datetime
        При отправке битриксу даты нужно явно указывать часовой пояс даты.
        Иначе битрикс будет ее интерпретировать по своему. Не смотря на то, что сам битрикс отдает дату в utc.
        В случае заказчика, это было важно, так как учитывалось рабочее время сотрудника.
        """
        deadline = self.performers_last_deadline
        task_duration = timedelta(seconds=self.calculation.time)
        # Прибавляем дни по рабочим часам
        while task_duration > self.staff_calendar.work_day_duration:
            deadline += timedelta(days=1)
            task_duration -= self.staff_calendar.work_day_duration
            while not self.staff_calendar.is_working_day(deadline):
                deadline += timedelta(days=1)
        # Проверка того, чтобы остаток не попал на время после окончания рабочего дня
        deadline += task_duration
        remains = timedelta(hours=deadline.hour, minutes=deadline.minute, seconds=deadline.second)
        if remains > self.staff_calendar.work_time_end:
            deadline += timedelta(days=1) - self.staff_calendar.work_day_duration
        # Проверка на выходные, праздники и тп.
        while not self.staff_calendar.is_working_day(deadline):
            deadline += timedelta(days=1)
        return deadline

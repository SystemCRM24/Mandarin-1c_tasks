import asyncio
from os import environ

from .bx_task import BXTask
from api.v2 import bitrix
from ..file import Uploader
from ...schemas import onec


DIRECTOR_ID = environ.get('DIRECTOR_ID')


class TaskHandler:
    """Класс - интерфейс для работы с задачами"""

    def __init__(
        self, 
        order: onec.OrderSchema,
        calculation: onec.CalculationItemSchema,
        uploader: Uploader
    ):
        self.order = order
        self.calculation = calculation
        self.uploader = uploader
        self.task = BXTask()
        self.log = []
    
    async def put(self):
        """Ставит задачу"""
        self.preprocessing()
        await asyncio.gather(
            self.select_assigner(),
            self.select_responsible()
        )
        return self.log
    
    def preprocessing(self):
        """Подготовка различных параметров задачи перед ее постановкой"""
        self.task.title = f"{self.calculation.position}: {self.order.name}"
        self.task.description = "\n".join((
            f"Сумма: {self.calculation.amount}", 
            f"Рекомендуемая дата сдачи: {self.order.deadline}"
        ))
        self.task.date_start = self.order.acceptance
        self.task.deadline = self.order.deadline
        self.task.time_estimate = self.calculation.time
    
    async def select_assigner(self):
        """Определяет постановщика задачи"""
        departments: dict[str, dict] = await bitrix.get_departments_info(key='NAME')
        if self.calculation.position not in departments:
            self.log.append(f'Не найдено подразделение {self.calculation.position}.')
            self.task.assigner_id = DIRECTOR_ID
            self.task.responsible_id = DIRECTOR_ID
            return
        department = departments[self.calculation.position]
        assigner: str = department.get('UF_HEAD', '')
        if not assigner:
            self.task.assigner_id = DIRECTOR_ID
            self.log.append(f'В подразделении {self.calculation.position} нет руководителя.')
            return
        self.task.assigner_id = assigner

    async def select_responsible(self):
        """
        Устонавливает ответственного по задаче. 
        Дополнительно, определяет start_date_plan, end_date_plan без учета рабочего времени.
        """
        departments: dict[str, dict] = await bitrix.get_departments_info(key='NAME')
        if self.calculation.position not in departments:
            return
        
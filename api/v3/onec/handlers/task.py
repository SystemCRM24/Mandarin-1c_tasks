import asyncio
from datetime import datetime
from typing import Self

from api.v3.bitrix.task import BXTask
from api.v3.constants import SCHEDULE_ID, ONEC_GROUP_ID
from api.v3.bitrix.schedule import get_work_schedule, Schedule
from api.v3.bitrix.requests import get_tasks_list, call_batch
from api.v3.schemas.onec import OrderSchema, CalculationItemSchema, TaskItemSchema


def get_onec_id(order: OrderSchema, calculation: CalculationItemSchema) -> str:
    """Возвращает идентификатор для задачи"""
    return f'{order.id}:{calculation.position}'


class TaskHandler:

    def __init__(
        self, 
        order: OrderSchema, 
        calculation: CalculationItemSchema,
        schedule: Schedule
    ):
        self.order = order
        self.calculation = calculation
        self.schedule = schedule
        self.bx_task: BXTask = None
        self.batch = ''
        self.response = TaskItemSchema(self.calculation.position)
    
    async def create(self) -> Self:
        bx_task = self.bx_task = BXTask()
        bx_task.onec_id = get_onec_id(self.order, self.calculation)
        bx_task.group_id = ONEC_GROUP_ID,
        bx_task.allow_time_tracking = 'Y'
        bx_task.assigner_id = await self.select_assigner()
        responsible, start_time = await self.select_responsible()
        bx_task.responsible_id = responsible
        bx_task.title = f"{self.calculation.position}: {self.order.name}"
        bx_task.description = self.get_description()
        bx_task.created_date = self.order.acceptance
        bx_task.deadline = self.order.deadline
        bx_task.start_date_plan = start_time
        bx_task.end_date_plan = self.schedule.add_duration(start_time, self.calculation.time)
        bx_task.time_estimate = self.calculation.time
        self.batch = bx_task.get_create_batch()
        return self

    async def update(self, task_dct: dict) -> Self:
        bx_task = self.bx_task = BXTask.from_bitrix_response(task_dct)
        if self.order.completed:
            bx_task.status = 5   # выполнен
        bx_task.assigner_id = await self.select_assigner()
        bx_task.description = self.get_description()
        bx_task.deadline = self.order.deadline
        bx_task.time_estimate = self.calculation.time
        bx_task.end_date_plan = self.schedule.add_duration(bx_task.start_date_plan, bx_task.time_estimate)
        self.batch = bx_task.get_update_batch()
        return self

    async def select_assigner(self) -> str:
        """Определяет Постановщика"""
    
    async def select_responsible(self) -> tuple[str, datetime]:
        """Получает исполнителя задачи и крайнее время"""

    def get_description(self) -> str:
        """Возвращает описание"""
        return "\n".join((
            f'Контрагент: {self.order.counterparty}',
            f"Сумма: {self.calculation.amount}", 
            f"Рекомендуемая дата сдачи: {self.order.deadline.date()} {str(self.order.deadline.time())[:8]}"
        ))


class TasksHandler:
    """Обработка задач: Постановка или обновление"""

    def __init__(self, order: OrderSchema):
        self.order = order
        self.handlers: list[TaskHandler] = []
    
    async def process(self) -> list[TaskItemSchema]:
        """Обрабатывает задачи"""
        calc_by_onec_id = {get_onec_id(self.order, c): c for c in self.order.calculation}
        response = await get_tasks_list({f'@{BXTask.PARAM_BY_ATTR['onec_id']}': list[calc_by_onec_id]})
        await self._match_handler(calc_by_onec_id, response)
        await self._send_batch()
        return [h.response for h in self.handlers]

    async def _match_handler(self, calc_by_onec_id: dict, response: list[dict]):
        """Разделяет задачи на создание и обновление"""
        schedule = await get_work_schedule(SCHEDULE_ID)
        coros = []
        # Пошло на обновление
        for task_dct in response:
            onec_id = task_dct.get('ufAuto151992241453', '')
            calculation = calc_by_onec_id.pop(onec_id)
            task_handler = TaskHandler(self.order, calculation, schedule)
            coros.append(task_handler.update(task_dct))
        # Пошло на создание
        for calculation in calc_by_onec_id.values():
            task_handler = TaskHandler(self.order, calculation, schedule)
            coros.append(task_handler.create())
        handlers = await asyncio.gather(*coros)
        self.handlers.extend(handlers)

    async def _send_batch(self):
        """Посылает батчи"""
        requests = [h.batch for h in self.handlers]
        response: list[dict] = await call_batch(requests)
        for index, task in enumerate(response):
            handler = self.handlers[index]
            handler.response.id = task.get('id')

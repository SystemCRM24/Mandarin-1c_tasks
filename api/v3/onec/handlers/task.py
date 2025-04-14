import asyncio
from datetime import datetime
from typing import Self

from api.utils.loggers import uvicorn_logger
from api.v3 import constants
from api.v3.bitrix import requests
from api.v3.bitrix.task import BXTask
from api.v3.bitrix.pool import Pool
from api.v3.schemas.onec import OrderSchema, CalculationItemSchema, TaskItemSchema
from .service import get_onec_id


class TaskHandler:
    pool = Pool()

    @classmethod
    def from_bx_task(
        cls, 
        order: OrderSchema, 
        calculation: CalculationItemSchema,
        bx_task_dct: dict
    ) -> Self:
        """Создает объект на основе запроса из битрикса"""
        handler = cls(order, calculation)
        handler.bx_task = BXTask.from_bitrix_response(bx_task_dct)
        handler.for_create = False
        handler.response.id = handler.bx_task.id
        return handler

    def __init__(self, order: OrderSchema, calculation: CalculationItemSchema):
        self.order = order
        self.calculation = calculation
        self.for_create = True
        self.bx_task: BXTask = None
        self.response = TaskItemSchema(position=calculation.position)
    
    async def process(self):
        """Обработка задачи"""
        if self.for_create:
            return await self.create()
        return await self.update()
    
    def get_batch(self) -> str | None:
        """Выдает батч для создания/обновления задачи или None"""
        if self.for_create:
            return self.bx_task.get_create_batch()
        return self.bx_task.get_update_batch()
    
    async def create(self) -> str:
        bx_task = self.bx_task = BXTask()
        bx_task.onec_id = get_onec_id(self.order, self.calculation)
        bx_task.group_id = constants.ONEC_GROUP_ID
        bx_task.allow_time_tracking = 'Y'
        bx_task.assigner_id = await self.select_assigner()
        responsible, start_time = await self.select_responsible()
        bx_task.responsible_id = responsible
        bx_task.title = f"{self.calculation.position}: {self.order.name}"
        bx_task.description = self.get_description()
        bx_task.created_date = self.order.acceptance
        bx_task.deadline = self.order.deadline
        bx_task.start_date_plan = start_time
        edp = self.pool._schedule.add_duration(start_time, self.calculation.time)
        bx_task.end_date_plan = edp
        bx_task.time_estimate = self.calculation.time
        self._update_response_message('Задача создана.')

    async def update(self) -> str | None:
        if self.order.completed:
            self.bx_task.status = '5'   # выполнен
        self.bx_task.assigner_id = await self.select_assigner()
        self.bx_task.description = self.get_description()
        self.bx_task.deadline = self.order.deadline
        self.bx_task.time_estimate = self.calculation.time
        edp = self.pool._schedule.add_duration(self.bx_task.start_date_plan, self.bx_task.time_estimate)
        self.bx_task.end_date_plan = edp
        self._update_response_message('Задача обновлена.')

    async def select_assigner(self) -> str:
        """Определяет Постановщика"""
        manager_id = await requests.get_manager(self.order.manager)
        if manager_id is None:
            manager_id = constants.DIRECTOR_ID
            self._update_response_message(f'Постановщик заменен на пользователя ID={manager_id}, так как не был найден пользователь с именем ({self.order.manager})')
        return manager_id

    async def select_responsible(self) -> tuple[str, datetime]:
        """Получает исполнителя задачи и крайнее время"""
        tasks = self.pool._get_tasks_by_department()
        position_tasks = tasks.get(self.calculation.position, None)
        if position_tasks is None:
            self._update_response_message(f'Не найдено подразделение {self.calculation.position}. Исполнитель задачи назначен пользователь (id={constants.DIRECTOR_ID})')
            return constants.DIRECTOR_ID, datetime.now(constants.MOSCOW_TZ)
        responsible_id = start_date = None
        for user_id, user_tasks in position_tasks.items():
            if len(user_tasks) == 0:
                return user_id, datetime.now(constants.MOSCOW_TZ)
            last_task = user_tasks[-1]
            if start_date is None or last_task.end_date_plan < start_date:
                responsible_id = user_id
                start_date = last_task.end_date_plan
        if responsible_id is None:
            self._update_response_message(f'Не найден пользователь для {self.calculation.position}. Исполнитель задачи назначен пользователь (id={constants.DIRECTOR_ID})')
            responsible_id = constants.DIRECTOR_ID
        if start_date is None:
            start_date = datetime.now(constants.MOSCOW_TZ)
        return responsible_id, start_date

    def get_description(self) -> str:
        """Возвращает описание"""
        return "\n".join((
            f'Контрагент: {self.order.counterparty}',
            f"Сумма: {self.calculation.amount}", 
            f"Рекомендуемая дата сдачи: {self.order.deadline.date()} {str(self.order.deadline.time())[:8]}"
        ))
    
    def _update_response_message(self, message: str):
        """Обновляет сообщение"""
        if self.response.message:
            message = ' ' + message
        self.response.message += message

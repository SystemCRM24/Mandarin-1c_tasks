import asyncio

from .file import FileHandler
from .task import TaskHandler
from api.utils.loggers import uvicorn_logger
from api.v3.bitrix.task import BXTask
from api.v3.bitrix.pool import Pool
from api.v3.bitrix import requests
from .service import get_onec_id
from api.v3.schemas.onec import OrderSchema, ResponseSchema


class OrderHandler:
    """Логика обработки запроса на уровне заказа"""
    pool = Pool()

    __slots__ = ('order', '_task_handlers')

    def __init__(self, order: OrderSchema):
        self.order = order
        self._task_handlers: list[TaskHandler] = []

    async def process(self) -> ResponseSchema:
        """Запуск обработки заказа"""
        file_handler = FileHandler(self.order)
        file_handler.send_files()
        await asyncio.gather(
            self.pool.update_context(),
            self._match_task_handlers()
        )
        await asyncio.gather(*(th.process() for th in self._task_handlers))
        await self._send_batch()
        file_handler.attach_to_tasks(self._task_handlers)
        task_items = [h.response for h in self._task_handlers]
        return ResponseSchema(order=self.order.name, tasks=task_items)

    async def _match_task_handlers(self):
        """Определяет, что нужно делать с задачей: обновлять или создавать"""
        onec_id_field = BXTask.PARAM_BY_ATTR['onec_id']
        calc_by_onec = {get_onec_id(self.order, c): c for c in self.order.calculation}
        task_filter = {f'@{onec_id_field}': list(calc_by_onec)}
        response = await requests.get_tasks_list(task_filter)
        # Пошло на обновление
        for task_dct in response:
            onec_id = task_dct.get('ufAuto151992241453', '')
            calculation = calc_by_onec.pop(onec_id)
            handler = TaskHandler.from_bx_task(self.order, calculation, task_dct)
            self._task_handlers.append(handler)
        # Пошло на создание
        for calculation in calc_by_onec.values():
            handler = TaskHandler(self.order, calculation)
            self._task_handlers.append(handler)

    async def _send_batch(self):
        """Посылает запрос на создание/обновление группы задач."""
        index_by_batch = {}
        for index, handler in enumerate(self._task_handlers):
            batch = handler.get_batch()
            if batch is not None:
                index_by_batch[index] = batch
        batch_indexes = tuple(index_by_batch.keys())
        batch_values = list(index_by_batch.values())
        response = await requests.call_batch(batch_values)
        for index, task_item in enumerate(response):
            handler_index = batch_indexes[index]
            handler: TaskHandler = self._task_handlers[handler_index]
            if handler.for_create:
                task_dct = task_item.get('task')
                task_id = task_dct.get('id')
                handler.bx_task.id = task_id
                handler.response.id = task_id
        uvicorn_logger.info(f'Handled {len(batch_values)} tasks of order={self.order.name}')
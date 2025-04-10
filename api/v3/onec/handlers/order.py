import asyncio

from .file import FileHandler
from .task import TasksHandler
from api.utils import BatchBuilder
from api.utils.loggers import uvicorn_logger
from api.v3.bitrix.requests import call_batch
from api.v3.schemas.onec import OrderSchema, ResponseSchema, TaskItemSchema


class OrderHandler:
    """Логика обработки запроса на уровне заказа"""

    __slots__ = ('order', )

    def __init__(self, order: OrderSchema):
        self.order = order

    async def process(self) -> ResponseSchema:
        """Запуск обработки заказа"""
        tasks_handler = TasksHandler(self.order)
        file_handler = FileHandler(self.order.files)
        tasks_handler_at = asyncio.create_task(tasks_handler.process())
        file_handler_at = asyncio.create_task(file_handler.process())
        asyncio.create_task(self._attach_files(tasks_handler_at, file_handler_at))
        tasks_items: list[TaskItemSchema] = await tasks_handler_at
        return ResponseSchema(order=self.order.name, tasks=tasks_items)

    async def _attach_files(self, tasks_handler_at: asyncio.Task, file_handler_at: asyncio.Task):
        """присоединяет файлы к задачам."""
        result = await asyncio.gather(tasks_handler_at, file_handler_at)
        tasks_items: list[TaskItemSchema] = result[0]
        files_ids: list[int] = result[1]
        if not files_ids:
            return
        requests = []
        for task in tasks_items:
            params = {
                'taskId': task.id,
                'fields': {'UF_TASK_WEBDAV_FILES': files_ids}
            }
            batch = BatchBuilder('tasks.task.update', params) 
            requests.append(batch.build())
        await call_batch(requests)
        uvicorn_logger.info(f'Files attached to order={self.order.name} tasks.')

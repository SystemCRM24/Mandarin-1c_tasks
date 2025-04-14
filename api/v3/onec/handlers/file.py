import asyncio

from api.utils import BatchBuilder
from api.utils.loggers import uvicorn_logger
from api.v3.schemas.onec import OrderSchema
from api.v3.constants import UPLOAD_DIR_ID
from api.v3.bitrix.requests import call_batch
from .task import TaskHandler


class FileHandler:
    """Класс для работы с отправляемыми на сервер файлами"""

    __slots__ = ('order', 'to_upload', 'file_ids', '_upload_at')

    def __init__(self, order: OrderSchema):
        self.order = order
        self.to_upload = order.files
        self.file_ids = []
        self._upload_at = None
    
    def send_files(self) -> asyncio.Task:
        """Создает асинхронную задачу на отправку файлов"""
        self._upload_at = asyncio.create_task(self._send_files())
        return self._upload_at

    async def _send_files(self) -> list[int]:
        requests = []
        if not self.to_upload:
            return requests
        for file in self.to_upload:
            params = {
                'id': UPLOAD_DIR_ID,
                'fileContent': [file.name, file.binary],
                "data": {"NAME": file.name},
                "generateUniqueName": True,
            }
            batch = BatchBuilder('disk.folder.uploadfile', params)
            requests.append(batch.build())
        result: list[dict] = await call_batch(requests)
        for file in result:
            self.file_ids.append(file.get('ID', 0))
    
    def attach_to_tasks(self, tasks: list[TaskHandler]) -> asyncio.Task:
        """Создает асинхронную задачу на обновление файлов"""
        return asyncio.create_task(self._attach_to_tasks(tasks))

    async def _attach_to_tasks(self, tasks: list[TaskHandler]):
        """Присоединяет файлы к задачам."""
        await self._upload_at
        if not self.to_upload:
            return
        requests = []
        for handler in tasks:
            for file_id in self.file_ids:
                params = {'taskId': handler.bx_task.id, 'fileId': file_id}
                batch = BatchBuilder('tasks.task.files.attach', params)
                requests.append(batch.build())
        await call_batch(requests)
        uvicorn_logger.info(f'Files attached to order={self.order.name} tasks.')

import asyncio

from api.utils.loggers import uvicorn_logger
from api.v3.bitrix import requests
from api.v3.bitrix.task import BXTask
from api.v3 import constants


class Pool:
    __instance = None

    def __new__(cls):
        """Для бассейна нужен синглтон"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.__lock = asyncio.Lock()
        self.__tasks: dict[str, BXTask] = {}
        self._responsibles: dict[str, str] = {}

    async def fill(self):
        """Заполняет бассейн актуальными задачами"""
        await asyncio.gather(self._update_tasks(), self._update_responsibles())
        uvicorn_logger.info(f'Pool was filled with {len(self.__tasks)} tasks.')
    
    async def _update_tasks(self):
        """Обновляет словарь задач"""
        async with self.__lock:
            self.__tasks.clear()
            response: list[dict] = await requests.get_tasks_list({
                'GROUP_ID': constants.ONEC_GROUP_ID,
                '!STATUS': 5
            })
            for task_dct in response:
                bx_task = BXTask.from_bitrix_response(task_dct)
                if bx_task.is_valid():
                    self.__tasks[bx_task.id] = bx_task

    async def _update_responsibles(self):
        """Обновляет словарь ответственных по задачам"""

    
    async def add(self, bxtask: BXTask):
        """Добавляет задачу в бассейн"""
        if bxtask.id in self.__tasks:
            return await self.update(bxtask)
        async with self.__lock:
            self.__tasks[bxtask.id] = bxtask
        uvicorn_logger.info(f'The new task (id={bxtask.id}) has been added to the Pool.')
        asyncio.create_task(self.recalculate())
    
    async def update(self, bxtask: BXTask):
        """Обновляет задачу в бассейне"""
        if bxtask.id in self.__tasks:
            async with self.__lock:
                self.__tasks[bxtask.id] = bxtask.id
            uvicorn_logger.info(f'Task (id={bxtask.id}) was update.')
            asyncio.create_task(self.recalculate())
        else:
            uvicorn_logger.info(f'Task (id={bxtask.id}) not in pool.')

    async def delete(self, task_id: str):
        """Удаляет задачу из бассейна"""
        if task_id in self.__tasks:
            async with self.__lock:
                self.__tasks.pop(task_id, None)
            uvicorn_logger.info(f'Task (id={task_id}) was delete from the Pool.')
            asyncio.create_task(self.recalculate())
        else:
            uvicorn_logger.info(f'Task (id={task_id}) not in pool.')

    async def recalculate(self):
        """Перерасчет задач в бассейне"""


p = Pool()
asyncio.create_task(p.fill())
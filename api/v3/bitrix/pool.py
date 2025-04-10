import asyncio

from api.utils.loggers import uvicorn_logger
from api.v3.bitrix import requests
from api.v3.bitrix.task import BXTask
from api.v3.bitrix.schedule import Schedule, get_work_schedule
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
        self._schedule: Schedule = None

    async def fill(self):
        """Заполняет бассейн актуальными задачами"""
        async with self.__lock:
            await asyncio.gather(
                self._update_tasks(), 
                self._update_responsibles(),
                self._update_schedule()
            )
        uvicorn_logger.info(f'Pool was filled with {len(self.__tasks)} tasks.')
    
    async def _update_tasks(self):
        """Обновляет словарь задач"""
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
        self._responsibles = await requests.get_responsibles()

    async def _update_schedule(self):
        """Обновляет объект расписания"""
        self._schedule = await get_work_schedule(constants.SCHEDULE_ID)

    async def add(self, bxtask: BXTask):
        """Добавляет задачу в бассейн"""
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
        async with self.__lock:
            await asyncio.gather(
                self._update_responsibles(),
                self._update_schedule()
            )
            tasks_by_user = self._get_tasks_by_responsibles()
            for tasks_line in tasks_by_user.values():
                self._normalize_line(tasks_line)

    def _get_tasks_by_responsibles(self) -> dict[str, list[BXTask]]:
        """Выдает задачи распределенные по пользователям"""
        result = {user_id: [] for user_id in self._responsibles}
        for task in self.__tasks.values():
            task_list: list = result.get(task.responsible_id, None)
            if task_list is not None:
                task_list.append(task)
        return result

    def _normalize_line(self, tasks_line: list[BXTask]):
        """Нормализует задачи для выбранного пользователя"""


p = Pool()
asyncio.create_task(p.fill())
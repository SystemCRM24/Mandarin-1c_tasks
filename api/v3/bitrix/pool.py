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
        self._responsibles: dict[str, dict] = {}
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
    
    async def update_context(self):
        """Обновляет контекст: пользователей и расписание"""
        async with self.__lock:
            await asyncio.gather(
                self._update_schedule(),
                self._update_responsibles()
            )
    
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
            self._normalize_tasks(tasks_by_user)
            batch_list = self._get_batch_list()
            if len(batch_list) > 0:
                asyncio.create_task(requests.call_batch(batch_list))
                uvicorn_logger.info(f'Pool recalculate {len(batch_list)} tasks')

    def _get_tasks_by_responsibles(self) -> dict[str, list[BXTask]]:
        """Выдает задачи распределенные по пользователям"""
        result: dict[str, list[BXTask]] = {user_id: [] for user_id in self._responsibles}
        for task in self.__tasks.values():
            task_list: list = result.get(task.responsible_id, None)
            if task_list is not None:
                task_list.append(task)
        for tasks in result.values():
            tasks.sort(key=lambda bxtask: bxtask.start_date_plan)
        return result
    
    def _get_tasks_by_department(self) -> dict[str, dict[str, list[BXTask]]]:
        """Выдает задачи представленные по подразделениям."""
        tasks_by_responsibles = self._get_tasks_by_responsibles()
        result = {}
        for responsible_id, tasks in tasks_by_responsibles.items():
            responsible = self._responsibles[responsible_id]
            department_name = responsible['DEPARTMENT']['NAME']
            department = result.get(department_name, None)
            if department is None:
                department = result[department_name] = {}
            department[responsible_id] = tasks
        return result
    
    def _normalize_tasks(self, tasks_by_user: dict[str, list[BXTask]]):
        """Нормализует задачи всего контекста выполнения"""
        for user_tasks in tasks_by_user.values():
            for index, task in enumerate(user_tasks):
                time_estimate = self._schedule.get_duration(task.start_date_plan, task.end_date_plan)
                task.time_estimate = int(time_estimate.total_seconds())
                if index == 0:
                    start_date_plan = task.start_date_plan
                else:
                    prev_task = user_tasks[index - 1]
                    start_date_plan = prev_task.end_date_plan
                task.start_date_plan = self._schedule.get_nearest_datetime(start_date_plan)
                task.end_date_plan = self._schedule.add_duration(task.start_date_plan, time_estimate)
    
    def _get_batch_list(self) -> list[str]:
        """Формирует батч на обновление задач и фиксирует задачи для исключения повторной обработки"""
        batch_list = []
        for task in self.__tasks.values():
            batch = task.get_update_batch()
            if batch is None:
                continue
            batch_list.append(batch)
            constants.TO_AVOID[task.id] = task.last_update
        return batch_list


p = Pool()
# asyncio.create_task(p.fill())

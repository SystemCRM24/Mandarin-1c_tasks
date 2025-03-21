import asyncio
from datetime import datetime
from api.v2 import constants

from api.v2.bitrix.task import BXTask
from api.v2.bitrix.schedule import from_bitrix_schedule
from api.v2.bitrix import requests
from api.v2.service import funcs
from .file import Uploader
from ..schemas import onec


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
        self.department_tasks: dict[str, list[BXTask]] = {}
        self.log = []
    
    async def handle(self) -> onec.ResponseItemSchema:
        """Ставит задачу"""
        await self.get_department_tasks()
        handler = self._select_handler()
        task_id = await handler
        response = onec.ResponseItemSchema(
            position=self.calculation.position,
            task_id=task_id
        )
        if self.log:
            response.message = ' '.join(self.log)
        return response
    
    async def get_department_tasks(self):
        """
        Получает задачи персонала подразделения. Обновляет атрибут self.department_tasks
        """
        departments: dict[str, dict] = await requests.get_departments_info(key='NAME')
        department = departments.get(self.calculation.position, None)
        if department is None:
            return
        department_id = department.get('ID')
        users = await requests.get_users_by_department(department_id)
        if not users:
            return
        coros = (funcs.get_bxtasks_from_user(u['ID']) for u in users)
        tasks = await asyncio.gather(*coros)
        for i in range(len(users)):
            key = users[i]['ID']
            value = tasks[i]
            self.department_tasks[key] = value

    def _select_handler(self):
        """
        Определяет обработчик задачи, т.е. что нужно сделать с задачей. 
        Создать, обновить или выполнить. Они там рехнулись, шлют на один эндпоинт все.
        Возвращает объект корутины.
        """
        task_name = f"{self.calculation.position}: {self.order.name}"
        responsible_id = None
        empty_tasks_flag = False
        start_date_plan = None
        for user_id, tasks in self.department_tasks.items():
            for task in tasks:
                if task.title == task_name:
                    if self.order.completed:    
                        return self.execute_task(task)
                    return self.update_task(task)
            if tasks:
                last_task = tasks[-1]
                if not empty_tasks_flag:
                    if start_date_plan is None or last_task.end_date_plan < start_date_plan:
                        responsible_id = user_id
                        start_date_plan = last_task.end_date_plan
            else:
                responsible_id = user_id
                empty_tasks_flag = True
        return self.create_task(responsible_id, start_date_plan)

    async def create_task(self, responsible_id, start_date_plan):
        bxtask = BXTask()
        bxtask.group_id = constants.ONEC_GROUP_ID
        bxtask.allow_time_tracking = 'Y'
        bxtask.assigner_id = await self.select_assigner()
        if responsible_id is None:
            self.log.append(f'Не найден исполнитель для {self.calculation.position}.')
            responsible_id = constants.DIRECTOR_ID
        bxtask.responsible_id = responsible_id
        bxtask.title = f"{self.calculation.position}: {self.order.name}"
        bxtask.description = "\n".join((
            f"Сумма: {self.calculation.amount}", 
            f"Рекомендуемая дата сдачи: {self.order.deadline.date()} {str(self.order.deadline.time())[:8]}"
        ))
        bxtask.created_date = self.order.acceptance
        bxtask.deadline = self.order.deadline
        schedule = await from_bitrix_schedule()
        if start_date_plan is None:
            start_date_plan = schedule.get_nearest_datetime(datetime.now(constants.MOSCOW_TZ))
        bxtask.start_date_plan = start_date_plan
        bxtask.end_date_plan = schedule.add_duration(start_date_plan, self.calculation.time)
        bxtask.time_estimate = self.calculation.time
        await self.uploader._event.wait()
        bxtask.webdav_files = [file_schema.bx_id for file_schema in self.uploader.to_upload]
        return await bxtask.create()

    async def update_task(self, bxtask: BXTask):
        schedule = await from_bitrix_schedule()
        bxtask.description = "\n".join((
            f"Сумма: {self.calculation.amount}", 
            f"Рекомендуемая дата сдачи: {self.order.deadline}"
        ))
        bxtask.created_date = self.order.acceptance
        bxtask.deadline = self.order.deadline
        bxtask.time_estimate = self.calculation.time
        bxtask.end_date_plan = schedule.add_duration(bxtask.start_date_plan, bxtask.time_estimate)
        await self.uploader._event.wait()
        bxtask.webdav_files = [file_schema.bx_id for file_schema in self.uploader.to_upload]
        self.log.append(f'Задача была обновлена.')
        return await bxtask.update()

    async def execute_task(self, bxtask: BXTask):
        self.log.append(f'Задача была выполнена.')
        return await bxtask.execute()
    
    async def select_assigner(self) -> str | None:
        """Определяет постановщика задачи"""
        departments: dict[str, dict] = await requests.get_departments_info(key='NAME')
        if self.calculation.position not in departments:
            self.log.append(f'Не найдено подразделение {self.calculation.position}.')
            return
        department = departments[self.calculation.position]
        assigner: str = department.get('UF_HEAD', None)
        if assigner is None:
            self.log.append(f'В подразделении {self.calculation.position} нет руководителя.')
            return constants.DIRECTOR_ID
        return assigner

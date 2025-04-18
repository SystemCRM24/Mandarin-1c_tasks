from datetime import datetime, timedelta
import asyncio
import aiocache

from api.v2 import constants
from api.v2.schemas import front
from api.v2.bitrix import requests, schedule
from api.v2.service.funcs import get_bxtasks_from_user, get_bxtask_from_id, BXTask
from api.v2.utils import log_exception


async def fetch_websocket_message() -> front.WebSocketMessageSchema:
    data = await fetch_websocket_data()
    return front.WebSocketMessageSchema(
        meta='data',
        content=data
    )


async def fetch_websocket_data() -> front.WebSocketDataSchema:
    now = datetime.now(constants.MOSCOW_TZ)
    resources_dct = await get_resources()
    start, end, tasks = await get_tasks(resources_dct)
    if start is None:
        start = now
    if end is None:
        end = now
    interval = await generate_total_range(start, end)
    ranges = await generate_workdate_ranges(interval)
    return front.WebSocketDataSchema(
        interval=interval,
        workIntervals=ranges,
        resources=list(resources_dct.values()),
        tasks=tasks
    )


async def get_resources() -> dict[str, front.ResourceSchema]:
    """Возвращает дочерние подразделения для Производства"""
    departments: list[dict] = await requests.get_departments_info(key=None)
    production_childs = {}
    coros = []
    for department in departments:
        parent_id = department.get('PARENT', '')
        if parent_id == constants.DEPARTMENT_ID:
            department_id = int(department['ID'])
            production_childs[department_id] = department['NAME']
            coros.append(requests.get_users_by_department(department_id))
    users_by_department: list[list[dict]] = await asyncio.gather(*coros)
    resources = {}
    for department in users_by_department:
        for user in department:
            main_department = user.get('UF_DEPARTMENT')[0]
            department_name = production_childs.get(main_department, None)
            if department_name is None:
                continue
            user_id = user.get('ID', None)
            resources[user_id] = front.ResourceSchema(
                id=user_id,
                department=main_department,
                label=f'{department_name}: {user.get('NAME', '')} {user.get('LAST_NAME', '')}'
            )
    return resources


async def get_tasks(resources: dict[str, front.ResourceSchema]) -> tuple[str, str, list[front.TaskSchema]]:
    """Возвращает задачи и соответствующие крайние даты"""
    coros = (get_bxtasks_from_user(user_id) for user_id in resources)
    tasks_by_user = await asyncio.gather(*coros)
    tasks = []
    first_task_start = last_task_end = None
    for user_tasks in tasks_by_user:
        last_task: front.TaskSchema = None
        for task in user_tasks:
            if first_task_start is None or first_task_start > task.start_date_plan:
                first_task_start = task.start_date_plan
            if last_task_end is None or last_task_end < task.end_date_plan:
                last_task_end = task.end_date_plan
            task_obj = front.TaskSchema(
                id=task.id,
                label=task.title.split(' ')[-1],
                resourceId=task.responsible_id,
                deadline=task.deadline,
                time=front.IntervalSchema(
                    start=task.start_date_plan,
                    end=task.end_date_plan
                )
            )
            tasks.append(task_obj)
    return first_task_start, last_task_end, tasks


async def generate_total_range(start: datetime, end: datetime) -> front.IntervalSchema:
    """
    Округляет старт и энд до первой и последней секунды в неделе.
    Дополнительно прибавляет неделю, если end - пятница, суббота или воскресенье.
    """
    to_subtract = start.weekday()
    start_of_week = (start - timedelta(days=to_subtract)).replace(hour=0, minute=0, second=0)
    # Энд округляем в потолок
    end_weekday = end.weekday()
    to_add = 6 - end_weekday
    end_of_week = (end + timedelta(days=to_add + 14)).replace(hour=23, minute=59, second=59)
    return front.IntervalSchema(start=start_of_week, end=end_of_week)


wd_ranges_cache = aiocache.cached(ttl=60 * 60 * 24, namespace="wd_ranges")

@wd_ranges_cache
async def generate_workdate_ranges(interval: front.IntervalSchema) -> list[front.IntervalSchema]:
    """Генерирует рабочие промежутки."""
    main_schedule: schedule.Schedule = await schedule.from_bitrix_schedule()
    ranges = []
    day = interval.start + main_schedule.work_time_start
    interval_end = interval.end
    while day < interval_end:
        if main_schedule.is_working_time(day):
            ranges.append(
                front.IntervalSchema(
                    start=day,
                    end=day + main_schedule.work_day_duration
                )
            )
        day += timedelta(days=1)
    return ranges


async def update_from_front_task(json_string: str):
    try:
        task = front.FromFrontTaskSchema.model_validate_json(json_string)
        bxtask: BXTask = await get_bxtask_from_id(task.id)
        bxtask.responsible_id = task.resourceId
        bxtask.start_date_plan = task.time.start.astimezone(constants.MOSCOW_TZ)
        bxtask.end_date_plan = task.time.end.astimezone(constants.MOSCOW_TZ)
        await bxtask.update()
    except Exception as exc:
        asyncio.create_task(log_exception(exc, "frontend_update_from_websocket"))

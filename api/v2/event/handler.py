from api.v2.bitrix.task import BXTask
from api.v2.bitrix.schedule import Schedule, from_bitrix_schedule
from ..service.funcs import tasks_cache, get_bxtask_from_id, get_bxtasks_from_user
from api.v2.utils import uvicorn_logger


async def task_update_handler(task_id: str):
    await clear_cache(task_id)
    task = await get_bxtask_from_id(task_id)
    if task is None:
        uvicorn_logger.info(f'Task={task_id} is not valid.')
        return
    user_tasks = await get_bxtasks_from_user(task.responsible_id)
    schedule: Schedule = await from_bitrix_schedule()
    normalize(schedule, user_tasks)
    for task in user_tasks:
        if task._updated:
            uvicorn_logger.info(f'Task={task.id} was normalize.')
        await task.update()


def normalize(schedule: Schedule, tasks: list[BXTask]):
    """Нормализует время в задачах, если это необходимо"""
    for index, task in enumerate(tasks):
        if index == 0:
            start_date_plan = task.start_date_plan
        else:
            prev_task = tasks[index - 1]
            start_date_plan = prev_task.end_date_plan
        task.start_date_plan = schedule.get_nearest_datetime(start_date_plan)
        time_estimate = schedule.get_duration(task.start_date_plan, task.end_date_plan)
        task.time_estimate = int(time_estimate.total_seconds())
        task.end_date_plan = schedule.add_duration(task.start_date_plan, time_estimate)


async def clear_cache(task_id: str) -> bool:
    """Чистит кеш от задачи, если она там есть"""
    k: str = tasks_cache.get_cache_key(get_bxtask_from_id, (task_id, ), {})
    if await tasks_cache.cache.exists(key=k):
        await tasks_cache.cache.delete(k)
        return True
    return False

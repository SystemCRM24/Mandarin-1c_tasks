from datetime import datetime, timedelta
import aiocache

from api.v3.bitrix.pool import Pool
from api.v3.schemas import front
from api.v3 import constants


POOL = Pool()


async def fetch_websocket_message() -> front.DataSchema:
    now = datetime.now(constants.MOSCOW_TZ)
    pool_tasks = await POOL.get_tasks()
    start, end, tasks = fetch_tasks(pool_tasks)
    if start is None:
        start = now
    if end is None:
        end = now
    interval = generate_total_range(start, end)
    ranges = await generate_workdate_ranges(interval)
    resources = fetch_resources()
    content = front._DataSchema(
        interval=interval,
        workIntervals=ranges,
        resources=resources,
        tasks=tasks
    )
    return front.DataSchema(content=content)


def fetch_resources() -> list[front.ResourceSchema]:
    resources: list[front.ResourceSchema] = []
    for user in POOL._responsibles.values():
        department = user['DEPARTMENT']
        label = f'{department['NAME']}: {user['NAME']}'
        if user['LAST_NAME']:
            label += f' {user['LAST_NAME']}'
        resource = front.ResourceSchema(id=user['ID'], label=label, department=department['ID'])
        resources.append(resource)
    resources.sort(key=lambda r: r.department)
    return resources


def fetch_tasks(pool_tasks) -> tuple[datetime, datetime, list[front.TaskSchema]]:
    tasks = []
    first_start = last_end = None
    for task in pool_tasks.values():
        if first_start is None or first_start > task.start_date_plan:
            first_start = task.start_date_plan
        if last_end is None or last_end < task.end_date_plan:
            last_end = task.end_date_plan
        task_schema = front.TaskSchema(
            id=task.id,
            label=task.title,
            resourceId=task.responsible_id,
            deadline=task.deadline,
            description=task.description,
            time=front.IntervalSchema(
                start=task.start_date_plan,
                end=task.end_date_plan
            )
        )
        tasks.append(task_schema)
    return first_start, last_end, tasks


def generate_total_range(start: datetime, end: datetime) -> front.IntervalSchema:
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
    pool = Pool()
    ranges = []
    day = interval.start + pool._schedule.work_time_start
    interval_end = interval.end
    while day < interval_end:
        if pool._schedule.is_working_time(day):
            ranges.append(
                front.IntervalSchema(
                    start=day,
                    end=day + pool._schedule.work_day_duration
                )
            )
        day += timedelta(days=1)
    return ranges

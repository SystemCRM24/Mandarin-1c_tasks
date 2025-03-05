from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .bitrix import requests, schedule
from .schemas.front import IntervalSchema, WebSocketSchema


async def fetch_websocket_data() -> WebSocketSchema:
    """Получает данные для отправки по websocket-соединению"""
    departments = await get_departments()
    staff = await get_staff(departments)
    tasks, first_task_start, last_task_end = await get_tasks(staff)
    interval = await generate_total_range(first_task_start, last_task_end)
    work_intervals = await generate_workdate_ranges(interval)
    return WebSocketSchema(
        departments=departments,
        staff=staff,
        tasks=tasks,
        interval=interval,
        workIntervals=work_intervals,
        now=datetime.now(ZoneInfo('Europe/Moscow'))
    )

async def get_departments() -> dict:
    """Возвращает подразделения"""
    all_departments = await requests.get_departments_info()
    return {d.ID: d for d in all_departments if d.PARENT == '29'}


async def get_staff(departments: dict) -> dict:
    """Возвращает персонал"""
    staff = {}
    for department_id in departments.keys():
        response = await requests.get_staff_from_department_id(department_id)
        for user in response:
            staff[user.ID] = user
    return staff


async def get_tasks(staff: dict) -> tuple[str, str, dict]:
    """Возвращает задачи и соответствующие крайние даты"""
    tasks_data = await requests.get_staff_tasks(staff.values())
    tasks = {}
    first_task_start = last_task_end = None
    for task_group in tasks_data:
        for task in task_group:
            tasks[task.id] = task
            if first_task_start is None or first_task_start > task.startDatePlan:
                first_task_start = task.startDatePlan
            if last_task_end is None or last_task_end < task.endDatePlan:
                last_task_end = task.endDatePlan
    return tasks, first_task_start, last_task_end


async def generate_total_range(start: datetime, end: datetime) -> IntervalSchema:
    """Округляет старт и энд до первой и последней секунды в неделе"""
    # Старт округляем в пол
    to_subtract = start.weekday()
    start_of_week = (start - timedelta(days=to_subtract)).replace(hour=0, minute=0, second=0)
    # Энд округляем в потолок
    to_add = 6 - end.weekday()
    end_of_week = (end + timedelta(days=to_add)).replace(hour=23, minute=59, second=59)
    return IntervalSchema(start=start_of_week, end=end_of_week)


async def generate_workdate_ranges(interval: IntervalSchema) -> list[IntervalSchema]:
    """Генерирует робочие промежутки."""
    main_schedule = schedule.BXSchedule()
    await main_schedule.update_from_bxschedule(1)   # ИД основного расписания
    ranges = []
    day = interval.start
    interval_end = interval.end
    while day < interval_end:
        if main_schedule.is_working_day(day):
            ranges.append(
                IntervalSchema(
                    start=day + main_schedule.work_time_start,
                    end=day + main_schedule.work_time_end
                )
            )
        day += timedelta(days=1)
    return ranges

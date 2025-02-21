import aiocache
from . import requests
from datetime import datetime, timedelta

    

class BXSchedule:
    """За битрикс реализуем рабочий календарь"""

    def __init__(self):
        self.schedule_id: str | int | None = None
        self.exclusions = set(("01.01", "02.01", "07.01", "23.02", "08.03", "01.05", "09.05", "12.06", "04.11"))
        self.work_days = '12345'
        self.work_time_start = timedelta(seconds=32_400)
        self.work_time_end = timedelta(seconds=64_800)
        self.work_day_duration = timedelta(seconds=32_400)

    async def update_from_bxschedule(self, id: str | int = 1):
        """Корректирует объкт расписания на основе инфы из битрикса"""
        schedule: dict = await get_schedule_info(id)
        for attr in self.__dict__:
            value = schedule.get(attr, None)
            if value is not None:
                setattr(self, attr, value)
    
    def is_working_day(self, date: datetime) -> bool:
        """
        Проверяет, что переданный datetime - рабочий день. Учитывает праздники и выходные дни.
        Проверка проходит только на уровне дней.
        """
        date_repr = date.strftime(r"%d.%m")
        if date_repr in self.exclusions:
            return False
        day_number = date.strftime("%w")
        return day_number in self.work_days


@aiocache.cached(ttl=60 * 60 * 24, namespace="work_schedule")
async def get_schedule_info(id: str | int = 1) -> dict:
    """
    Получает информацию по указанному расписанию и возвращает ее в виде словаря, 
    где имена ключей соответствуют атрибутам BXSchedule
    """
    schedule_data = await requests.get_work_schedule(id)
    # Дополнительные выходные
    exclusions = set()
    current_calendar = schedule_data.get("EXCLUSIONS", {})
    exclusions_data = current_calendar.get("EXCLUSIONS", {})
    for _, months in exclusions_data.items():
        for month, days in months.items():
            for day, value in days.items():
                if value == "0":  # Выходной
                    exclusions.add(f"{day.zfill(2)}.{month}")
    # Рабочий день
    work_days = work_time_start = work_time_end = work_day_duration = None
    try:
        shifts = schedule_data["SHIFTS"][0]
        work_days = shifts["WORK_DAYS"]
        work_time_start = timedelta(seconds=shifts["WORK_TIME_START"])
        work_time_end = timedelta(seconds=shifts["WORK_TIME_END"])
        work_day_duration = work_time_end - work_time_start
    except:
        pass
    return {
        'exclusions': exclusions,
        'work_days': work_days,
        'work_time_start': work_time_start,
        'work_time_end': work_time_end,
        'work_day_duration': work_day_duration
    }
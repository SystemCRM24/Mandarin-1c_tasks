import asyncio
from datetime import datetime, timedelta
from .requests import get_work_schedule
    

class BXCalendar:
    """За битрикс реализуем рабочий календарь"""
    # Инстансы объектов-календарей расписаний.
    _instances = {}
    # Типизация
    schedule_id: str | int | None      # ид расписания
    exclusions: set                    # Праздники и нерабочие дни
    work_days: str                     # Номера рабочих дней в неделе
    work_time_start: timedelta         # Начало рабочего дня
    work_time_end: timedelta           # Конец рабочего дня
    work_day_duration: timedelta       # Продолжительность рабочего дня

    @classmethod
    def for_schedule(cls, schedule_id: str | int = '1'):
        """Создает календарь для указанного расписания"""
        instance = cls._instances.get(schedule_id, None)
        if instance is not None:
            instance['count'] += 1
            return instance['calendar']
        instance = cls._instances[schedule_id] = {'calendar': cls(), 'count': 1}
        calendar = instance['calendar']
        calendar.schedule_id = schedule_id
        # Обновление 
        event_loop = asyncio.get_running_loop()
        schedule_data: dict = event_loop.run_until_complete(get_work_schedule(schedule_id))
        # Дополнительные выходные
        current_calendar = schedule_data.get("EXCLUSIONS", {})
        exclusions = current_calendar.get("EXCLUSIONS", {})
        for _, months in exclusions.items():
            for month, days in months.items():
                for day, value in days.items():
                    if value == "0":  # Выходной
                        calendar.exclusions.add(f"{day.zfill(2)}.{month}")
        # Рабочий день
        try:
            shifts = schedule_data["SHIFTS"][0]
            calendar.work_days = shifts["WORK_DAYS"]
            calendar.work_time_start = timedelta(seconds=shifts["WORK_TIME_START"])
            calendar.work_time_end = timedelta(seconds=shifts["WORK_TIME_END"])
            calendar.work_day_duration = timedelta(seconds=shifts["WORK_TIME_END"] - shifts["WORK_TIME_START"] - shifts["BREAK_DURATION"])
        except:
            pass
        return calendar

    def __init__(self):
        self.schedule_id = None
        self.exclusions = set(("01.01", "02.01", "07.01", "23.02", "08.03", "01.05", "09.05", "12.06", "04.11"))
        self.work_days = '12345'
        self.work_time_start = timedelta(seconds=32_400)
        self.work_time_end = timedelta(seconds=64_800)
        self.work_day_duration = timedelta(seconds=28_800)

    def __del__(self):
        if self.schedule_id is not None:
            instance = BXCalendar._instances[self.schedule_id]
            instance['count'] -= 1
            if instance['count'] == 0:
                del BXCalendar._instances[self.schedule_id]
        return super().__del__()

    def is_working_day(self, date: datetime) -> bool:
        """Проверяет, что этот день рабочий. True - да"""
        date_repr = date.strftime(r"%d.%m")
        if date_repr in self.exclusions:
            return False
        day_number = date.strftime("%w")
        return day_number in self.work_days

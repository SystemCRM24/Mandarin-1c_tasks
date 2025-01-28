from datetime import datetime, timedelta

from src.bitrix.requests import get_work_schedule

# Момент, который пришлось жестко прописать
# Если изменятся графики для подразделений, то их стоит прописать тут.
SCHEDULE = {"Основной": "1"}
HOLIDAYS = set(["01.01", "02.01", "07.01", "23.02", "08.03", "01.05", "09.05", "12.06", "04.11"])


class Calendar:
    """За битрикс реализуем рабочий календарь"""

    def __init__(self, position: str):
        self.position = position
        self.exclusions = set()
        self.work_days = "12345"
        self.work_time_start = timedelta(seconds=32_400)  # 9 утра
        self.work_time_end = timedelta(seconds=64_800)  # 18 вечера
        self.work_day_duration = timedelta(seconds=28_800)  # 8 часов

    async def update(self):
        """Обновляет календарь, наделяет его информацией о праздниках, выходных днях и т.п."""
        schedule_id = SCHEDULE.get(self.position, "1")
        schedule: dict = await get_work_schedule(schedule_id)
        # Дополнительные выходные
        current_calendar = schedule.get("EXCLUSIONS", {})
        exclusions = current_calendar.get("EXCLUSIONS", {})
        for year, months in exclusions.items():
            for month, days in months.items():
                for day, value in days.items():
                    if value == "0":  # Выходной
                        self.exclusions.add(f"{day.zfill(2)}.{month}")
        # Рабочий день
        try:
            shifts = schedule["SHIFTS"][0]
            self.work_days = shifts["WORK_DAYS"]
            self.work_time_start = timedelta(seconds=shifts["WORK_TIME_START"])
            self.work_time_end = timedelta(seconds=shifts["WORK_TIME_END"])
            self.work_day_duration = timedelta(
                seconds=shifts["WORK_TIME_END"] - shifts["WORK_TIME_START"] - shifts["BREAK_DURATION"]
            )
        except:
            pass

    def is_working_day(self, date: datetime) -> bool:
        """Проверяет, что этот день рабочий. True - да"""
        date_repr = date.strftime(r"%d.%m")
        if date_repr in HOLIDAYS or date_repr in self.exclusions:
            return False
        day_number = date.strftime("%w")
        return day_number in self.work_days

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
# from api.v2.utils import uvicorn_logger


COMMON_HOLIDAYS = set(("01.01", "02.01", "07.01", "23.02", "08.03", "01.05", "09.05", "12.06", "04.11"))


class Schedule:
    """За битрикс реализуем рабочий календарь"""

    def __init__(self):
        self.exclusions = COMMON_HOLIDAYS.copy()
        self.work_days = '12345'
        self.work_time_start = timedelta(seconds=32_400)
        self.work_time_end = timedelta(seconds=64_800)
        self.work_day_duration = timedelta(seconds=32_400)
    
    @staticmethod
    def split_timedelta(td: timedelta) -> tuple[int, int, int]:
        """
        Разбивает объект timedelta на часы, минуты и секунды.
        Если присутсвуют микросекунды, то они будут отброшены.
        """
        seconds_in_delta = int(td.total_seconds())
        hours = seconds_in_delta // 3600
        minutes = (seconds_in_delta % 3600) // 60
        seconds = seconds_in_delta % 60
        return hours, minutes, seconds
    
    def is_working_time(self, dt: datetime) -> bool:
        """
        Проверяет, что переданный объект datetime находится в промежутках рабочего времени.
        """
        if dt.strftime(r"%d.%m") in self.exclusions:
            return False
        if dt.strftime("%w") not in self.work_days:
            return False
        time_from_dt = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        return self.work_time_start <= time_from_dt < self.work_time_end

    def get_nearest_datetime(self, dt: datetime) -> datetime:
        """Получает ближайшеий объект datetime, который находится в промежутке рабочего времени, к указанному dt"""
        if self.is_working_time(dt):
            return dt
        hour, minute, second = self.split_timedelta(self.work_time_start)
        dt = dt.replace(hour=hour, minute=minute, second=second) + timedelta(days=1)
        while not self.is_working_time(dt):
            dt += timedelta(days=1)
        return dt

    def _add_duration(self, start: datetime, duration: int | timedelta) -> datetime:
        """Прибавляет к start duration - время в секундах (или готовый объект timedelta) c учетом рабочего времени."""
        if isinstance(duration, (int, float)):
            duration = timedelta(seconds=duration)
        dt = self.get_nearest_datetime(start)
        # Различное черное колдунство с датами.
        wd_duration = int(self.work_day_duration.total_seconds())
        duration_by_seconds = int(duration.total_seconds())
        wd_in_duration = duration_by_seconds // wd_duration     # полных рабочих дней
        remains = duration_by_seconds % wd_duration             # остаток
        remains_td = timedelta(seconds=remains)
        dt_delta = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        total_delta = dt_delta + remains_td
        dt += remains_td
        # Отнимаем секунду, чтобы прошла проверка. 
        if total_delta == self.work_time_end:
            dt -= timedelta(seconds=1)
        if total_delta > self.work_time_end:
            dt = self.get_nearest_datetime(dt) + (total_delta - self.work_time_end)  
        # Прибавляем дни по рабочим часам
        while wd_in_duration:
            dt += timedelta(days=1)
            if self.is_working_time(dt):
                wd_in_duration -= 1
        # возрващаем отнятую секунду
        if total_delta == self.work_time_end:
            dt += timedelta(seconds=1)
        return dt
    
    def add_duration(self, start: datetime, duration: int | timedelta) -> datetime:
        """
        Прибавляет к start duration - время в секундах (или готовый объект timedelta) c учетом рабочего времени.
        Если результат равен 9:00, то откатывает до 18:00 предыдущего рабочего дня.
        """
        result = self._add_duration(start, duration)
        result_delta = timedelta(hours=result.hour, minutes=result.minute, seconds=result.second)
        if result_delta == self.work_time_start:
            while True:
                result -= timedelta(days=1)
                if self.is_working_time(result):
                    break
            hour, minute, second = self.split_timedelta(self.work_time_end)
            result = result.replace(hour=hour, minute=minute, second=second)
        return result
    
    def get_duration(self, start: datetime, end: datetime) -> timedelta:
        """Высчитывает продолжительность рабочего времени между start и end"""
        minute = timedelta(minutes=1)
        duration = timedelta(minutes=0)
        while start < end:
            if self.is_working_time(start):
                duration += minute
            start += minute
        return duration


sc = Schedule()

start = datetime.fromisoformat('2025-03-21T09:00:00.000000+03:00')
end = datetime.fromisoformat('2025-03-21T18:00:00.000000+03:00')

dn = sc.get_duration(start, end)
print(sc.add_duration(start, dn))
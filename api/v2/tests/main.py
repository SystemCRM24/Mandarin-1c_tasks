from zoneinfo import ZoneInfo
from datetime import datetime


MOSCOW_TZ = ZoneInfo('Europe/Moscow')


now = datetime.now(MOSCOW_TZ)

print(type(MOSCOW_TZ.utcoffset(now)))
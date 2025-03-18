from zoneinfo import ZoneInfo
from datetime import datetime


MOSCOW_TZ = ZoneInfo('Europe/Moscow')


now = datetime.now(MOSCOW_TZ)

print(now.date(), str(now.time())[:8])
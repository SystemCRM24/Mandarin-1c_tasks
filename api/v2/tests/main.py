from datetime import datetime
from zoneinfo import ZoneInfo


d = datetime.fromisoformat('2025-03-19T09:30:00.000Z')
d = d.astimezone(ZoneInfo('Europe/Moscow'))
print(d)
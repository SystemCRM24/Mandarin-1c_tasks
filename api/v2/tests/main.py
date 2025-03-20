from datetime import datetime
from zoneinfo import ZoneInfo


d = datetime.now() - datetime.now()
print(d.total_seconds())
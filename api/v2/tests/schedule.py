from pathlib import Path
import sys

p = Path(__file__).parent.parent.parent.parent
sys.path.append(str(p))


from datetime import datetime
from zoneinfo import ZoneInfo
from api.v2.bitrix.schedule import Schedule


sc = Schedule()

start = datetime.fromisoformat('2025-04-07T10:09:00+03:00')
end = datetime.fromisoformat('2025-04-08T17:29:00+03:00')

print(end - start)

wt_duration = sc.get_duration(start, end)
print(wt_duration)


# nearest = sc.get_nearest_datetime(start1)
# print(nearest)

# result = sc.add_duration(nearest, duration)
# print(result)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


start = datetime.fromisoformat('2025-03-18 12:10:36.280473+03:00')
end = datetime.fromisoformat('2025-03-24 12:10:36.280473+03:00')

to_subtract = start.weekday()
start_of_week = (start - timedelta(days=to_subtract)).replace(hour=0, minute=0, second=0)
# Энд округляем в потолок
end_weekday = end.weekday()
to_add = 6 - end_weekday
if end_weekday in (4, 5, 6):
    to_add += 7
end_of_week = (end + timedelta(days=to_add)).replace(hour=23, minute=59, second=59)
print(start_of_week, end_of_week, sep='\n')
# return front.IntervalSchema(start=start_of_week, end=end_of_week)
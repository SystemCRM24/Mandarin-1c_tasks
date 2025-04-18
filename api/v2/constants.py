from dotenv import dotenv_values
from zoneinfo import ZoneInfo
from aiocache import Cache
from asyncio import Event, Queue


_values = dotenv_values()


# Константы из виртуального окружения
BITRIX_WEBHOOK = _values.get('BITRIX_WEBHOOK')
DIRECTOR_ID = _values.get('DIRECTOR_ID')
ONEC_GROUP_ID = _values.get('ONEC_GROUP_ID')
UPLOAD_DIR_ID = _values.get('UPLOAD_DIR_ID')
SCHEDULE_ID = _values.get('SCHEDULE_ID')
DEPARTMENT_ID = _values.get('DEPARTMENT_ID')
TIMEZONE_COMPENSATION = _values.get('TIMEZONE_COMPENSATION') != '0'


# Остальное
MOSCOW_TZ = ZoneInfo('Europe/Moscow')
CACHE = Cache()
EVENT = Event()     # Отслеживание изменений для фронта
QUEUE = Queue()     # Очередь для работы с событиями из битрикса.

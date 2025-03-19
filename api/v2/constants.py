from os import environ
from zoneinfo import ZoneInfo
from aiocache import Cache
import asyncio


# Проверка на виртуальное окружение
if environ.get('BITRIX_WEBHOOK') is None:
    import dotenv
    dotenv.load_dotenv()

# Константы из виртуального окружения
BITRIX_WEBHOOK = environ.get('BITRIX_WEBHOOK')
DIRECTOR_ID = environ.get('DIRECTOR_ID')
ONEC_GROUP_ID = environ.get('ONEC_GROUP_ID')
UPLOAD_DIR_ID = environ.get('UPLOAD_DIR_ID')
SCHEDULE_ID = environ.get('SCHEDULE_ID')
DEPARTMENT_ID = environ.get('DEPARTMENT_ID')
TIMEZONE_COMPENSATION = bool(environ.get('TIMEZONE_COMPENSATION'))


# Остальное
MOSCOW_TZ = ZoneInfo('Europe/Moscow')
CACHE = Cache()
EVENT = asyncio.Event()     # Отслеживание изменений для фронта
QUEUE = asyncio.Queue()     # Очередь для работы с событиями из битрикса.

from dotenv import dotenv_values
from zoneinfo import ZoneInfo
from asyncio import Event, Queue
from fastapi import WebSocket


_values = dotenv_values()


# Константы из виртуального окружения
BITRIX_WEBHOOK = _values.get('BITRIX_WEBHOOK')
DIRECTOR_ID = _values.get('DIRECTOR_ID')
ONEC_GROUP_ID = _values.get('ONEC_GROUP_ID')
UPLOAD_DIR_ID = _values.get('UPLOAD_DIR_ID')
SCHEDULE_ID = _values.get('SCHEDULE_ID')
DEPARTMENT_ID = _values.get('DEPARTMENT_ID')


# Остальное
MOSCOW_TZ = ZoneInfo('Europe/Moscow')
CONNECTIONS: set[WebSocket] = set()     # Подключения к front
QUEUE = Queue()                         # Очередь для работы с событиями из битрикса.
START_SYNC = Event()                    # Сигнал о начале синхронизации бассейна
END_SYNC = Event()                      # Сигнал об окончании синхронизации бассейна
DATA_EVENT = Event()                    # Сигнал на отправку данных на фронт
TO_AVOID: dict[str, int] = {}
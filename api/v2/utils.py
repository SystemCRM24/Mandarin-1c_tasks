import logging
from datetime import datetime
import traceback

from .constants import MOSCOW_TZ


debug_logger = logging.getLogger("debug_logger")
debug_logger.setLevel(logging.DEBUG)
debug_logger.handlers = [logging.FileHandler("logs/debug.log", encoding="utf-8")]

separator = '---------- {0} ----------'


async def log_exception(e: Exception):
    """Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    debug_logger.info(separator.format(datetime.now(tz=MOSCOW_TZ)))
    for frame in traceback.format_exception(e):
        debug_logger.info(frame[:-1])

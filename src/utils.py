import logging
from datetime import datetime


debug_logger = logging.getLogger("debug_logger")
debug_logger.setLevel(logging.INFO)
debug_logger.handlers = [logging.FileHandler("logs/create_task.log", encoding="utf-8")]

separator = '---------- {0} ----------'


async def log_error(e, info=None):
    """Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    debug_logger.info(separator.format(datetime.now()))
    debug_logger.error(e, exc_info=True, stack_info=True)
    if info:
        debug_logger.info(str(info))

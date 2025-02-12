import logging
from datetime import datetime


async def log_error(e, info=None):
    """Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    logger = logging.getLogger("debug_logger")
    logger.setLevel(logging.INFO)
    logger.handlers = [logging.FileHandler("log.log", encoding="utf-8")]
    logger.info("-----" * 6)
    logger.info(str(datetime.now()))
    if info:
        logger.info(str(info))
    logger.error(e, exc_info=True)

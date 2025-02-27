import logging
from datetime import datetime
from pydantic import BaseModel


debug_logger = logging.getLogger("debug_logger")
debug_logger.setLevel(logging.DEBUG)
debug_logger.handlers = [logging.FileHandler("logs/debug.log", encoding="utf-8")]

separator = '---------- {0} ----------'


async def debug_log(e: Exception):
    """Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    debug_logger.info(separator.format(datetime.now()))
    debug_logger.exception(e.with_traceback())


async def log_schema(schema: BaseModel):
    """Записывает в файл схему"""
    filename = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S-%f')
    json_string = schema.model_dump_json(indent=4)
    with open(f'logs/{filename}.json', 'w') as file:
        file.write(json_string)

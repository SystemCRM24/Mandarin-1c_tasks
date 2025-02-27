import logging
from datetime import datetime
from pydantic import BaseModel
import traceback
import json


debug_logger = logging.getLogger("debug_logger")
debug_logger.setLevel(logging.DEBUG)
debug_logger.handlers = [logging.FileHandler("logs/debug.log", encoding="utf-8")]

separator = '---------- {0} ----------'


ct_logger = logging.getLogger('main_logger')
ct_logger.setLevel(logging.DEBUG)
ct_logger.handlers = [logging.FileHandler("logs/ct_responses.log", encoding="utf-8")]


async def log_exception(e: Exception):
    """Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    debug_logger.info(separator.format(datetime.now()))
    for frame in traceback.format_exception(e):
        debug_logger.info(frame[:-1])


async def log_create_task_response(obj):
    """Логгирует ответ от приложения на создание задачи"""
    ct_logger.info(separator.format(datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S-%f')))
    ct_logger.info(json.dumps(obj, indent=4))


async def log_schema(schema: BaseModel):
    """Записывает в файл схему"""
    filename = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S-%f')
    json_string = schema.model_dump_json(indent=4)
    with open(f'logs/{filename}.json', 'w') as file:
        file.write(json_string)

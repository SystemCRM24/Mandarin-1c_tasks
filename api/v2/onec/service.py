from datetime import datetime
import logging
import asyncio
from .file import Uploader
from .task import TaskHandler
from ..schemas.onec import OrderSchema, ResponseItemSchema


onec_logger = logging.getLogger('onec_logger')
onec_logger.setLevel(logging.DEBUG)
onec_logger.handlers = [logging.FileHandler("logs/onec.log", encoding="utf-8")]

separator = '---------- {0} ----------'


def create_tasks_coros(order: OrderSchema, uploader: Uploader):
    """Генератор который возвращает корутины для постановки задач"""
    for calculation in order.calculation:
        handler = TaskHandler(order, calculation, uploader)
        yield handler.put()

 
async def log_request(filename: str, order: OrderSchema, uploader: Uploader):
    """Записывает в файл схему"""
    json_string = order.model_dump_json(indent=2)
    with open(f'logs/{filename}.json', 'w') as file:
        file.write(json_string)


async def log_response(filename: str, response: list[ResponseItemSchema]):
    """Логгирует ответ по постановке задачи"""
    onec_logger.info(separator.format(filename))
    for model in response:
        json_string = model.model_dump_json(indent=2)
        onec_logger.info(json_string)
    

def log_info(order: OrderSchema, uploader: Uploader, response: list[ResponseItemSchema]):
    """Логгирует шизу Мандарина. Закидывает соответствующие задачки в фон"""
    now = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S')
    filename = f'{now}_{order.name}'
    asyncio.create_task(log_request(filename, order, uploader))
    asyncio.create_task(log_response(filename, response))

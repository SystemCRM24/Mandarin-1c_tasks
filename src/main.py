from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from schemas import OrderSchema
from bitrix.task import Task, UpdateTaskException
from bitrix.file import Files
import asyncio

# Для дебага
import logging
from datetime import datetime

logger = logging.getLogger('debug_logger')
logger.setLevel(logging.INFO)
logger.handlers = [logging.FileHandler('log.log', encoding='utf-8')]


app = FastAPI(
    title='Постановка задач',
    description='Автоматическая постановка задач для Битрикс24 компании Мандарин на основе POST-запроса.'
)


@app.get("/ping/", status_code=200)
async def ping():
    """Пингует сервер"""
    return {'message': 'Pong'}


@app.post("/", status_code=200)
async def create_tasks(order: OrderSchema):
    """Создание задач"""
    files = Files(order.attached_files)
    tasks = (Task(order, td, files).put_task() for td in order.calculation)
    try:
        await asyncio.gather(files.upload(), *tasks)
        return {'message': 'ok'}
    except Exception as e:
        logger.info('-----' * 6)
        logger.info(str(datetime.now()))
        logger.info(str(order))
        logger.error(e, stack_info=True)
        if isinstance(e, UpdateTaskException):
            return {'message': 'При обновлении задачи произошла ошибка. Скорее всего, некоторые данные в задаче были обновлены, но что-то пошло не так.'}
        raise HTTPException(500, detail=str(e))


# uvicorn main:app --host 0.0.0.0 --port 80
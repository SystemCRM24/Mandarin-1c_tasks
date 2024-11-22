from fastapi import FastAPI
from schemas import OrderSchema
from bitrix.task import Task
from bitrix.file import Files
import asyncio


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
    await asyncio.gather(files.upload(), *tasks)
    return {'message': 'success'}


# uvicorn main:app --host 0.0.0.0 --port 80
import asyncio

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.bitrix.file import FileUploader
from src.bitrix.task import Task, UpdateTaskException
from src.bitrix import requests

from src.schemas import OrderSchema, UpdateTaskSchema
from src.utils import log_error
from src.service import fetch_websocket_data
from src.websocket import ws_router, UPDATE_EVENT


app = FastAPI(
    title="Постановка задач",
    description="Автоматическая постановка задач для Битрикс24 компании Мандарин на основе POST-запроса.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)


@app.get("/ping", status_code=200, tags=['1c'])
async def ping():
    """Пингует сервер"""
    return {"message": "Pong"}


@app.post("/create_task", status_code=200, tags=['1c'])
async def create_tasks(order: OrderSchema):
    """Создание задач"""
    try:
        async with asyncio.TaskGroup() as group:
            file_handler = FileUploader(order.attached_files)
            upload_task = group.create_task(file_handler.upload())
            file_handler.atask = upload_task
            for calculation in order.calculation:
                bx_task = Task(order, calculation, file_handler)
                group.create_task(bx_task.put_task())
        return {"message": "ok"}
    except Exception as e:
        asyncio.create_task(log_error(e))
        if isinstance(e, UpdateTaskException):
            return {"message": "Ошибка при обновлении задачи. Некоторые данные могли не сохраниться."}
        raise HTTPException(500, detail=str(e))
    

@app.get("/fetch_data", tags=['Front'])
async def fetch_data():
    """Тестирование корректности отправляемых данных"""
    return await fetch_websocket_data()


@app.get('/trigger_event', tags=['Front'])
async def trigger_event():
    """Тригеррит эвент на обновление вебсокетов"""
    UPDATE_EVENT.set()
    return {'message': 'Event triggered'}


@app.patch('/update_task/{task_id}', tags=['Front'])
async def update_task(task_id: int, data: UpdateTaskSchema):
    """Обновление задачи"""
    try:
        await requests.update_task(task_id, data.model_dump())
        msg = {"message": "ok"}
    except:
        msg = {"message": "Ошибка при обновлении задачи. Некоторые данные могли не сохраниться."}
    UPDATE_EVENT.set()
    return msg

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from bitrix.file import FileUploader
from bitrix.task import Task, UpdateTaskException
from schemas import OrderSchema

from utils import log_error
from service import fetch_websocket_data


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


@app.get("/", status_code=200, tags=['1c'])
async def ping():
    """Пингует сервер"""
    return {"message": "Pong"}


@app.post("/", status_code=200, tags=['1c'])
async def create_tasks(order: OrderSchema):
    """Создание задач"""
    try:
        async with asyncio.TaskGroup() as group:
            files = group.create_task(FileUploader(order.attached_files).upload())
            for calculation in order.calculation:
                group.create_task(Task(order, calculation, files).put_task())
        return {"message": "ok"}
    except Exception as e:
        asyncio.create_task(log_error(e, order))
        if isinstance(e, UpdateTaskException):
            return {"message": "Ошибка при обновлении задачи. Некоторые данные могли не сохраниться."}
        raise HTTPException(500, detail=str(e))


# Хранилище активных соединений
CONNECTIONS: list[WebSocket] = []
UPDATE_EVENT = asyncio.Event()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CONNECTIONS.append(websocket)
    try:
        while True:
            UPDATE_EVENT.clear()
            data = await fetch_websocket_data()
            async with asyncio.TaskGroup() as group:
                for connection in CONNECTIONS:
                    group.create_task(connection.send_json(data))
            await UPDATE_EVENT.wait();
    except WebSocketDisconnect:
        CONNECTIONS.remove(websocket)

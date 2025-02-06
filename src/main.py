import asyncio
from datetime import datetime

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from bitrix.file import Files
from bitrix.task import Task, UpdateTaskException
from schemas import OrderSchema
from src.bitrix.requests import get_work_schedule
from src.bitrix.utils.date_range import generate_date_range
from src.bitrix.utils.logger_util import log_error
from src.bitrix.utils.websocket_utils import data_validator

app = FastAPI(
    title="Постановка задач",
    description="Автоматическая постановка задач для Битрикс24 компании Мандарин на основе POST-запроса.",
)

# origins = [
#     "https://3638421-ng03032.twc1.net",
#     "http://3638421-ng03032.twc1.net",
#     "http://0.0.0.0",
#     "http://0.0.0.0:8000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Хранилище активных соединений
active_connections: list[WebSocket] = []


data_update_event = asyncio.Event()


@app.get("/ping/", status_code=200)
async def ping():
    """Пингует сервер"""
    return {"message": "Pong"}


@app.post("/", status_code=200)
async def create_tasks(order: OrderSchema):
    """Создание задач"""
    files = Files(order.attached_files)
    tasks = (Task(order, td, files).put_task() for td in order.calculation)
    try:
        await asyncio.gather(*tasks)
        return {"message": "ok"}
    except Exception as e:
        log_error(e, order)
        if isinstance(e, UpdateTaskException):
            return {
                "message": "При обновлении задачи произошла ошибка. Скорее всего, "
                "некоторые данные в задаче были обновлены, но что-то пошло не так."
            }
        raise HTTPException(500, detail=str(e))


@app.get("/worktime/", status_code=200)
async def get_work_time_periods(
    start: datetime = Query(..., description="Start time"),
    end: datetime = Query(..., description="End time"),
):
    """Отдает массив рабочих дней"""

    work_days = await get_work_schedule()
    data = generate_date_range(start, end, work_days)

    return data


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    start: datetime = Query(..., description="Start time"),
    end: datetime = Query(..., description="End time"),
):
    await websocket.accept()
    active_connections.append(websocket)

    # data_update_event.set()  # Добавить к ивентам

    data_to_send = await data_validator(start, end)

    try:
        while True:
            # Отправляем данные всем подключенным клиентам
            for connection in active_connections:
                await connection.send_json(data_to_send)

            # Сбрасываем событие
            data_update_event.clear()

            # Ожидаем следующего события
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)

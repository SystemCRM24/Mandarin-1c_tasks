"""Роутер для работы с фронт-частью приложения"""
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.service import fetch_websocket_data
from src.schemas.front import UpdateTaskSchema
from src.bitrix import requests


router = APIRouter(tags=['front'])

CONNECTIONS: set[WebSocket] = set()
UPDATE_EVENT = asyncio.Event()


async def update_event_handler():
    """Обработчик обновлений"""
    while True:
        await UPDATE_EVENT.wait()
        UPDATE_EVENT.clear()
        data = await fetch_websocket_data()
        tasks = [ws.send_json(data) for ws in CONNECTIONS]
        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.create_task(update_event_handler())



@router.patch('/update_task/{task_id}')
async def update_task(task_id: int, data: UpdateTaskSchema):
    """Обновление задачи"""
    try:
        await requests.update_task(task_id, data.model_dump())
        msg = {"message": "ok"}
    except:
        msg = {"message": "Ошибка при обновлении задачи. Некоторые данные могли не сохраниться."}
    UPDATE_EVENT.set()
    return msg


@router.websocket("/ws")
async def handle_connection(websocket: WebSocket):
    """Метод для обработки подключения"""
    await websocket.accept()
    CONNECTIONS.add(websocket)
    try:
        while True:
            data = await fetch_websocket_data()
            await websocket.send_json(data)
            await websocket.receive_text()
    except WebSocketDisconnect:
        CONNECTIONS.discard(websocket)

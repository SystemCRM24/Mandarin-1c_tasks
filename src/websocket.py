import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .service import fetch_websocket_data


ws_router = APIRouter(tags=['ws'])

CONNECTIONS: set[WebSocket] = set()
UPDATE_EVENT = asyncio.Event()


async def event_handler():
    """Обработчик обновлений"""
    while True:
        UPDATE_EVENT.clear()
        data = await fetch_websocket_data()
        tasks = [ws.send_json(data) for ws in CONNECTIONS]
        await asyncio.gather(*tasks, return_exceptions=True)
        await UPDATE_EVENT.wait()

asyncio.create_task(event_handler())


@ws_router.websocket("/ws")
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

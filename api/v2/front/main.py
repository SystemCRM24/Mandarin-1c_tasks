import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .service import fetch_websocket_data, update_from_front_task
from api.v2.constants import EVENT


router = APIRouter(prefix='/front')


CONNECTIONS: set[WebSocket] = set()


async def update_event_observer():
    """Обработчик обновлений"""
    while True:
        await EVENT.wait()
        EVENT.clear()
        data = await fetch_websocket_data()
        json_string = data.model_dump_json()
        coros = (s.send_text(json_string) for s in CONNECTIONS)
        await asyncio.gather(*coros, return_exceptions=True)

asyncio.create_task(update_event_observer())


@router.get('/fetch_data', status_code=200)
async def fetch_data():
    """Возвращает. Просто возвращает."""
    return await fetch_websocket_data()


@router.websocket('/ws')
async def handle_connection(socket: WebSocket):
    """Обработка подключений"""
    await socket.accept()
    CONNECTIONS.add(socket)
    try:
        data = await fetch_websocket_data()
        if data is None:
            await socket.close()
            raise WebSocketDisconnect
        await socket.send_text(data.model_dump_json())
        while True:
            task = await socket.receive_text()
            await update_from_front_task(task)
    except WebSocketDisconnect:
        CONNECTIONS.discard(socket)

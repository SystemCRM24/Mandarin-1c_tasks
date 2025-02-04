from typing import Any

from fastapi import WebSocket


# Функция для рассылки данных всем подключенным клиентам
async def broadcast(active_connections: list[WebSocket], data: dict[str, Any]):
    for connection in active_connections:
        await connection.send_json(data)


async def wait_for_updates(data, data_update_event, websocket: WebSocket):
    while True:
        await data_update_event.wait()
        await websocket.send_json(data)
        data_update_event.clear()

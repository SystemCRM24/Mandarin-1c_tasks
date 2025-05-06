from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .service import fetch_websocket_message
from api.v3.constants import CONNECTIONS


router = APIRouter(prefix='')


@router.websocket('/ws')
async def handle_connection(socket: WebSocket):
    """Обработка подключений"""
    await socket.accept()
    CONNECTIONS.add(socket)
    try:
        data = await fetch_websocket_message()
        await socket.send_text(data.model_dump_json())
        while True:
            await socket.receive_text()
    except WebSocketDisconnect:
        CONNECTIONS.discard(socket)

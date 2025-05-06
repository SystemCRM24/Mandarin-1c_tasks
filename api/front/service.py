from fastapi import APIRouter
import asyncio

from api.utils import log_exception
from api.v3 import constants
from api.v3.schemas.front import SyncSchema
from .funcs import fetch_websocket_message


router = APIRouter(prefix="/service")


@router.get('/fetch_data', status_code=200)
async def fetch_data():
    return await fetch_websocket_message()


@router.get('/start_sync_event', status_code=200)
async def start_sync_event():
    constants.START_SYNC.set()


@router.get('/end_sync_event', status_code=200)
async def start_sync_event():
    constants.END_SYNC.set()


async def send_message(message: str):
    """Посылает сообщения всем соединениям"""
    try:
        coros = (s.send_text(message) for s in constants.CONNECTIONS)
        await asyncio.gather(*coros)
    except Exception as exc:
        asyncio.create_task(log_exception(exc, 'send_websocker_message')) 


async def start_sync_observer():
    """Наблюдающий за началом синхронизации задач"""
    while True:
        await constants.START_SYNC.wait()
        constants.START_SYNC.clear()
        message = SyncSchema(content=True)
        await send_message(message.model_dump_json())

asyncio.create_task(start_sync_observer())


async def send_end_sync_message():
    """Посылает сообщение об окончании синхронизации"""
    try:
        await asyncio.sleep(2)
        message = SyncSchema(content=False)
        await send_message(message.model_dump_json())
    except asyncio.CancelledError:
        pass


_END_SYNC_ATASK = asyncio.create_task(send_end_sync_message())


async def end_sync_observer():
    """Наблюдающий за окончанием синхронизации задач"""
    global _END_SYNC_ATASK
    while True:
        await constants.END_SYNC.wait()
        constants.END_SYNC.clear()
        _END_SYNC_ATASK.cancel()
        _END_SYNC_ATASK = asyncio.create_task(send_end_sync_message())

asyncio.create_task(end_sync_observer())


async def data_event_observer():
    """Наблюдающий за эвентом отправки данных"""
    while True:
        await constants.DATA_EVENT.wait()
        constants.DATA_EVENT.clear()
        message = await fetch_websocket_message()
        await send_message(message.model_dump_json())

asyncio.create_task(data_event_observer())

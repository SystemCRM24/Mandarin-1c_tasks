import asyncio

from fastapi import APIRouter, Request
from api.v2.constants import QUEUE, EVENT
from api.v2.utils import log_exception
from .handler import task_update_handler


router = APIRouter(prefix='/event')


@router.post('/on_task_update', status_code=200)
async def on_task_update(request: Request):
    async with request.form() as form:
        task_id = form.get('data[FIELDS_AFTER][ID]')
    if task_id is not None:
        await QUEUE.put(task_id)
        

async def event_observer():
    """Прослушивает очередь и вызывает обработчик обновлений"""
    while True:
        task_id = await QUEUE.get()
        try:
            await task_update_handler(task_id)
        except Exception as exc:
            asyncio.create_task(log_exception(exc, "bitrix_event_observer"))
        if QUEUE.empty():
            EVENT.set()

asyncio.create_task(event_observer())

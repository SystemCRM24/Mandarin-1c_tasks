import asyncio
from fastapi import APIRouter, Request

from api.utils.loggers import uvicorn_logger
from api.utils import log_exception
from api.v3 import constants
from .pool import Pool
from .task import BXTask


router = APIRouter(prefix='/bitrix')


async def get_task_id_from_form(request: Request) -> str | None:
    async with request.form() as form:
        return form.get('data[FIELDS_AFTER][ID]', None)


async def get_bxtask_from_form(request: Request) -> tuple[str, BXTask | None]:
    """Возвращает task_id и объект задачи"""
    bxtask = None
    task_id = await get_task_id_from_form(request)
    if task_id is not None:
        bxtask = await BXTask.from_bitrix(task_id)
    return task_id, bxtask
    

@router.post('/on_task_create', status_code=200)
async def on_task_create(request: Request):
    """Ловим эвенты создания задач"""
    task_id, bxtask = await get_bxtask_from_form(request)
    if bxtask is not None:
        bxtask.mark_timestamp()
    if bxtask is None or not bxtask.is_valid():
        uvicorn_logger.info(f'-- Task id={task_id} is not valid. --')
        return
    pool = Pool()
    aiotask = asyncio.create_task(pool.add(bxtask))
    constants.QUEUE.put_nowait(aiotask)


@router.post('/on_task_update', status_code=200)
async def on_task_update(request: Request):
    """Ловим эвенты обновления задач"""
    task_id, bxtask = await get_bxtask_from_form(request)
    if bxtask is None or not bxtask.is_valid():
        uvicorn_logger.info(f'-- Task id={task_id} is not valid. --')
        return
    task_id_from_avoid = constants.TO_AVOID.get(bxtask.last_update, None)
    if task_id_from_avoid == bxtask.id:
        constants.TO_AVOID.pop(bxtask.last_update, None)
        uvicorn_logger.info(f'-- The update event for the task (id={bxtask.id}) was avoided. --')
        return
    pool = Pool()
    if bxtask.status == '5':
        aiotask = asyncio.create_task(pool.delete(task_id))
    else:
        aiotask = asyncio.create_task(pool.update(bxtask))
    constants.QUEUE.put_nowait(aiotask)


@router.post('/on_task_delete', status_code=200)
async def on_task_delete(request: Request):
    """Ловим эвенты на удаление задач"""
    task_id = await get_task_id_from_form(request)
    async with request.form() as form:
        uvicorn_logger.info(str(form))
    if task_id is None:
        return
    pool = Pool()
    aiotask = asyncio.create_task(pool.delete(task_id))
    constants.QUEUE.put_nowait(aiotask)


async def queue_observer():
    """Прослушивает очередь и вызывает обработчик обновлений"""
    while True:
        try:
            aiotask = await constants.QUEUE.get()
            if not constants.START_SYNC.is_set():
                constants.START_SYNC.set()
            await aiotask
        except Exception as exc:
            asyncio.create_task(log_exception(exc, 'bitrix_event_observer'))
        if constants.QUEUE.empty():
            constants.END_SYNC.set()
            constants.DATA_EVENT.set()

asyncio.create_task(queue_observer())

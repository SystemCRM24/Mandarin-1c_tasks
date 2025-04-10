from fastapi import APIRouter, Request

from api.utils.loggers import uvicorn_logger
from .pool import Pool


router = APIRouter(prefix='/bitrix')


@router.post('/on_task_create', status_code=200)
async def on_task_create(request: Request):
    """Ловим эвенты создания задач"""
    pass
    


@router.post('/on_task_update', status_code=200)
async def on_task_update(request: Request):
    """Ловим эвенты обновления задач"""
    form = await request.form()
    uvicorn_logger.info(str(form))
    # async with request.form() as form:
    #     task_id = form.get('data[FIELDS_AFTER][ID]')
    # if task_id is not None:
    #     await QUEUE.put(task_id)


@router.post('/on_task_delete', status_code=200)
async def on_task_delete(request: Request):
    """Ловим эвенты на удаление задач"""
    pass

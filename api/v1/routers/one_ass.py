"""Роутер для работы с 1с"""
import asyncio
from fastapi import APIRouter, exceptions

from .front import UPDATE_EVENT
from api.v1.schemas.one_ass import OrderSchema
from api.v1.bitrix.file import FileUploader
from api.v1.bitrix.task import Task
from api.v1 import utils


router = APIRouter()


@router.post("/create_task", status_code=200)
async def create_tasks(order: OrderSchema):
    """Создание задач"""
    try:
        file_uploader = FileUploader(order.attached_files)
        asyncio.create_task(file_uploader.upload())
        coros = (Task(order, c, file_uploader).put() for c in order.calculation)
        result = await asyncio.gather(*coros)
        asyncio.create_task(utils.log_schema(order))
        asyncio.create_task(utils.log_create_task_response(result))
        UPDATE_EVENT.set()
        return result
    except Exception as e:
        asyncio.create_task(utils.log_exception(e))
        raise exceptions.HTTPException(status_code=500, detail=str(e))

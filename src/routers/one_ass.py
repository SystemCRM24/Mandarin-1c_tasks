"""Роутер для работы с 1с"""
import asyncio
from fastapi import APIRouter, exceptions

from src.schemas.one_ass import OrderSchema
from src.bitrix.file import FileUploader
from src.bitrix.task import Task
from src import utils


router = APIRouter(tags=['1c'])


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
        return result
    except Exception as e:
        asyncio.create_task(utils.log_exception(e))
        raise exceptions.HTTPException(status_code=500, detail=str(e))

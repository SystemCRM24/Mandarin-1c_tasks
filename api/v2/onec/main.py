import asyncio
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from ..schemas.onec import OrderSchema, ResponseItemSchema
from .file import Uploader
from . import service
from api.v2 import utils


router = APIRouter(prefix='/onec')


@router.post('', status_code=200)
async def process_order(order: OrderSchema) -> list[ResponseItemSchema]:
    try:
        uploader = Uploader(order.files)
        asyncio.create_task(uploader.upload())
        coros = service.create_tasks_coros(order, uploader)
        result = await asyncio.gather(*coros)
        service.log_info(order, uploader, result)
        return result
    except Exception as exc: 
        asyncio.create_task(utils.log_exception(exc))
        raise HTTPException(status_code=500, detail=str(exc))

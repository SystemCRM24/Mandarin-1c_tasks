from fastapi import APIRouter
from fastapi.exceptions import HTTPException
import asyncio

from api.utils import log_exception
from api.v3.service.main import log_onec_request
from api.v3.schemas.onec import OrderSchema
from .handlers import OrderHandler


router = APIRouter(prefix="/onec")


@router.post("", status_code=200)
async def process_order(order: OrderSchema):
    handler = OrderHandler(order)
    try: 
        response = await handler.process()
        asyncio.create_task(log_onec_request(order, response))
        return response
    except Exception as exc:
        asyncio.create_task(log_exception(exc, 'onec'))
        raise HTTPException(500, exc)

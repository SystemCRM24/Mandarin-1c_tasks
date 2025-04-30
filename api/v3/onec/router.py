from fastapi import APIRouter
import asyncio

from api.utils import log_exception
from api.v3.service.main import log_onec_request
from api.v3.schemas.onec import OrderSchema
from .handlers import OrderHandler


router = APIRouter(prefix="/onec")


@router.post("", status_code=200)
async def process_order(order: OrderSchema) -> str:
    handler = OrderHandler(order)
    try: 
        response = await handler.process()
        asyncio.create_task(log_onec_request(order, response))
        return f"Задачи по заказу: {order.name} поставлены успешно"
    except Exception as exc:
        asyncio.create_task(log_exception(exc, 'onec'))
        return f"При постановке задач по заказу: {order.name} возникла ошибка."

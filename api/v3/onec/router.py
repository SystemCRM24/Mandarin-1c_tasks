from fastapi import APIRouter

from api.v3.schemas.onec import OrderSchema
from .handlers import OrderHandler


router = APIRouter(prefix="/onec")


@router.post("", status_code=200)
async def process_order(order: OrderSchema):
    handler = OrderHandler(order)
    return await handler.process()

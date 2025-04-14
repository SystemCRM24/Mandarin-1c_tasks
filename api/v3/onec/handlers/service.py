from api.v3.schemas.onec import OrderSchema, CalculationItemSchema


def get_onec_id(order: OrderSchema, calculation: CalculationItemSchema) -> str:
    """Возвращает идентификатор для задачи"""
    return f'{order.id}:{calculation.position}'

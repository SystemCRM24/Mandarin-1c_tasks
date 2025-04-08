class OrderHandler:
    """Обрабатывает входящий запрос из 1c"""

    def __init__(self, order):
        self.order = order

    async def process(self) -> list:
        """Запускает обработку заказа и возвращает результат"""
        return []

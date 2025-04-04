import asyncio


class Pool:
    __instance = None

    def __new__(cls):
        """Для бассейна нужен синглтон"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.lock = asyncio.Lock()
        self.tasks = {}

    async def fill(self):
        """Заполняет бассейн актуальными задачами"""
        async with self.lock:
            self.tasks.clear()


p1 = Pool()
p2 = Pool()

print(p1 is p2)
import aiocache
import asyncio


CACHE = aiocache.Cache()


class Cached:
    """Реализация особой логики кеширования"""

    def __init__(self, ttl: int = 300, namespace: str = 'default'):
        self.ttl = ttl
        self.namespace = namespace
        self._event = asyncio.Event()
        self._event.set()

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            key = self.get_cache_key(func, args, kwargs)
            result = await CACHE.get(key=key, namespace=self.namespace)
            if result is None:
                if self._event.is_set():
                    self._event.clear()
                    asyncio.create_task(self.decorator(key, func, args, kwargs))
                await self._event.wait()
                result = await CACHE.get(key=key, namespace=self.namespace)
            return result
        return wrapper

    async def decorator(self, key, func, args, kwargs):
        """Выполняет функцию и записывает ее результат в кеш"""
        result = await func(*args, **kwargs)
        await CACHE.set(key=key, value=result, ttl=self.ttl, namespace=self.namespace)
        self._event.set()

    @staticmethod
    def get_cache_key(func, args, kwargs):
        """Формирует ключ для поиска по кэшу"""
        ordered_kwargs = sorted(kwargs.items())
        return (
            (func.__module__ or "")
            + func.__name__
            + str(args)
            + str(ordered_kwargs)
        )
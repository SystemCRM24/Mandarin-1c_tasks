import aiocache
import asyncio


decorator = aiocache.cached(namespace='test')


@decorator
async def get_some_dict(some_arg = None):
    print('calculated')
    return {'1': 1, 'some_arg': some_arg}


async def main():
    await get_some_dict()
    await get_some_dict(1)
    k = decorator.get_cache_key(get_some_dict, tuple(), {})
    await decorator.cache.delete(k, 'test')
    r = await decorator.cache.exists(key=k, namespace='test')
    print(r)
    # print(await cache.exists(None, 'test'))
    # d1 = await cache.get(key=get_some_dict.cache_key(None), namespace='test')
    # d2 = await cache.get(key=get_some_dict.cache_key(None), namespace='test')
    # print(d1)
    # print(d2)


asyncio.run(main())
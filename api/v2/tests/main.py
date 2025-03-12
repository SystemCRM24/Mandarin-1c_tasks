import aiocache
import asyncio


@aiocache.cached()
async def get_some_dict():
    print('calculated')
    return {'1': 1,'2': None}


async def main():
    f = filter(
        lambda x: x is not None,
        [None, 1, {1: 1}]
    )
    print(*f)


asyncio.run(main())
import asyncio


async def main():
    d = {}
    for i in range(5):
        task = asyncio.create_task(asyncio.sleep(i))
        d[i] = task
    await asyncio.gather(*d.values())
    print(d)


asyncio.run(main())
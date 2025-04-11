from pathlib import Path
import sys
import asyncio


parent = Path(__file__).parent.parent.parent.parent
sys.path.append(str(parent))


from api.v3.bitrix import requests
from api.v3.bitrix.pool import Pool


async def main():
    pool = Pool()
    await pool.fill()
    result = pool._get_tasks_by_department()
    print(result)


asyncio.run(main())


# async def test():
#     await asyncio.sleep(1)
#     return 'Hello world!'

# async def main():
#     t = asyncio.create_task(test())
#     result = await t
#     result1 = await t
#     print(result, result1)


# asyncio.run(main())
from pathlib import Path
import sys
import asyncio


parent = Path(__file__).parent.parent.parent.parent
sys.path.append(str(parent))


from api.v3.bitrix.pool import Pool
from api.v3.front.funcs import fetch_websocket_message


async def main():
    pool = Pool()
    await pool.fill()
    result = await fetch_websocket_message()
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
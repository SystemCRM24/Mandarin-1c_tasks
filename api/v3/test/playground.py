from pathlib import Path
import sys
import asyncio


parent = Path(__file__).parent.parent.parent.parent
sys.path.append(str(parent))


from api.v3.bitrix import requests


async def main():
    result = await requests.get_task_info(2035)
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
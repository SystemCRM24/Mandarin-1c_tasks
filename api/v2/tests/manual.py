import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT))

import asyncio
import unittest

from api.v2.bitrix.requests import get_task_info


async def main():
    response = await get_task_info(1803)
    print(response)


asyncio.run(main())


# class TestBitrixRequests(unittest.IsolatedAsyncioTestCase):

#     # async def test_get_user_tasks(self):
#     #     from api.v2.bitrix import get_user_tasks
#     #     response = await get_user_tasks(12)
#     #     self.assertTrue(response)

#     async def test_get_task_info(self):
#         from api.v2.bitrix.requests import get_task_info
#         response = await get_task_info(8438)
#         print(response)


# if __name__ == '__main__':
#     unittest.main()

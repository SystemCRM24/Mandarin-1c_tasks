import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT))


class TestBitrixRequests(unittest.IsolatedAsyncioTestCase):

    async def test_get_user_tasks(self):
        from api.v2.bitrix import get_user_tasks
        response = await get_user_tasks(12)
        self.assertTrue(response)

    async def test_get_task_info(self):
        from api.v2.bxtask import get_bxtask_from_id
        response = await get_bxtask_from_id(1580)
        print(response)


if __name__ == '__main__':
    unittest.main()

import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent.__str__())


import asyncio
from src.bitrix import requests
from src.schemas.main import DepartmentSchema


async def main():
    result = await requests.get_user_from_id(1)
    tasks = await requests.get_staff_tasks([result])
    print(tasks)


asyncio.run(main())
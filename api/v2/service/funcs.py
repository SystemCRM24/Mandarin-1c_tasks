import aiocache
import asyncio
from api.v2.bitrix.requests import get_task_info, get_user_tasks
from api.v2.bitrix.task import BXTask


tasks_cache = aiocache.cached(ttl=60 * 60 * 4, namespace='tasks')

@tasks_cache
async def get_bxtask_from_id(task_id: str | int) -> BXTask | None:
    """Возвращает объект BXTask или None, если ответ от сервера не прошел валидацию"""
    response = await get_task_info(task_id)
    if response is None:    # Если ничего не пришло (маловероятно, но оставим)
        return None
    bxtask = BXTask.from_bitrix(response)
    if not bxtask.is_valid():
        return None
    return bxtask


async def get_bxtasks_from_user(user_id: str | int) -> list[BXTask]:
    """
    Возвращает актуальные задачи пользователя.
    Дополнительно сортирует их по возрастанию атрибута end_date_plan.

    """
    tasks_ids = await get_user_tasks(user_id)
    print(tasks_ids)
    if not tasks_ids:
        return tasks_ids
    coros = (get_bxtask_from_id(t['ID']) for t in tasks_ids)
    response = await asyncio.gather(*coros)
    return sorted(
        filter(
            lambda bxtask: bxtask is not None, 
            response
        ),
        key=lambda bxtask: bxtask.start_date_plan
    )

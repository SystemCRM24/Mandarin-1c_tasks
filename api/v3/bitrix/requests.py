"""
Запросы к битриксу
"""
from fast_bitrix24 import BitrixAsync
import aiocache
from typing import Iterable

from api.v2 import constants


BX = BitrixAsync(constants.BITRIX_WEBHOOK)


async def call_batch(requests: Iterable) -> dict:
    """Посылает батч-запрос"""
    cmd = {i: r for i, r in enumerate(requests)}
    return await BX.call_batch(params={'halt': 0, 'cmd': cmd})


async def get_task_info(task_id: str, select: Iterable = None) -> dict | None:
    """Получает информацию по задаче"""
    if select is None:
        select = ('*', )
    params = {'taskId': task_id, 'select': tuple(select)}
    result: dict = await BX.call('tasks.task.get', params, raw=True)
    task_outer: dict = result.get('result', {})
    if isinstance(task_outer, list):
        return None
    return task_outer.get('task', None)
    
"""
Запросы к битриксу
"""
from fast_bitrix24 import BitrixAsync
from typing import Iterable
import aiocache

from api.v3 import constants
from .task import BXTask


BX = BitrixAsync(constants.BITRIX_WEBHOOK)


async def call_batch(requests: Iterable) -> dict:
    """Посылает батч-запрос"""
    cmd = {i: r for i, r in enumerate(requests)}
    return await BX.call_batch(params={'halt': 0, 'cmd': cmd})


TAKS_SELECT_PARAMS = tuple(BXTask.PARAM_BY_ATTR.values())


async def get_task_info(task_id: str) -> dict | None:
    """Получает информацию по задаче"""
    params = {'taskId': task_id, 'select': TAKS_SELECT_PARAMS}
    result: dict = await BX.call('tasks.task.get', params, raw=True)
    task_outer: dict = result.get('result', {})
    if isinstance(task_outer, list):
        return None
    return task_outer.get('task', None)


async def get_tasks_list(filter: dict | None = None) -> list[dict]:
    """Получает список задач по переданным параметрам"""
    params = {'select': TAKS_SELECT_PARAMS}
    if isinstance(filter, dict):
        params['filter'] = filter
    response = await BX.call('tasks.task.list', items=params, raw=True)
    result: dict = response.get('result', {})
    return result.get('tasks', [])


async def get_work_schedule(id: int | str = 1) -> dict:
    """Получает настройки рабочего графика. По умолчанию - график под номером 1: для всех."""
    result = await BX.call(
        "timeman.schedule.get", 
        items={"id": id}, 
        raw=True
    )
    return result["result"]


responsibles_cache = aiocache.cached(ttl=60 * 60 * 4, namespace='department')

@responsibles_cache
async def get_responsibles() -> dict[str, dict]:
    """
    Получает словарь ответственных, где:
    ключ - ид ответственного
    значение - словарь, который характеризует ответственного.
    """
    departments = await get_departments()
    users = await get_users(departments)
    responsibles = {}
    for user in users:
        user_departments: list = user.get('UF_DEPARTMENT', None)
        main_department_id = str(user_departments[0])
        user['DEPARTMENT'] = departments[main_department_id]
        responsibles[user['ID']] = user
    return responsibles


async def get_departments() -> dict[str, dict]:
    """Возвращает информацию по подразделениям, дочерним к Производству."""
    response: list[dict] = await BX.get_all("department.get")
    return {d['ID']: d for d in response if d.get('PARENT', '') == constants.DEPARTMENT_ID}


async def get_users(departments: dict) -> list[dict]:
    """Возвращает информацию по пользователям, внутри подразделения."""
    params = {
        'ACTIVE': True,
        '@UF_DEPARTMENT': list(departments)
    }
    response: list[dict] = await BX.get_all(method='user.get', params=params)
    return response


manager_cache = aiocache.cached(ttl=60 * 60 * 4, namespace='department')

@manager_cache
async def get_manager(full_name: str) -> str | None:
    """Возвращает id менеджера или None, если менеджер не найден"""
    name_list = full_name.split(' ')
    to_search = ' '.join(name_list[:2])
    response = await BX.call(method='user.get', items={'NAME_SEARCH': to_search})
    if isinstance(response, dict):
        return response.get('ID', None)

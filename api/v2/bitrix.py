"""
Запросы к битриксу
"""
from fast_bitrix24 import BitrixAsync
import aiocache
from . import constants


BX = BitrixAsync(constants.BITRIX_WEBHOOK)


async def upload_file(name: str, b64_str: str, upload_dir_id: int | str | None = None) -> dict:
    """
    Загружает файлы на диск в папку прикрепленные файлы
    name: имя файла
    b64_str: Строка в кодировке base64, которая представляет файл.
    folder_id: id папки, куда будет загружен файл. 
    По умолчанию - 78 - Папка "Прикрепленные файлы" на портале Мандарина

    return: Словарь с информацией о загруженном файле.
    https://apidocs.bitrix24.ru/api-reference/disk/folder/disk-folder-upload-file.html
    """
    if upload_dir_id is None:
        upload_dir_id = constants.UPLOAD_DIR_ID
    items = {
        "id": upload_dir_id,
        "fileContent": [name, b64_str],
        "data": {"NAME": name},
        "generateUniqueName": True,
    }
    result: dict = await BX.call("disk.folder.uploadfile", items=items, raw=True)
    return result["result"]


department_cache = aiocache.cached(ttl=60 * 60 * 4, namespace='department')

@department_cache
async def get_departments_info(key: str | None = None) -> list[dict] | dict[str, dict]:
    """
    Возвращает информацию по всем подразделениям.
    Если указан key, то вместо списочного предстставления, вернет словарь.
    """
    response: list[dict] = await BX.get_all("department.get")
    if key is None:
        return response
    return {it[key]: it for it in response}


users_cache = aiocache.cached(ttl=60 * 60 * 4, namespace='users')

@users_cache
async def get_users_by_department(department_id: str | int | None = None) -> list[dict]:
    """Получает данные пользователя по его ID"""
    params = {'ACTIVE': True}
    if department_id is not None:
        params['@UF_DEPARTMENT'] = [department_id]
    response: list[dict] = await BX.get_all("user.get", params=params)
    return response


async def get_user_tasks(user_id: str | int) -> list[dict]:
    """Получаем список ID актуальных задач из 1с пользователя"""
    params = {
        'select': ['ID'],
        'filter': {
            'RESPONSIBLE_ID': user_id,
            '!STATUS': 5,                           # Все статусы, кроме выполненного
            'GROUP_ID': constants.ONEC_GROUP_ID     # Группа задач из 1с
        }
    }
    return await BX.get_all('tasks.task.list', params=params)


async def get_task_info(task_id: str | int) -> dict | None:
    """Получает информацию о задаче"""
    params = {
        'select': [
            'ID',                   # идентификатор задачи
            'TITLE',                # название задачи
            'DESCRIPTION',          # описание
            'STATUS',               # статус
            'GROUP_ID',             # рабочая группа
            'CREATED_BY',           # постановщик
            'RESPONSIBLE_ID',       # исполнитель
            'DATE_START',           # дата начала
            'DEADLINE',             # крайний срок
            'START_DATE_PLAN',      # плановое начало
            'END_DATE_PLAN',        # плановое завершение
            'TIME_ESTIMATE',        # время, выделенное на задачу;
            'UF_TASK_WEBDAV_FILES', # Прикрепленные файлы 
            'ALLOW_TIME_TRACKING',  # Флаг для разрешения трекинга времени
        ],
        'filter': {
            'ID': task_id
        }
    }
    response = await BX.call('tasks.task.list', params, raw=True)
    tasks = response['result']['tasks']
    if tasks:
        return tasks[0]


async def create_task(request_data: dict) -> str:
    """Создает таску в битриксе"""
    response = await BX.call(
        method="tasks.task.add", 
        items={"fields": request_data},
        raw=True
    )
    print(response)


async def update_task(task_id: int | str, request_data: dict) -> str:
    """Обновляет задачу"""
    response = await BX.call(
        method="tasks.task.update", 
        items={
            "taskId": task_id, 
            "fields": request_data
        },
        raw=True
    )
    print(response)


async def execute_task(task_id: int | str) -> str:
    """Выполняет задачу"""
    response = await BX.call(
        method="tasks.task.complete", 
        items={"taskId": task_id},
        raw=True
    )
    print(response)
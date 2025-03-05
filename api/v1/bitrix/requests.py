import aiocache
from os import environ

from fast_bitrix24 import BitrixAsync
from api.v1.schemas.main import DepartmentSchema, UserSchema, TaskSchema


BITRIX_WEBHOOK = environ.get('BITRIX_WEBHOOK')
BX = BitrixAsync(BITRIX_WEBHOOK)


@aiocache.cached(ttl=60 * 60 * 24, namespace="department")
async def get_departments_info() -> list[DepartmentSchema]:
    """Возвращает информацию"""
    response: list[dict] = await BX.get_all("department.get")
    return [DepartmentSchema.model_validate(item) for item in response]


@aiocache.cached(ttl=60 * 60 * 4, namespace="staff")
async def get_staff_from_department_id(department_id: str) -> list[UserSchema]:
    """Получает персонал подразделения"""
    response: list[dict] = await BX.get_all(
        "user.get", 
        params={
            "UF_DEPARTMENT": department_id,
            'ACTIVE': True
        }
    )
    return [UserSchema.model_validate(item) for item in response]


@aiocache.cached(ttl=60 * 60 * 24, namespace="user")
async def get_user_from_id(user_id: str | int) -> UserSchema:
    """Получает данные пользователя по его ID"""
    response = await BX.call(
        'user.get',
        items={'ID': user_id},
        raw=True
    )
    user_data: dict = response['result'][0]
    return UserSchema.model_validate(user_data)


async def get_staff_tasks(staff: list[UserSchema]) -> list[list]:
    """Получает задачи персонала по переданному списку"""
    params = {"halt": 0, "cmd": {}}
    # Исключаем выполненные задачи
    for i, s in enumerate(staff):
        params["cmd"][i] = f'tasks.task.list?filter[!STATUS]=5&filter[RESPONSIBLE_ID]={s.ID}'
    response = await BX.call_batch(params=params)
    tasks = []
    for user_data in response:
        user_tasks = []
        if user_data['tasks']:
            for task_data in user_data['tasks']:
                user_tasks.append(TaskSchema.model_validate(task_data))
        tasks.append(user_tasks)
    return tasks


async def create_task(request_data: dict):
    """Создает таску в битриксе"""
    await BX.call(method="tasks.task.add", items={"fields": request_data})


async def update_task(task_id: int | str, request_data: dict):
    """Обновляет задачу"""
    await BX.call(method="tasks.task.update", items={"taskId": task_id, "fields": request_data})


async def upload_file(name: str, binary_str: str) -> dict:
    """
    Загружает файлы на диск в папку прикрепленные файлы
    name: имя файла
    binary_str: Строка в кодировке base64

    return: Словарь с информацией о загруженном файле.
    https://apidocs.bitrix24.ru/api-reference/disk/folder/disk-folder-upload-file.html
    """
    result: dict = await BX.call(
        method="disk.folder.uploadfile",
        items={
            "id": 78,  # Папка: Прикрепленные файлы
            "fileContent": [name, binary_str],
            "data": {"NAME": name},
            "generateUniqueName": True,
        },
        raw=True,
    )
    return result["result"]


async def get_work_schedule(id: int | str = 1) -> dict:
    """Получает настройки рабочего графика. По умолчанию - график под номером 1: для всех."""
    result = await BX.call("timeman.schedule.get", items={"id": id}, raw=True)
    return result["result"]


# if __name__ == "__main__":
#     import asyncio

#     # asyncio.run(create_task({'TITLE': 'test','RESPONSIBLE_ID': 1, 'TIME_ESTIMATE': 60 * 60, 'ALLOW_TIME_TRACKING': 'Y'}))
#     asyncio.run(main())

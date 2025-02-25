from fast_bitrix24 import BitrixAsync
import aiocache
from os import environ


BITRIX_WEBHOOK = environ.get('BITRIX_WEBHOOK')
if BITRIX_WEBHOOK is None:
    import dotenv
    BITRIX_WEBHOOK = dotenv.dotenv_values().get('BITRIX_WEBHOOK')


BX = BitrixAsync(BITRIX_WEBHOOK)


async def get_department_id_from_name(name: str) -> str:
    """Получает id подразделения по его имени. Если не нашло, то вернет id администрации"""
    departments = await get_department_info()
    for department in departments:
        if department["NAME"] == name:
            return department["ID"]
    return "1"


async def get_department_head_from_name(name: str) -> str:
    """Получает ID руководителя подразделения"""
    departments = await get_department_info()
    for department in departments:
        if department["NAME"] == name:
            return department.get("UF_HEAD", '1')
    return "1"


@aiocache.cached(ttl=60 * 60 * 24, namespace="department")
async def get_department_info() -> list:
    """Возвращает информацию"""
    return await BX.get_all("department.get")


@aiocache.cached(ttl=60 * 60 * 4, namespace="staff")
async def get_staff_from_department_id(department_id: str) -> list:
    """Получает персонал подразделения. Если ничего нет, то возвращает персонал админского подразделения"""
    response = await BX.get_all("user.get", params={"UF_DEPARTMENT": department_id})
    if not response:
        admin_department_id = await get_department_id_from_name("admin")
        return await get_staff_from_department_id(admin_department_id)
    return response


async def get_staff_tasks(staff: list):
    """Получает задачи персонала по переданному списку"""
    params = {"halt": 0, "cmd": {}}
    # Исключаем выполненные задачи
    for i, s in enumerate(staff):
        params["cmd"][i] = f'tasks.task.list?filter[!STATUS]=5&filter[RESPONSIBLE_ID]={s["ID"]}'
    response = await BX.call_batch(params=params)
    return [x["tasks"] for x in response]


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

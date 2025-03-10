import aiocache

from os import environ
from fast_bitrix24 import BitrixAsync


BITRIX_WEBHOOK = environ.get('BITRIX_WEBHOOK')
BX = BitrixAsync(BITRIX_WEBHOOK)

CACHE = aiocache.Cache.MEMORY


async def upload_file(name: str, b64_str: str, folder_id: int | str = 78) -> dict:
    """
    Загружает файлы на диск в папку прикрепленные файлы
    name: имя файла
    b64_str: Строка в кодировке base64, которая представляет файл.
    folder_id: id папки, куда будет загружен файл. 
    По умолчанию - 78 - Папка "Прикрепленные файлы" на портале Мандарина

    return: Словарь с информацией о загруженном файле.
    https://apidocs.bitrix24.ru/api-reference/disk/folder/disk-folder-upload-file.html
    """
    result: dict = await BX.call(
        method="disk.folder.uploadfile",
        items={
            "id": folder_id,
            "fileContent": [name, b64_str],
            "data": {"NAME": name},
            "generateUniqueName": True,
        },
        raw=True,
    )
    return result["result"]


@aiocache.cached(ttl=60 * 60 * 4, namespace='department', cache=CACHE)
async def get_departments_info(key: str | None = None) -> list[dict] | dict[str, dict]:
    """
    Возвращает информацию по всем подразделениям.
    Если указан key, то вместо списочного предстставления, вернет словарь.
    """
    response: list[dict] = await BX.get_all("department.get")
    if key is None:
        return response
    return {it[key]: it for it in response}

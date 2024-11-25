from asyncio import Lock, sleep, gather
from .requests import upload_file
from schemas import AttachedFilesItem


class Files:
    """Класс для работы с отправляемыми на сервер файлами"""

    def __init__(self, files_to_upload: list[AttachedFilesItem]):
        self.files_to_upload = files_to_upload
        self._lock = Lock()
        self._request = []

    async def upload(self):
        """Загружает файлы на сервер"""
        if not self.files_to_upload:
            return
        async with self._lock:
            tasks = (upload_file(item.name, item.binary) for item in self.files_to_upload)
            response = await gather(*tasks)
            for file in response:
                self._request.append('n' + str(file['ID']))
        
    async def get_request(self) -> list:
        """Возвращает список из id загруженных файлов. Если таких нет, то вернется пустой список."""
        if self._lock.locked:
            async with self._lock:
                pass
        return self._request

from asyncio import Lock, sleep


class Files:
    """Класс для работы с отправляемыми на сервер файлами"""

    def __init__(self, files_to_upload: list):
        self.files_to_upload = files_to_upload
        self._lock = Lock()
        self._request = []

    async def upload(self):
        """Загружает файлы на сервер"""
        if not self.files_to_upload:
            return
        async with self._lock:
            await sleep(5)
        
    async def get_request(self) -> list:
        """Возвращает список из id загруженных файлов. Если таких нет, то вернется пустой список."""
        async with self._lock:
            return self._request

import asyncio

from src.bitrix.requests import upload_file
from src.schemas.one_ass import AttachedFilesItem


class FileUploader:
    """Класс для работы с отправляемыми на сервер файлами"""

    def __init__(self, files_to_upload: list[AttachedFilesItem]):
        self.files_to_upload = files_to_upload
        self.uploaded_files = []
        self._upload_event = asyncio.Event()

    async def upload(self):
        """Загружает файлы на сервер"""
        self._upload_event.clear()
        if self.files_to_upload:
            tasks = (upload_file(i.name, i.binary) for i in self.files_to_upload)
            response = await asyncio.gather(*tasks)
            for file in response:
                self.uploaded_files.append("n" + str(file["ID"]))
        self._upload_event.set()

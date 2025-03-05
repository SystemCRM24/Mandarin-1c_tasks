import asyncio
from urllib.parse import unquote

from api.v1.bitrix.requests import upload_file
from api.v1.schemas.one_ass import AttachedFilesItem


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
            coros = []
            for file in self.files_to_upload:
                b64_message = unquote(file.binary)
                coros.append(upload_file(file.name, b64_message))
            response = await asyncio.gather(*coros)
            for file in response:
                self.uploaded_files.append("n" + str(file["ID"]))
        self._upload_event.set()

from asyncio import gather, create_task

from src.bitrix.requests import upload_file
from src.schemas import AttachedFilesItem


class Files:
    """Класс для работы с отправляемыми на сервер файлами"""

    def __init__(self, files_to_upload: list[AttachedFilesItem]):
        self.files_to_upload = files_to_upload
        self.request = []
        self.atask = create_task(self.upload())

    async def upload(self):
        """Загружает файлы на сервер"""
        if not self.files_to_upload:
            return
        tasks = (upload_file(item.name, item.binary) for item in self.files_to_upload)
        response = await gather(*tasks)
        for file in response:
            self.request.append("n" + str(file["ID"]))

import asyncio

from ..schemas.onec import FileItemSchema
from ..bitrix import upload_file


class Uploader:
    """Класс для работы с отправляемыми на сервер файлами"""

    __slots__ = '_event', 'to_upload', 'files'

    def __init__(self, to_upload: list[FileItemSchema]):
        self._event = asyncio.Event()
        self.to_upload = to_upload
    
    async def upload(self):
        """Загружает файлы на сервер. Наполняет объект строками, соответствющими ID загруженных файлов"""
        self._event.clear()
        async with asyncio.TaskGroup() as tg:
            for file_item in self.to_upload:
                tg.create_task(self._upload_file(file_item))
        self._event.set()

    @staticmethod
    async def _upload_file(file_item: FileItemSchema):
        """Основная логика загрузки"""
        response = await upload_file(file_item.name, file_item.binary)
        file_item.bx_id = response["ID"]

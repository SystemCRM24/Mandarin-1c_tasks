from api.utils import BatchBuilder
from api.v3.schemas.onec import FileItemSchema
from api.v3.constants import UPLOAD_DIR_ID
from api.v3.bitrix.requests import call_batch


class FileHandler:
    """Класс для работы с отправляемыми на сервер файлами"""

    __slots__ = ('to_upload', )

    def __init__(self, to_upload: list[FileItemSchema]):
        self.to_upload = to_upload

    async def process(self) -> list[int]:
        requests = []
        if not self.to_upload:
            return requests
        for file in self.to_upload:
            params = {
                'id': UPLOAD_DIR_ID,
                'fileContent': [file.name, file.binary],
                "data": {"NAME": file.name},
                "generateUniqueName": True,
            }
            batch = BatchBuilder('disk.folder.uploadfile', params)
            requests.append(batch.build())
        result: list[dict] = await call_batch(requests)
        return [f.get('ID', 0) for f in result]

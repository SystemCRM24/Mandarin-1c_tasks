from datetime import datetime
from api.utils import SERVER_TZ

from api.v3.schemas.onec import ResponseSchema, OrderSchema
from pydantic import BaseModel


class LogSchema(BaseModel):
    time: datetime
    request: OrderSchema
    response: ResponseSchema


async def log_onec_request(request: OrderSchema, response: ResponseSchema):
    """Логгирует запрос и ответ на него по задаче из 1с"""
    now = datetime.now(SERVER_TZ)
    request = request.model_copy(deep=True)
    for file_item in request.files:
        file_item.binary = file_item.binary[:40] + '(...)'
    log = LogSchema(
        time=now,
        request=request,
        response=response
    )
    with open(f'logs/{now.strftime(r'%Y-%m-%d_%H-%M-%S')}_{request.name}.json', 'w') as file:
        file.write(log.model_dump_json(indent=2))

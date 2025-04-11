from datetime import datetime
import json
from api.utils import SERVER_TZ

from api.v3.schemas.onec import ResponseSchema, OrderSchema


async def log_onec_request(request: OrderSchema, response: ResponseSchema):
    """Логгирует запрос и ответ на него по задаче из 1с"""
    now = datetime.now(SERVER_TZ)
    request = request.model_dump()
    for file_item in request.get('files'):
        file_item['binary'] = file_item.get('binary', '')[:40] + '(...)'
    dct = {
        'time': now.isoformat(),
        'request': request,
        'response': response.model_dump()
    }
    with open(f'logs/{now.strftime(r'%Y-%m-%d_%H-%M-%S')}_{request['name']}.json', 'w') as file:
        json.dump(dct, file, ensure_ascii=True, indent=2)

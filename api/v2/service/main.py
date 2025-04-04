from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import json
import base64

from .cat import html_cat
from api.v2.constants import EVENT
from api.v2.bitrix.requests import upload_file


router = APIRouter(prefix='/service')


@router.get('/ping', status_code=200, response_class=HTMLResponse)
async def ping() -> str:
    return html_cat


@router.get('/trigger_ws_event', status_code=200)
async def trigger_ws_event() -> str:
    EVENT.set()
    return 'Event was triggered'


@router.post('/upload_json', status_code=200)
async def upload_json(data: dict):
    """Загружает произвольный json-файл на диск битрикса"""
    json_string = json.dump(data, ensure_ascii=True, indent=2)
    b64_binary = base64.b64encode(json_string)
    b64_message = b64_binary.decode('utf-8')
    await upload_file('request.json', b64_message)

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .cat import html_cat
from api.v2.constants import EVENT


router = APIRouter(prefix='/service')


@router.get('/ping', status_code=200, response_class=HTMLResponse)
async def ping() -> str:
    return html_cat


@router.get('/trigger_ws_event', status_code=200)
async def trigger_ws_event() -> str:
    EVENT.set()
    return 'Event was triggered'

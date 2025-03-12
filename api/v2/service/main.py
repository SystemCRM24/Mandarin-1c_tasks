from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .cat import html_cat


router = APIRouter(prefix='/service')


@router.get('/ping', status_code=200, response_class=HTMLResponse)
async def ping() -> str:
    return html_cat
"""Тестовые роутеры"""
from fastapi import APIRouter
from src.service import fetch_websocket_data
from .front import UPDATE_EVENT


router = APIRouter(tags=['test'])


@router.get("/ping", status_code=200)
async def ping():
    """Пингует сервер"""
    return {"message": "Pong"}


@router.get("/fetch_data")
async def fetch_data():
    """Тестирование корректности отправляемых данных"""
    return await fetch_websocket_data()


@router.get('/trigger_event')
async def trigger_event():
    """Тригеррит эвент на обновление вебсокетов"""
    UPDATE_EVENT.set()
    return {'message': 'Event triggered'}

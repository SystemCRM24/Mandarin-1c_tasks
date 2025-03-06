from fastapi import APIRouter
from typing import Dict, Any
import json


router = APIRouter(prefix='/onec')


@router.post('', status_code=200)
async def process_order(order: Dict[str, Any]):
    print(order.items()[0])
    with open('logs/sample.json', 'w') as file:
        json.dump(order, file)
    return {'message': 'success'}

from fastapi import APIRouter


router = APIRouter(prefix='/front')


@router.get('/fetch_data', status_code=200)
async def fetch_data():
    pass
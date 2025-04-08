from fastapi import APIRouter


router = APIRouter(prefix="/service")


@router.get('/fetch_data', status_code=200)
async def fetch_data():
    pass


@router.get('/clear_cache', status_code=200)
async def clear_cache():
    pass
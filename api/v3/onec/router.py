from fastapi import APIRouter


router = APIRouter(prefix="/onec")


@router.post("", status_code=200)
async def process_order():
    pass

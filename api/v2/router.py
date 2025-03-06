from fastapi import APIRouter
from .onec.main import router as onec_router


router = APIRouter(prefix='/v2', tags=['v2'])


router.include_router(onec_router)

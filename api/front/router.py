from fastapi import APIRouter

from .service import router as service_router
from .ws import router as ws_router


router = APIRouter(prefix='/front', tags=['front'])

router.include_router(ws_router)
router.include_router(service_router)

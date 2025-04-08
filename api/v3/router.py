from fastapi import APIRouter
from .bitrix.router import router as bitrix_router
from .onec.router import router as onec_router
from .front.router import router as front_router
from .service.router import router as service_router


router = APIRouter(prefix='/v3', tags=['v3'])

router.include_router(bitrix_router)
router.include_router(onec_router)
router.include_router(front_router)
router.include_router(service_router)

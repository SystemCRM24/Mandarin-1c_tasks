from fastapi import APIRouter
from .event.main import router as event_router
from .front.main import router as front_router
from .onec.main import router as onec_router
from .service.main import router as service_router


router = APIRouter(prefix='/v2', tags=['v2'])

router.include_router(event_router)
router.include_router(front_router)
router.include_router(onec_router)
router.include_router(service_router)

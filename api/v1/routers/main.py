from fastapi import APIRouter

from .front import router as front_router
from .one_ass import router as one_ass_router
from .tests import router as tests_router


router = APIRouter(prefix='/v1', tags=['v1'])
router.include_router(front_router)
router.include_router(one_ass_router)
router.include_router(tests_router)

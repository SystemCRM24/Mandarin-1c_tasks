from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routers.main import router as v1_router
from api.v2.router import router as v2_router
from api.v3.router import router as v3_router
from api.utils.router import router as utils_router


app = FastAPI(
    title="Постановка задач",
    description="Автоматическая постановка задач для Битрикс24 компании Мандарин на основе POST-запроса.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils_router)
app.include_router(v1_router)
app.include_router(v2_router)
app.include_router(v3_router)

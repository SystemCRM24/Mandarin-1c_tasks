from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.v3.router import router as v3_router
from api.utils.router import router as utils_router
from api.front.router import router as front_router


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

app.mount("/guntt", StaticFiles(directory='front/public', html=True), name='guntt')

app.include_router(front_router)
app.include_router(v3_router)
app.include_router(utils_router)

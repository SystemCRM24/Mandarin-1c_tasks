from fastapi import FastAPI, Request, HTTPException
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

app.include_router(front_router)
app.include_router(v3_router)
app.include_router(utils_router)


# Для возможности получения файлов
class CustomStaticFiles(StaticFiles):
    async def __call__(self, scope, receive, send):
        if scope['method'] == 'POST':
            scope['method'] = 'GET'
        return await super().__call__(scope, receive, send)


app.mount("/guntt", CustomStaticFiles(directory='front/public', html=True), name='guntt')

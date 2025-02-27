from os import environ

# Проверка на виртуальное окружение
if environ.get('BITRIX_WEBHOOK') is None:
    import dotenv
    dotenv.load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import routers


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


app.include_router(routers.front_router)
app.include_router(routers.one_ass_router)
app.include_router(routers.tests_router)

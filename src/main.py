import asyncio
from datetime import datetime

from fastapi import FastAPI, Query, Response
from fastapi.exceptions import HTTPException

from bitrix.file import Files
from bitrix.task import Task, UpdateTaskException
from schemas import OrderSchema
from src.bitrix.requests import get_work_schedule
from src.bitrix.utils.date_range import generate_date_range
from src.bitrix.utils.logger_util import log_error

app = FastAPI(
    title="Постановка задач",
    description="Автоматическая постановка задач для Битрикс24 компании Мандарин на основе POST-запроса.",
)


@app.get("/ping/", status_code=200)
async def ping():
    """Пингует сервер"""
    return {"message": "Pong"}


@app.post("/", status_code=200)
async def create_tasks(order: OrderSchema):
    """Создание задач"""
    files = Files(order.attached_files)
    tasks = (Task(order, td, files).put_task() for td in order.calculation)
    try:
        await asyncio.gather(*tasks)
        return {"message": "ok"}
    except Exception as e:
        log_error(e, order)
        if isinstance(e, UpdateTaskException):
            return {
                "message": "При обновлении задачи произошла ошибка. Скорее всего, "
                "некоторые данные в задаче были обновлены, но что-то пошло не так."
            }
        raise HTTPException(500, detail=str(e))


@app.get("/worktime/", status_code=200)
async def get_work_time_periods(
    start: datetime = Query(..., description="Start time"),
    end: datetime = Query(..., description="End time"),
):
    """Отдает массив рабочих дней"""

    work_days = await get_work_schedule()
    data = generate_date_range(start, end, work_days)

    return Response(content=data, headers={'Access-Control-Allow-Origin': '*'})


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)

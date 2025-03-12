from api.v2.utils import uvicorn_logger


async def task_update_handler(task_id: str):
    uvicorn_logger.info(f'Handling task {task_id}')

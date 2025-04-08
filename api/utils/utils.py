from datetime import datetime
import traceback
from zoneinfo import ZoneInfo

from .loggers import uvicorn_logger, debug_logger


SERVER_TZ = ZoneInfo('Europe/Moscow')


def create_batch_request(method: str, params: dict | None = None) -> str:
    """Создаент батч-запрос из переданных параметров"""
    if params is None:
        params = {}
    batch = f"{method}?"
    for cmd, cmd_params in params.items():
        cmd = f"&{cmd}"
        if isinstance(cmd_params, dict):
            for key, value in cmd_params.items():
                batch += f'{cmd}[{key}]={value}'
        if isinstance(cmd_params, list | tuple):
            for index, item in enumerate(cmd_params):
                batch += f'{cmd}[{index}]={item}'
    return batch



async def log_exception(e: Exception, module="main"):
    """Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    uvicorn_logger.info(f"An exception {str(e)} occurred in the module {module}")
    message = f'---------- {datetime.now(tz=SERVER_TZ)} ----------'
    debug_logger.info(message)
    for frame in traceback.format_exception(e):
        debug_logger.info(frame[:-1])
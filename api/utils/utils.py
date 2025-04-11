from datetime import datetime
import traceback
from zoneinfo import ZoneInfo
from urllib.parse import quote as url_quote

from .loggers import uvicorn_logger, debug_logger


SERVER_TZ = ZoneInfo('Europe/Moscow')


class BatchBuilder:
    """Создает батч запрос"""

    __slots__ = ('method', 'params')

    def __init__(self, method: str, params: dict | None = None):
        self.method = method
        self.params = params or {}
        if method.startswith('tasks'):
            uvicorn_logger.info(str(self.params))
    
    def build(self) -> str:
        """Возвращает батч-запрос в виде строки"""
        batch = f"{self.method}?"
        for cmd, cmd_params in self.params.items():
            match cmd_params:
                case dict() as params:
                    batch += self._get_subbatch_from_dict(cmd, params)
                case tuple() | list() as params:
                    batch += self._get_subbatch_from_iterable(cmd, params)
                case params:
                    batch += self._get_subbatch(cmd, params)
        return url_quote(batch)

    @staticmethod
    def _get_subbatch_from_dict(cmd, params: dict) -> str:
        """Возвращает подзапрос для словарей"""
        subbatch = ''
        for key, value in params.items():
            subbatch += f'&{cmd}[{key}]={value}'
        return subbatch
    
    @staticmethod
    def _get_subbatch_from_iterable(cmd, params: list | tuple) -> str:
        """Возвращает подзапрос для словарей"""
        subbatch = ''
        for index, value in enumerate(params):
            subbatch += f'&{cmd}[{index}]={value}'
        return subbatch

    @staticmethod
    def _get_subbatch(cmd, params: int | float | str) -> str:
        """Возвращает подзапрос для этих типов данных"""
        subbatch = f'&{cmd}={params}'
        return subbatch


async def log_exception(e: Exception, module="main"):
    """Асинхронное Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    uvicorn_logger.info(f"An exception {str(e)} occurred in the module {module}")
    message = f'---------- {module} {datetime.now(tz=SERVER_TZ)} ----------'
    debug_logger.info(message)
    for frame in traceback.format_exception(e):
        debug_logger.info(frame[:-1])

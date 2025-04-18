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
        return batch

    @staticmethod
    def _get_subbatch_from_dict(cmd, params: dict) -> str:
        """Возвращает подзапрос для словарей"""
        subbatch = ''
        for key, value in params.items():
            if isinstance(value, tuple | list):
                for sub_cmd in BatchBuilder._iterable_iterator(value):
                    subbatch += f'&{cmd}[{key}]{sub_cmd}'
            else:
                value = url_quote(str(value))
                subbatch += f'&{cmd}[{key}]={value}'
        return subbatch
    
    @staticmethod
    def _get_subbatch_from_iterable(cmd, params: list | tuple) -> str:
        """Возвращает подзапрос для словарей"""
        subbatch = ''
        for sub_cmd in BatchBuilder._iterable_iterator(params):
            subbatch += f'&{cmd}{sub_cmd}'
        return subbatch

    @staticmethod
    def _iterable_iterator(iterable: tuple | list):
        """Генератор строк из кортежа или списка"""
        for index, value in enumerate(iterable):
            value = url_quote(str(value))
            yield f'[{index}]={value}'

    @staticmethod
    def _get_subbatch(cmd, params: int | float | str) -> str:
        """Возвращает подзапрос для этих типов данных"""
        params = url_quote(str(params))
        subbatch = f'&{cmd}={params}'
        return subbatch


async def log_exception(e: Exception, module="main"):
    """Асинхронное Логирование ошибок. Передаём ошибку и дополнительную информацию"""
    uvicorn_logger.info(f"An exception {str(e)} occurred in the module {module}")
    message = f'---------- {module} {datetime.now(tz=SERVER_TZ)} ----------'
    debug_logger.info(message)
    for frame in traceback.format_exception(e):
        debug_logger.info(frame[:-1])

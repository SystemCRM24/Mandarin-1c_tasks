import logging


uvicorn_logger = logging.getLogger('uvicorn')

debug_logger = logging.getLogger("debug_logger")
debug_logger.setLevel(logging.DEBUG)
debug_logger.handlers = [logging.FileHandler("logs/debug.log", encoding="utf-8")]

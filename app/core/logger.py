import logging
import os
import time
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

ENV = os.getenv("ENV", "local")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "2"))
ENABLE_CONSOLE_LOG = ENV in ("local", "dev")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_PATH = BASE_DIR / LOG_DIR
APP_LOG_DIR = LOG_PATH / "app"
ERROR_LOG_DIR = LOG_PATH / "error"

APP_LOG_DIR.mkdir(parents=True, exist_ok=True)
ERROR_LOG_DIR.mkdir(parents=True, exist_ok=True)


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


class CustomFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.relativePath = os.path.relpath(record.pathname)
        except Exception:
            record.relativePath = record.pathname
        return super().format(record)


LOG_FORMAT = (
    "%(asctime)s | %(name)s | %(levelname)s | %(relativePath)s:%(lineno)d | %(message)s"
)


def create_handler(log_file: Path, log_level: int):
    handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        backupCount=LOG_RETENTION_DAYS,
        encoding="utf-8",

    )
    handler.setLevel(log_level)
    handler.suffix = ""
    formatter = CustomFormatter(LOG_FORMAT)
    formatter.converter = time.gmtime

    handler.setFormatter(formatter)
    return handler

def setup_logger():
    # Use the root logger to capture all logs globally
    logger = logging.getLogger("app")
    
    if logger.handlers:
        return logger

    logger.handlers = [] # Clear any existing handlers if they were somehow partially set
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    app_handler = create_handler(APP_LOG_DIR / "app.log", logging.INFO)
    app_handler.addFilter(MaxLevelFilter(logging.INFO))
    error_handler = create_handler(ERROR_LOG_DIR / "error.log", logging.ERROR)

    logger.addHandler(app_handler)
    logger.addHandler(error_handler)

    if ENABLE_CONSOLE_LOG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = CustomFormatter(
            "%(name)s | %(levelname)s | %(relativePath)s:%(lineno)d | %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = False
        uvicorn_logger.addHandler(app_handler)
        uvicorn_logger.addHandler(error_handler)
        if ENABLE_CONSOLE_LOG:
            uvicorn_logger.addHandler(console_handler)
        
    return logger
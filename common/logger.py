# common/logger.py
from loguru import logger

def get_logger(name: str = "app"):
    logger.add("logs/app.log", rotation="1 week", retention="2 months",
               enqueue=True, backtrace=True, diagnose=True)
    return logger.bind(mod=name)

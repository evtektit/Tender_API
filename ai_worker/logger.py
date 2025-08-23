from common.logger import get_logger as watchdog_get_logger

def get_logger(name: str, filename: str = "app.log"):
    """
    Обёртка над watchdog.get_logger
    :param name: имя логгера (например, __name__)
    :param filename: файл логов (по умолчанию app.log)
    """
    return watchdog_get_logger(name, filename)

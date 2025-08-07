import os
import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter  # pip install colorlog

# 📁 Путь до папки с логами
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 📄 Путь до файла лога
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 🎨 Цветной вывод в консоль
console_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)

# 👇 Обработчики
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=2 * 1024 * 1024,  # 2 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

# 🧠 Главный логгер
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

import logging

# Логгер СРАЗУ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("telegram_bot.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

print("🟡 bot.py начал выполняться")


# Потом всё остальное
import os
from dotenv import load_dotenv
load_dotenv()

import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.critical("❌ BOT_TOKEN не найден в .env или переменной окружения!")
    raise RuntimeError("❌ BOT_TOKEN не найден в .env или переменной окружения!")

import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import httpx
from common.logger import get_logger

# Логгер
logger = get_logger(__name__)
logger.info("🚀 Telegram-бот стартует")

# Загрузка .env
load_dotenv()

import socket

BOT_TOKEN = os.getenv("BOT_TOKEN")
ENVIRONMENT = os.getenv("ENVIRONMENT", "docker")

# Выбор API_URL в зависимости от среды
if ENVIRONMENT == "local":
    API_URL = "http://localhost:8000/ai/ask"
else:
    API_URL = "http://api:8000/ai/ask"

# Логируем важную информацию
logger.info(f"🧠 Окружение: {ENVIRONMENT}")
logger.info(f"🌐 API_URL: {API_URL}")
logger.info(f"🔐 BOT_TOKEN начинается с: {BOT_TOKEN[:10] if BOT_TOKEN else '❌ отсутствует'}")
logger.info(f"🧬 PID процесса: {os.getpid()}")
try:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    logger.info(f"🖥️ Хост: {hostname} | IP: {ip}")
except Exception as e:
    logger.warning(f"⚠️ Не удалось определить IP: {e}")

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def handle_start(message: Message):
    logger.info(f"📩 Пользователь {message.from_user.id} начал с /start")
    await message.answer("👋 Привет! Я готов помочь с тендерами. Напиши свой вопрос.")

# Любое сообщение
@dp.message()
async def handle_any_message(message: Message):
    user_input = message.text
    logger.info(f"📝 Сообщение от {message.from_user.id}: {user_input}")
    await message.answer("🤖 Думаю...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json={"prompt": user_input})
            result = response.json()
            reply = result.get("response", "⚠️ Нет ответа от AI")
    except Exception as e:
        logger.exception("💥 Ошибка при запросе к AI")
        reply = f"❌ Ошибка при запросе к AI: {e}"

    await message.answer(reply)

# Основной запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

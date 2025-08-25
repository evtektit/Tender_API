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
    await message.answer("🔎 Ищу подходящие тендеры...")

    try:
        async with httpx.AsyncClient() as client:
            # Сначала отправляем запрос на /search
            search_url = API_URL.replace("/ai/ask", "/search")
            search_resp = await client.post(search_url, json={"query": user_input})
            search_data = search_resp.json()
            result = search_data.get("result", "")

            if result:
                await message.answer(f"📦 Найдено:\n{result}")
                return

            # Если не найдено — спрашиваем AI
            await message.answer("🤖 Думаю как AI...")
            ai_resp = await client.post(API_URL, json={"question": user_input})
            ai_data = ai_resp.json()
            reply = ai_data.get("answer", "⚠️ Нет ответа от AI")

    except Exception as e:
        logger.exception("💥 Ошибка при запросе")
        reply = f"❌ Ошибка при обработке: {e}"

    await message.answer(reply)

# Основной запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

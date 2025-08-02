# telegram_bot/bot.py
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import httpx
from logger import get_logger

# Логгер
logger = get_logger(__name__)
logger.info("🚀 Telegram-бот стартует")

# Загрузка .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "http://api:8000/ai/ask"

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

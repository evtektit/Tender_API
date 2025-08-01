import os
from dotenv import load_dotenv
load_dotenv()

import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не найден в .env или переменной окружения!")

# Логгер
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("telegram_bot.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"▶️ /start от пользователя {user_id}")
    await update.message.reply_text("Привет! Я бот-парсер. Напиши /ai для анализа ТЗ через AI.")

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"✋ /ai от пользователя {user_id}")
    await update.message.reply_text("✍️ Пришли текст ТЗ для анализа:")
    user_states[user_id] = "waiting_for_tz"

async def handle_ai_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_states.get(user_id) == "waiting_for_tz":
        text = update.message.text
        logger.info(f"📨 ТЗ от {user_id}: {text[:100]}...")
        await update.message.reply_text("🔍 Отправляю в AI...")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post("http://api:8000/ai/ask", json={"prompt": text})
                result = response.json().get("response", "⚠️ Ошибка AI")
                logger.info(f"✅ Ответ от AI для {user_id}: {result[:100]}")
                await update.message.reply_text(result)
        except Exception as e:
            logger.error(f"❌ Ошибка связи с AI для {user_id}: {e}")
            await update.message.reply_text(f"⚠️ Ошибка связи с AI: {e}")
        user_states[user_id] = None

async def main():
    logger.info("🚀 Telegram-бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(Dockerfile.watchdogCommandHandler("ai", ai_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_text))

    logger.info("🤖 Бот запущен и ждёт команды")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.get_event_loop().run_until_complete(main())

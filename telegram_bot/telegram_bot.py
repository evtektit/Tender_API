from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
import logging
import httpx

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-парсер. Напиши /ai для анализа ТЗ через AI.")

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Пришли текст ТЗ для анализа:")
    user_states[update.effective_user.id] = "waiting_for_tz"

async def handle_ai_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_states.get(user_id) == "waiting_for_tz":
        text = update.message.text
        await update.message.reply_text("🔍 Отправляю в AI...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/analyze", json={"text": text})
                result = response.json().get("response", "⚠️ Ошибка AI")
                await update.message.reply_text(result)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Ошибка связи с AI: {e}")
        user_states[user_id] = None

async def init_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ai", ai_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_text))
    return app

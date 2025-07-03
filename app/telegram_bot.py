from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from app.ai import ask_gpt
import os
from dotenv import load_dotenv
import logging

# 🔧 Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🟢 Логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🧠 Память состояний пользователей
user_states = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-парсер. Напиши /ai для анализа ТЗ через AI.")

# /ai
async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Пришли текст ТЗ для анализа:")
    user_states[update.effective_user.id] = "waiting_for_tz"

# обработка текста
async def handle_ai_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_states.get(user_id) == "waiting_for_tz":
        text = update.message.text
        await update.message.reply_text("🔍 Обрабатываю через AI...")
        result = ask_gpt(text)
        await update.message.reply_text(result)
        user_states[user_id] = None

# 🚀 Запуск бота
def run_bot():
    logger.info("🚀 TenderBot AI запущен и работает в режиме polling")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ai", ai_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_text))
    try:
        app.run_polling()
    except KeyboardInterrupt:
        logger.info("🛑 TenderBot остановлен вручную.")

if __name__ == "__main__":
    run_bot()

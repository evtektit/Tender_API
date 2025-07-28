# telegram_bot/handlers.py
from ai_worker.openai_client import ask_gpt
from aiogram import types

async def handle_message(message: types.Message):
    user_input = message.text
    await message.answer("🤖 Думаю...")
    reply = ask_gpt(user_input)
    await message.answer(reply)

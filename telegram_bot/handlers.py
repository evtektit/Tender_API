# telegram_bot/handlers.py
from aiogram import types
import httpx

API_URL = "http://api:8000/ai/ask"

async def handle_message(message: types.Message):
    user_input = message.text
    await message.answer("🤖 Думаю...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json={"prompt": user_input})
            result = response.json()
            reply = result.get("response", "⚠️ Нет ответа от AI")
    except Exception as e:
        reply = f"❌ Ошибка при обращении к AI: {e}"

    await message.answer(reply)

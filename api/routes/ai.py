import os
from fastapi import APIRouter, Body  # ← ВАЖНО: нужно импортировать APIRouter!
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# 🟢 Роутер для подключения к FastAPI
router = APIRouter()

# 🔐 Загрузка ключа
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🤖 Функция запроса к GPT
def ask_gpt(prompt: str, model="gpt-4", temperature=0.7) -> str:
    try:
        chat = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты — помощник по анализу тендерной документации. Отвечай кратко, по сути."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Ошибка AI: {str(e)}"

# Модель тела запроса
class GPTRequest(BaseModel):
    prompt: str

# POST-эндпоинт
@router.post("/ai/ask")
async def ask_gpt_api(data: GPTRequest):
    answer = ask_gpt(data.prompt)
    return JSONResponse(content={"response": answer})

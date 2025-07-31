import os
from dotenv import load_dotenv
from openai import OpenAI
from logger import get_logger
logger = get_logger(__name__)

def ask_gpt(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2", temperature: float = 0.7):
    logger.info(f"🤖 Получен запрос к ИИ: {prompt}")
    try:
        # Твой вызов модели тут:
        response = {
            "choices": [{
                "message": {
                    "content": "🔧 Заглушка: ИИ пока не отвечает"
                }
            }]
        }
        logger.debug(f"📥 Ответ от модели: {response}")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.exception("💥 Ошибка при обращении к Together.ai")
        return "⚠️ Произошла ошибка при обращении к ИИ"

load_dotenv()

client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

def ask_gpt(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2", temperature: float = 0.7) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты — AI-помощник по тендерам. Отвечай кратко и по делу."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"🛑 Ошибка Together.ai: {e}"

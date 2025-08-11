import os
from openai import OpenAI
from dotenv import load_dotenv
from ai_worker.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

logger.info(f"🔑 TOGETHER_API_KEY загружен: {bool(client.api_key)}")

def ask_gpt(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2", temperature: float = 0.7) -> str:
    logger.info(f"🤖 Получен запрос к ИИ: {prompt}")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты — AI-помощник по тендерам. Отвечай кратко и по делу."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        reply = response.choices[0].message.content.strip()
        logger.debug(f"🧠 Ответ ИИ: {reply}")
        return reply
    except Exception as e:
        logger.exception("💥 Ошибка при обращении к Together AI")
        return "⚠️ Ошибка при работе с ИИ"

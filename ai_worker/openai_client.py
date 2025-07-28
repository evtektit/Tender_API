# ai_worker/openai_client.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("TOGETHER_API_KEY")
openai.api_base = "https://api.together.xyz/v1"

def ask_gpt(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2", temperature: float = 0.7) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты — AI-помощник по тендерам. Отвечай кратко и по делу."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"🛑 Ошибка Together.ai: {e}"

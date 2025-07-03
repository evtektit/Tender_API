import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt: str, model="gpt-4", temperature=0.7) -> str:
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
        return f"⚠️ Ошибка GPT: {str(e)}"

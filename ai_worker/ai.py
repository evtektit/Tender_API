import os
from openai import OpenAI
from dotenv import load_dotenv
import socket
import time

load_dotenv()

# Подключение к Together API
client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

def wait_for_internet(timeout=60):
    print("⏳ Проверяем интернет через VPN...")
    for i in range(timeout):
        try:
            socket.gethostbyname('openai.com')
            print(f"🌐 Интернет через VPN доступен (на {i+1}-й секунде)")
            return True
        except socket.gaierror:
            time.sleep(1)
    print("❌ Интернет через VPN недоступен")
    return False

def ask_gpt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Ошибка GPT: {str(e)}"

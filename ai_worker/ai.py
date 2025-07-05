import os
import openai
from dotenv import load_dotenv
import socket
import time  # 🔧 Добавляем это

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    return f"🧠 (заглушка): получил '{prompt}'"

# def ask_gpt(prompt: str) -> str:
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"⚠️ Ошибка GPT: {str(e)}"
#
#
# if __name__ == "__main__":
#     print("💬 Отправляем запрос к GPT...")
#
#     if wait_for_internet():
#         response = ask_gpt("Привет! Ты работаешь?")
#         print("🧠 Ответ GPT:", response)
#     else:
#         print("🚫 GPT-запрос отменён из-за отсутствия VPN")

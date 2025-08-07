import os
import time
import logging
import requests
import socket

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("watchdog.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Определение среды (в Docker или нет)
def is_running_in_docker():
    return os.path.exists("/.dockerenv")

# Определение адреса API
if is_running_in_docker():
    API_URL = os.getenv("API_URL", "http://api:8000/health")
else:
    API_URL = os.getenv("API_URL", "http://localhost:8000/health")

logging.info("🐶 Watchdog запущен")
logging.info(f"🔍 Проверяем API по адресу: {API_URL}")

def check_api():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            logging.info("✅ API доступен (200 OK)")
        else:
            logging.warning(f"⚠️ API ответил: {response.status_code}")
    except Exception as e:
        logging.error("❌ Ошибка при проверке API:")
        logging.exception(e)

if __name__ == "__main__":
    while True:
        check_api()
        time.sleep(10)

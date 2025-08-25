import os
import time
import logging
import requests

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("watchdog.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Проверяем, в Docker или нет
IS_DOCKER = os.path.exists("/.dockerenv")

# Список сервисов
SERVICES = {
    "api": "http://api:8000/health",
    "ai_worker": "http://ai_worker:8001/health",
    "telegram_bot": "http://telegram_bot:8002/health",
    "parsers": "http://parsers:8003/health",
    "eis_loader": "http://eis_loader:8004/health"
}

# В локальной среде замени хосты на localhost и порты
if not IS_DOCKER:
    SERVICES = {
        name: url.replace(f"{name}", "localhost") for name, url in SERVICES.items()
    }

logging.info("🐶 Watchdog начал отслеживание следующих сервисов:")
for name, url in SERVICES.items():
    logging.info(f"  - {name}: {url}")

def check_service(name, url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logging.info(f"✅ {name} доступен (200 OK)")
        else:
            logging.warning(f"⚠️ {name} ответил: {response.status_code}")
    except Exception as e:
        logging.error(f"❌ Ошибка при проверке {name}: {e}")

if __name__ == "__main__":
    while True:
        for name, url in SERVICES.items():
            check_service(name, url)
        time.sleep(10)

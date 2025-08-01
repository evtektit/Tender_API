import socket
import time
import logging

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("watchdog.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def check_bot(host="telegram_bot", port=88):
    try:
        with socket.create_connection((host, port), timeout=5):
            logging.info("✅ Telegram-бот доступен")
            return True
    except Exception as e:
        logging.error(f"❌ Нет связи с Telegram-ботом: {e}")
        return False

if __name__ == "__main__":
    logging.info("🚨 Watchdog запущен и следит за ботом...")
    while True:
        check_bot()
        time.sleep(30)  # Проверка каждые 30 сек

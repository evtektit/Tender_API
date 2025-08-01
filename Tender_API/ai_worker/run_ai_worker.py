from ai_worker.openai_client import ask_gpt
from ai_worker.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("🚀 Запуск run_ai_worker")
    result = ask_gpt("Объясни, как участвовать в тендере по 44-ФЗ")
    logger.info(f"🤖 Ответ: {result}")

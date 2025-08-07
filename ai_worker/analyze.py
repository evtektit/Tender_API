from ai_worker.openai_client import ask_gpt
from ai_worker.logger import get_logger

logger = get_logger(__name__)


def analyze_text(text: str) -> str:
    logger.info("🔍 Анализ текста запущен")
    if not text:
        logger.warning("⚠️ Недостаточно данных для анализа")
        return "⚠️ Пустой текст для анализа."

    return ask_gpt(f"Анализируй это тендерное задание: {text}")

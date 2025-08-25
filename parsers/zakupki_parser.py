# parsers/zakupki_parser.py

from .playwright_parser import fetch_playwright
from .selenium_parser import fetch_selenium
from common.logger import get_logger

logger = get_logger(__name__)


def run_parser(query: str) -> list[dict]:
    logger.info(f"🟢 Парсер стартовал. Запрос: {query}")

    try:
        logger.info("🔎 Пробуем Playwright...")
        results = fetch_playwright(query)
        logger.info(f"✅ Playwright дал результат: {len(results)} записей")
        return results
    except Exception as pw_error:
        logger.warning(f"⚠️ Ошибка Playwright: {pw_error}")
        logger.info("🔁 Пробуем Selenium как fallback...")
        try:
            results = fetch_selenium(query)
            logger.info(f"✅ Selenium дал результат: {len(results)} записей")
            return results
        except Exception as se_error:
            logger.error(f"❌ Selenium тоже не сработал: {se_error}")
            return []

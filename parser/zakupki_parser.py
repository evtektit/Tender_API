import requests
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger(__name__)

def search_tenders(query: str) -> list:
    """
    Реальный парсинг с zakupki.gov.ru по ключевому слову.
    Возвращает список тендеров (заголовок + цена).
    """
    logger.info(f"🔍 Поиск тендеров по: {query}")
    url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            logger.warning(f"⚠️ Ошибка запроса: статус {response.status_code} для {url}")
            return [f"❌ Ошибка запроса: {response.status_code}"]

        soup = BeautifulSoup(response.text, "html.parser")
        tenders = []

        for item in soup.select(".search-registry-entry-block"):
            title = item.select_one(".registry-entry__header-mid__text")
            price = item.select_one(".price-block__value")

            if title and price:
                title_text = title.get_text(strip=True)
                price_text = price.get_text(strip=True)
                tenders.append(f"📝 {title_text} — 💰 {price_text}")

        if not tenders:
            logger.warning("🔍 Парсинг завершён, но данные не извлечены. Вероятно, изменилась структура страницы.")
            return ["ℹ️ Не удалось извлечь данные. Возможно, структура страницы изменилась."]

        logger.debug(f"📦 Найдено тендеров: {len(tenders)}")
        return tenders[:5]

    except Exception as e:
        logger.exception("💥 Исключение при парсинге тендеров")
        return [f"⚠️ Ошибка при парсинге: {str(e)}"]

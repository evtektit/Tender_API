import requests
from bs4 import BeautifulSoup
from logger import get_logger
logger = get_logger(__name__)

def search_tenders(query):
    logger.info(f"🔍 Поиск тендеров по: {query}")
    ...
    logger.debug(f"🔢 Найдено результатов: {len(results)}")
    return results

def search_tenders(query: str) -> list:
    """
    Реальный парсинг с zakupki.gov.ru по ключевому слову.
    Возвращает список тендеров (заголовок + цена).
    """
    url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
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
            return ["ℹ️ Не удалось извлечь данные. Возможно, структура страницы изменилась."]

        return tenders[:5]  # вернём до 5 результатов

    except Exception as e:
        return [f"⚠️ Ошибка при парсинге: {str(e)}"]

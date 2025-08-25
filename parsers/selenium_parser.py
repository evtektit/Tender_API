# parsers/selenium_parser.py

def fetch_selenium(query: str) -> list[dict]:
    # TODO: Реализовать с Selenium
    print(f"🔍 [Selenium] Обработка запроса: {query}")
    return [
        {"title": f"📦 Лот по запросу (Selenium): {query}", "price": "120 000 ₽", "link": "https://zakupki.gov.ru/example2"},
    ]

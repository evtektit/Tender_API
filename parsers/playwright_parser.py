# parsers/playwright_parser.py

def fetch_playwright(query: str) -> list[dict]:
    # TODO: Реализовать с Playwright
    print(f"🔍 [Playwright] Обработка запроса: {query}")
    return [
        {"title": f"📦 Лот по запросу (Playwright): {query}", "price": "100 000 ₽", "link": "https://zakupki.gov.ru/example1"},
    ]

async def parse_tenders(query: str) -> str:
    results = fetch_playwright(query)
    if not results:
        return "❌ Ничего не найдено."

    output = ""
    for item in results:
        output += f"{item['title']} — {item['price']}\n{item['link']}\n\n"
    return output.strip()

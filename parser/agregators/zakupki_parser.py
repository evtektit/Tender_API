from typing import List, Dict

def search(query: str, limit: int = 10) -> List[Dict]:
    # TODO: заменить на реальный парсинг zakupki.gov.ru
    limit = max(1, min(limit, 20))
    base = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
    return [{
        "title": f"Zakupki: {query} — {i}",
        "price": None,
        "deadline": None,
        "url": f"{base}?searchString={query}&pageNum={i}",
    } for i in range(1, limit + 1)]

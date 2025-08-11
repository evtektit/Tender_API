from typing import List, Dict

def search(query: str, limit: int = 10) -> List[Dict]:
    # TODO: реальный парсинг агрегатора (многие страницы грузят JS → Playwright)
    limit = max(1, min(limit, 20))
    base = "https://example-agregator.ru/search"
    return [{
        "title": f"Agregator: {query} — {i}",
        "price": None,
        "deadline": None,
        "url": f"{base}?q={query}&p={i}",
    } for i in range(1, limit + 1)]

from typing import List, Dict

def search(query: str, limit: int = 10) -> List[Dict]:
    # TODO: заменить на реальный парсинг (requests/playwright)
    limit = max(1, min(limit, 20))
    base = "https://rts-tender.ru"
    return [{
        "title": f"РТС: {query} — {i}",
        "price": None,
        "deadline": None,
        "url": f"{base}/search?q={query}&p={i}",
    } for i in range(1, limit + 1)]

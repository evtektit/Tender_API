from typing import List, Dict

def search(query: str, limit: int = 10) -> List[Dict]:
    # TODO: реальный парсинг sberbank-ast (скорее через Playwright)
    limit = max(1, min(limit, 20))
    base = "https://sberbank-ast.ru"
    return [{
        "title": f"Sber AST: {query} — {i}",
        "price": None,
        "deadline": None,
        "url": f"{base}/search?q={query}&p={i}",
    } for i in range(1, limit + 1)]

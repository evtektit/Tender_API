# parser/agregators/rts_parser.py
import httpx
from typing import List, Dict, Any

URL = "https://rts-tender.ru/poisk/search/getsearchprofile"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
}


async def rts_search(query: str, limit: int = 10, logger=None) -> List[Dict[str, Any]]:
    if logger:
        logger.info(f"🔍 RTS API: query={query} (limit={limit})")

    payload = {
        "type": 1,
        "searchQuery": query,
        "skip": 0,
        "top": limit,
        "sortType": 1
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        if logger:
            logger.error(f"❌ RTS API ошибка: {e}")
        return []

    tenders = []
    for item in data.get("data", []):
        tenders.append({
            "title": item.get("name", "Без названия"),
            "url": item.get("url", ""),
            "price": item.get("price", None),
            "deadline": item.get("publishDate", None),
        })

    if logger:
        logger.info(f"📦 RTS API: собрано {len(tenders)} позиций")
    return tenders


# Точка входа для run_all.py
async def search(query: str, limit: int = 10, logger=None) -> list[dict]:
    return await rts_search(query=query, limit=limit, logger=logger)

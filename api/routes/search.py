from fastapi import APIRouter, Query
import asyncio
import logging

from parsers.playwright_parser import search_tenders as playwright_search
from parsers.selenium_parser import search_tenders as selenium_search

router = APIRouter()
log = logging.getLogger("api.search")

@router.get("/search")
async def search_tenders(q: str = Query(..., description="Строка поиска")):
    log.info(f"🔎 Search запрос: {q}")

    try:
        # Запускаем оба парсера параллельно
        results_playwright, results_selenium = await asyncio.gather(
            playwright_search(q),
            selenium_search(q),
        )

        return {
            "ok": True,
            "playwright_count": len(results_playwright),
            "selenium_count": len(results_selenium),
            "playwright": results_playwright[:10],  # первые 10 для примера
            "selenium": results_selenium[:10],
        }
    except Exception as e:
        log.exception("Ошибка поиска")
        return {"ok": False, "error": str(e)}

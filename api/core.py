import os
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from parsers.playwright_parser import parse_tenders

from common.logger import get_logger
from api.routes import home, ai  # подключаем роутеры

logger = get_logger(__name__)
logger.info("api started!")

BASE_DIR = Path(__file__).resolve().parent  # .../api
app = FastAPI(debug=True)

# статика по абсолютному пути
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# === Telegram polling (отключён, потому что бот — отдельный контейнер) ===
TG_POLLING = os.getenv("TG_POLLING", "0") == "1"
_polling_task: asyncio.Task | None = None

@app.on_event("startup")
async def _startup():
    logger.info("🚀 FastAPI стартовал")

@app.on_event("shutdown")
async def _shutdown():
    logger.info("🛑 FastAPI завершил работу")

# здоровье
@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})

# поиск тендеров парсера
from fastapi import Query

@app.get("/search")
async def search_tenders_api(q: str = Query(..., description="Строка поиска")):
    logger.info(f"📥 Поисковый запрос: {q}")

    try:
        result = await parse_tenders(q)
        return {"ok": True, "playwright": result, "playwright_count": len(result)}
    except Exception as e:
        logger.exception("Ошибка парсинга")
        return {"ok": False, "error": str(e)}

# подключаем роутеры (главная страница и ИИ)
app.include_router(home.router)
app.include_router(ai.router)

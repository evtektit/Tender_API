from pathlib import Path
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# логгер: используем твой, а если его нет — стандартный
try:
    from ai_worker.logger import get_logger
    logger = get_logger(__name__)
except Exception:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger(__name__)

from api.routes import home, ai  # подключим роутеры

BASE_DIR = Path(__file__).resolve().parent  # .../api
app = FastAPI(debug=True)

# статика по абсолютному пути, чтобы независимо от рабочей директории
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.on_event("startup")
async def _startup():
    logger.info("🚀 FastAPI стартовал")

@app.on_event("shutdown")
async def _shutdown():
    logger.info("🛑 FastAPI завершил работу")

# здоровье
@app.get("/health")
def health():
    return {"ok": True}

# простой API-заглушка для поиска
@app.post("/search")
async def search_tenders_api(request: Request):
    data = await request.json()
    query = data.get("query", "")
    logger.info(f"📥 Поисковый запрос: {query}")
    return JSONResponse({"result": f"🔍 Имитация результатов по запросу: {query}"})

# подключаем роутеры (главная страница и эндпоинт ИИ)
app.include_router(home.router)
app.include_router(ai.router)

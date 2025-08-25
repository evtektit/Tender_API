import sys
import asyncio
from parsers.playwright_parser import parse_tenders
from common.logger import get_logger

logger = get_logger(__name__)
logger.info("ai_worker started!")

# ВАЖНО: ставим Proactor ДО любых импортов FastAPI/uvicorn/asyncio-задач
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import home, ai
app = FastAPI()


@app.post("/search")
async def search_tenders_api(request: Request):
    data = await request.json()
    query = data.get("query", "")
    logger.info(f"📥 Поисковый запрос: {query}")

    try:
        results = await parse_tenders(query)  # это твоя реальная логика парсера
        return JSONResponse({"result": results})
    except Exception as e:
        logger.exception("❌ Ошибка парсинга тендеров")
        return JSONResponse({"result": f"⚠️ Ошибка: {str(e)}"})

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

logger = get_logger(__name__)   # логгер с app.log по умолчанию
logger.info("🚀 Запуск FastAPI приложения")

# Подключаем роуты
app.include_router(home.router)
app.include_router(ai.router)

if __name__ == "__main__":
    import uvicorn
    # На Windows отключаем reload, иначе uvicorn снова переключит политику на Selector
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False if sys.platform == "win32" else True,
    )

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.routes import home
from api.routes import ai
from api.routes import parser_route
from ai_worker.logger import get_logger  # кастомный логгер

# ✅ Инициализация FastAPI
app = FastAPI()

# ✅ Один раз определяем /health
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

# ✅ Настройка логгера
logger = get_logger("main")
logger.info("🚀 Запуск FastAPI приложения")

# ✅ Подключаем маршруты
app.include_router(home.router)
app.include_router(ai.router)
app.include_router(parser_route.router)

# ✅ Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


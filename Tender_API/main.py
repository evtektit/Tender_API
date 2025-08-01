from fastapi import FastAPI
from api.routes import home
from api.routes import ai
from ai_worker.logger import get_logger  # ✅ Подключаем кастомный логгер
from api.routes import parser_route

logger = get_logger("main")  # 🧠 Название логгера: "main"
logger.info("🚀 Запуск FastAPI приложения")

# 🔧 Инициализация FastAPI
app = FastAPI()

# 🔌 Подключаем маршруты
app.include_router(home.router)
app.include_router(ai.router)
app.include_router(parser_route.router)
# 🚀 Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

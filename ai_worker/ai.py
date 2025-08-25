from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from .openai_client import ask_gpt
from common.logger import get_logger
from fastapi.responses import JSONResponse

logger = get_logger(__name__)
logger.info("ai_worker started!")
app = FastAPI()

class GPTRequest(BaseModel):
    text: str

@app.post("/ai/ask")
async def ask_route(request: Request, data: GPTRequest = Body(...)):
    logger.info("📥 Получен запрос в /ai/ask")
    reply = ask_gpt(data.text)
    logger.debug(f"🧠 Ответ: {reply}")
    return {"answer": reply}

def get_uptime():
    # Тут должна быть твоя логика подсчёта аптайма
    return "42h 15m"

def database_connected():
    # Пример: пинг к БД или флаг соединения
    return True

@app.get("/health")
async def health():
    if not database_connected():
        return JSONResponse(status_code=503, content={"status": "db down"})

    return JSONResponse(content={
        "status": "ok",
        "uptime": get_uptime(),
        "version": "1.2.3"
    })

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 ai_worker: Запуск uvicorn")
    uvicorn.run("ai:app", host="0.0.0.0", port=8001)

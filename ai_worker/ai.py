from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from .openai_client import ask_gpt
from .logger import get_logger

logger = get_logger(__name__)
app = FastAPI()

class GPTRequest(BaseModel):
    text: str

@app.post("/ai/ask")
async def ask_route(request: Request, data: GPTRequest = Body(...)):
    logger.info("📥 Получен запрос в /ai/ask")
    reply = ask_gpt(data.text)
    logger.debug(f"🧠 Ответ: {reply}")
    return {"answer": reply}

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 ai_worker: Запуск uvicorn")
    uvicorn.run("ai:app", host="0.0.0.0", port=8001)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from common.logger import get_logger
from ai_worker.openai_client import ask_gpt
import inspect

logger = get_logger(__name__)
logger.info("api started!")
router = APIRouter()


# --- Модель для POST: поддерживаем alias "query" ---
class GPTRequest(BaseModel):
    # Если придёт {"query": "..."} — положим в prompt
    prompt: str | None = Field(None, alias="query")

    class Config:
        populate_by_name = True  # разрешает использовать имя поля ("prompt")


async def _call_ai(text: str) -> str:
    """Безопасный вызов ask_gpt: синхронно/асинхронно и с логом ошибок."""
    try:
        if inspect.iscoroutinefunction(ask_gpt):
            return await ask_gpt(text)
        return ask_gpt(text)
    except Exception as e:
        logger.exception("AI call failed")
        raise HTTPException(status_code=502, detail=f"AI error: {e}")


# --- GET /ai/ask?prompt=... или ?query=... ---
@router.get("/ai/ask")
async def ask_gpt_get(prompt: str | None = None, query: str | None = None):
    text = prompt or query
    if not text:
        raise HTTPException(status_code=422, detail="Передай prompt или query")
    answer = await _call_ai(text)
    return {"answer": answer}


# --- POST /ai/ask c JSON телом {"prompt": "..."} или {"query": "..."} ---
@router.post("/ai/ask")
async def ask_gpt_post(body: GPTRequest):
    if not body.prompt:
        raise HTTPException(status_code=422, detail="Передай prompt или query в теле запроса")
    answer = await _call_ai(body.prompt)
    return {"answer": answer}

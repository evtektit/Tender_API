# api/routes/home.py
from fastapi import APIRouter, HTTPException
import os
import httpx

router = APIRouter()

AI_WORKER_URL = os.getenv("AI_WORKER_URL", "http://ai_worker:8010")  # имя сервиса из docker-compose

# универсальная обёртка для вызова AI
async def call_ai_worker(path: str, payload: dict, timeout: float = 60.0) -> dict:
    url = f"{AI_WORKER_URL}{path}"
    # простая устойчивость: 3 попытки с бэкофом
    backoffs = [0, 0.5, 1.5]
    last_err = None
    for wait in backoffs:
        if wait:
            import asyncio; await asyncio.sleep(wait)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.post(url, json=payload)
                r.raise_for_status()
                return r.json()
        except httpx.HTTPError as e:
            last_err = e
    raise HTTPException(status_code=502, detail=f"ai_worker error: {last_err}")

@router.post("/ask")
async def ask(payload: dict):
    # Предполагаем, что у ai_worker есть POST /ask
    return await call_ai_worker("/ask", payload)

from fastapi import APIRouter, HTTPException
import os
import httpx
import asyncio

router = APIRouter()

# URL ai_worker, по сети docker-compose (см. docker-compose.yml)
AI_WORKER_URL = os.getenv("AI_WORKER_URL", "http://ai_worker:8010")

async def call_ai_worker(path: str, payload: dict, timeout: float = 60.0) -> dict:
    url = f"{AI_WORKER_URL}{path}"
    for delay in (0, 0.5, 1.5):  # 3 попытки
        if delay:
            await asyncio.sleep(delay)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.post(url, json=payload)
                r.raise_for_status()
                return r.json()
        except httpx.HTTPError as e:
            last_err = e
    raise HTTPException(status_code=502, detail=f"ai_worker error: {last_err}")

@router.post("/ai/ask")
async def ask(payload: dict):
    # здесь API просто пересылает запрос в ai_worker
    return await call_ai_worker("/ask", payload)

import os
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from ai_worker.openai_client import ask_gpt  # ✅ используем рабочую реализацию (Together.ai)

router = APIRouter()

class GPTRequest(BaseModel):
    prompt: str

@router.post("/ai/ask")
async def ask_gpt_api(data: GPTRequest):
    answer = ask_gpt(data.prompt)
    return JSONResponse(content={"response": answer})

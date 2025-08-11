from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from ai_worker.openai_client import ask_gpt

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class AskIn(BaseModel):
    prompt: str

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main_template_ui.html", {"request": request})

@router.post("/ask")
async def ask_json(payload: AskIn):
    answer = await run_in_threadpool(ask_gpt, payload.prompt)
    return {"answer": answer}

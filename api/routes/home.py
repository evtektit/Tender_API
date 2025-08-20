from pathlib import Path
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# /api/routes/home.py -> родитель = /api
API_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(API_DIR / "templates"))

from ai_worker.openai_client import ask_gpt  # твой клиент

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main_template_ui.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def ask(request: Request, prompt: str = Form(...)):
    response = ask_gpt(prompt)
    return templates.TemplateResponse("main_template_ui.html", {
        "request": request,
        "ai_answer": response
    })
